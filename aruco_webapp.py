

# import libs
from skimage import measure, io, img_as_ubyte, morphology, util, color
from skimage.color import label2rgb, rgb2gray
import numpy as np
import pandas as pd
import cv2
import streamlit as st

DEMO_IMAGE = 'demo.png' # a demo image for the segmentation page, if none is uploaded
favicon = 'favicon.png'

# main page
st.set_page_config(page_title='Aruco area calculation - LeeEl Yehezkel', page_icon = favicon, layout = 'wide', initial_sidebar_state = 'auto')
st.title('Image area calculation using aruco, by LeeEl Yehezkel')

# main page
st.set_page_config(page_title='Aruco area calculation - LeeEl Yehezkel', page_icon = favicon, layout = 'wide', initial_sidebar_state = 'auto')
st.title('Image area calculation using aruco, by LeeEl Yehezkel')

# side bar
st.markdown(
    """
    <style>
    [data-testid="stSidebar"][aria-expanded="true"] . div:first-child{
        width: 350px
    }
    
    [data-testid="stSidebar"][aria-expanded="false"] . div:first-child{
        width: 350px
        margin-left: -350px
    }    
    </style>
    
    """,
    unsafe_allow_html=True,


)

st.sidebar.title('Aruco Sidebar')
st.sidebar.subheader('Site Pages')

# using st.cache so streamlit runs the following function only once, and stores in cache (until changed)
@st.cache()

# take an image, and return a resized that fits our page
def image_resize(image, width=None, height=None, inter = cv2.INTER_AREA):
    dim = None
    (h,w) = image.shape[:2]
    
    if width is None and height is None:
        return image
    
    if width is None:
        r = width/float(w)
        dim = (int(w*r),height)
    
    else:
        r = width/float(w)
        dim = (width, int(h*r))
        
    # resize the image
    resized = cv2.resize(image, dim, interpolation=inter)
    
    return resized

# add dropdown to select pages on left
app_mode = st.sidebar.selectbox('Navigate',
                                  ['About App', 'Find Area'])

# About page
if app_mode == 'About App':
    st.markdown('In this app we will find the area of the image using the Aruco method.')
    
    
    # side bar
    st.markdown(
        """
        <style>
        [data-testid="stSidebar"][aria-expanded="true"] . div:first-child{
            width: 350px
        }

        [data-testid="stSidebar"][aria-expanded="false"] . div:first-child{
            width: 350px
            margin-left: -350px
        }    
        </style>

        """,
        unsafe_allow_html=True,


    )

    # add a video to the page
    st.video('https://www.youtube.com/watch?v=UlM2bpqo_o0')


    st.markdown('''
                ## About the app \n
                Hey, this web app is a great one to calculate image area. \n
                 \n
                Enjoy! LeeEl


                ''')

# Run image
if app_mode == 'Find Area':
    
    st.sidebar.markdown('---') # adds a devider (a line)
    
    # side bar
    st.markdown(
        """
        <style>
        [data-testid="stSidebar"][aria-expanded="true"] . div:first-child{
            width: 350px
        }

        [data-testid="stSidebar"][aria-expanded="false"] . div:first-child{
            width: 350px
            margin-left: -350px
        }    
        </style>

        """,
        unsafe_allow_html=True,


    )

#define aruco function to call further down
def aruco_area(image):
  grayscale = img_as_ubyte(rgb2gray(image))
  
  # Load Aruco detector
  parameters = cv2.aruco.DetectorParameters_create()
  aruco_dict = cv2.aruco.Dictionary_get(cv2.aruco.DICT_5X5_50)# Get Aruco marker
  corners, _, _ = cv2.aruco.detectMarkers(image, aruco_dict, parameters=parameters)
  
  # Aruco Area
  aruco_area = cv2.contourArea (corners[0])

  # Pixel to cm ratio
  pixel_cm_ratio = 5*5 / aruco_area# since the AruCo is 5*5 cm, so we devide 25 cm*cm by the number of pixels
  return pixel_cm_ratio

# read an image from the user
img_file_buffer = st.sidebar.file_uploader("Upload an image", type=['jpg', 'jpeg', 'png'])

# assign the uplodaed image from the buffer, by reading it in
if img_file_buffer is not None:
    image = io.imread(img_file_buffer)
else: # if no image was uploaded, then segment the demo image
    demo_image = DEMO_IMAGE
    image = io.imread(demo_image)

# display on the sidebar the uploaded image
st.sidebar.text('Original Image')
st.sidebar.image(image)
val = aruco_area(image)
st.markdown('Ratio - Each pixel is',val, 'cm*cm')
