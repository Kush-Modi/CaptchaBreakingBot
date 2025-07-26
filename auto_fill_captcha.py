import os
import time
import requests
import numpy as np
import cv2
from PIL import Image
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from tensorflow.keras.models import load_model
from sklearn.preprocessing import LabelBinarizer


MODEL_PATH = "char_recognition_cnn.h5"
CAPTCHA_IMAGE_PATH = "captcha.png"
DATASET_CLASSES_PATH = "char_dataset"
URL = "http://localhost123/🛡️-captcha-verification-form/"


model = load_model(MODEL_PATH)
classes = sorted(os.listdir(DATASET_CLASSES_PATH))
lb = LabelBinarizer()
lb.fit(classes)

options = Options()
options.add_argument("--start-maximized")
service = Service("C:/chromedriver/chromedriver.exe")
driver = webdriver.Chrome(service=service, options=options)
driver.get(URL)

time.sleep(2)  


driver.find_element(By.NAME, "your-name").send_keys("Kush Modi")
driver.find_element(By.NAME, "your-email").send_keys("kushmodi@example.com")
time.sleep(2) 
driver.find_element(By.NAME, "your-message").send_keys("I have designed this form to test captcha automation which shouldnt be possible" \
" but I have done it successfully. This is a test message. captcha is something which robots shouldnt be able to solve.")



captcha_img = driver.find_element(By.CLASS_NAME, "wpcf7-captcha-your-captcha")
captcha_src = captcha_img.get_attribute("src")
response = requests.get(captcha_src)
with open(CAPTCHA_IMAGE_PATH, 'wb') as f:
    f.write(response.content)


image = cv2.imread(CAPTCHA_IMAGE_PATH)
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
blur = cv2.GaussianBlur(gray, (3, 3), 0)
_, thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 2))
dilated = cv2.dilate(thresh, kernel, iterations=1)

contours, _ = cv2.findContours(dilated, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
boxes = []

for cnt in contours:
    x, y, w, h = cv2.boundingRect(cnt)
    if w * h < 100:
        continue
    if w > 1.6 * h:
        w_half = w // 2
        boxes.append((x, y, w_half, h))
        boxes.append((x + w_half, y, w - w_half, h))
    else:
        boxes.append((x, y, w, h))


boxes = sorted(boxes, key=lambda b: b[0])

if len(boxes) != 4:
    print(f"❌ Error: Expected 4 characters but found {len(boxes)}")
    driver.quit()
    exit()


predicted_text = ""
for (x, y, w, h) in boxes:
    pad = 2
    x, y = max(0, x - pad), max(0, y - pad)
    char_img = image[y:y + h + 2 * pad, x:x + w + 2 * pad]
    char_img = cv2.cvtColor(char_img, cv2.COLOR_BGR2GRAY)
    char_img = cv2.resize(char_img, (64, 64)) / 255.0
    char_img = char_img.reshape(1, 64, 64, 1)
    prediction = model.predict(char_img)
    predicted_label = lb.inverse_transform(prediction)[0]
    predicted_text += predicted_label

print(f"🔐 Predicted CAPTCHA: {predicted_text}")


captcha_input = driver.find_element(By.NAME, "your-captcha")
captcha_input.clear()
captcha_input.send_keys(predicted_text)


time.sleep(5)


submit_button = driver.find_element(By.CSS_SELECTOR, "input[type='submit']")
submit_button.click()

print("✅ Form submitted!")

time.sleep(5)
driver.quit()
