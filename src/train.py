import os
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader
from tqdm import tqdm
import json
import matplotlib.pyplot as plt

from dataset import BrainTumorDataset
from model import get_unet_model

# -----------------------------
# ⿡ إعداد المسارات
# -----------------------------
IMAGE_DIR = "/content/clean_data/clean_data/images"  # عدلي حسب مكان الصور
MASK_DIR  = "/content/clean_data/clean_data/masks"   # عدلي حسب مكان الماسكات

image_paths = sorted([os.path.join(IMAGE_DIR, x) for x in os.listdir(IMAGE_DIR) if x.endswith(".png")])
mask_paths  = sorted([os.path.join(MASK_DIR, x)  for x in os.listdir(MASK_DIR)  if x.endswith(".png")])

print(f"عدد الصور: {len(image_paths)}")
print(f"عدد الماسكات: {len(mask_paths)}")

dataset = BrainTumorDataset(image_paths, mask_paths, image_size=256)
train_loader = DataLoader(dataset, batch_size=4, shuffle=True)

# -----------------------------
# ⿢ التحضير للجهاز والمودل
# -----------------------------
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = get_unet_model(in_channels=1, classes=1).to(device)

criterion = nn.BCEWithLogitsLoss()
optimizer = optim.Adam(model.parameters(), lr=1e-4)


history = {"epoch": [], "loss": []}
best_loss = float("inf")


EPOCHS = 5

def normalize_mask(mask):
    return (mask > 0.5).float()  # تحويل ماسك 0-255 → 0/1

for epoch in range(EPOCHS):
    model.train()
    running_loss = 0.0

    loop = tqdm(train_loader, desc=f"Epoch {epoch+1}/{EPOCHS}")

    for imgs, masks in loop:
        imgs = imgs.to(device)
        masks = masks.to(device)
        masks = normalize_mask(masks)

        optimizer.zero_grad()
        outputs = model(imgs)
        loss = criterion(outputs, masks)
        loss.backward()
        optimizer.step()

        running_loss += loss.item()
        loop.set_postfix(loss=loss.item())

    epoch_loss = running_loss / len(train_loader)
    history["epoch"].append(epoch + 1)
    history["loss"].append(epoch_loss)

    # حفظ أفضل مودل
    if epoch_loss < best_loss:
        best_loss = epoch_loss
        torch.save(model.state_dict(), "best_model.pth")
        print("===> Best model updated")

# -----------------------------
# ⿥ حفظ آخر مودل + history
# -----------------------------
torch.save(model.state_dict(), "last_model.pth")
with open("history.json", "w") as f:
    json.dump(history, f)


plt.figure()
plt.plot(history["epoch"], history["loss"], marker='o')
plt.xlabel("Epoch")
plt.ylabel("Loss")
plt.title("Training Loss Curve")
plt.grid(True)
plt.savefig("loss_curve.png")
plt.close()

print("\n✅ Training Completed Successfully!")
print("Saved files: best_model.pth, last_model.pth, history.json, loss_curve.png")