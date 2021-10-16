from tkinter import *
from PIL import Image, ImageTk
from tkinter import filedialog
import cv2
import numpy as np
import math
import crypto
import time
import constants as const

import sys
import helper
import facedetect
import base64

global image

# image size constraints for GUI
image_size = 300,300

watermarkfile = open('watermarks.txt', 'r')
message = watermarkfile.read()


def on_click():
	global image

	# retrieve image path using file dialog
	image = filedialog.askopenfilename()

	# load the image using the path
	load_image = Image.open(image)

	# set the image into the GUI using the thumbnail function from tkinter
	load_image.thumbnail(image_size, Image.ANTIALIAS)

	# load the image as a numpy array for efficient computation and change the type to unsigned integer
	np_load_image = np.asarray(load_image)
	np_load_image = Image.fromarray(np.uint8(np_load_image))
	render = ImageTk.PhotoImage(np_load_image)
	img = Label(middle_frame, image=render)
	img.image = render

	button_sign.place(x = const.RIGHT_BUTTON)
	img.pack(side = LEFT)


# create a signature from a message and embed it into an image
def sign_image():
	global image
	global label_success
	label_success.destroy()

	# used for performance metric
	intime = time.time_ns()
	
	# Generate signature using message
	signature = crypto.sign(message)
	print(f'-\nSignature:\n{signature}')

	# Convert signature to base64
	signature = base64.b64encode(signature)
	print(f'-\nBase64 Signature:\n{signature}')

	data = signature

	# load the image
	img = cv2.imread(image)



    #### FACIAL DETECTION ####

	# establish initial bounds
	# [x, y, width, height] where x, y is for the top left bounding pixel
	bounds = [0, 0, img.shape[0], img.shape[1]]

    # update our bounds based on the largest face detected
	bounds = facedetect.getFace(image)

	# narrow our facial bounds to: 
    # - improve performance during verification
    # - focus our manipulation onto the main facial area
	bounds = [bounds[0] + bounds[2] // 4, bounds[1] + bounds[3] // 4, bounds[2] // 2, bounds[3] // 2]

	
    #### STEGANOGRAPHY ####
    # strip the signature from the image by inverting our LSB algorithm
	
	# check if data (+ 5-character stopping sequence) can fit in the bounds
	if (len(data) + 5) * 8 > bounds[2] * bounds[3] * 3:
		raise ValueError('ERROR: too much data to fit in facial bounds')

	# append stopping sequence of 5 underscores '_____'
	data_str = str(data) + '_____'

	print('-\nFINAL DATA STRING:\n' + data_str)
	
	# convert data to binary
	bin_data = helper.to_binary(data_str)

	# keep track of where we are in bin_data
	data_index = 0

	for x in range(bounds[1], bounds[1] + bounds[3]): # rows
		for y in range(bounds[0], bounds[0] + bounds[2]): # cols
			r, g, b = helper.to_binary(img[x, y])

			# apply LSB manipulation
			if data_index < len(bin_data):
				# red channel: replace LSB with current index of our binary data
				img[x][y][0] = int(r[:-1] + bin_data[data_index], 2)
				data_index += 1
			if data_index < len(bin_data):
				# green channel: replace LSB with current index of our binary data
				img[x][y][1] = int(g[:-1] + bin_data[data_index], 2)
				data_index += 1
			if data_index < len(bin_data):
				# blue channel: replace LSB with current index of our binary data
				img[x][y][2] = int(b[:-1] + bin_data[data_index], 2)
				data_index += 1
			
			# check if we've reached the end of our data
			if data_index >= len(bin_data):
				break

	# path and image name were separated  and modified for organization during experimentation
	path = image[:image.rfind('/')]
	image = image[image.rfind('/'):image.rfind('.')] + '_signed.png'

	# write the signed image to a new file
	cv2.imwrite(f'{path}{image}', img)

	# used for performance metrics
	outtime = time.time_ns() 
	signtime = (outtime - intime) // 1000000

	# create a clean console output for gathering performance metrics
	print(f"""----------
	FILENAME: {path}{image}
	DIMENSIONS: {img.shape[1]} x {img.shape[0]}
	MESSAGE LENGTH: {len(message)}
	SIGNING TIME: {signtime}
----------""")

	#display the success label
	label_success = Label(bottom_frame, text="Signing Successful!", bg='lightgreen', font=('arial',20))
	label_success.pack(side = LEFT)


#Design Tkinter main app frame 600 x 600
app = Tk()
app.configure(background='light blue')
app.title('Sign')
app.geometry('600x600')

#Design Tkinter top frame 
top_frame = Frame(app)
top_frame.configure(background='light blue')
top_frame.place(x = const.LEFT_BUTTON) #FIXME

#Design Tkinter middle frame
middle_frame = Frame(top_frame)
middle_frame.configure(background= 'light blue')
middle_frame.pack(side = BOTTOM)

#Design Tkinter bottom frame 
bottom_frame = Frame(middle_frame)
bottom_frame.configure(background='light blue')
bottom_frame.pack(side = BOTTOM)

#create choose image button 
button_chooseImage = Button(top_frame, text='Choose Image', bg='white', fg='black', command=on_click)
button_chooseImage.pack(side = LEFT)

#create sign button
button_sign = Button(top_frame, text='Sign Image', bg='white', fg='black', command=sign_image)

label_success = Label(bottom_frame, text='', bg='light blue')
app.mainloop()