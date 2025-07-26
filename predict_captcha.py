import os
import numpy as np
from sklearn.preprocessing import LabelBinarizer

# Recreate from folder names
classes = sorted(os.listdir("char_dataset"))
print(f"📚 Classes found: {classes}")

# Build encoder
lb = LabelBinarizer()
lb.fit(classes)

# Simulate decoding
example_output = np.zeros((1, len(classes)))
example_output[0][5] = 1  # Simulate class index 5
decoded = lb.inverse_transform(example_output)
print(f"🔍 Class index 5 is: {decoded}")
