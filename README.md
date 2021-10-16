# Steganography

Sign an image with a watermark, then verify a signed image to evaluate the authenticity

## Table of Contents

- [Steganography](#steganography)
  - [Table of Contents](#table-of-contents)
  - [Requirements](#requirements)
  - [How to Use](#how-to-use)
  - [FaceSwap - Download and Installation](#faceswap---download-and-installation)
  - [Downloading Our FaceSwap Models](#downloading-our-faceswap-models)
  - [Generating a Deepfake using Our Models](#generating-a-deepfake-using-our-models)
    - [Creating an Alignments File](#creating-an-alignments-file)
    - [Creating a Deepfake](#creating-a-deepfake)
  - [Known Bugs (and How to Currently Address Them)](#known-bugs-and-how-to-currently-address-them)

## Requirements

1. [Python3.X](https://www.python.org/downloads/) is required, the project was tested using Python3.9
2. [pip](https://pip.pypa.io/en/stable/) is included with python3.4+
3. [Cryptography](https://cryptography.io/en/latest/) this is used for RSA objects for signing and verifying
4. [Tkinter](https://docs.python.org/3/library/tkinter.html) is used for gui and included with python3.1+
5. [Pillow](https://pillow.readthedocs.io/en/stable/) is used for image manipulation
6. [NumPy](https://numpy.org/) is used for vectors and matrix
7. [OpenCV](https://pypi.org/project/opencv-python/) is used for facial detection

Installation Instructions:

`text in this format means you can run it in your terminal`

**Required Libraries**

1. `pip install cryptography`
2. `pip install pillow`
3. `pip install numpy`
4. `pip install opencv-python`

**Clone This Repository**

Navigate to directory you wish to clone repository to.

`git clone https://github.com/csunspl/CodeFSwap.git`

---

## How to Use

A short video demonstration of this project can be found [here](https://drive.google.com/file/d/1-gga9Gh0Y9Ob9Rxrf8-Jxt2HY-vf5dkO/view?usp=sharing).

**Generate asymmetric keys**

This is only needed if you do not already have a private and public key pair.

1. Open terminal at the directory with this repository.
2. `python3 crypto.py`

This will create the files `public_shared.pem` and `private_noshare.pem`, which are required for signing and verification.

**Sign image with watermark**

1. Open terminal at the directory with this repository.
2. `python3 sign.py`
3. Click "Choose Image" and select the image you wish to sign.

   ![Choose Image](https://i.imgur.com/8FmA2d0.png)

4. After image is selected, click "Sign Image" to sign watermark into image

   ![Sign Image](https://i.imgur.com/Ck1nSEZ.png)

5. Close application

**Verify image with watermark**

1. Open terminal at the directory with this repository.
2. `python3 verify.py`
3. Click "Verify Image" and select the image you want to verify.

   ![Verify Image](https://i.imgur.com/u0L2R4X.png)

4. After image is selected, the watermark will automatically be verified and the result will appear below the image.

**Successful Signing**

![Successful Signing](https://i.imgur.com/yyKtkcq.png)

**Successful Verification**

![Successful Verification](https://i.imgur.com/lGsVVeH.png)

**Failed Verification**

![Failed Verification](https://i.imgur.com/pvz2PwF.png)

---

## FaceSwap - Download and Installation

If you already have FaceSwap installed on your system or don't care to test the verification against deepfakes, don't worry about this.

**NOTE:** For a more detailed download/installation guide, refer to [INSTALL.md](https://github.com/deepfakes/faceswap/blob/master/INSTALL.md) in the FaceSwap GitHub repository.

To download the latest stable version of FaceSwap (currently v2.0.0), head to the [downloads page](https://faceswap.dev/download) and select the installer for your operating system. Windows and Linux systems have the easiest installation, so it is highly recommended to use Windows or Linux if possible. All other platforms are required to download the repository from [GitHub](https://github.com/deepfakes/faceswap/releases). To install, launch the installer and follow the prompts.

The FaceSwap site contains guides for [Extraction](https://forum.faceswap.dev/viewtopic.php?f=25&t=27), [Training](https://forum.faceswap.dev/viewtopic.php?f=6&t=146), and [Conversion](https://forum.faceswap.dev/viewtopic.php?f=24&t=1083).

---

## Downloading Our FaceSwap Models

Due to the models being too large to host on GitHub, they (along with a slew of sample images to use) can be found on [Google Drive](https://drive.google.com/drive/folders/1lLi5BL6RDnsekg7lTISJbfwMr5ta-OWm?usp=sharing).

---

## Generating a Deepfake using Our Models

This section will outline the steps needed to create a deepfake using any of our 3 models. During this outline, it is assumed:

- you have a folder containing **only** signed image(s) of a single subject
- you have a model trained on that subject

### Creating an Alignments File

Before we can generate our deepfake, we will first need an alignments file for the image(s) we would like to deepfake. Luckily, making one is quite easy.

1. Launch FaceSwap and navigate to the **Extract** tab in the left panel.
2. Set the following fields:

   _Data:_

   - **Input Dir** - the filepath to the folder holding the image(s) you want to deepfake
   - **Output Dir** - for our purposes, this should be identical to **Input Dir**

   _Plugins:_

   - **Detector** - Mtcnn
   - **Aligner** - Fan
   - **Normalization** - Clahe (any setting for this is fine, Clahe is just what we used)
   - **Re Feed** - 3

   _Face Processing:_

   - **Min Size** - 80 (can be increased if needed)

   _Output:_

   - **Size** - 256
   - **Extract Every N** - 1
   - **Save Interval** - 0

   _Settings:_

   - Enable **Skip Saving Faces**

3. Click **Extract**

This will generate a file `alignments.fsa` to the **Input Dir** you specified.

### Creating a Deepfake

Now we have our alignments file, so we can make our deepfake. Once again, the setup is fairly simple.

1. Navigate to the **Convert** tab in the left panel.
2. Set up the following fields:

   _Data:_

   - **Input Dir** - the filepath to the folder holding the image(s) you want to deepfake
   - **Output Dir** - the filepath to the folder you want the deepfake(s) saved in
   - **Alignments** - the filepath to the `alignments.fsa` file generated in the previous section
   - **Model Dir** - the filepath to the folder holding the model to be used for deepfake generation

   _Plugins:_

   - **Color Adjustment** - Avg-Color (any setting for this is fine, some may yield better results for certain images)
   - **Mask Type** - Vgg-Clear
   - **Writer** - Opencv

   _Settings:_

   - **Swap Model** may need to be enabled depending on the subject of your image(s) and the model used
   - If your output doesn't appear to have a swapped face, try toggling this

3. Click **Convert**

This will generate a deepfake of each image in the specified **Input Dir**.

---

## Known Bugs (and How to Currently Address Them)

- **There are some UI bugs caused by opening an image while one has already been opened.**

  - These can be addressed by closing and re-opening either software after it has been used once.

- **There is a rare bug that can sometimes cause signed images to incorrectly fail verification (a result of our merging of facial detection with steganography).**

  - This can be addressed by re-signing the unsigned version of the image until you have a signed copy that passes verification (This emulates the automatic software solution that would have been implemented given more time).
