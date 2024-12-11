import os.path
import numpy as np
from PIL import Image
import os
import matplotlib.pyplot as plt

def get_patch_label(img_arr, img_area=None, channel=1, threshold=0.3):
    if img_area is None:
        img_area = img_arr.shape[0]*img_arr.shape[1]
    pos_rate = np.sum((img_arr[:, :, channel] == 0).flatten())/img_area
    # print(pos_rate)
    if pos_rate > threshold:
        return 1
    else:
        return 0

if __name__ == "__main__":
    data_dir = r"\\mfad\researchmn\HCPR\HCPR-GYNECOLOGICALTUMORMICROENVIRONMENT\Archive\Penile_SCC_Study\processed_annotations"
    wrt_csv_fn = os.path.join(data_dir, "patch_level_labels.csv")
    wrt_str = "slide_id,patch_fn,label\n"
    sub_dirs = os.listdir(data_dir)
    img_area = 512*512
    for sd in sub_dirs:
        fn_dir = os.path.join(data_dir, sd)
        if os.path.isdir(fn_dir):
            for fn in os.listdir(fn_dir):
                if "Tumor-mask" in fn:
                    print(f"processing: {fn}")
                    full_fn = os.path.join(data_dir, sd, fn)
                    img_arr = np.array(Image.open(full_fn))
                    org_fn_front = fn[0:fn.index("_Tumor-mask")]
                    org_fn_back = fn[fn.index("_Tumor-mask") + len("_Tumor-mask"): -4]
                    full_org_fn = os.path.join(data_dir, sd, org_fn_front + org_fn_back +".jpg")
                    org_img = Image.open(full_org_fn)
                    # fig,axs = plt.subplots(1,2)
                    # axs[0].imshow(org_img)
                    # axs[1].imshow(img_arr)
                    # plt.show()
                    label = get_patch_label(img_arr, img_area)
                    print("\t\t" + full_org_fn)
                    print("\t\t" + str(label))
                    wrt_str += sd + "," +full_org_fn + "," + str(label) + "\n"
    fp = open(wrt_csv_fn, 'w')
    fp.write(wrt_str)
    fp.close()



