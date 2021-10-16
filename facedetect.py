import cv2
import sys

# Get the bounds for the largest face in an image
def getFace(imagePath):
    # Get the haar cascade xml file included in opencv
    faceCascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

    # Read the image
    image = cv2.imread(imagePath)

    # Convert to grayscale image
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Detect faces in the image
    faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(30, 30),
        flags = cv2.CASCADE_SCALE_IMAGE
    )

    print(f"--\nFound {len(faces)} faces!")

    
    if len(faces) == 0:
        # No faces found so just return the image bounds
        return [0, 0, image.shape[0], image.shape[1]]
    else:
        # At least 1 face, so return the largest
        largest_index = 0
        largest_size = 0
        current_index = 0
        for (x, y, w, h) in faces:
            if w * h > largest_size:
                largest_size = w * h
                largest_index = current_index

            print(f"- Facial Bounds: x:{x}\ty:{y}\tw:{w}\th:{h}")
            current_index += 1

        print("--")
        return faces[largest_index] # we assume the largest face will be our desired face

