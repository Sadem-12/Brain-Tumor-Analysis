import torch
import matplotlib.pyplot as plt
from PIL import Image
import torchvision.transforms as transforms
from dataset import BrainTumorDataset
from model import get_unet_model
import os


IMAGE_DIR = "/content/clean_data/clean_data/images"  
OUTPUT_DIR = "/content/results"
os.makedirs(OUTPUT_DIR, exist_ok=True)

image_files = sorted([f for f in os.listdir(IMAGE_DIR) if f.endswith(".png")])[:3]


device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = get_unet_model(in_channels=1, classes=1).to(device)
model.load_state_dict(torch.load("best_model.pth", map_location=device))
model.eval()

transform = transforms.Compose([
    transforms.Resize((256, 256)),
    transforms.ToTensor()
])


for img_name in image_files:
    img_path = os.path.join(IMAGE_DIR, img_name)
    img = Image.open(img_path).convert("L")
    img_tensor = transform(img).unsqueeze(0).to(device)

    with torch.no_grad():
        pred = model(img_tensor)
        pred = torch.sigmoid(pred)
        pred_mask = (pred > 0.5).float().cpu().squeeze(0).squeeze(0)

    
    import numpy as np
    img_np = np.array(img.resize((256, 256)))
    mask_np = pred_mask.numpy() * 255
    overlay = img_np.copy()
    overlay[mask_np > 0] = 255  
    
    plt.figure(figsize=(12,4))

    plt.subplot(1,3,1)
    plt.imshow(img_np, cmap='gray')
    plt.title("Original")
    plt.axis("off")

    plt.subplot(1,3,2)
    plt.imshow(mask_np, cmap='gray')
    plt.title("Predicted Mask")
    plt.axis("off")

    plt.subplot(1,3,3)
    plt.imshow(overlay, cmap='gray')
    plt.title("Overlay")
    plt.axis("off")

    out_path = os.path.join(OUTPUT_DIR, f"{img_name[:-4]}_result.png")
    plt.savefig(out_path)
    plt.close()

    print(f"✅ Saved result: {out_path}")

print("\nAll inference images saved in:", OUTPUT_DIR)