import cv2
import pytesseract
from tkinter import Tk, Label
from PIL import Image, ImageTk
from tkhtmlview import HTMLLabel

# Configuración de Pytesseract
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

class OCRApp:
    def __init__(self, window, window_title):
        self.window = window
        self.window.title(window_title)

        self.vid = cv2.VideoCapture(0)

        if not self.vid.isOpened():
            raise ValueError("Error: No se puede acceder a la cámara.")

        # Crear un label HTML para cargar el HTML con estilo CSS
        with open("index.html", "r") as file:
            html_content = file.read()

        self.html_label = HTMLLabel(window, html=html_content)
        self.html_label.pack(fill="both", expand=True)

        self.video_img = self.html_label.html.parser.get_element_by_id("video_img")
        self.threshold_img = self.html_label.html.parser.get_element_by_id("threshold_img")
        self.exit_button = self.html_label.html.parser.get_element_by_id("exit_button")

        # Vincular el botón de salida con la función de salida
        self.exit_button.bind("<Button-1>", lambda e: window.quit())

        self.delay = 15
        self.update()

        self.window.mainloop()

    def update(self):
        ret, frame = self.vid.read()
        if ret:
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            _, thresholded = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
            numbers_text = pytesseract.image_to_string(thresholded, config='--psm 10 --oem 3 digits').strip()

            cv2.putText(frame, f"Número detectado: {numbers_text}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

            self.photo = ImageTk.PhotoImage(image=Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)))
            self.threshold_photo = ImageTk.PhotoImage(image=Image.fromarray(thresholded))

            self.video_img.src = self.photo
            self.threshold_img.src = self.threshold_photo

        self.window.after(self.delay, self.update)

    def __del__(self):
        if self.vid.isOpened():
            self.vid.release()

if __name__ == "__main__":
    root = Tk()
    app = OCRApp(root, "Reconocimiento de Números en Tiempo Real")
