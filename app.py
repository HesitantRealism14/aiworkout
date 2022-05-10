import streamlit as st
from PIL import Image
import cv2
import numpy as np
import requests
import mediapipe as mp

mp_drawing = mp.solutions.drawing_utils
mp_holistic = mp.solutions.holistic

st.markdown(
"### AI Workout Assistant"
)

base_url = 'https://predictionapi-fja4gelnpq-ew.a.run.app'

# if 'uploaded_img' not in st.session_state:
#     st.session_state['uploaded_img'] = False
# if 'confirmed_pose' not in st.session_state:
#     st.session_state['confirmed_pose'] = False

img_file_buffer = st.file_uploader('Choose a file')


if img_file_buffer is not None:
    st.session_state['uploaded_img'] = True
    bytes_data = img_file_buffer.getvalue()
    cv2_img = cv2.imdecode(np.frombuffer(bytes_data, np.uint8), cv2.IMREAD_COLOR)

    predict_request_url = f"{base_url}/predict_pose"
    pose = requests.post(predict_request_url, files={'img': bytes_data}).json().get('workout pose')

    option = st.selectbox(f'Your workout pose is: {pose}. Is that correct?',
                          ('-', 'Yes', 'No'))

    if option == 'No':
        pose = st.radio('Please choose your pose for scoring',
                        ('bench', 'deadlift', 'squat'))
        option = 'Yes'
        # st.session_state['confirmed_pose'] = True

    if option == 'Yes':
        # st.session_state['confirmed_pose'] = True
        st.write('One moment...')
        request_url = f"{base_url}/getangle{pose}"
        response = requests.post(request_url, {'img': bytes_data}).json()

        st.write(response.get('angle'))

        image = np.array(Image.open(img_file_buffer))
        image_height, image_width, _ = image.shape
        with mp_holistic.Holistic(static_image_mode=True, model_complexity=2,enable_segmentation=True) as holistic:
            results = holistic.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
            out_image = image.copy()
            mp_drawing.draw_landmarks(
                out_image, results.pose_landmarks, mp_holistic.POSE_CONNECTIONS)
            mp_drawing.draw_landmarks(
                out_image, results.pose_landmarks, mp_holistic.POSE_CONNECTIONS)
            mp_drawing.draw_landmarks(
                out_image, results.pose_landmarks, mp_holistic.POSE_CONNECTIONS)
            mp_drawing.draw_landmarks(
                out_image, results.pose_landmarks, mp_holistic.POSE_CONNECTIONS)
            st.image(out_image, use_column_width=True)
