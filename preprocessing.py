import numpy as np
from tensorflow.keras.preprocessing import image

# الحجم المستهدف للصور (كما استخدمناه في التدريب)
TARGET_SIZE = (150, 150)

def resize_and_normalize(img_path, target_size=TARGET_SIZE):
    """
    يقوم بتحميل الصورة، تغيير حجمها، وتحويلها إلى مصفوفة NumPy ثم تطبيعها.
    """
    # 1. تحميل الصورة وتغيير حجمها (Resize)
    img = image.load_img(img_path, target_size=target_size)
    
    # 2. التحويل إلى مصفوفة NumPy (NumPy Array)
    img_array = image.img_to_array(img)
    
    # 3. التطبيع (Normalization): جعل القيم بين 0 و 1
    normalized_array = img_array / 255.0
    
    # ملاحظة: يتم إرجاع مصفوفة لصورة واحدة (H, W, C). يجب على الـ Backend إضافة بُعد الدفعة.
    return normalized_array

def convert_to_torch_tensor(numpy_array):
    """
    دالة اختيارية: لتحويل مصفوفة NumPy إلى PyTorch Tensor.
    تستخدم فقط إذا كان الـ Backend مبنيًا على PyTorch.
    """
    try:
        import torch
        # PyTorch يتوقع أن تكون القنوات أولاً (C, H, W)، لذا نقوم بتغيير ترتيب الأبعاد
        tensor = torch.from_numpy(numpy_array).permute(2, 0, 1).float()
        return tensor
    except ImportError:
        print("PyTorch library is not installed. Cannot convert to torch tensor.")
        return None