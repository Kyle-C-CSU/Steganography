# Steganography
Sign an image with a watermark then verify a signed image to evaluate the authenticity 

**Requirements:** 
1. Python3.X the project is was tested using Python3.9
2. pip is included with python3.4 < later 
3. Cryptography.py this is used for RSA objects for signing and verifying
4. tkinter is used for gui and included with python3.1 < later 
5. Pillow.py is used for image manipulation 
6. numpy.py is used for vectors and matrix 

Installation Instructions:
**Required Libraries**
1. 'pip install Cryptography'
2. `pip install Pillow`
3. <pip install Numpy>

**Clone Repo**
Navigate to directory you wish to clone repo too.
<git clone https://github.com/Kyle-C-CSU/Steganography.git>

How to use instuctions: 
**Sign image with watermark**
1. Open terminal to navigate to directory with steganography repo. 
2. <python3 sign.py>
3. Click "Choose Image" on gui and select the image you wish to encode. 
![Screen Shot 2021-04-07 at 4 35 23 PM](https://user-images.githubusercontent.com/71400517/113930548-6ab92b80-97bf-11eb-817c-500a5d30672a.png)
4. After image is selected click the encode button to encode watermark into image
![Screen Shot 2021-04-07 at 4 39 19 PM](https://user-images.githubusercontent.com/71400517/113930940-e6b37380-97bf-11eb-94ed-a9a387aebb89.png)
5. close gui 

**Verify image with watermark**
1. Open terminal to navigate to directory with steganography repo. 
2. <python3 verify.py>
3. Click "Decrypt image" on gui to select the image you want to verify 
![Screen Shot 2021-04-07 at 4 42 32 PM](https://user-images.githubusercontent.com/71400517/113931368-62152500-97c0-11eb-9de8-371eec697e7f.png)
4. After image is slected the watermark will automatically be verified and the result will appear below the image. 
![Screen Shot 2021-04-07 at 4 48 05 PM](https://user-images.githubusercontent.com/71400517/113932036-2b8bda00-97c1-11eb-8bb4-935fd152316b.png)
