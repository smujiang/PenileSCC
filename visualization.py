import os.path

import pandas as pd
import umap
import matplotlib.pyplot as plt
import numpy as np
from itertools import compress
from utils import copy_files_to_target, encode_parent_folders, encode_integers_to_colors

from sklearn.decomposition import PCA
from sklearn.manifold import TSNE
data_dir = r"/projects/wangc/jun/data/Penile_SCC_Study"
img_features_fn = os.path.join(data_dir, "embeddings", "all_embedding_fullresolution.csv")
df = pd.read_csv(img_features_fn, sep=",", header=0).astype(float)
img_features = np.array(df.iloc[:, :-1])
lb = list(df.iloc[:, -2])
lb_int = [int(x) for x in lb]
encoded_colors = encode_integers_to_colors(lb_int)

dm_red = umap.UMAP(random_state=12)
pca_cell_f = dm_red.fit_transform(img_features)

plt.scatter(pca_cell_f[:, 0], pca_cell_f[:, 1], c=encoded_colors, marker=".", s=1)
plt.title("Image embeddings: Tumor/Stroma")
save_to = os.path.join(data_dir, "embeddings", "Tumor_Stroma_img_embed_scatter.png")
plt.savefig(save_to)
plt.close()
# plt.show()


slide_id = list(df.iloc[:, -1])
slide_id_set = list(set(slide_id))
slide_id_ind = [slide_id_set.index(x) for x in slide_id]
encoded_colors = encode_integers_to_colors(slide_id_ind)

dm_red = umap.UMAP(random_state=12)
pca_cell_f = dm_red.fit_transform(img_features)

plt.scatter(pca_cell_f[:, 0], pca_cell_f[:, 1], c=encoded_colors, marker=".", s=1)
plt.title("Image embeddings UMap: Slide batch")
save_to = os.path.join(data_dir, "embeddings", "Slide_batch_img_embed_scatter.png")
plt.savefig(save_to)
plt.close()







print("Done")



