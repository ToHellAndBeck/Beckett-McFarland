import os
import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf
from tensorflow.keras.layers import Dense, Reshape, Conv2DTranspose, Conv2D, Flatten
from tensorflow.keras.models import Sequential
from tensorflow.keras.losses import BinaryCrossentropy
from tensorflow.keras.optimizers import Adam

# Load preprocessed images from the folder
image_folder_path = r"C:\Users\Beckett\Pictures\AI Training\Wedgies"  # Update with your image folder path
preprocessed_images = np.load(os.path.join(image_folder_path, "preprocessed_images.npy"))

# Normalize input images to range [-1, 1]
preprocessed_images = (preprocessed_images.astype(np.float32) - 127.5) / 127.5

# Define the Generator
def build_generator(input_shape=(100,)):
    model = Sequential([
        Dense(8 * 8 * 256, activation='relu', input_shape=input_shape),  # Adjusted input shape
        Reshape((8, 8, 256)),  # Adjusted shape to match subsequent layers
        Conv2DTranspose(128, (4, 4), strides=(2, 2), padding='same', activation='relu'),  # Adjusted filter size
        Conv2DTranspose(64, (4, 4), strides=(2, 2), padding='same', activation='relu'),  # Adjusted filter size
        Conv2D(3, (3, 3), padding='same', activation='tanh')
    ])
    return model

# Define the Discriminator
def build_discriminator(input_shape=(128, 128, 3)):
    model = Sequential([
        Conv2D(32, (3, 3), strides=(2, 2), padding='same', activation='relu', input_shape=input_shape),
        Conv2D(64, (3, 3), strides=(2, 2), padding='same', activation='relu'),
        Flatten(),
        Dense(1, activation='sigmoid')
    ])
    return model

# Build and compile the GAN
input_dim = 100
image_shape = (128, 128, 3)
generator = build_generator(input_shape=(100,))

discriminator = build_discriminator(input_shape=(128, 128, 3))
discriminator.compile(optimizer=Adam(learning_rate=0.0002, beta_1=0.5), loss='binary_crossentropy', metrics=['accuracy'])

# The combined GAN model
discriminator.trainable = False
gan_input = tf.keras.layers.Input(shape=(input_dim,))
x = generator(gan_input)
gan_output = discriminator(x)
gan = tf.keras.models.Model(gan_input, gan_output)
gan.compile(optimizer=Adam(learning_rate=0.0002, beta_1=0.5), loss='binary_crossentropy')

# Train the GAN
epochs = 100
batch_size = 32
num_samples = preprocessed_images.shape[0]

for epoch in range(epochs):
    for batch_start in range(0, num_samples, batch_size):
        batch_end = min(batch_start + batch_size, num_samples)
        real_images = preprocessed_images[batch_start:batch_end]
        
        # Define batch_end here
        noise = np.random.randn(batch_end - batch_start, input_dim) 
        # Train the discriminator
        d_loss_real = discriminator.train_on_batch(real_images, np.ones((batch_end - batch_start, 1)))
        d_loss_fake = discriminator.train_on_batch(generator.predict(noise), np.zeros((batch_end - batch_start, 1)))

        # Train the generator (via the GAN model)
        g_loss = gan.train_on_batch(noise, np.ones((batch_end - batch_start, 1)))

        print(f"Epoch {epoch+1}/{epochs}, Batch {batch_start // batch_size + 1}/{num_samples // batch_size}, D Loss Real: {d_loss_real[0]}, D Loss Fake: {d_loss_fake[0]}, G Loss: {g_loss}")

        # Visualize generated images
        if batch_start % (batch_size * 10) == 0:
            noise = np.random.randn(5, input_dim)
            generated_images = generator.predict(noise)

            plt.figure(figsize=(10, 4))
            for i in range(5):
                ax = plt.subplot(1, 5, i + 1)
                plt.imshow((generated_images[i] + 1) / 2)  # Scale from [-1, 1] to [0, 1]
                plt.title("Generated")
                plt.axis('off')

            plt.show()
