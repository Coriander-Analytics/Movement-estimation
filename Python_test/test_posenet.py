import tensorflow as tf
import numpy as np
import cv2
from PIL import Image

"""
	Note: Most of this is copied from a Medium article by Ivan Kunyankin at
	https://towardsdatascience.com/pose-estimation-and-matching-with-tensorflow-lite-posenet-model-ea2e9249abbd
"""

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

template_image_src = cv2.imread(template_path)
# src_tepml_width, src_templ_height, _ = template_image_src.shape
template_image = cv2.resize(template_image_src, (width, height))
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

def parse_output(heatmap_data,offset_data, threshold):

  '''
  Input:
    heatmap_data - hetmaps for an image. Three dimension array
    offset_data - offset vectors for an image. Three dimension array
    threshold - probability threshold for the keypoints. Scalar value
  Output:
    array with coordinates of the keypoints and flags for those that have
    low probability
  '''

  joint_num = heatmap_data.shape[-1]
  pose_kps = np.zeros((joint_num,3), np.uint32)

  for i in range(heatmap_data.shape[-1]):

      joint_heatmap = heatmap_data[...,i]
      max_val_pos = np.squeeze(np.argwhere(joint_heatmap==np.max(joint_heatmap)))
      remap_pos = np.array(max_val_pos/8*257,dtype=np.int32)
      pose_kps[i,0] = int(remap_pos[0] + offset_data[max_val_pos[0],max_val_pos[1],i])
      pose_kps[i,1] = int(remap_pos[1] + offset_data[max_val_pos[0],max_val_pos[1],i+joint_num])
      max_prob = np.max(joint_heatmap)

      if max_prob > threshold:
        if pose_kps[i,0] < 257 and pose_kps[i,1] < 257:
          pose_kps[i,2] = 1

  return pose_kps

""" Draws keypoints on image """
def draw_kps(show_img, kps, ratio=None):
    for i in range(5,kps.shape[0]):
      if kps[i,2]:
        if isinstance(ratio, tuple):
          cv2.circle(show_img,(int(round(kps[i,1]*ratio[1])),int(round(kps[i,0]*ratio[0]))),2,(0,255,255),round(int(1*ratio[1])))
          continue
        cv2.circle(show_img,(kps[i,1],kps[i,0]),2,(0,255,255),-1)
    return show_img

"""
	Q: What's the 127.5 bit for? Some sort of normalization?
"""
template_show = np.squeeze((template_input.copy()*127.5+127.5)/255.0)
template_show = np.array(template_show*255,np.uint8)
template_kps = parse_output(template_heatmaps,template_offsets,0.3)

cv2.imshow("Image with drawn joints", draw_kps(template_show.copy(),template_kps))
cv2.waitKey(0) # waits until a key is pressed
cv2.destroyAllWindows() # destroys the window showing image
