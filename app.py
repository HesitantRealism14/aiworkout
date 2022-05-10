import streamlit as st
from PIL import Image
import cv2
import requests
import numpy as np

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
    st.image(Image.open(img_file_buffer), caption='Image you uploaded')
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

        annotate_url = f"{base_url}/annotate"
        out_image = requests.post(annotate_url, {'img': bytes_data}).json().get('annotated')
        st.image(out_image)
