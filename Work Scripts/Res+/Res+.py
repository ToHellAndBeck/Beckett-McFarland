from PIL import Image

def increase_resolution(input_image_path, output_image_path, factor):
    # Open the image
    with Image.open(input_image_path) as img:
        # Get the original image dimensions
        width, height = img.size

        # Calculate the new dimensions
        new_width = int(width * factor)
        new_height = int(height * factor)

        # Resize the image
        resized_image = img.resize((new_width, new_height))

        # Save the resized image
        resized_image.save(output_image_path, format='JPEG')
        print(f"Image saved to: {output_image_path}")

if __name__ == "__main__":
    input_image_path = r"C:\Users\beckett.mcfarland\Pictures\cover-6118552115502988.png"  # Replace with the path to your input image
    output_image_path = r"C:\Users\beckett.mcfarland\downloads"  # Replace with the desired output path
    resize_factor = 3  # Increase resolution by a factor of 2

    increase_resolution(input_image_path, output_image_path, resize_factor)
