import numpy as np
import tensorflow as tf
import datetime
from tensorflow.keras.models import load_model
# import all modules from the original code that are still needed
from tensorflow.keras.preprocessing.image import ImageDataGenerator
import os

# Import the necessary function from the preprocessing module
from preprocessing import resize_and_normalize 

# Define class names as learned by the model (needed before prediction)
class_names = ['glioma', 'meningioma', 'notumor', 'pituitary']

# --- تحميل النموذج الجاهز بدلاً من بنائه وتدريبه ---

try:
    # >>> التعديل الرئيسي: تحميل النموذج المحفوظ (brain_tumor_model.h5) <<<
    model = load_model('brain_tumor_model.h5')
    print("Trained model loaded successfully for fast prediction.")
except Exception as e:
    print(f"Error loading model: {e}")
    print("Ensure 'brain_tumor_model.h5' exists in the project folder and TensorFlow is correctly installed.")
    # يمكن هنا إيقاف البرنامج إذا كان التحميل ضرورياً
    exit()

# تم إزالة الأكواد التالية لعدم الحاجة إليها بعد الآن:
# - Set the correct paths for the training and testing folders
# - Prepare data using ImageDataGenerator
# - Load training data from directories (train_generator)
# - Load test data from directories (test_generator)
# - Build the model architecture (model = Sequential([...]))
# - Compile the model
# - model.fit(...)
# - model.save(...)

# --- Prediction and Report Generation Functions ---

def predict_tumor(img_path):
    """
    Predicts the class of a single image using the dedicated preprocessing module.
    """
    # 1. استخدام دالة المعالجة للحصول على مصفوفة مطبّعة (150, 150, 3)
    normalized_array = resize_and_normalize(img_path) 
    
    # 2. إضافة بُعد الدفعة (Batch Dimension) لأن الموديل يتوقعها
    img_array = np.expand_dims(normalized_array, axis=0)
    
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

# --- Execution ---

# Path to an image from the test folder (يجب أن يبقى هذا المسار كما هو)
image_path = r'C:\Users\Sadem Alsaleh\Desktop\Graduation Project\brain tumor model\archive\Testing\meningioma\Te-me_0016.jpg' 

# Perform prediction
predicted_class, confidence, predictions = predict_tumor(image_path)

# Generate and print the report
report = generate_report(predicted_class, confidence, predictions)
print("\n" + report)