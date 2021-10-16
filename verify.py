import cv2
from tkinter import filedialog, Tk, Button, Label
from PIL import Image, ImageTk
import numpy as np
import crypto
import time

import helper
import facedetect
import base64

# image size constraints for GUI
image_size = 300, 300

# pull watermark from text file
watermarkfile = open('watermarks.txt','r')
original_message = watermarkfile.read()



# Verify if an image is authentic (has an intact signature)
def verify_image():
    global message_label
    message_label.destroy()
    
    # retrieve image path using file dialog
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

    # used for performance metric
    intime = time.time_ns()

    # get a new reference to the image
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
    

    bin_data = '' # a string of our binary data, initially empty
    stop_found = False # true if we have found our stop sequence (5 underscores)

    # loop through each pixel within our facial bounds
    for x in range(bounds[1], bounds[1] + bounds[3]):
        for y in range(bounds[0], bounds[0] + bounds[2]):

            # get red, green, blue LSBs and append to the data string
            r, g, b = helper.to_binary(img[x][y])
            bin_data += r[-1] + g[-1] + b[-1]

    # convert string of bits into array of byte-length strings
    byte_data = [bin_data[i : i+8] for i in range(0, len(bin_data), 8)]

    # convert byte array to character string
    data_str = ''
    for byte in byte_data:
        data_str += chr(int(byte, 2))

        #check for stop sequence of 5 underscores ('_____') in last 5 characters added
        if data_str[-5:] == '_____':
            # remove the stop sequence from the data
            data_str = data_str[:-5]
            stop_found = True
            break


    # check if we ever found the stop sequence
    if not stop_found:
        # signature must be invalid since it was never terminated with the stop sequence
        message = 'Failed Authentication...'
        print(f'AUTHENTICATION FAILED\nReason: no stop sequence found')

        # used for performance metrics
        verifytime = (time.time_ns() - intime) // 1000000
        testout(image, img, original_message, verifytime, "fake")

        # display failed authentication message
        message_label = Label(app, text=message, bg='red', font=("arial", 20),wraplength=500)
        message_label.pack()
        return
    
    
    print(f'-\nBase64 Signature:\n{data_str}')

    # Decode the base64 signature into its original format, removing the residual " b' " from the beginning and " ' " from the end
    try:
        signature = base64.b64decode(data_str[2:-1])
    except:
        # part of our base64 string can't be decoded
        message = 'Failed Authentication...'
        print(f'AUTHENTICATION FAILED\nReason: invalid characters found in signature')

        # used for performance metrics
        verifytime = (time.time_ns() - intime) // 1000000
        testout(image, img, original_message, verifytime, "fake")

        #display failed authentication message
        message_label = Label(app, text=message, bg='red', font=("arial", 20),wraplength=500)
        message_label.pack()
        return

    print(f'-\nDecoded Signature:\n{signature}\n-')

    # Attempt to authenticate the image by verifying the signature is valid
    try:
        print('Verifying image...')
        message = crypto.verify(signature,original_message)
        print(f'AUTHENTICATION SUCCESSFUL!')

        verifytime = (time.time_ns() - intime) // 1000000
        testout(image, img, original_message, verifytime, "real")

        message_label = Label(app, text='Authentication Succesful!', bg='light green', font=("arial", 20),wraplength=500)
    except crypto.cryptography.exceptions.InvalidSignature:
        message = 'AUTHENTICATION FAILED'
        print(f'{message}\nReason: signature did not match expected result')

        verifytime = (time.time_ns() - intime) // 1000000
        testout(image, img, original_message, verifytime, "fake")

        message_label = Label(app, text=message, bg='red', font=("arial", 20),wraplength=500)
    message_label.pack()



# create a clean console output for gathering performance metrics
def testout(image, img, message, verifytime, result):
    print(f"""----------
    FILENAME: {image}
    DIMENSIONS: {img.shape[1]} x {img.shape[0]}
    MESSAGE LENGTH: {len(message)}
    VERIFY TIME: {verifytime}
    RESULT: {result}
----------""")


# Define the TKinter object app with background light blue, title Verify, and app size 600*600 pixels
app = Tk()
app.configure(background='light blue')
app.title("Verify")
app.geometry('600x600')

# Add the button to call the function decrypt
main_button = Button(app, text="Verify image", bg='white', fg='black', command=verify_image)
main_button.pack()

# Add an empty label that will be used to hold
message_label = Label(app, text='', bg='light blue')
message_label.pack()
app.mainloop()