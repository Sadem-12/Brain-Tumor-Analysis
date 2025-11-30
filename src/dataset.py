from torch.utils.data import Dataset
from PIL import Image
import torchvision.transforms as transforms

class BrainTumorDataset(Dataset):
    def __init__(self, image_paths, mask_paths, image_size=256):
        self.image_paths = image_paths
        self.mask_paths = mask_paths
        self.image_size = image_size
        self.transform = transforms.Compose([
            transforms.Resize((image_size, image_size)),
            transforms.ToTensor()
        ])
    
    def __len__(self):
        return len(self.image_paths)
    
    def __getitem__(self, idx):
        img = Image.open(self.image_paths[idx]).convert("L")  # gray
        mask = Image.open(self.mask_paths[idx]).convert("L")
        img = self.transform(img)
        mask = self.transform(mask)
        return img, mask