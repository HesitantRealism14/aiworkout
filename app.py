import streamlit as st
from PIL import Image
import requests

st.markdown(
"### AI Workout Assistant"
)

base_url = 'https://predictionapi-fja4gelnpq-ew.a.run.app'
local_url = 'http://127.0.0.1:8000'

img_file_buffer = st.file_uploader('Choose a file')


if img_file_buffer is not None:
    st.image(Image.open(img_file_buffer), caption='Image you uploaded')
    bytes_data = img_file_buffer.getvalue()

    predict_request_url = f"{base_url}/predict_pose"
    pose = requests.post(predict_request_url, files={'img': bytes_data}).json().get('workout pose')

    option = st.selectbox(f'Your workout pose is: {pose}. Is that correct?',
                          ('-', 'Yes', 'No'))

    if option == 'No':
        pose = st.radio('Please choose your pose for scoring',
                        ('bench', 'deadlift', 'squat'))
        option = 'Yes'


    if option == 'Yes':
        st.write('One moment...')
        request_url = f"{base_url}/getangle{pose}"

        # request_url = f"{local_url}/getangle{pose}"
        response = requests.post(request_url, files={'img': bytes_data}).json()

        st.write(response.get('angle'))

        # annotate_url = f"{local_url}/annotate"
        annotate_url = f"{base_url}/annotate"

        out_image = requests.post(annotate_url, files={'img': bytes_data}, stream=True).content
        st.image(out_image)
