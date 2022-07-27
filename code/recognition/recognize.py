import time
import torch
import pickle
import numpy as np
import asyncio
import cv2
import pdb

from recognition.models import models_inits, models
from torchvision import transforms

class Recognize_single():
    
    def __print(self, *arg):
        if self.verbose:
            print(*arg)
    
    def print_time_since(self, t=time.time(), str_prefix=""):
        self.__print(str_prefix + ": {} ms".format((time.time() - t)*1000))
        return time.time()
    '''
    def trans_resize(self, pil_image, size):
        image = np.array(pil_image) 
        image = cv2.resize(image, size)
        return torch.from_numpy(image.transpose((2, 0, 1))).float().div(255)
    '''
    # model_path: path to model.pth
    def __init__(self, model_path, device, async_run=False, verbose=False):

        self.device = device
        self.async_run = bool(async_run)
        self.version = 3
        self.verbose = verbose
        self.__print("[Init] Loading Models")
        
        t = time.time()

        for init_name in models_inits:
            self.__print("[Init] Importing {} models".format(init_name))
            exec(models_inits[init_name])
            
            t = self.print_time_since(t, "[Init] Take")
        
        self.__print("[Init] Unpacking Model Pack")
        self.model_pack = torch.load(model_path, map_location=torch.device(device))
        
        t = self.print_time_since(t, "[Init] Take")

        if self.model_pack['version'] != self.version:
            raise Exception("Version not match, model pack version is {}, but code version is {}".format(
                self.model_pack['version'],
                self.version,
            ))

        self.models = dict()
        
        t = self.print_time_since(t, "[Init] Take")
        
        for model_name, model_dict in self.model_pack['l1_models_state_dict']:

            t= time.time()
            
            self.__print("[Init] Loading Layer 1 Model: {}".format(model_name))
            
            if model_name not in models:
                raise Exception("Not support model: {} at this version".format(model_name))

            model_struct = {
                'img_size': (models[model_name]['img_size'], models[model_name]['img_size']),
                'tfms': transforms.Compose([
                    transforms.Resize((models[model_name]['img_size'], models[model_name]['img_size'])),
                    transforms.ToTensor(),
                ]),
                'model_object': eval(models[model_name]['model_str']),
            }

            model_struct['model_object'].load_state_dict(model_dict)
            model_struct['model_object'].eval()
            model_struct['model_object']

            self.models[model_name] = model_struct
            
            t = self.print_time_since(t, "[Init] Take")
    
    async def reco_async(self, raw_img):
        
        outputs = [0.0] * self.model_pack['class_num']
        tasks = []
               
        for model_name in self.models:
            tasks.append(self.reco(raw_img, model_name))
        
        result = await asyncio.gather(*tasks)
               
        for r in result:
            for i in range(self.model_pack['class_num']):
                outputs[i] += r[i]
        
        return outputs
            
    async def reco(self, raw_img, model_name):
        
        outputs = [0.0] * self.model_pack['class_num']
                   
        img = self.models[model_name]['tfms'](raw_img)
        #img = self.trans_resize(raw_img, self.models[model_name]['img_size'])
        output = self.models[model_name]['model_object'](img.unsqueeze(0))
        if type(output) == tuple:
            output, aux = output

        for i in range(self.model_pack['class_num']):
            outputs[i] += float(output[0][i])
        
        return outputs
    
    def __call__async(self, raw_img):

        return asyncio.run(self.reco_async(raw_img))
   
    def __call__sync(self, raw_img):
 
        outputs = [0.0] * self.model_pack['class_num']

        for model_name in self.models:

            img = self.models[model_name]['tfms'](raw_img)
            #img = self.trans_resize(raw_img, self.models[model_name]['img_size'])
            output = self.models[model_name]['model_object'](img.unsqueeze(0))
                
            for i in range(self.model_pack['class_num']):
                outputs[i] += float(output[0][i])
        return outputs

    def __call__(self, raw_img):

        outputs = dict()
        
        t = time.time()
        
        if self.async_run:
            outputs = self.__call__async(raw_img)
        else:
            outputs = self.__call__sync(raw_img)
        
        #t = self.print_time_since(t, "[Runtime] Photo recognize take at L1")
                
        return np.argmax(outputs), outputs
    
class Recognize_multi():
    
    def __print(self, *arg):
        if self.verbose:
            print(*arg)
    
    def print_time_since(self, t=time.time(), str_prefix=""):
        self.__print(str_prefix + ": {} ms".format((time.time() - t)*1000))
        return time.time()
    '''
    def trans_resize(self, pil_image, size):
        image = np.array(pil_image) 
        image = cv2.resize(image, size)
        return torch.from_numpy(image.transpose((2, 0, 1))).float().div(255)
    '''
    # model_path: path to model.pth
    def __init__(self, model_path, device, async_run=False, verbose=False):

        self.device = device
        self.async_run = bool(async_run)
        self.version = 3
        self.verbose = verbose
        self.__print("[Init] Loading Models")
        
        t = time.time()

        for init_name in models_inits:
            self.__print("[Init] Importing {} models".format(init_name))
            exec(models_inits[init_name])
            
            t = self.print_time_since(t, "[Init] Take")
        
        self.__print("[Init] Unpacking Model Pack")
        self.model_pack = torch.load(model_path, map_location=torch.device(device))
        
        t = self.print_time_since(t, "[Init] Take")

        if self.model_pack['version'] != self.version:
            raise Exception("Version not match, model pack version is {}, but code version is {}".format(
                self.model_pack['version'],
                self.version,
            ))

        self.models = dict()
        
        t = self.print_time_since(t, "[Init] Take")
        
        for model_name, model_dict in self.model_pack['l1_models_state_dict']:

            t= time.time()
            
            self.__print("[Init] Loading Layer 1 Model: {}".format(model_name))
            
            if model_name not in models:
                raise Exception("Not support model: {} at this version".format(model_name))

            model_struct = {
                'img_size': (models[model_name]['img_size'], models[model_name]['img_size']),
                'tfms': transforms.Compose([
                    transforms.Resize((models[model_name]['img_size'], models[model_name]['img_size'])),
                    transforms.ToTensor(),
                ]),
                'model_object': eval(models[model_name]['model_str']),
            }

            model_struct['model_object'].load_state_dict(model_dict)
            model_struct['model_object'].eval()
            model_struct['model_object']

            self.models[model_name] = model_struct
            
            t = self.print_time_since(t, "[Init] Take")
    
    async def reco_async(self, raw_imgs):
        
        #outputs = [0.0] * self.model_pack['class_num']
        outputs = torch.zeros([len(raw_imgs), self.model_pack['class_num']], device=self.device)
        tasks = []
               
        for model_name in self.models:
            tasks.append(self.reco(raw_imgs, model_name))
        
        result = await asyncio.gather(*tasks)
               
        for r in result:
            outputs += r
        
        return outputs.cpu().detach().numpy()
    
    async def reco(self, raw_imgs, model_name):
        
        #outputs = [0.0] * self.model_pack['class_num']
        #outputs = torch.zeros([len(raw_imgs), self.model_pack['class_num']], device=self.device)
        
        input_values = torch.tensor([], dtype=torch.float32, device=self.device)
        for raw_img in raw_imgs:
            resize_img_tensor = (self.models[model_name]['tfms'](raw_img)).to(self.device)
            input_values = torch.cat([input_values, resize_img_tensor.unsqueeze(0)], dim=0)

        output = self.models[model_name]['model_object'].to(self.device)(input_values.to(self.device))
        return output
    
    
    def __call__async(self, raw_imgs):

        return asyncio.run(self.reco_async(raw_imgs))
   
    def __call__sync(self, raw_imgs):
 
        #outputs = [0.0] * self.model_pack['class_num']
        outputs = torch.zeros([len(raw_imgs), self.model_pack['class_num']], device=self.device)
    
        for i, model_name in enumerate(self.models):
            input_values = torch.tensor([], dtype=torch.float32, device=self.device)
            for raw_img in raw_imgs:
                resize_img_tensor = (self.models[model_name]['tfms'](raw_img)).to(self.device)
                input_values = torch.cat([input_values, resize_img_tensor.unsqueeze(0)], dim=0)
            #img = self.trans_resize(raw_img, self.models[model_name]['img_size'])
            output = self.models[model_name]['model_object'].to(self.device)(input_values.to(self.device))
            '''
            for i in range(self.model_pack['class_num']):
                outputs[i] += float(output[0][i])
            '''
            outputs += output
            
            if i == 0:
                break
            
        return outputs.cpu().detach().numpy()

    def __call__(self, raw_imgs):

        outputs = dict()
        
        t = time.time()
        
        if self.async_run:
            outputs = self.__call__async(raw_imgs)
        else:
            outputs = self.__call__sync(raw_imgs)
        #t = self.print_time_since(t, "[Runtime] Photo recognize take at L1")
                
        return np.argmax(outputs, axis=1).tolist(), outputs
