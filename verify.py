import cv2
from tkinter import filedialog, Tk, Button, Label
from PIL import Image, ImageTk
import numpy as np
import Crypto3 as crypto

import helper
import base64

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

    # FACIAL DETECTION START

    # TODO: We should be able to just copy the facial detection code straight from sign.py, since identical images should produce identical
    # bounding boxes. If the bounding box is different, it probably indicates a tampered image, so failed authentication is what we want anyway.

    # establish initial bounds
    # the LSB portion is already set up to use the values of bounds
    bounds = [0, 0, img.shape[0], img.shape[1]] # [x, y, width, height] where x, y is for the top left bounding pixel


    # FACIAL DETECTION END


    # STEG START
    
    bin_data = ''
    stop_found = False

    for y in range(bounds[3]): # rows
        for x in range(bounds[2]): # cols
            # get red, green, blue LSBs and append to the data string
            r, g, b = helper.to_binary(img[x][y])
            bin_data += r[-1] + g[-1] + b[-1]

    # convert string of bits into array of byte-length strings
    byte_data = [bin_data[i : i+8] for i in range(0, len(bin_data), 8)]

    # convert byte array to character string
    data_str = ''
    for byte in byte_data:
        data_str += chr(int(byte, 2))

        #check for stop sequence of 5 underscores ('_____') in last 5 characters
        if data_str[-5:] == '_____':
            # remove the stop sequence from the data
            data_str = data_str[:-5]
            stop_found = True
            break


    if not stop_found:
        # signature must be invalid since it was never terminated with the stop sequence
        message = 'Failed Authentication...'
        print(f'[*] AUTHENTICATION FAILED\nReason: no stop sequence found')
        message_label = Label(app, text=message, bg='red', font=("arial", 20),wraplength=500)
        #message_label.place(x=150, y=250)
        message_label.pack()
        return
    

    # STEG END
    
    print(f'-\nBase64 Signature:\n{data_str}')

    # check if all the characters are ascii. if they aren't we know it can't have the correct signature
    # why? because we used a base64-encoded string to apply LSB, which only accepts ascii characters.
    # FIXME: something with this seems to be working wrong, because things get by it, but still cause an error
    # due to having unsupported characters for b64decode(). The stop sequence check tends to catch most things before
    # can even get this far though, so it isn't a huge deal presently.
    if not data_str.isascii:
        message = 'Failed Authentication...'
        print(f'[*] AUTHENTICATION FAILED\nReason: invalid characters found in signature')
        message_label = Label(app, text=message, bg='red', font=("arial", 20),wraplength=500)
        #message_label.place(x=150, y=250)
        message_label.pack()
        return

    # Decode the base64 signature into its original format, removing the residual "b'" from the beginning and "'" from the end
    signature = base64.b64decode(data_str[2:-1])
    print(f'-\nDecoded Signature:\n{signature}\n-')

    # Attempt to authenticate the image by verifying the signature is valid
    try:
        print('Decrypting Message...')
        message = crypto.decrypt(signature,original_message)
        print(f'[*] AUTHENTICATION SUCCESSFUL!')
        message_label = Label(app, text='Authentication Succesful!', bg='light green', font=("arial", 20),wraplength=500)
    except crypto.cryptography.exceptions.InvalidSignature:
        message = '[*] AUTHENTICATION FAILED'
        print(f'{message}\nReason: signature did not match expected result')
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