import os
from pathlib import Path
import sys
from datetime import datetime
import time
import threading
from threading import Thread
import json
import cv2
import numpy
import pytesseract
import requests
import Linguist


def tesseract_location(root):
    """
    Sets the tesseract cmd root and exits is the root is not set correctly

    Tesseract needs a pointer to exec program included in the install.
    Example: User/Documents/tesseract/4.1.1/bin/tesseract
    See tesseract documentation for help.
    """
    try:
        pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'
    except FileNotFoundError:
        print("Please double check the Tesseract file directory or ensure it's installed.")
        sys.exit(1)


class RateCounter:
    """
    Class for finding the iterations/second of a process

    `Attributes:`
        start_time: indicates when the time.perf_counter() began
        iterations: determines number of iterations in the process

    `Methods:`
        start(): Starts a time.perf_counter() and sets it in the self.start_time attribute
        increment(): Increases the self.iterations attribute
        rate(): Returns the iterations/seconds
    """

    def __init__(self):
        self.start_time = None
        self.iterations = 0

    def start(self):
        """
        Starts a time.perf_counter() and sets it in the self.start_time attribute

        :return: self
        """
        self.start_time = time.perf_counter()
        return self

    def increment(self):
        """
        Increases the self.iterations attribute
        """
        self.iterations += 1

    def rate(self):
        """
        Returns the iterations/seconds
        """
        elapsed_time = (time.perf_counter() - self.start_time)
        return self.iterations / elapsed_time


class VideoStream:
    """
    Class for grabbing frames from CV2 video capture.

    `Attributes:`
        stream: CV2 VideoCapture object
        grabbed: bool indication whether the frame from VideoCapture() was read correctly
        frame: the frame from VideoCapture()
        stopped: bool indicating whether the process has been stopped

    `Methods:`
        start()
            Creates a thread targeted at get(), which reads frames from CV2 VideoCapture
        get()
            Continuously gets frames from CV2 VideoCapture and sets them as self.frame attribute
        get_video_dimensions():
            Gets the width and height of the video stream frames
        stop_process()
            Sets the self.stopped attribute as True and kills the VideoCapture stream read
    """

    def __init__(self, src=0):
        self.stream = cv2.VideoCapture(src)
        (self.grabbed, self.frame) = self.stream.read()
        self.stopped = False

    def start(self):
        """
        Creates a thread targeted at get(), which reads frames from CV2 VideoCapture

        :return: self
        """
        Thread(target=self.get, args=()).start()
        return self

    def get(self):
        """
        Continuously gets frames from CV2 VideoCapture and sets them as self.frame attribute
        """
        while not self.stopped:
            (self.grabbed, self.frame) = self.stream.read()

    def get_video_dimensions(self):
        """
        Gets the width and height of the video stream frames

        :return: height `int` and width `int` of VideoCapture
        """
        width = self.stream.get(cv2.CAP_PROP_FRAME_WIDTH)
        height = self.stream.get(cv2.CAP_PROP_FRAME_HEIGHT)
        return int(width), int(height)

    def stop_process(self):
        """
        Sets the self.stopped attribute as True and kills the VideoCapture stream read
        """
        self.stopped = True


class OCR:
   
   

    # def __init__(self, exchange: VideoStream, language=None):
    def __init__(self):
        self.boxes = None
        self.stopped = False
        self.exchange = None
        self.language = None
        self.width = None
        self.height = None
        self.crop_width = None
        self.crop_height = None

    def start(self):
        """
        Creates a thread targeted at the ocr process
        :return: self
        """
        Thread(target=self.ocr, args=()).start()
        return self

    def set_exchange(self, video_stream):
        """
        Sets the self.exchange attribute with a reference to VideoStream class
        :param video_stream: VideoStream class
        """
        self.exchange = video_stream

    def set_language(self, language):
        """
        Sets the self.language parameter
        :param language: language code(s) for detecting custom languages in pytesseract
        """
        self.language = language

    def ocr(self):
        """
        Creates a process where frames are continuously grabbed from the exchange and processed by pytesseract OCR.
        Output data from pytesseract is stored in the self.boxes attribute.
        """
        while not self.stopped:
            if self.exchange is not None:  # Defends against an undefined VideoStream reference
                frame = self.exchange.frame

                # # # CUSTOM FRAME PRE-PROCESSING GOES HERE # # #
                frame = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
                # frame = cv2.adaptiveThreshold(frame, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
                # # # # # # # # # # # # # # # # # # # #

                frame = frame[self.crop_height:(self.height - self.crop_height),
                              self.crop_width:(self.width - self.crop_width)]

                self.boxes = pytesseract.image_to_data(frame, lang=self.language)

    def set_dimensions(self, width, height, crop_width, crop_height):
       
        self.width = width
        self.height = height
        self.crop_width = crop_width
        self.crop_height = crop_height

    def stop_process(self):
        
        self.stopped = True


def capture_image(frame, captures=0):
    
    cwd_path = os.getcwd()
    Path(cwd_path + '/images').mkdir(parents=False, exist_ok=True)

    now = datetime.now()
    # Example: "OCR 2021-04-8 at 12:26:21-1.jpg"  ...Handles multiple captures taken in the same second
    name = "OCR " + now.strftime("%Y-%m-%d") + " at " + now.strftime("%H:%M:%S") + '-' + str(captures + 1) + '.jpg'
    path = 'images/' + name
    cv2.imwrite(path, frame)
    captures += 1
    print(name)
    return captures


def views(mode: int, confidence: int):
   
    conf_thresh = None
    color = None

    if mode == 1:
        conf_thresh = 75  # Only shows boxes with confidence greater than 75
        color = (0, 255, 0)  # Green

    if mode == 2:
        conf_thresh = 0  # Will show every box
        if confidence >= 50:
            color = (0, 255, 0)  # Green
        else:
            color = (0, 0, 255)  # Red

    if mode == 3:
        conf_thresh = 0  # Will show every box
        color = (int(float(confidence)) * 2.55, int(float(confidence)) * 2.55, 0)

    if mode == 4:
        conf_thresh = 0  # Will show every box
        color = (0, 0, 255)  # Red

    return conf_thresh, color


def put_ocr_boxes(boxes, frame, height, crop_width=0, crop_height=0, view_mode=1):
   

    if view_mode not in [1, 2, 3, 4]:
        raise Exception("A nonexistent view mode was selected. Only modes 1-4 are available")

    text = ''  # Initializing a string which will later be appended with the detected text
    if boxes is not None:  # Defends against empty data from tesseract image_to_data
        for i, box in enumerate(boxes.splitlines()):  # Next three lines turn data into a list
            box = box.split()
            if i != 0:
                if len(box) == 12:
                    x, y, w, h = int(box[6]), int(box[7]), int(box[8]), int(box[9])
                    conf = box[10]
                    word = box[11]
                    x += crop_width  # If tesseract was performed on a cropped image we need to 'convert' to full frame
                    y += crop_height

                    conf_thresh, color = views(view_mode, int(float(conf)))

                    if int(float(conf)) > conf_thresh:
                        cv2.rectangle(frame, (x, y), (w + x, h + y), color, thickness=1)
                        text = text + ' ' + word

        if text.isascii():  # CV2 is only able to display ascii chars at the moment
            cv2.putText(frame, text, (5, height - 5), cv2.FONT_HERSHEY_DUPLEX, 1, (200, 200, 200))
    
    return frame, text


def put_crop_box(frame: numpy.ndarray, width: int, height: int, crop_width: int, crop_height: int):
    """
    Simply draws a rectangle over the frame with specified height and width to show a crop zone

    :param numpy.ndarray frame: CV2 display frame for crop-box destination
    :param int width: Width of the CV2 frame
    :param int height: Height of the CV2 frame
    :param int crop_width: Horizontal crop amount
    :param int crop_height: Vertical crop amount

    :return: CV2 display frame with crop box added
    """
    cv2.rectangle(frame, (crop_width, crop_height), (width - crop_width, height - crop_height),
                  (255, 0, 0), thickness=1)
    return frame


def put_rate(frame: numpy.ndarray, rate: float) -> numpy.ndarray:
    """
    Places text showing the iterations per second in the CV2 display loop.

    This is for demonstrating the effects of multi-threading.

    :param frame: CV2 display frame for text destination
    :param rate: Iterations per second rate to place on image

    :return: CV2 display frame with rate added
    """

    cv2.putText(frame, "{} Iterations/Second".format(int(rate)),
                (10, 35), cv2.FONT_HERSHEY_DUPLEX, 1.0, (255, 255, 255))
    return frame


def put_language(frame: numpy.ndarray, language_string: str) -> numpy.ndarray:
    """
    Places text showing the active language(s) in current OCR display

    :param numpy.ndarray frame: CV2 display frame for language name destination
    :param str language_string: String containing the display language name(s)

    :returns: CV2 display frame with language name added
    """
    cv2.putText(frame, language_string,
                (10, 65), cv2.FONT_HERSHEY_DUPLEX, 1.0, (255, 255, 255))
    return frame


def ocr_stream(crop: list[int, int], source: int = 0, view_mode: int = 1, language=None):
    """
    Begins the video stream and text OCR in two threads, then shows the video in a CV2 frame with the OCR
    boxes overlaid in real-time.

    When viewing the real-time video stream, push 'c' to capture a still image, push 'q' to quit the view session

    :param list[int, int] crop: A two-element list with width, height crop amount in pixels. [0, 0] indicates no crop
    :param source: SRC video source (defaults to 0) for CV2 video capture.
    :param int view_mode: There are 4 possible view modes that control how the OCR boxes are drawn over text:

        mode 1: (Default) Draws boxes on text with >75 confidence level

        mode 2: Draws red boxes on low-confidence text and green on high-confidence text

        mode 3: Color changes according to each word's confidence; brighter indicates higher confidence

        mode 4: Draws a box around all detected text regardless of confidence

    :param str language: ISO 639-2/T language code to specify OCR language. Multiple langs can be appended with '+'
        Defaults to None, which will perform OCR in English.

    """
    captures = 0  # Number of still image captures during view session

    video_stream = VideoStream(source).start()  # Starts reading the video stream in dedicated thread
    img_wi, img_hi = video_stream.get_video_dimensions()

    if crop is None:  # Setting crop area and confirming valid parameters
        cropx, cropy = (200, 200)  # Default crop if none is specified
    else:
        cropx, cropy = crop[0], crop[1]
        if cropx > img_wi or cropy > img_hi or cropx < 0 or cropy < 0:
            cropx, cropy = 0, 0
            print("Impossible crop dimensions supplied. Dimensions reverted to 0 0")

    ocr = OCR().start()  # Starts optical character recognition in dedicated thread
    print("OCR stream started")
    print("Active threads: {}".format(threading.activeCount()))
    ocr.set_exchange(video_stream)
    ocr.set_language(language)
    ocr.set_dimensions(img_wi, img_hi, cropx, cropy)  # Tells the OCR class where to perform OCR (if img is cropped)

    cps1 = RateCounter().start()
    lang_name = Linguist.language_string(language)  # Creates readable language names from tesseract langauge code

    # Main display loop
    print("\nPUSH C TO CAPTURE AN IMAGE. PUSH Q1 TO VIEW VIDEO STREAM\n")
    while True:

        # Quit condition:
        pressed_key = cv2.waitKey(1) & 0xFF
        if pressed_key == ord('q'):
            video_stream.stop_process()
            ocr.stop_process()
            print("OCR stream stopped\n")
            print("{} image(s) captured and saved to current directory".format(captures))
            break

        frame = video_stream.frame  # Grabs the most recent frame read by the VideoStream class

        # # # All display frame additions go here # # # CUSTOMIZABLE
        frame = put_rate(frame, cps1.rate())
        frame = put_language(frame, lang_name)
        frame = put_crop_box(frame, img_wi, img_hi, cropx, cropy)
        frame, text = put_ocr_boxes(ocr.boxes, frame, img_hi,
                                    crop_width=cropx, crop_height=cropy, view_mode=view_mode)
        # # # # # # # # # # # # # # # # # # # # # # # #

        # Photo capture:
        if pressed_key == ord('c'):
            captures = capture_image(frame, captures)
            if text != " ":
                text=text.strip()
                f=open('carDBExt.json',encoding='utf-8')
                data=json.load(f)
                passid=next((item for item in data['cardetails'] if item["CarRegistration"] == text),-1)
                return passid
       

        if pressed_key == ord('e'):
            sys.exit(1)
            

        cv2.imshow("realtime OCR", frame)
        cps1.increment()  # Incrementation for rate counter
def passApi(item):
    return item