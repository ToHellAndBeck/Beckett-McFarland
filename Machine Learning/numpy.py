import os
import numpy as np
from PIL import Image

def preprocess_image(image_path, target_size=(128, 128)):
    """
    Preprocess an image by resizing and normalizing pixel values.

    Parameters:
        image_path (str): Path to the image file.
        target_size (tuple): Desired output image size.

    Returns:
        numpy.ndarray: Preprocessed image as a numpy array.
    """
    img = Image.open(image_path)
    img = img.resize(target_size)
    img = np.asarray(img) / 255.0  # Normalize pixel values to range [0, 1]
    return img

def preprocess_image_folder(folder_path, target_size=(128, 128)):
    """
    Preprocess a folder of images and store them in a numpy array.

    Parameters:
        folder_path (str): Path to the folder containing image files.
        target_size (tuple): Desired output image size.

    Returns:
        numpy.ndarray: Numpy array containing preprocessed images.
    """
    # Get a list of image files in the folder
    image_files = [f for f in os.listdir(folder_path) if f.endswith(('.jpg', '.png', '.jpeg'))]

    # Preprocess each image and store in a numpy array
    preprocessed_images = []
    for image_file in image_files:
        image_path = os.path.join(folder_path, image_file)
        preprocessed_img = preprocess_image(image_path, target_size)
        preprocessed_images.append(preprocessed_img)

    # Convert the list of preprocessed images to a numpy array
    preprocessed_images = np.array(preprocessed_images)

    return preprocessed_images

# Example usage:
# Provide the path to your image folder and specify the target size
image_folder_path = "path_to_your_image_folder"
target_size = (128, 128)

# Preprocess the images and store them in a numpy array
preprocessed_images = preprocess_image_folder(image_folder_path, target_size)

# Save the preprocessed images to a numpy file
np.save("preprocessed_images.npy", preprocessed_images)

# Load the preprocessed images from the numpy file
loaded_images = np.load("preprocessed_images.npy")

# Print the shape of the loaded images array
print("Loaded images shape:", loaded_images.shape)
