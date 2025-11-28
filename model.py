import torch
import torch.nn as nn
import segmentation_models_pytorch as smp

def get_unet_model(encoder="resnet34", in_channels=1, classes=1, pretrained=True):
    """
    إنشاء مودل UNet باستخدام مكتبة segmentation_models_pytorch
    """
    model = smp.Unet(
        encoder_name=encoder,
        encoder_weights="imagenet" if pretrained else None,
        in_channels=in_channels,
        classes=classes,
    )
    return model
