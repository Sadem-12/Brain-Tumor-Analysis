import os
from torch.utils.data import Dataset
from PIL import Image

class TumorDataset(Dataset):
    def __init__(self, images_dir, masks_dir, transform=None):
        self.images_dir = images_dir
        self.masks_dir = masks_dir
        self.transform = transform

        self.images = sorted(os.listdir(images_dir))
        self.masks = sorted(os.listdir(masks_dir))

        assert len(self.images) == len(self.masks), "عدد الصور والماسكات غير متساوي!"

    def __len__(self):
        return len(self.images)

    def __getitem__(self, idx):
        img_path = os.path.join(self.images_dir, self.images[idx])
        mask_path = os.path.join(self.masks_dir, self.masks[idx])

        # نفتح الصور والماسكات
        image = Image.open(img_path).convert("RGB")
        mask = Image.open(mask_path).convert("L")  # ماسك = أبيض/أسود

        if self.transform:
            image = self.transform(image)
            mask = self.transform(mask)

        return image, mask
