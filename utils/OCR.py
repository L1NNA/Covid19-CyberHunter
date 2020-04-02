from PIL import Image
import pytesseract


class OCR():
    @staticmethod
    def image_to_string(file):
        return pytesseract.image_to_string(Image.open(file))
    @staticmethod
    def batch_image_to_string(file):
        if (file[-4:] == ".txt"):
            return pytesseract.image_to_string(file)
        else:
            raise "wrong format"
