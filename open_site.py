from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time

# Set up Chrome options
options = Options()
options.add_argument("--start-maximized")

# Path to your ChromeDriver
service = Service("C:/chromedriver/chromedriver.exe")

# Launch browser
driver = webdriver.Chrome(service=service, options=options)

# Open your custom local domain
driver.get("http://localhost123/%F0%9F%9B%A1%EF%B8%8F-captcha-verification-form/")

# Wait to see it
time.sleep(5000)
