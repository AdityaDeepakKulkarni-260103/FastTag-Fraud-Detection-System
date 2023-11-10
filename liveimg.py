from PIL import Image
from pytesseract import pytesseract



# importing OpenCV library
import cv2 as cv


cam_port = 0
cam = cv.VideoCapture(cam_port)


result, image = cam.read()


if result:

	
	

	
	cv.imwrite("live.png", image)

	
	
	


else:
	print("No image detected. Please! try again")

path_to_tesseract = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
image_path = image

# Opening the image & storing it in an image object
img = Image.open(image_path)

# Providing the tesseract executable
# location to pytesseract library
pytesseract.tesseract_cmd = path_to_tesseract

# Passing the image object to image_to_string() function
# This function will extract the text from the image
text = pytesseract.image_to_string(img)

# Displaying the extracted text
print(text[:-1])
