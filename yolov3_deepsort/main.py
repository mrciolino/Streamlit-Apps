import os
import wget
import streamlit as st


def get_classes():
    return "suitcase, frisbee, skis, snowboard, sports ball, kite, baseball bat, baseball glove, skateboard, surfboard, tennis racket, bottle, wine glass, cup, fork, knife, spoon, bowl, banana, apple, sandwich, orange, broccoli, carrot, hot dog, pizza, donut, cake, chair, sofa, pottedplant, bed, diningtable, toilet, tvmonitor, laptop, mouse, remote, keyboard, cell phone, microwave, oven, toaster, sink, refrigerator, book, clock, vase, scissors, teddy bear, hair drier, toothbrush"


def load_model():
    if not os.path.exists('weights/yolov3.weights'):
        wget.download('https://pjreddie.com/media/files/yolov3.weights', 'weights/yolov3.weights')
        os.system("python load_weights.py")


def run(video_file):
    with open('input/test.mp4', 'wb') as f:
        f.write(video_file.read())
    os.system("python object_tracker.py --video ./input/test.mp4 --output ./output/results.avi")
    os.system("ffmpeg -y -i ./output/results.avi -vcodec libx264 ./output/results.mp4")


def process(upload, col3):
    with st.spinner('Detecting and Tracking ...'):
        run(upload)
    video_bytes = open('output/results.mp4', 'rb').read()
    st.video(video_bytes)
    col3.download_button(label="Download Tracked Video", data=video_bytes, file_name='results.mp4', mime='video/mp4')


def main():

    # create homepage feel
    st.set_page_config()
    st.image("https://media.giphy.com/media/CBGnySk8skmldpCzFQ/giphy.gif", use_column_width=True)
    st.markdown("<h1 style='text-align: center; color: white;'>YOLOv3 Deep Sort</h1>", unsafe_allow_html=True)

    # project descriptions
    st.markdown(
        "This repository implements YOLOv3 and Deep SORT in order to perfrom real-time object tracking. Yolov3 \
        is an algorithm that uses deep convolutional neural networks to perform object detection. We can feed \
        these object detections into Deep SORT (Simple Online and Realtime Tracking with a Deep Association \
        Metric) in order for a real-time object tracker to be created. \
        The model is based on the paper \
        <a href='https://arxiv.org/abs/1804.02767'> YOLOv3: An Incremental Improvement</a>. Adapted from  \
        <a href='https://github.com/theAIGuysCode/yolov3_deepsort'>yolov3_deepsort</a>.  \
        Check it out for yourself below!",
        unsafe_allow_html=True)

    # make columns for extra info
    col1, col2, col3 = st.columns(3)
    if col1.button("Display Trackable Objects"):
        st.info(str(get_classes()))
    if col2.button("Run Small Demo Video"):
        upload = open('input/small_test.mp4', 'rb')
        process(upload, col3)

    # logic
    upload = st.file_uploader('Upload Video', type=['gif', 'avi', 'mp4'])
    if upload is not None:
        filetype = upload.name.split('.')[-1]
        if filetype in ['avi', 'mp4', 'gif']:
            process(upload, col3)
        else:
            st.warning('Unsupported file type.')


if __name__ == '__main__':
    load_model()
    main()
