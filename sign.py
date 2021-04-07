from tkinter import *
from PIL import Image, ImageTk
from tkinter import filedialog
import cv2
import numpy as np
import math
import Crypto3 as crypto
import time

import constants as const


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
signature = 'secretWaterMark'

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
	button_encrypt.place(x= const.RIGHT_BUTTON)
	img.pack(side = LEFT)
	text.pack(side = RIGHT)


def encrypt_data_into_image():
	global image
	global label_success
	label_success.destroy()
	#data = text.get(1.0, 'end-1c')#1.0 = start line 1 char 0, end-1c = read to end -1 char (\n)
	data =  signature
	print(f'signature: {data}\nencrypting data...')
	data = crypto.encrypt(data)
	print(f'encrypted data: {data}')
	#load image
	img = cv2.imread(image)
	#remove image extension .ext = 4
	image = image[:len(image)-4]
	#break the image into its char level. Represent the chars in ASCII
	data = [format(i, '08b') for i in data]
	_, width, _ = img.shape
	#algorithm to encode the image
	PixReq = len(data)*3

	RowReq = PixReq/width
	RowReq = math.ceil(RowReq)

	count = 0
	charCount = 0

	for i in range(RowReq + 1):
		while(count < width and charCount < len(data)):
			char = data[charCount]
			charCount += 1

			for index_k, k in enumerate(char):
				if((k == '1' and img[i][count][index_k % 3] % 2 == 0) or k == '0' and img[i][count][index_k % 3] % 2 == 1):
					img[i][count][index_k % 3] -= 1
				if index_k % 3 == 2 : 
					count += 1
				if index_k == 7:
					if(charCount*3 < PixReq and img[i][count][2] % 2 == 1):
						img[i][count][2] -= 1
					if(charCount*3 >= PixReq and img [i][count][2] % 2 == 0):
						img[i][count][2] -= 1
					count += 1
		count = 0
		#write the encrypted image into a new file
		cv2.imwrite(f'{image}_encrypted.png', img)
		#display the success label
		label_success = Label(bottom_frame, text="Encryption Successful!", bg='lightgreen', font=('arial',20))
		#label_success.place(x=160, y=300)
	label_success.pack(side = LEFT)
#create instance of asymetric keys
#crypto.genAsyKeys()

#Design Tkinter main app frame 600 x 600
app = Tk()
app.configure(background='light blue')
app.title('Encrypt')
app.geometry('600x600')

#Design Tkinter top frame 
top_frame = Frame(app)
top_frame.configure(background='light blue')
top_frame.place(x= const.LEFT_BUTTON)

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

#create encrypt button
button_encrypt = Button(top_frame, text='Encode Image', bg='white', fg='black', command=encrypt_data_into_image)
#button_encrypt.place(x=250,y=250)
#button_encrypt.pack(side = RIGHT)

label_success = Label(bottom_frame, text='', bg='light blue')
app.mainloop()