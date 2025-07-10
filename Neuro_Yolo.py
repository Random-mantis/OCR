from ultralytics import YOLO
import cv2
import os
import json
import logging


MODEL_PATH = 'yolo_model.pt'            # путь к обученной модели
IMAGES_FOLDER = 'images'                 # папка с изображениями для детекции
DETECTIONS_FOLDER = 'detections'        # папка для JSON с результатами детекции
CLASS_NAMES_PATH = './dataset/classes'  # файл классов
CONF_THRESHOLD = 0.3

logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s]: %(message)s')

os.makedirs(DETECTIONS_FOLDER, exist_ok=True)

def load_class_names(path):
    with open(path, 'r', encoding='utf-8') as f:
        return [line.strip() for line in f if line.strip()]

def main():
    class_names = load_class_names(CLASS_NAMES_PATH)
    model = YOLO(MODEL_PATH)

    for filename in os.listdir(IMAGES_FOLDER):
        if not filename.lower().endswith(('.jpg', '.jpeg', '.png')):
            continue

        image_path = os.path.join(IMAGES_FOLDER, filename)
        results = model.predict(image_path, conf=CONF_THRESHOLD)[0]
        boxes = results.boxes

        detection_data = []
        for box in boxes:
            cls_id = int(box.cls[0])
            label = class_names[cls_id]
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            conf = float(box.conf[0])

            detection_data.append({
                'class_id': cls_id,
                'label': label,
                'bbox': [x1, y1, x2, y2],
                'confidence': conf
            })

        json_path = os.path.join(DETECTIONS_FOLDER, os.path.splitext(filename)[0] + '.json')
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(detection_data, f, ensure_ascii=False, indent=2)

        logging.info(f"Обработано {filename}, сохранён файл {json_path}")

if __name__ == "__main__":
    main()
