import streamlit as st
from PIL import Image
import cv2
import numpy as np
import requests

st.markdown('''
# AI Workout Assistant
''')

local_url = 'https://predictionapi-fja4gelnpq-ew.a.run.app'

angle_ranges = {
    'squat': range(40, 47),
    'deadlift': range(43, 181),
    'bench': range(149, 160)
}

if 'selected_pose' not in st.session_state:
    st.session_state['selected_pose'] = None

if not st.session_state.selected_pose:
    pose = st.selectbox('Which pose are you trying to score?',
                ('bench', 'deadlift', 'squat'))

    st.write('You selected: ', pose)

    img_file_buffer = st.file_uploader('Choose a file')

    if img_file_buffer is not None:
        # To read image file buffer with OpenCV:

        bytes_data = img_file_buffer.getvalue()
        cv2_img = cv2.imdecode(np.frombuffer(bytes_data, np.uint8), cv2.IMREAD_COLOR)

        # Check the type of cv2_img:
        # # Should output: <class 'numpy.ndarray'>
        # st.write(type(cv2_img))

        # # Check the shape of cv2_img:
        # # Should output shape: (height, width, channels)
        # st.write(cv2_img.shape)

        if st.button('Submit'):

            files = {'img': bytes_data}

            request_url = f"{local_url}/getangle{pose}"
            response = requests.post(request_url, files=files)
            angle = response.json().get('angle')

            st.image(Image.open(img_file_buffer), caption='Image you uploaded')

            st.write(f"The angle of your pose is {angle}")

            if angle not in angle_ranges.get(pose):
                score = 0
                if angle_ranges.get(pose)[0] - angle > 0:
                    st.write("Try widening the angle")
                elif angle - angle_ranges.get(pose)[0] > 0:
                    st.write("Try narrowing your angle")
            else:
                score = 1
                st.write("Great job!")

            st.write(f"You received a score of {score}")


            st.session_state.selected_pose = None
