# Visualize the predictions from a trained model

from keras.models import Sequential
from keras.models import load_model

import time, sys
import numpy as np

import matplotlib
import matplotlib.pyplot as plt
plt.switch_backend('Qt4Agg')
import matplotlib.image as mpimg

from PIL import Image

action_conditional = 0

SCALE_FACTOR = 255.0

#model_file = '../data/trained_models/sprites_2016-11-20_09:53:23.h5' # action-conditional 
model_file = '../data/trained_models/sprites_2016-11-20_10:15:01.h5'
model = load_model(model_file)

data_file = '../data/sprites/sprites_training.npz'
data = np.load(data_file)
inputs = data['frames']
labels = data['labels']
actions = data['actions']

num_frames = inputs.shape[0]
input_channels = inputs.shape[1]
frame_height = inputs.shape[2]
frame_width = inputs.shape[3]

if len(actions.shape) != 1:
	action_dim = actions.shape[1]
else:
	action_dim = 1

# Display side-by-side the predicted frame and true frame
display_iters = num_frames

# Set up image display
plt.ion()
fig = plt.figure()
pred_handle = fig.add_subplot(1,2,1)
pred_handle.set_title('Predicted Image')
true_handle = fig.add_subplot(1,2,2)
true_handle.set_title('True Image')

for i in range(0, display_iters):
	# Input
	frame_input = inputs[i,:,:,:]
	frame_input = np.reshape(frame_input, [1, input_channels, frame_height, frame_width])
	action_input = actions[i]
	action_input = np.reshape(actions[i], [1, action_dim])

	# Predict Image
	if action_conditional:
		prediction_input = [frame_input, action_input]
	else:
		prediction_input = [frame_input]
	predicted_frame = model.predict(prediction_input)
	predicted_frame = np.reshape(predicted_frame, [frame_height, frame_width])
	predicted_frame = predicted_frame * SCALE_FACTOR

	# Compare to true image
	true_frame = labels[i,:,:,:]
	true_frame = np.reshape(true_frame, [frame_height, frame_width])
	true_frame = true_frame * SCALE_FACTOR

	# Display
	pred_handle = fig.add_subplot(1,2,1)
	true_handle = fig.add_subplot(1,2,2)

	if i == 0:
		phandle = pred_handle.imshow(predicted_frame)
		thandle = true_handle.imshow(true_frame)
	else:
		phandle.set_data(predicted_frame)
		thandle.set_data(true_frame)

	fig.show()
	ans = raw_input("Press [enter] to continue, type anything to exit.")
	if len(ans) > 0:
		sys.exit(0)