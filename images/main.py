import streamlit as st
import numpy as np
import cv2
from PIL import Image

# Title of the web-app
st.title('Barcode Decoding with OpenCV')

# Uploading the images
img_file_buffer = st.file_uploader("Upload an image for decoding", type=["jpg", "jpeg", "png"])

def preprocess_image(image):
    # Convert the image to grayscale
    image = np.array(Image.open(img_file_buffer))
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Apply thresholding to convert to binary image
    _, binary = cv2.threshold(gray, 128, 255, cv2.THRESH_BINARY_INV)
    
    return binary

def find_start_and_end(binary_image):
    # Find the leftmost and rightmost non-zero pixel columns
    start_col = np.argmax(binary_image.sum(axis=0) > 0)
    end_col = binary_image.shape[1] - np.argmax(np.flip(binary_image.sum(axis=0)) > 0)
    
    return start_col, end_col

def decode_barcode(binary_image, start_col, end_col):
    # Decoding logic (simplified for example)
    barcode_data = ""
    
    # Assuming each bar is 3 pixels wide
    bar_width = 3
    for col in range(start_col, end_col, bar_width):
        bar_sum = binary_image[:, col:col+bar_width].sum()
        if bar_sum > binary_image.shape[0] * bar_width // 2:
            barcode_data += "1"
        else:
            barcode_data += "0"
    
    return barcode_data

if img_file_buffer is not None:

  image = Image.open(img_file_buffer) # read image with PIL library
  st.image(image) #display

  binary_image = preprocess_image(img_file_buffer)
  st.image(binary_image)

  start_col, end_col = find_start_and_end(binary_image)
 
