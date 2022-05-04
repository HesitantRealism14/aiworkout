
import os
import numpy as np
from tqdm import tqdm
from PIL import Image

import tensorflow as tf
from tensorflow.keras.utils import to_categorical

GCP_BUCKET_PATH = ""
LOCAL_IMG_PATH = "raw_data/train_img"

def get_img(local=True,**kwargs):

    if local:
        data_path = LOCAL_IMG_PATH
    else:
        data_path = GCP_BUCKET_PATH

    classes = {'bench':0,
               'deadlift':1,
               'squat':2}
    imgs= []
    labels = []

    for cl,i in classes.items():
        img_path = [elt for elt in os.listdir(os.path.join(data_path,cl)) if elt.find('.jpg')>0]

        for img in tqdm(img_path[:120]):
            path = os.path.join(data_path,cl,img)
            if os.path.exists(path):
                image = Image.open(path).convert('RGB')
                image = image.resize((256,256))
                imgs.append(np.array(image))
                labels.append(i)

    X = np.array(imgs)
    num_classes = len(set(labels))
    y = to_categorical(labels,num_classes)

    p = np.random.permutation(len(X))
    X,y = X[p],y[p]

    return X,y

if __name__ == "__main__":

    X,y = get_img()
