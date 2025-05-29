# Import necessary libraries
import cv2  # OpenCV for image processing
import numpy as np  # Numerical operations
import matplotlib.pyplot as plt  # For displaying images
from skimage.metrics import structural_similarity as ssim  # SSIM for image comparison
import tkinter as tk  # GUI framework
from tkinter import filedialog, messagebox  # File picker and message boxes

# Load an image from a given file path using OpenCV
def load_image(path):
    image = cv2.imread(path)
    if image is None:
        raise ValueError(f"❌ Could not load image: {path}")
    return image

# Resize the second image to match the size of the first image
def resize_to_match(img1, img2):
    if img1.shape != img2.shape:
        img2 = cv2.resize(img2, (img1.shape[1], img1.shape[0]))
    return img1, img2

# Compare two images using SSIM and return score, diff image, and result message
def compare_images(img1, img2, threshold=0.95):
    # Resize if needed
    img1, img2 = resize_to_match(img1, img2)

    # Convert both images to grayscale (SSIM requires single channel)
    gray1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
    gray2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)

    # Compute SSIM score and difference image
    score, diff = ssim(gray1, gray2, full=True)
    diff = (diff * 255).astype("uint8")  # Scale difference image to 0-255

    # Determine similarity result
    result = "✅ Images are similar." if score >= threshold else "❌ Images are different."

    # Print results in console
    print(f"SSIM Score: {score:.4f}")
    print(result)

    return score, diff, result

# Main function: GUI image selection and comparison
def select_images_and_compare():
    root = tk.Tk()
    root.withdraw()  # Hide the root window

    # Prompt user to select the first image
    file1 = filedialog.askopenfilename(
        title="Select First Image",
        filetypes=[("Image Files", "*.png *.jpg *.jpeg *.bmp *.tiff")]
    )
    if not file1:
        return  # Exit if no file is selected

    # Prompt user to select the second image
    file2 = filedialog.askopenfilename(
        title="Select Second Image",
        filetypes=[("Image Files", "*.png *.jpg *.jpeg *.bmp *.tiff")]
    )
    if not file2:
        return  # Exit if no file is selected

    try:
        # Load both selected images
        img1 = load_image(file1)
        img2 = load_image(file2)

        # Compare them and get results
        score, diff, result_text = compare_images(img1, img2)

        # Show result in a pop-up box
        messagebox.showinfo("Comparison Result", f"SSIM Score: {score:.4f}\n{result_text}")

        # Show side-by-side comparison
        fig, axes = plt.subplots(1, 3, figsize=(15, 5))
        axes[0].imshow(cv2.cvtColor(img1, cv2.COLOR_BGR2RGB))
        axes[0].set_title("Image 1")
        axes[1].imshow(cv2.cvtColor(img2, cv2.COLOR_BGR2RGB))
        axes[1].set_title("Image 2")
        axes[2].imshow(diff, cmap='gray')
        axes[2].set_title("Difference (Grayscale)")
        for ax in axes:
            ax.axis("off")  # Hide axes
        plt.tight_layout()
        plt.show()

    except Exception as e:
        # If there's any error, show it in a message box
        messagebox.showerror("Error", str(e))

# Run the app
if __name__ == "__main__":
    select_images_and_compare()