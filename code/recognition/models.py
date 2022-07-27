models_inits = {
    'Timm': "import timm",
    "GitHub-Effs": "from efficientnet_pytorch import EfficientNet",
}

models = {
    "GITHUB-EFFB0": {
        "img_size": 224,
        "model_str": "EfficientNet.from_name('efficientnet-b0', num_classes=3)",
    },
    "GITHUB-EFFB1": {
        "img_size": 240,
        "model_str": "EfficientNet.from_name('efficientnet-b1', num_classes=3)",
    },
    "GITHUB-EFFB2": {
        "img_size": 260,
        "model_str": "EfficientNet.from_name('efficientnet-b2', num_classes=3)",
    },
    "GITHUB-EFFB3": {
        "img_size": 300,
        "model_str": "EfficientNet.from_name('efficientnet-b3', num_classes=3)",
    },
    "GITHUB-EFFB4": {
        "img_size": 380,
        "model_str": "EfficientNet.from_name('efficientnet-b4', num_classes=3)",
    },
    "GITHUB-EFFB5": {
        "img_size": 456,
        "model_str": "EfficientNet.from_name('efficientnet-b5', num_classes=3)",
    },
    "GITHUB-EFFB6": {
        "img_size": 528,
        "model_str": "EfficientNet.from_name('efficientnet-b6', num_classes=3)",
    },
    "GITHUB-EFFB7": {
        "img_size": 600,
        "model_str": "EfficientNet.from_name('efficientnet-b7', num_classes=3)",
    },
    "GITHUB-EFFB8": {
        "img_size": 672,
        "model_str": "EfficientNet.from_name('efficientnet-b8', num_classes=3)",
    },
    "GITHUB-EFFL2": {
        "img_size": 800,
        "model_str": "EfficientNet.from_name('efficientnet-l2', num_classes=3)",
    },
    "TIMM-EFFB0-BASE": {
        "img_size": 224,
        "model_str": "timm.create_model('efficientnet_b0', pretrained=False, num_classes=3)",
    },
    "TIMM-EFFB1-BASE": {
        "img_size": 240,
        "model_str": "timm.create_model('efficientnet_b1', pretrained=False, num_classes=3)",
    },
    "TIMM-EFFB2-BASE": {
        "img_size": 260,
        "model_str": "timm.create_model('efficientnet_b2', pretrained=False, num_classes=3)",
    },
    "TIMM-EFFB3-BASE": {
        "img_size": 300,
        "model_str": "timm.create_model('efficientnet_b3', pretrained=False, num_classes=3)",
    },
    "TIMM-EFFB0-TF": {
        "img_size": 224,
        "model_str": "timm.create_model('tf_efficientnet_b0', pretrained=False, num_classes=3)",
    },
    "TIMM-EFFB1-TF": {
        "img_size": 240,
        "model_str": "timm.create_model('tf_efficientnet_b1', pretrained=False, num_classes=3)",
    },
    "TIMM-EFFB2-TF": {
        "img_size": 260,
        "model_str": "timm.create_model('tf_efficientnet_b2', pretrained=False, num_classes=3)",
    },
    "TIMM-EFFB3-TF": {
        "img_size": 300,
        "model_str": "timm.create_model('tf_efficientnet_b3', pretrained=False, num_classes=3)",
    },
    "TIMM-EFFB0-TF-AP": {
        "img_size": 224,
        "model_str": "timm.create_model('tf_efficientnet_b0_ap', pretrained=False, num_classes=3)",
    },
    "TIMM-EFFB1-TF-AP": {
        "img_size": 240,
        "model_str": "timm.create_model('tf_efficientnet_b1_ap', pretrained=False, num_classes=3)",
    },
    "TIMM-EFFB2-TF-AP": {
        "img_size": 260,
        "model_str": "timm.create_model('tf_efficientnet_b2_ap', pretrained=False, num_classes=3)",
    },
    "TIMM-EFFB3-TF-AP": {
        "img_size": 300,
        "model_str": "timm.create_model('tf_efficientnet_b3_ap', pretrained=False, num_classes=3)",
    },
    "TIMM-EFFB0-TF-NS": {
        "img_size": 224,
        "model_str": "timm.create_model('tf_efficientnet_b0_ns', pretrained=False, num_classes=3)",
    },
    "TIMM-EFFB1-TF-NS": {
        "img_size": 240,
        "model_str": "timm.create_model('tf_efficientnet_b1_ns', pretrained=False, num_classes=3)",
    },
    "TIMM-EFFB2-TF-NS": {
        "img_size": 260,
        "model_str": "timm.create_model('tf_efficientnet_b2_ns', pretrained=False, num_classes=3)",
    },
    "TIMM-EFFB3-TF-NS": {
        "img_size": 300,
        "model_str": "timm.create_model('tf_efficientnet_b3_ns', pretrained=False, num_classes=3)",
    },
    "TIMM-NFNET-L0": {
        "img_size": 224,
        "model_str": "timm.create_model('nfnet_l0', pretrained=False, num_classes=3)",
    },
    "TIMM-NFNET-L0-ECA": {
        "img_size": 224,
        "model_str": "timm.create_model('eca_nfnet_l0', pretrained=False, num_classes=3)",
    },
    "TIMM-NFNET-L1-ECA": {
        "img_size": 256,
        "model_str": "timm.create_model('eca_nfnet_l1', pretrained=False, num_classes=3)",
    },
    "TIMM-NFNET-F0-DEEPMIND": {
        "img_size": 192,
        "model_str": "timm.create_model('dm_nfnet_f0', pretrained=False, num_classes=3)",
    },
    "TIMM-NFNET-F0S": {
        "img_size": 192,
        "model_str": "timm.create_model('nfnet_f0s', pretrained=False, num_classes=3)",
    },
    "TIMM-NFNET-F1-DEEPMIND": {
        "img_size": 224,
        "model_str": "timm.create_model('dm_nfnet_f1', pretrained=False, num_classes=3)",
    },
    "TIMM-NFNET-F1S": {
        "img_size": 224,
        "model_str": "timm.create_model('nfnet_f1s', pretrained=False, num_classes=3)",
    },
    "DEIT-DIS-TINY": {
        "img_size": 224,
        "model_str": "torch.hub.load('facebookresearch/deit:main', 'deit_tiny_distilled_patch16_224', pretrained=False, num_classes=3)",
    },
    "DEIT-DIS-SMAL": {
        "img_size": 224,
        "model_str": "torch.hub.load('facebookresearch/deit:main', 'deit_tiny_distilled_patch16_224', pretrained=False, num_classes=3)",
    },
    "DEIT-DIS-BASE": {
        "img_size": 224,
        "model_str": "torch.hub.load('facebookresearch/deit:main', 'deit_tiny_distilled_patch16_224', pretrained=False, num_classes=3)",
    },
}