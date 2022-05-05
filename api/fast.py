from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import joblib
import numpy as np

PATH_TO_LOCAL_MODEL = 'model.joblib'

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

@app.get("/")
def index():
    return {"greeting": "Hello world"}

@app.get("/predict_pose")
def make_predict(img):

    model = joblib.load(PATH_TO_LOCAL_MODEL)
    y_pred = model.predict(img)

    classes = {'bench':0,
               'deadlift':1,
               'squat':2}


    return {'workout_pose':classes.get(np.argmax(y_pred),'workout pose not found')}
