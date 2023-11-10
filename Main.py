import argparse
import os
import OCR
import Linguist


def main():
   
    parser = argparse.ArgumentParser()

   

    # Optional:
    parser.add_argument('-c', '--crop', help="crop OCR area in pixels (two vals required): width height",
                        nargs=2, type=int, metavar='')

    parser.add_argument('-v', '--view_mode', help="view mode for OCR boxes display (default=1)",
                        default=1, type=int, metavar='')
    parser.add_argument('-sv', '--show_views', help="show the available view modes and descriptions",
                        action="store_true")

    parser.add_argument("-l", "--language",
                        help="code for tesseract language, use + to add multiple (ex: chi_sim+chi_tra)",
                        metavar='', default=None)
    parser.add_argument("-sl", "--show_langs", help="show list of tesseract (4.0+) supported langs",
                        action="store_true")
    parser.add_argument("-s", "--src", help="SRC video source for video capture",
                        default=0, type=int)

    args = parser.parse_args()

    if args.show_langs:
        Linguist.show_codes()

    if args.show_views:
        print(OCR.views.__doc__)

    tess_path = os.path.normpath("C:/ProgramFiles/Tesseract-OCR/tesseract")
    # This is where OCR is started...
    OCR.tesseract_location(tess_path)
    passApi=OCR.ocr_stream(view_mode=args.view_mode, source=args.src, crop=args.crop, language=args.language)
    return passApi

if __name__ == '__main__':
    # To run in IDE (instead of commamnd line), comment out main() and uncomment the block below:
    main()

    # tess_path =  r"C:\Program Files\Tesseract-OCR\tesseract.exe"  # Windows example
    # tess_path = '/usr/local/Cellar/tesseract/4.1.1/bin/tesseract'  # MAC example
    # view_mode = 1
    # source = 0
    # crop = [100, 100]
    # language = "en"
    # OCR.ocr_stream(view_mode=view_mode, source=source, crop=crop, language=language)
