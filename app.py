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

# API call references
base_url = 'https://predictionapi-fja4gelnpq-ew.a.run.app'
local_url = 'http://127.0.0.1:8000'

# toggle to chinese
cn_switch = st.checkbox("切换中文")
if cn_switch:
    # app title and description
    st.header('AI健身教练')
    st.sidebar.title('上传你的健身💪照片📸 立即✨获得动作改善建议!')

    # user upload
    img_file_buffer = st.file_uploader('上传文件')

    # display image user uploaded
    if img_file_buffer is not None:
        st.sidebar.image(Image.open(img_file_buffer), caption='你上传的照片')

        # spinner while backend fetches pose classification prediction
        bytes_data = img_file_buffer.getvalue()
        predict_request_url = f"{base_url}/predict_pose"

        if requests.post(predict_request_url, files={'img': bytes_data}).status_code == 200:
            with st.spinner('请稍等...'):
                pose = requests.post(predict_request_url, files={'img': bytes_data}).json().get('workout pose')
                lookup = {
                    'squat': '深蹲',
                    'bench':'推举',
                    'deadlift':'硬拉',
                    'pushup':'俯卧撑',
                    'bridge':'臀桥'
                }
                pose_cn = lookup[pose]
                st.write('⬅️ 我们分类了你的健身动作，请在左侧窗口确认我们的判断是否正确')

                st.sidebar.write(f'你的健身动作是: {pose_cn}.')

            # option for user to choose pose if prediction is wrong
            option = st.sidebar.selectbox('是否正确?', ('-', '是', '否'))

            if option == '否':
                pose = st.sidebar.radio('请选择你的健身动作',
                                (lookup['bench'], lookup['deadlift'], lookup['squat'], lookup['bridge'], lookup['pushup']))
                option = '是'
                # fetching scoring results
            if option == '是':
                with st.spinner('请稍等...'):
                    # display annotated image
                    annotate_url = f"{base_url}/annotate"
                    out_image = requests.post(annotate_url, files={'img': bytes_data}, stream=True).content
                    st.image(out_image)

                    # display score and comments
                    request_url = f"{base_url}/getangle{pose}"
                    if requests.post(request_url, files={'img': bytes_data}).status_code == 200:
                        response = requests.post(request_url, files={'img': bytes_data})
                        feedback = response.json().get('angle')
                        score = re.search(r'( \d* )', feedback)[0]
                        cn_request_url = f"{base_url}/getangle{pose}cn"
                        cn_response = requests.post(cn_request_url, files={'img': bytes_data}).json()
                        cn_feedback = cn_response.get('angle')
                        st.metric(label="分数", value=score)
                        if '100' in score:
                            st.balloons()
                        st.write(cn_feedback)
                    else:
                        st.write('对不起 我们的服务器暂时出现延迟问题 请稍后重试')
        else:
            st.write('动作检测失败，请换一张照片尝试')
else:
    # app title and description
    st.header('AI Workout Assistant')
    st.sidebar.title('Upload pics📸 of your workout💪 and get instant✨ feedback!')

    # user upload
    img_file_buffer = st.file_uploader('Choose a file')

    # display image user uploaded
    if img_file_buffer is not None:
        st.sidebar.image(Image.open(img_file_buffer), caption='Image you uploaded')
        # spinner while backend fetches pose classification prediction
        bytes_data = img_file_buffer.getvalue()
        predict_request_url = f"{base_url}/predict_pose"
        if requests.post(predict_request_url, files={'img': bytes_data}).status_code == 200:
            with st.spinner('Wait for it...'):
                pose = requests.post(predict_request_url, files={'img': bytes_data}).json().get('workout pose')
                st.write('⬅️ We have classified your pose - confirm in the side panel!')
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
                    if requests.post(request_url, files={'img': bytes_data}).status_code == 200:
                        response = requests.post(request_url, files={'img': bytes_data})
                        feedback = response.json().get('angle')
                        score = re.search(r'( \d* )', feedback)[0]
                        comment = re.search(r'[A-Z].*', feedback)[0]
                        st.metric(label="Score", value=score)
                        if '100' in score:
                            st.balloons()
                        st.write(comment)
                    else:
                        st.write("We're sorry - our server is experiencing unexpected delays, please try again later.")
        else:
            st.write('Pose not detected. Please try with another picture.')
