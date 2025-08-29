import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageOps, ImageTk
from tf_keras.models import load_model
import numpy as np

# Load the model
model = load_model("./model/keras_model.h5", compile=False)

# Load the labels
class_names = [label.strip() for label in open("./model/labels.txt", "r").readlines()]

# Function to classify waste
def classify_image(image_path):
    try:
        # Create an array of the right shape
        data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)

        # Open and process the image
        image = Image.open(image_path).convert("RGB")
        size = (224, 224)
        image = ImageOps.fit(image, size, Image.Resampling.LANCZOS)
        image_array = np.asarray(image)

        # Normalize the image
        normalized_image_array = (image_array.astype(np.float32) / 127.5) - 1
        data[0] = normalized_image_array

        # Predict the class
        prediction = model.predict(data)
        index = np.argmax(prediction)
        class_name = class_names[index]
        confidence_score = prediction[0][index]

        return index, class_name, confidence_score
    except Exception as e:
        messagebox.showerror("Error", f"Failed to classify image: {e}")
        return None, None, None

# Function to handle image upload
def upload_image():
    file_path = filedialog.askopenfilename(
        filetypes=[("Image files", "*.png;*.jpg;*.jpeg")]
    )
    if not file_path:
        return

    # Open and resize the image to fit within the window
    img = Image.open(file_path).convert("RGB")
    img.thumbnail((500, 500))  # Resize to fit in the window, maintaining aspect ratio
    photo = ImageTk.PhotoImage(img)

    # Update the label with the new image
    image_label.config(image=photo)
    image_label.image = photo

    # Classify the image
    index, class_name, confidence = classify_image(file_path)
    if class_name:
        result_label.config(text=f"Class: {class_name}\nConfidence: {confidence:.2f}")
        highlight_class(index)

# Function to highlight the predicted class
def highlight_class(index):
    for i, label in enumerate(class_labels):
        if i == index:
            label.config(bg="yellow", font=("Arial", 14, "bold"))
        else:
            label.config(bg="white", font=("Arial", 12))

# Create the main Tkinter app
app = tk.Tk()
app.title("Waste Classification App")
app.geometry("600x800")
app.resizable(True, True)  # Allow resizing the window

# Title Label
title_label = tk.Label(app, text="Waste Classification App", font=("Arial", 18, "bold"))
title_label.pack(pady=10)

# Image Display
image_label = tk.Label(app, text="Upload an image", font=("Arial", 14), bg="lightgray", relief="groove")
image_label.pack(pady=20)

# Upload Button
upload_button = tk.Button(app, text="Upload Image", command=upload_image, font=("Arial", 14), bg="#4CAF50", fg="white")
upload_button.pack(pady=10)

# Classes Label
classes_frame = tk.Frame(app, relief="groove", borderwidth=2)
classes_frame.pack(pady=20)

classes_title = tk.Label(classes_frame, text="Waste Classes", font=("Arial", 14, "bold"))
classes_title.pack()

class_labels = []
for class_name in class_names:
    label = tk.Label(classes_frame, text=class_name, font=("Arial", 12), anchor="w", width=40, bg="white", relief="flat")
    label.pack(fill="x", padx=5, pady=2)
    class_labels.append(label)

# Result Display
result_label = tk.Label(app, text="Confidence will appear here", font=("Arial", 14), wraplength=400, justify="center")
result_label.pack(pady=20)

# Run the App
app.mainloop()
