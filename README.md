
# CAPTCHA Breaking Bot

A Python-based automation tool that recognizes and solves 4-character image-based CAPTCHAs using a Convolutional Neural Network (CNN), and auto-fills a local web form using Selenium.

## 📁 Project Structure

```
CaptchaBreakingBot/
├── char_dataset/              # Dataset containing labeled character images for training
├── char_recognition_cnn.h5    # Trained CNN model for character recognition
├── captcha.png                # Downloaded CAPTCHA image (temporary)
├── auto_fill_captcha.py       # Main automation script
```

## 🔧 Prerequisites

Ensure the following Python packages are installed:

```bash
pip install numpy opencv-python pillow tensorflow scikit-learn matplotlib selenium requests
```

Also required:
- Google Chrome browser
- ChromeDriver executable (ensure it matches your Chrome version and is in PATH)

## 🚀 Usage

1. Launch the local CAPTCHA verification form hosted at:
   ```
   http://localhost123/captcha-verification-form/
   ```
   > If you do not have an existing form, you can create your own simple website for testing purposes. The CAPTCHA model is trained specifically on images generated using the **WordPress plugin "Really Simple CAPTCHA"**.

2. Execute the bot:

   ```bash
   python auto_fill_captcha.py
   ```

   The script will:
   - Open the form using Selenium and ChromeDriver
   - Fill in the name, email, and message fields
   - Download the CAPTCHA image
   - Process and segment the image
   - Predict each character using the trained CNN model
   - Input the CAPTCHA solution and submit the form

## 📦 Model Requirements

- CAPTCHA images must contain exactly four distinct characters.
- The dataset used for training (`char_dataset/`) should contain subdirectories for each character class, with labeled images.
- The model file `char_recognition_cnn.h5` must be pre-trained on the exact character set expected in the CAPTCHAs.

## 📽️ Demo 
```markdown
https://www.linkedin.com/feed/update/urn:li:activity:7354791357078454272/
```

## ⚠️ Legal Disclaimer

This tool is intended strictly for educational and research purposes. Unauthorized use against real-world CAPTCHA systems or websites without explicit permission is prohibited and may violate applicable laws or terms of service.
