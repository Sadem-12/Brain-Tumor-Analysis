import numpy as np
import tensorflow as tf
import datetime
from tensorflow.keras.preprocessing import image
from tensorflow.keras.models import Sequential, load_model
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout
from tensorflow.keras.preprocessing.image import ImageDataGenerator
import os

# Set the correct paths for the training and testing folders
TRAIN_PATH = r'C:\Users\Sadem Alsaleh\Desktop\Graduation Project\brain tumor model\archive\Training'
TEST_PATH = r'C:\Users\Sadem Alsaleh\Desktop\Graduation Project\brain tumor model\archive\Testing'

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

# Build the model architecture (with added layers)
model = Sequential([
    Conv2D(32, (3, 3), activation='relu', input_shape=(150, 150, 3)),
    MaxPooling2D((2, 2)),
    
    Conv2D(64, (3, 3), activation='relu'),
    MaxPooling2D((2, 2)),
    
    Conv2D(128, (3, 3), activation='relu'),
    MaxPooling2D((2, 2)),
    
    Conv2D(256, (3, 3), activation='relu'),
    MaxPooling2D((2, 2)),
    
    Flatten(),
    Dense(512, activation='relu'),
    Dropout(0.5),
    Dense(256, activation='relu'),
    Dropout(0.5),
    Dense(4, activation='softmax')  # 4 classes
])

# Compile the model
model.compile(
    optimizer='adam',
    loss='categorical_crossentropy',
    metrics=['accuracy']
)

print("Starting the training process. This may take some time...")

# Train the model
history = model.fit(
    train_generator,
    steps_per_epoch=train_generator.samples // train_generator.batch_size,
    epochs=40,
    validation_data=test_generator,
    validation_steps=test_generator.samples // test_generator.batch_size
)

print("Model training is complete!")

# --- Prediction and Report Generation ---

# Save the model after training
model.save('brain_tumor_model.h5')

# Define class names as learned by the model
class_names = ['glioma', 'meningioma', 'notumor', 'pituitary']

def predict_tumor(img_path):
    """
    Predicts the class of a single image.
    """
    # Load and resize the image
    img = image.load_img(img_path, target_size=(150, 150))
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    img_array = img_array / 255.0
    
    # Perform prediction
    predictions = model.predict(img_array)
    predicted_class_index = np.argmax(predictions[0])
    predicted_class_name = class_names[predicted_class_index]
    confidence = np.max(predictions[0]) * 100
    
    # Return the predicted class name, confidence, and full predictions
    return predicted_class_name, confidence, predictions[0]

def generate_report(predicted_class, confidence, predictions):
    """
    Generates a textual report based on the prediction results.
    """
    report = f"--- MRI Image Analysis Report ---\n"
    report += f"Date: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
    report += f"Predicted Class: {predicted_class}\n"
    report += f"Confidence Score: {confidence:.2f}%\n"
    
    # Detailed confidence breakdown for all classes
    report += "\nConfidence Breakdown:\n"
    for i, class_name in enumerate(class_names):
        report += f"  - {class_name.capitalize()}: {predictions[i]*100:.2f}%\n"

    if predicted_class == 'notumor':
        report += "\nAnalysis: No tumor was detected in the image. For a final diagnosis, a consultation with a medical professional is recommended.\n"
    else:
        report += f"\nAnalysis: A tumor of the '{predicted_class}' type was detected. Further medical consultation is advised.\n"

    report += "\n--- End of Report ---\n"
    return report

# Path to an image from the test folder
image_path = r'C:\Users\Sadem Alsaleh\Desktop\Graduation Project\brain tumor model\archive\Testing\meningioma\Te-me_0016.jpg' 

# Perform prediction
predicted_class, confidence, predictions = predict_tumor(image_path)

# Generate and print the report
report = generate_report(predicted_class, confidence, predictions)
print("\n" + report)