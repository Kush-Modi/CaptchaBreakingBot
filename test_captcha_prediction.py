# Load your trained model
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import img_to_array

model = build_char_cnn()  # or use load_model()
model.load_weights("char_cnn.weights.h5")

characters = '0123456789abcdefghijklmnopqrstuvwxyz'

# Instead of saving chars, predict them:
for filename in os.listdir(captcha_folder):
    if not filename.endswith(".png"):
        continue

    image = cv2.imread(os.path.join(captcha_folder, filename))
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
        print(f"⚠️ Skipping {filename} — Detected {len(boxes)} boxes instead of 4")
        continue

    predicted = ""
    for (x, y, w, h) in boxes:
        pad = 2
        x, y = max(0, x - pad), max(0, y - pad)
        char_img = image[y:y + h + 2 * pad, x:x + w + 2 * pad]
        char_img = cv2.cvtColor(char_img, cv2.COLOR_BGR2GRAY)
        char_img = cv2.resize(char_img, (64, 64))
        char_img = char_img.astype("float32") / 255.0
        char_img = np.expand_dims(char_img, axis=-1)
        char_img = np.expand_dims(char_img, axis=0)

        pred = model.predict(char_img, verbose=0)
        predicted += characters[np.argmax(pred)]

    print(f"{filename} → {predicted}")
