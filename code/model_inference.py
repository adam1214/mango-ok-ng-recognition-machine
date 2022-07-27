#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import socket
from glob  import glob
from recognition import recognize
from PIL import Image
import pdb
import numpy as np
import os
import torch
import time
import asyncio
'''
async def inference():
    tasks = []
    tasks.append(r(input_img0)[0])
    tasks.append(r(input_img1)[0])
    tasks.append(r(input_img0)[0])
    
    result = await asyncio.gather(*tasks)
    
    for re in result:
        print(re)
'''
def single_batch_inference():
    r = recognize.Recognize_single(
            model_path='recognition/model_pack_v3_1619986187.pth', device=device,
            async_run=False, 
            verbose=True)
    imgs_f0 = 'examples/webcam/螢幕擷取畫面 (6).png'
    imgs_f1 = 'examples/工業相機/背面01_1.png'
    if '.png' in imgs_f0: # four channels to three channels
        input_img0 = Image.open(imgs_f0)
        input_img_arr = np.array(input_img0)
        input_img_arr = input_img_arr[:, :, :3]
        input_img0 = Image.fromarray(input_img_arr)
    else:
        input_img0 = Image.open(imgs_f0)
        
    if '.png' in imgs_f1: # four channels to three channels
        input_img1 = Image.open(imgs_f1)
        input_img_arr = np.array(input_img1)
        input_img_arr = input_img_arr[:, :, :3]
        input_img1 = Image.fromarray(input_img_arr)
    else:
        input_img1 = Image.open(imgs_f0)
    print(imgs_f0)
    print(imgs_f1)
    print(input_img0.size)
    print(input_img1.size)
    t0 = time.time()
    #asyncio.run(inference())
    result_num0 = r(input_img0)[0]
    result_num1 = r(input_img1)[0]
    result_num2 = r(input_img0)[0]
    t1 = time.time()
    print('inference time:', round(t1-t0,2), 'sec')
    
    print(result_num0)
    print(result_num1)
    print(result_num0)
    '''
    outdata = 'NG' if 2 == result_num0 else 'OK'
    print('send: ' + outdata)
    '''
    
def multi_batch_inference():
    r = recognize.Recognize_multi(
            model_path='recognition/model_pack_v3_1619986187.pth', device=device,
            async_run=False, 
            verbose=True)
    imgs_file_path_list = glob('./examples/0704/cam4/*.png')
    imgs_list = []
    for imgs_file_path in imgs_file_path_list:
        if '.png' in imgs_file_path: # four channels to three channels
            input_img = Image.open(imgs_file_path)
            input_img_arr = np.array(input_img)
            input_img_arr = input_img_arr[:, :, :3]
            input_img = Image.fromarray(input_img_arr)
        else:
            input_img = Image.open(imgs_file_path)
        imgs_list.append(input_img)
    for i in range(0, len(imgs_list), 2):
        t0 = time.time()
        if i+2 > len(imgs_list):
            result_nums_list = r(imgs_list[i:])[0]
            print(imgs_file_path_list[i:])
        else:
            result_nums_list = r(imgs_list[i:i+2])[0]
            print(imgs_file_path_list[i:i+2])
        
        ok_ng_list = []
        for num in result_nums_list:
            if num == 2:
                ok_ng_list.append('NG')
            else:
                ok_ng_list.append('OK')
        
        t1 = time.time()
        #print('inference time:', round(t1-t0,2), 'sec')
        print(ok_ng_list)
    
if __name__ == '__main__':
    os.environ["CUDA_VISIBLE_DEVICES"] = '0'
    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
    #device = 'cpu'
    print(device)
    
    #single_batch_inference()
    
    multi_batch_inference()
