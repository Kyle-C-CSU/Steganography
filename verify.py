import cv2
from tkinter import filedialog, Tk, Button, Label
from PIL import Image, ImageTk
import numpy as np
import Crypto3 as crypto

image_size = 300,300
original_message = 'secretWaterMark'

def decrypt():
    global message_label
    message_label.destroy()
    # use the tkinter filedialog library to open the file using a dialog box.
    # obtain the image of the path
    image = filedialog.askopenfilename()
    
    # load the image using the path
    load_image = Image.open(image)
    # set the image into the gui using the thumbnail function from tkinter
    load_image.thumbnail(image_size, Image.ANTIALIAS)
    
    # load the image as a numpy array for efficient computation and change the type to unsigned integer
    np_load_image = np.asarray(load_image)
    np_load_image = Image.fromarray(np.uint8(np_load_image))
    render = ImageTk.PhotoImage(np_load_image)
    img = Label(app, image=render)
    img.image = render
    img.pack()

    # algorithm to decrypt the data from the image
    img = cv2.imread(image)
    data = []
    stop = False
    for index_i, i in enumerate(img):
        i.tolist()
        for index_j, j in enumerate(i):
            if((index_j) % 3 == 2):
                # first pixel
                data.append(bin(j[0])[-1])
                # second pixel
                data.append(bin(j[1])[-1])
                # third pixel
                if(bin(j[2])[-1] == '1'):
                    stop = True
                    break
            else:
                # first pixel
                data.append(bin(j[0])[-1])
                # second pixel
                data.append(bin(j[1])[-1])
                # third pixel
                data.append(bin(j[2])[-1])
        if(stop):
            break
    bytelist = []
    # join all the bits to form letters (ascii representation)
    for i in range(int((len(data)+1)/8)):
        bytelist.append(data[i*8:(i*8+8)])
    # join all the letters to form the message.
    #print(f'printing byte list: \n{bytelist}')
    bytes_to_intlist = [int(''.join(i), 2) for i in bytelist]
    #print(f'converting bytes to ints: \n{bytes_to_intlist}')
    bytearrayObject = bytearray(bytes_to_intlist)
    #print(f'converting ints to byte array: \n{bytearrayObject}')
    encrypted_message = bytes(bytearrayObject)
    print(f'retreiving encrypted message: \n{encrypted_message}')
    #message = b''.join(list(message))
    try:
        print('decrypting message...')
        message = crypto.decrypt(encrypted_message,original_message)
        print(f'Authentication Succesfull!\nmessage: {message}')
        message_label = Label(app, text='Authentication Succesfull!', bg='light green', font=("arial", 20),wraplength=500)
    except crypto.cryptography.exceptions.InvalidSignature:
        message = 'Failed Authentication...'
        print(f'decryption unsuccessfull...\n{message}')
        message_label = Label(app, text=message, bg='red', font=("arial", 20),wraplength=500)
    #message_label.place(x=150, y=250)
    message_label.pack()

# Defined the TKinter object app with background lavender, title Decrypt, and app size 600*600 pixels.
app = Tk()
app.configure(background='light blue')
app.title("Decrypt")
app.geometry('600x600')
# Add the button to call the function decrypt.
main_button = Button(app, text="Decrypt image", bg='white', fg='black', command=decrypt)
#main_button.place(x=250, y=10)
main_button.pack()
message_label = Label(app, text='', bg='light blue')
#message_label.place(x=150, y=250)
message_label.pack()
app.mainloop()