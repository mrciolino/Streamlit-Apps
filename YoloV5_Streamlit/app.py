import os
import torch
import warnings
import numpy as np
from PIL import Image
from io import BytesIO
import streamlit as st

# setttings
os.environ['CUDA_VISIBLE_DEVICES'] = '1'
warnings.filterwarnings('ignore')
st.set_page_config()


@st.cache(show_spinner=False)
def load_model():
    with st.spinner('Getting Neruons in Order ...'):
        model = torch.hub.load('ultralytics/yolov5', 'custom', path='weights/xview_movers.pt', force_reload=True)
        return model


def run(model, file_path):
    # file_path = "refs/sat.png"
    results = model(file_path)
    return results


def show_detects(results):
    st.title("Results")
    st.image(results.render(), use_column_width=True)
    st.dataframe(results.pandas().xyxy[0])


def get_detect_path(results):
    img = Image.fromarray(np.squeeze(results.render()))
    buf = BytesIO()
    img.save(buf, format="JPEG")
    byte_im = buf.getvalue()
    return byte_im


def process(upload):
    # save upload to file
    filename = upload.name.split('.')[0]
    filetype = upload.name.split('.')[-1]
    name = len(os.listdir("images")) + 1
    file_path = os.path.join('images', f'{name}.{filetype}')
    with open(file_path, "wb") as f:
        f.write(upload.getbuffer())

    # predict detections and show results
    results = run(model, file_path)
    show_detects(results)

    # offer download
    detection_image = get_detect_path(results)
    st.download_button(label="Download Detections", data=detection_image,
                       file_name='{}.jpeg'.format(filename),
                       mime='image/jpeg')

    # clean up - if over 1000 images in folder, delete oldest 1
    if len(os.listdir("images")) > 1000:
        oldest = min(os.listdir("images"), key=os.path.getctime)
        os.remove(os.path.join("images", oldest))


def main(model):

    # create homepage feel
    st.image(os.path.join('refs', 'xview.png'), use_column_width=True)

    # title
    st.title("YoloV5 Object Detection")

    # project descriptions
    st.markdown("**YOLOv5** 🚀 is a family of object detection architectures and models pretrained on the COCO dataset, \
                and represents Ultralytics open-source research into future vision AI methods, incorporating lessons learned \
                and best practices evolved over thousands of hours of research and development. **xView** 🛰️ is one of the largest \
                publicly available data sets of overhead imagery. It contains images from complex scenes around the \
                world, annotated using bounding boxes. The DIUx xV iew 2018 Detection Challenge is focused on \
                accelerating progress in four computer vision frontiers.", unsafe_allow_html=True)

    # example
    if st.button("Example Image"):
        with st.spinner('Detecting and Counting Single Image...'):
            results = run(model, "refs/sat.png")
            show_detects(results)
            if st.button("Clear Example"):
                st.markdown("")

    # upload
    upload = st.file_uploader('Upload Images/Video', type=['jpg', 'jpeg', 'png'])
    if upload is not None:
        filetype = upload.name.split('.')[-1]
        if filetype in ['jpg', 'jpeg', 'png']:
            with st.spinner('Detecting and Counting Single Image...'):
                process(upload)
        else:
            st.warning('Unsupported file type.')


if __name__ == '__main__':
    model = load_model()
    main(model)
