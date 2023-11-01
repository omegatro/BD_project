import pandas as pd
import os

from dotenv import load_dotenv
load_dotenv()

IMG_PATH      = os.environ.get("IMG_PATH")
LABEL_PATH    = os.environ.get("LABEL_PATH")
METADATA_PATH = os.environ.get("METADATA_PATH")

#read data into memory
labels        = pd.read_csv(LABEL_PATH)
meta          = pd.read_csv(METADATA_PATH)
img_filenames = list(map(lambda x: x.replace('.jpg', ''),os.listdir(IMG_PATH)))

#removing information about downsampled images
labels = labels[~labels.image.str.contains('downsampled')]
meta = meta[~meta.image.str.contains('downsampled')]

#total number of image files
print(f'Total image files found: {len(img_filenames)}')

#check if labels contain duplicates
print(f'Unique image names /total label rows: {labels.image.unique().__len__()}/{labels.__len__()}')

#check if metadata contain duplicates
print(f'Unique image names /total metadata rows: {meta.image.unique().__len__()}/{meta.__len__()}')

#check if all available images have associated labels
missing_labels = set(img_filenames) - set(labels.image)
missing_label_count = len(missing_labels)
print(f'Number of image files missing labels: {missing_label_count}')
if missing_label_count > 0: print(f'The following images miss labels: {" ".join(missing_labels)}')

#check if all available images have associated metadata
missing_metadata = set(img_filenames) - set(meta.image)
missing_meta_count = len(missing_labels)
print(f'Number of image files missing metadata: {missing_meta_count}')
if missing_meta_count > 0: print(f'The following images miss metadata: {" ".join(missing_labels)}')

#check if some labels do not refer to existing image
missing_img_labels = set(labels.image) - set(img_filenames)
missing_imgl_count = len(missing_img_labels)
print(f'Number of labels missing images: {missing_imgl_count}')
if missing_imgl_count > 0: print(f'The following labels miss image files: {" ".join(missing_img_labels)}')

#check if some metadata do not refer to existing image
missing_img_meta = set(meta.image) - set(img_filenames)
missing_mimg_count = len(missing_img_meta)
print(f'Number of metadata records missing images: {missing_imgl_count}')
if missing_mimg_count > 0: print(f'The following labels miss image files: {" ".join(missing_img_labels)}')

