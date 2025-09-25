import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator

# المسار الصحيح لمجلد التدريب
TRAIN_PATH = r'C:\Users\Sadem Alsaleh\Desktop\Ai Graduation Project\archive\Training'

# إعداد مولد الصور (ImageDataGenerator) للتدريب
# هذا المولد سيقوم بتطبيع القيم وتوسيع البيانات (Data Augmentation)
datagen = ImageDataGenerator(
    rescale=1./255,            # تطبيع قيم البكسل
    rotation_range=20,         # تدوير عشوائي للصور
    width_shift_range=0.2,     # إزاحة أفقية عشوائية
    height_shift_range=0.2,    # إزاحة عمودية عشوائية
    shear_range=0.2,           # القص (Shearing)
    zoom_range=0.2,            # تكبير عشوائي
    horizontal_flip=True,      # قلب أفقي عشوائي
    fill_mode='nearest'        # ملء الفراغات الناتجة
)

# تحميل البيانات من المجلدات
train_generator = datagen.flow_from_directory(
    TRAIN_PATH,
    target_size=(150, 150),    # توحيد حجم الصور إلى 150x150
    batch_size=32,
    class_mode='categorical'   # نوع التصنيف هو فئات متعددة
)

print("\nData successfully processed")
print(f"Number of images in the training set: {train_generator.samples}")
print(f"Number of classification: {train_generator.num_classes}")
print(f"Classification arrangement: {train_generator.class_indices}")