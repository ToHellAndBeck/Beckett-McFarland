from PIL import Image

# Open the image
img = Image.open("pngwing.com.png")

# List of words to name the PNGs
type_words = [
    "BUG", "ELECTRIC", "FIRE", "GRASS", "NORMAL", "ROCK",
    "DARK", "FAIRY", "FLYING", "GROUND", "POISON", "DRAGON",
    "FIGHTING", "GHOST", "ICE", "PSYCHIC"
]

# Calculate image dimensions
image_width = int(img.width / 3)
image_height = int(img.height / 6)

# Iterate over rows in the DataFrame
for x in range(3):
    image_x = image_width * x
    for y in range(6):
        image_y = image_height * y
        print(image_x, image_y, image_width, image_height)

        # Crop the image
        new_image = img.crop((image_x, image_y, image_width + image_x, image_height + image_y))

        # Extract text using Tesseract

        # Name the PNG based on the words in the list
        i = x * 6 + y  # Calculate the index based on row and column
        word = type_words[i]
        new_image.save(f"{word}.png", "PNG")
