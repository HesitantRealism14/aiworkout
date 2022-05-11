import streamlit as st
from PIL import Image
import requests
import re

# set page tab display
st.set_page_config(
   page_title="Workout",
   page_icon= ':heart:',
   layout="wide",
   initial_sidebar_state="expanded",
)

# hide menu button
st.markdown(""" <style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
</style> """, unsafe_allow_html=True)


# app title and description
st.header('AI Workout Assistant')
st.sidebar.title('Upload pics📸 of your workout💪 and get instant✨ feedback!')

# API call references
base_url = 'https://predictionapi-fja4gelnpq-ew.a.run.app'
local_url = 'http://127.0.0.1:8000'

# user upload
img_file_buffer = st.file_uploader('Choose a file')

# display image user uploaded
if img_file_buffer is not None:
    st.sidebar.image(Image.open(img_file_buffer), caption='Image you uploaded')

    # spinner while backend fetches pose classification prediction
    with st.spinner('Wait for it...'):
        bytes_data = img_file_buffer.getvalue()
        predict_request_url = f"{base_url}/predict_pose"
        pose = requests.post(predict_request_url, files={'img': bytes_data}).json().get('workout pose')

    st.sidebar.write(f'Your workout pose is: {pose}.')

    # option for user to choose pose if prediction is wrong
    option = st.sidebar.selectbox('Is that correct?', ('-', 'Yes', 'No'))

    if option == 'No':
        pose = st.sidebar.radio('Please choose your pose for scoring',
                        ('bench', 'deadlift', 'squat', 'bridge', 'pushup'))

        option = 'Yes'

    # fetching scoring results
    if option == 'Yes':
        with st.spinner('Wait for it...'):
            # display annotated image
            annotate_url = f"{base_url}/annotate"
            out_image = requests.post(annotate_url, files={'img': bytes_data}, stream=True).content
            st.image(out_image)

            # display score and comments
            request_url = f"{base_url}/getangle{pose}"
            response = requests.post(request_url, files={'img': bytes_data}).json()
            feedback = response.get('angle')
            cn_request_url = f"{base_url}/getangle{pose}cn"
            cn_response = requests.post(cn_request_url, files={'img': bytes_data}).json()
            cn_feedback = cn_response.get('angle')
            score = re.search(r'( \d* )', feedback)[0]
            comment = re.search(r'[A-Z].*', feedback)[0]
            st.metric(label="Score", value=score)

        # toggle to chinese
        cn_switch = st.checkbox("切换中文")
        if cn_switch:
            st.write(cn_feedback)
        else:
            st.write(comment)

        if '100' in score:
            st.balloons()
