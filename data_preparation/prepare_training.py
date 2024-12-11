import numpy as np
import os 
from PIL import Image


def get_img_pairs(img_data_dir):
    org_img_fns = []
    mask_img_fns = []
    f_list = os.listdir(img_data_dir)
    for f in f_list:
        if "Tumor-mask.png" in f:
            mask_img_fns.append(os.path.join(img_data_dir,f))
        else:
            org_img_fns.append(os.path.join(img_data_dir, f))
    return sorted(org_img_fns), sorted(mask_img_fns)

def save_split_patches(img_arr, stride, patch_size, out_dir, fn, file_ext):
    w = img_arr.shape[0]
    h = img_arr.shape[1]
    grid_w = range(0, w, stride)
    grid_h = range(0, h, stride)
    for w_i in grid_w:
        for h_i in grid_h:
            if w_i+patch_size <= w and h_i+patch_size <= h:
                img = img_arr[h_i:h_i+patch_size, w_i:w_i+patch_size]
                if img.shape[0] == patch_size and img.shape[1] == patch_size:
                    sv_fn = os.path.join(out_dir, fn + "_" + str(w_i) + "_" + str(h_i) + file_ext)
                    # print(img.shape)
                    I = Image.fromarray(img)
                    I.save(sv_fn)

if __name__ == "__main__":
    anno_mask_dir = r"\\mfad\researchmn\HCPR\HCPR-GYNECOLOGICALTUMORMICROENVIRONMENT\Archive\Penile_SCC_Study\QuPath_output"
    out_dir = r"\\mfad\researchmn\HCPR\HCPR-GYNECOLOGICALTUMORMICROENVIRONMENT\Archive\Penile_SCC_Study\processed_annotations"
    sub_folders = ["5", "16", "17", "18", "115"]

    stride = 256
    patch_size = 512

    for sf in sub_folders:
        img_data_dir = os.path.join(anno_mask_dir, sf)
        org_img_fns, mask_img_fns = get_img_pairs(img_data_dir)
        for idx, org_img_fn in enumerate(org_img_fns):
            org_img = np.array(Image.open(org_img_fn))
            mask_img = np.array(Image.open(mask_img_fns[idx], 'r'))
            sub_out_dir = os.path.join(out_dir, sf)
            if not os.path.exists(sub_out_dir):
                os.makedirs(sub_out_dir)
            fn = os.path.split(org_img_fn)[1][:-4]
            save_split_patches(org_img, stride, patch_size, sub_out_dir, fn, ".jpg")
            fn = os.path.split(mask_img_fns[idx])[1][:-4]
            save_split_patches(mask_img, stride, patch_size, sub_out_dir, fn, ".png")










