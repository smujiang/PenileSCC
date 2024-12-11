import pandas as pd
import numpy as np
import torch
import torch.nn as nn
from torchvision import transforms
from PIL import Image
from torch.utils.data import Dataset
from ctran import ctranspath
import time
import os


downsample = "fullresolution"
data_dir = r"/projects/wangc/jun/data/Penile_SCC_Study"
infile = os.path.join(data_dir, "patch_level_labels.csv")

start_time = time.time()

mean = (0.485, 0.456, 0.406)
std = (0.229, 0.224, 0.225)
trnsfrms_val = transforms.Compose([
    transforms.Resize(224),
    transforms.ToTensor(),
    transforms.Normalize(mean=mean, std=std)
])

class roi_dataset(Dataset):
    def __init__(self, img_csv):
        super().__init__()
        self.transform = trnsfrms_val
        self.images_lst = img_csv

    def __len__(self):
        return len(self.images_lst)

    def __getitem__(self, idx):
        path = self.images_lst.filename[idx]
        label = self.images_lst.label[idx]  # Assuming you have a 'label' column in your CSV
        slide_id = self.images_lst.slide_id[idx]
        image = Image.open(path).convert('RGB')
        image = self.transform(image)
        return image, label, slide_id

img_csv = pd.read_csv(infile)
test_datat = roi_dataset(img_csv)
database_loader = torch.utils.data.DataLoader(test_datat, batch_size=1, shuffle=False)

model = ctranspath()
model.head = nn.Identity()
td = torch.load(os.path.join(data_dir, "pretrained_model", "ctranspath.pth"), weights_only=True)
model.load_state_dict(td['model'], strict=True)
model.eval()

slide_id_list = []
embed_list = []
label_list = []  # To store corresponding labels
with torch.no_grad():
    for batch, labels, slide_ids in database_loader:
        features = model(batch)
        features = features.cpu().numpy()
        embed_list.extend(features)
        label_list.extend(labels)
        slide_id_list.extend(slide_ids)

embeddings = np.vstack(embed_list)
print(embeddings.shape)

# Create a DataFrame from the numpy array
embeddings_with_labels = pd.DataFrame(embeddings, columns=[f"feature_{i}" for i in range(768)])

# Add the list of strings as a new column
embeddings_with_labels['label'] = np.array(label_list)
embeddings_with_labels['slide_id'] = np.array(slide_id_list)

print("--- %s minutes ---" % ((time.time() - start_time)/60))

outfile = os.path.join(data_dir, "embeddings", "all_embedding_" + downsample + ".csv")

embeddings_with_labels.to_csv(outfile, index=False)
