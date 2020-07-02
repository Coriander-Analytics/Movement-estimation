import tensorflow as tf
import numpy as np
import cv2 as cv
from PIL import Image

path = "models/posenet_mobilenet_v1_100_257x257_multi_kpt_stripped.tflite"
template_path = "example.jpg"

interpreter = tf.lite.Interpreter(model_path=path)
interpreter.allocate_tensors()

input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()
height = input_details[0]['shape'][1]
width = input_details[0]['shape'][2]

print("Height:", height)
print("Width:", width)

template_image_src = cv.imread(template_path)
# src_tepml_width, src_templ_height, _ = template_image_src.shape 
template_image = cv.resize(template_image_src, (width, height))
#cv2_imshow(template_image)

# add a new dimension to match model's input
template_input = np.expand_dims(template_image.copy(), axis=0)

float_model = input_details[0]['dtype'] == np.float32
if float_model:
    template_input = (np.float32(template_input) - 127.5) / 127.5

# Set the value of the input tensor
interpreter.set_tensor(input_details[0]['index'], template_input) # Run the calculations
interpreter.invoke() # Extract output data from the interpreter
template_output_data = interpreter.get_tensor(output_details[0]['index'])
template_offset_data = interpreter.get_tensor(output_details[1]['index'])

# Getting rid of the extra dimension
template_heatmaps = np.squeeze(template_output_data)
template_offsets = np.squeeze(template_offset_data)
print("template_heatmaps' shape:", template_heatmaps.shape)
print("template_offsets' shape:", template_offsets.shape)

# The output consist of 2 parts:
# - heatmaps (9,9,17) - corresponds to the probability of appearance of 
# each keypoint in the particular part of the image (9,9)(without applying sigmoid 
# function). Is used to locate the approximate position of the joint
# - offset vectors (9,9,34) is called offset vectors. Is used for more exact
#  calculation of the keypoint's position. First 17 of the third dimension correspond
# to the x coordinates and the second 17 of them correspond to the y coordinates
