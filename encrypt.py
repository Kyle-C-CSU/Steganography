from tkinter import *
from PIL import Image, ImageTk
from tkinter import filedialog
import cv2
import numpy as np
import math

global image

image_size = 300,300

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
	img = Label(app, image=render)
	img.image = render
	img.place(x=20, y=50)


def encrypt_data_into_image():
	global image
	data = text.get(1.0, 'end-1c')
	#load image
	img = cv2.imread(image)
	#break the image into its char level. Represent the chars in ASCII
	data = [format(ord(i), '08b') for i in data]
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
		cv2.imwrite('encrypted_image.png', img)
		#display the success label
		label_success = Label(app, text="Encryption Successful!", bg='lightgreen', font=('arial',20))
		label_success.place(x=160, y=300)

#Define Tkinter object
app = Tk()
app.configure(background='light blue')
app.title('Encrypt')
app.geometry('600x600')
#creat button 
button_chooseImage = Button(app, text='Choose Image', bg='white', fg='black', command=on_click)
button_chooseImage.place(x=250,y=10)
#create text box
text = Text(app,wrap=WORD, width=30)
text.place(x=340, y=55, height=165)

button_encrypt = Button(app, text='Encode Image', bg='white', fg='black', command=encrypt_data_into_image)
button_encrypt.place(x=435,y=230)
app.mainloop()