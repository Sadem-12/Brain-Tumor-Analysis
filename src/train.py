import os
import glob
import torch
import torch.nn as nn
from torch.utils.data import DataLoader
from sklearn.model_selection import train_test_split
from tqdm import tqdm
from tensorflow.keras.models import save_model

from dataset import BrainTumorDataset
from model import get_unet_model

# -------------------- المسارات --------------------
IMAGE_DIR = "/content/clean_data/clean_data/images"
MASK_DIR  = "/content/clean_data/clean_data/masks"

# -------------------- تحضير البيانات --------------------
image_paths = sorted(glob.glob(os.path.join(IMAGE_DIR, "*.png")))
mask_paths  = sorted(glob.glob(os.path.join(MASK_DIR, "*_mask.png")))

print("عدد الصور:", len(image_paths))
print("عدد الأقنعة:", len(mask_paths))

train_imgs, val_imgs, train_masks, val_masks = train_test_split(
    image_paths, mask_paths, test_size=0.2, random_state=42
)

BATCH_SIZE = 4
IMAGE_SIZE = 256

train_dataset = BrainTumorDataset(train_imgs, train_masks, IMAGE_SIZE)
val_dataset   = BrainTumorDataset(val_imgs, val_masks, IMAGE_SIZE)

train_loader = DataLoader(train_dataset, batch_size=BATCH_SIZE, shuffle=True)
val_loader   = DataLoader(val_dataset, batch_size=BATCH_SIZE, shuffle=False)

# -------------------- مقاييس --------------------
def dice_coef(y_pred, y_true, smooth=1e-6):
    y_pred = torch.sigmoid(y_pred)
    y_pred = (y_pred > 0.5).float()
    y_true = y_true.float()
    intersection = (y_pred * y_true).sum()
    return (2. * intersection + smooth) / (y_pred.sum() + y_true.sum() + smooth)

def iou_score(y_pred, y_true, smooth=1e-6):
    y_pred = torch.sigmoid(y_pred)
    y_pred = (y_pred > 0.5).float()
    y_true = y_true.float()
    intersection = (y_pred * y_true).sum()
    union = y_pred.sum() + y_true.sum() - intersection
    return (intersection + smooth) / (union + smooth)

# -------------------- بناء المودل --------------------
device = "cuda" if torch.cuda.is_available() else "cpu"
model = get_unet_model(in_channels=1, classes=1)
criterion = nn.BCEWithLogitsLoss()
optimizer = torch.optim.Adam(model.parameters(), lr=1e-4)
model.to(device)

# -------------------- التدريب --------------------
def train_model(model, train_loader, val_loader, criterion, optimizer, num_epochs=5, device="cuda"):
    for epoch in range(num_epochs):
        model.train()
        train_loss = 0
        for images, masks in tqdm(train_loader, desc=f"Epoch {epoch+1}/{num_epochs}", leave=False):
            images, masks = images.to(device), masks.to(device)
            optimizer.zero_grad()
            outputs = model(images)
            loss = criterion(outputs, masks)
            loss.backward()
            optimizer.step()
            train_loss += loss.item()
        train_loss /= len(train_loader)
        print(f"Epoch {epoch+1}/{num_epochs} - Train Loss: {train_loss:.4f}")
    return model

NUM_EPOCHS = 5
model = train_model(model, train_loader, val_loader, criterion, optimizer, num_epochs=NUM_EPOCHS, device=device)

# -------------------- حفظ المودل --------------------
save_model(model, "brain_tumor_unet.h5")
print("✅ تم حفظ المودل: brain_tumor_unet.h5")