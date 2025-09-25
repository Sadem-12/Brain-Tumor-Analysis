import os

# المسار الصحيح لمجلد التدريب بحرف T كبير
DATASET_PATH = r'C:\Users\Sadem Alsaleh\Desktop\Ai Graduation Project\archive\Training'

class_counts = {}

# التنقل بين المجلدات الفرعية في مجلد التدريب
for class_name in os.listdir(DATASET_PATH):
    # إنشاء المسار الكامل لكل فئة
    class_path = os.path.join(DATASET_PATH, class_name)
    
    # التأكد أن المسار هو لمجلد وليس لملف
    if os.path.isdir(class_path):
        # حساب عدد الملفات (الصور) داخل المجلد
        num_images = len(os.listdir(class_path))
        class_counts[class_name] = num_images

# طباعة النتائج
for class_name, count in class_counts.items():
    print(f"classification '{class_name}': {count} images")