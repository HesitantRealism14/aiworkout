import streamlit as st
from datetime import datetime
from PIL import Image
import numpy as np


LOCAL_URL = "http://localhost:8000/"
# PROD_URL = "https://lewagon-hfw5yigd4a-ue.a.run.app/predict"

st.markdown('''
# AI Workout Assistant
''')
if 'selected_pose' not in st.session_state:
    st.session_state['selected_pose'] = None

if not st.session_state.selected_pose:
    option = st.selectbox('Which pose are you trying to score?',
                ('bench', 'deadlift', 'squat'))

    st.write('You selected: ', option)

    img_file_buffer = st.file_uploader('Choose a file')

    if img_file_buffer is not None:
        # To read image file buffer as a PIL Image:
        img = Image.open(img_file_buffer)

        # To convert PIL Image to numpy array:
        img_array = np.array(img)

        if st.button('Submit'):
            # Check the type of img_array:
            # Should output: <class 'numpy.ndarray'>
            st.write(type(img_array))

            # Check the shape of img_array:
            # Should output shape: (height, width, channels)
            st.write(img_array.shape)

            st.image(img, caption='Image you uploaded')

            st.session_state.selected_pose = None
