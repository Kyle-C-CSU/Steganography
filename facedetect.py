import cv2
import sys

def getFace(imagePath):
    # Get user supplied values
    #imagePath = sys.argv[1]

    # Create the haar cascade xml file included in opencv
    faceCascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

    # Read the image
    try:
        image = cv2.imread(imagePath)
        print("Image read successfully for facial detection")
    except(e):
        print("Facial detection error: " + e)
    #gray scale image
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Detect faces in the image
    faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(30, 30),
        flags = cv2.CASCADE_SCALE_IMAGE
    )

    print("Found {0} faces!".format(len(faces)))

    # Draw a rectangle around the faces
    for (x, y, w, h) in faces:
        cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 2)
    print(f"Facial Bounds: x:{x}\ty:{y}\tw:{w}\th:{h}")
    return(x,y,w,h)
