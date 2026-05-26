from PIL import Image
import numpy as np

# Load image
img = Image.open("./assets/full_logo.png").convert("RGBA")
data = np.array(img)

# Define white threshold (treat near‑white as background too)
threshold = 240
white_mask = np.all(data[:, :, :3] > threshold, axis=-1)

# Make white pixels transparent
data[white_mask] = [255, 255, 255, 0]

# Make all other pixels pure white and fully opaque
data[~white_mask] = [255, 255, 255, 255]

# Save the result
out = Image.fromarray(data)
out.save("./assets/logo_white.png", format="PNG")
