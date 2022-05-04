
from get_data import get_img

import joblib
import numpy as np

GCP_BUCKET_PATH = ""
LOCAL_IMG_PATH = "raw_data/test_img"

PATH_TO_LOCAL_MODEL = 'model.joblib'

def get_test_img():

    X_test , y_test = get_img()
    return X_test,y_test

def get_model(path_to_joblib):

    model = joblib.load(path_to_joblib)
    return model

def get_result(y,y_pred):
    length = len(y)
    pred_list = []
    for i in range(length):
        if np.argmax(y[i]) == np.argmax(y_pred[i]):
            pred_list.append('True')
        else:
            pred_list.append('False')

    return pred_list


if __name__ == "__main__":
    X_test,y_test = get_test_img()
    model = get_model(PATH_TO_LOCAL_MODEL)
    y_pred = model.predict(X_test)
    res = get_result(y_test,y_pred)
    print(res)
