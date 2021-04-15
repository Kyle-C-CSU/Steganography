from tkinter import *
from PIL import Image, ImageTk
from tkinter import filedialog
import cv2
import numpy as np
import math
import crypto
import time

import constants as const

import helper
import facedetect
import base64

#Open the encrypted image and convert it into a numpy array.
#Obtain the data from the image by going through the encryption algorithm.
#Every pixel in every row has 1 bit of information, which is added into the data variable, using the for loop.
#Check if the EOF character is reached.
#If yes break from the for loop
#Otherwise, continue.
#The ASCII is stored serially in the data variable.
#After obtaining the ASCII bits, bits are grouped into letters by making groups of 8.
#The letters are stored in the message variable, which is linked using the join command in python.
#Finally, the proper message is shown on the screen.
#https://www.section.io/engineering-education/steganography-in-python/

global image

image_size = 300,300
message = 'secretWaterMark'

def on_click():
	global image
	# use the tkinter filedialog library to open the file using a dialog box.
    # obtain the image of the path
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
	#img.place(x=25, y=50)
	#button_encrypt.pack(side = RIGHT)
	button_sign.place(x= 150) #FIXME
	img.pack(side = LEFT)
	#text.pack(side = RIGHT)


def sign_image():
	global image
	global label_success
	label_success.destroy()
	#data = text.get(1.0, 'end-1c')#1.0 = start line 1 char 0, end-1c = read to end -1 char (\n)

	intime = time.time # testing
	
	print(f'Message: {message}\n-\Generating signature...')
	signature = crypto.sign(message)
	print(f'-\nSignature:\n{signature}')
	signature = base64.b64encode(signature)
	print(f'-\nBase64 Signature:\n{signature}')

	data = signature

	#load image
	img = cv2.imread(image)



	# FACIAL DETECTION START

	# establish initial bounds
	# the LSB portion is already set up to use the values of bounds
	bounds = [0, 0, img.shape[0], img.shape[1]] # [x, y, width, height] where x, y is for the top left bounding pixel
	bounds = facedetect.getFace(image)

	# FACIAL DETECTION END

	#remove image extension
	image = image[:image.rfind('.')]

	# STEG START
	
	# check if data (+ 5-character stopping sequence) can fit in the bounds
	if (len(data) + 5) * 8 > bounds[2] * bounds[3] * 3:
		raise ValueError('ERROR: too much data to fit in facial bounds')

	# append stopping sequence of 5 underscores '_____'
	data_str = str(data) + '_____'

	print('-\nFINAL DATA STRING:\n' + data_str)
	# convert data to binary
	bin_data = helper.to_binary(data_str)

	data_index = 0

	for y in range(bounds[1], bounds[3]): # rows
		for x in range(bounds[0], bounds[2]): # cols
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
				img[x][y][2] = int(r[:-1] + bin_data[data_index], 2)
				data_index += 1
			
			# check if we've reached the end of our data
			if data_index >= len(bin_data):
				break

	# STEG END


	#write the signed image into a new file
	cv2.imwrite(f'{image}_signed.png', img)

	outtime = time.time # testing

	signtime = outtime - intime	# testing

	print(f"""----------
	FILENAME: {image}
	DIMENSIONS: {img.shape[0]} x {img.shape[1]}
	MESSAGE LENGTH: {len(message)}
	SIGNING TIME: {signtime}
	----------""")



	#display the success label
	label_success = Label(bottom_frame, text="Signing Successful!", bg='lightgreen', font=('arial',20))
	#label_success.place(x=160, y=300)
	label_success.pack(side = LEFT)
#create instance of asymetric keys
#crypto.genAsyKeys()

#Design Tkinter main app frame 600 x 600
app = Tk()
app.configure(background='light blue')
app.title('Sign')
app.geometry('600x600')

#Design Tkinter top frame 
top_frame = Frame(app)
top_frame.configure(background='light blue')
top_frame.place(x= 150) #FIXME

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
#button_chooseImage.place(x=250,y=10)
button_chooseImage.pack(side = LEFT)

#create text box
#text = Text(middle_frame, wrap=WORD, width=30)
#text.tag_config('defaultText', foreground = 'gray')
#text.insert(END,'Enter CipherKey','defaultText')
#text.place(x=340, y=55, height=165)
#text.pack(side = RIGHT)

#create sign button
button_sign = Button(top_frame, text='Sign Image', bg='white', fg='black', command=sign_image)
#button_encrypt.place(x=250,y=250)
#button_encrypt.pack(side = RIGHT)

label_success = Label(bottom_frame, text='', bg='light blue')
app.mainloop()