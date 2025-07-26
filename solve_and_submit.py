import os
import time
import numpy as np
import requests
from PIL import Image
from io import BytesIO
import cv2
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from tensorflow.keras.models import load_model

# === Load model and get input shape ===
model = load_model('char_recognition_cnn.h5')
input_shape = model.input_shape
img_height, img_width = input_shape[1:3]

characters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'  # index 0–35

def preprocess_and_segment(image):
    # Convert to grayscale and invert
    gray = image.convert('L')
    img_array = np.array(gray)
    img_inv = cv2.bitwise_not(img_array)
    
    # Threshold
    _, thresh = cv2.threshold(img_inv, 127, 255, cv2.THRESH_BINARY)

    # Find contours
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours = sorted(contours, key=lambda c: cv2.boundingRect(c)[0])  # left to right

    chars = []
    for cnt in contours:
        x, y, w, h = cv2.boundingRect(cnt)
        if w > 5 and h > 10:  # Filter noise
            char_img = thresh[y:y+h, x:x+w]
            char_img = cv2.resize(char_img, (img_width, img_height))
            char_img = char_img.astype('float32') / 255.0
            char_img = np.expand_dims(char_img, axis=(0, -1))  # Shape: (1, H, W, 1)
            chars.append(char_img)
    return chars

def decode_prediction(pred):
    idx = np.argmax(pred)
    return characters[idx]

def predict_captcha(image_url):
    response = requests.get(image_url)
    img = Image.open(BytesIO(response.content))

    segments = preprocess_and_segment(img)
    result = ""
    for seg in segments:
        pred = model.predict(seg)
        result += decode_prediction(pred)
    return result

# === Set up Selenium ===
options = Options()
options.add_argument("--start-maximized")
service = Service("C:/chromedriver/chromedriver.exe")
driver = webdriver.Chrome(service=service, options=options)

# === Open CAPTCHA page ===
driver.get("http://localhost123/🛡️-captcha-verification-form/")
time.sleep(2)

# === Extract CAPTCHA URL ===
captcha_img = driver.find_element("css selector", "img.wpcf7-captcha-your-captcha")
captcha_url = captcha_img.get_attribute("src")

# === Predict text ===
captcha_text = predict_captcha(captcha_url)
print(f"[Predicted CAPTCHA] {captcha_text}")

# === Fill and submit ===
captcha_input = driver.find_element("css selector", "input[name='your-captcha']")
captcha_input.clear()
captcha_input.send_keys(captcha_text)

submit_btn = driver.find_element("css selector", "input.wpcf7-submit")
submit_btn.click()

time.sleep(10)
driver.quit()
