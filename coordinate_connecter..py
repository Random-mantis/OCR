import os
import json
import numpy as np
import logging

# --- Конфигурация ---
DETECTIONS_FOLDER = 'detections'  # папка с JSON из первого этапа
MATCHES_FOLDER = 'matches'         # папка с результатами сопоставления
TEXT_CLASS_NAME = 'text'
NUMBER_CLASS_NAME = 'number'

logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s]: %(message)s')

os.makedirs(MATCHES_FOLDER, exist_ok=True)

def compute_center(box):
    x1, y1, x2, y2 = box
    return ((x1 + x2) / 2, (y1 + y2) / 2)

def euclidean_distance(a, b):
    return np.sqrt((a[0] - b[0])**2 + (a[1] - b[1])**2)

def find_nearest_number(text_box, number_boxes):
    text_center = compute_center(text_box)
    return min(number_boxes, key=lambda n: euclidean_distance(text_center, compute_center(n)))

def main():
    for filename in os.listdir(DETECTIONS_FOLDER):
        if not filename.endswith('.json'):
            continue

        path = os.path.join(DETECTIONS_FOLDER, filename)
        with open(path, 'r', encoding='utf-8') as f:
            detections = json.load(f)

        text_boxes = [d for d in detections if d['label'] == TEXT_CLASS_NAME]
        number_boxes = [d for d in detections if d['label'] == NUMBER_CLASS_NAME]

        matches = []

        if not number_boxes or not text_boxes:
            logging.warning(f"В файле {filename} нет необходимых классов для сопоставления.")
            continue

        for text_obj in text_boxes:
            nearest_num = find_nearest_number(text_obj['bbox'], [n['bbox'] for n in number_boxes])

            # Получаем номер объекта по bbox
            number_obj = next(n for n in number_boxes if n['bbox'] == nearest_num)

            matches.append({
                'text_bbox': text_obj['bbox'],
                'number_bbox': number_obj['bbox'],
                'text_label': text_obj.get('text', ''),     # можно расширить, если нужна OCR
                'number_label': number_obj.get('text', '')  # можно расширить, если нужна OCR
            })

        out_path = os.path.join(MATCHES_FOLDER, filename)
        with open(out_path, 'w', encoding='utf-8') as f:
            json.dump(matches, f, ensure_ascii=False, indent=2)

        logging.info(f"Сопоставление завершено для {filename}, сохранено в {out_path}")

if __name__ == "__main__":
    main()
