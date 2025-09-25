import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout

# Correct path for the training folder (same as before)
TRAIN_PATH = r'C:\Users\Sadem Alsaleh\Desktop\Ai Graduation Project\archive\Training'
# Correct path for the testing folder
TEST_PATH = r'C:\Users\Sadem Alsaleh\Desktop\Ai Graduation Project\archive\Testing'

# Prepare data using ImageDataGenerator for training
train_datagen = ImageDataGenerator(
    rescale=1./255,
    rotation_range=20,
    width_shift_range=0.2,
    height_shift_range=0.2,
    shear_range=0.2,
    zoom_range=0.2,
    horizontal_flip=True,
    fill_mode='nearest'
)

# Prepare data for the test set (no data augmentation)
test_datagen = ImageDataGenerator(rescale=1./255)

# Load training data from directories
train_generator = train_datagen.flow_from_directory(
    TRAIN_PATH,
    target_size=(150, 150),
    batch_size=32,
    class_mode='categorical'
)

# Load test data from directories
test_generator = test_datagen.flow_from_directory(
    TEST_PATH,
    target_size=(150, 150),
    batch_size=32,
    class_mode='categorical'
)

# Build the model architecture
model = Sequential([
    Conv2D(32, (3, 3), activation='relu', input_shape=(150, 150, 3)),
    MaxPooling2D((2, 2)),
    Conv2D(64, (3, 3), activation='relu'),
    MaxPooling2D((2, 2)),
    Conv2D(128, (3, 3), activation='relu'),
    MaxPooling2D((2, 2)),
    Flatten(),
    Dense(512, activation='relu'),
    Dropout(0.5),
    Dense(4, activation='softmax')  # 4 classes
])

# Compile the model
model.compile(
    optimizer='adam',
    loss='categorical_crossentropy',
    metrics=['accuracy']
)

# Display a summary of the model's layers
model.summary()

print("\nStarting the training process. This may take some time...")

# Train the model
history = model.fit(
    train_generator,
    steps_per_epoch=train_generator.samples // train_generator.batch_size,
    epochs=20, # You can increase this number later
    validation_data=test_generator,
    validation_steps=test_generator.samples // test_generator.batch_size
)

print("\nModel training is complete!")