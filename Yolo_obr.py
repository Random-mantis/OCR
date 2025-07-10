import os
import json
import logging


MATCHES_FOLDER = 'matches'
TEXTS_FOLDER = 'texts'

logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s]: %(message)s')

os.makedirs(TEXTS_FOLDER, exist_ok=True)

def main():
    for filename in os.listdir(MATCHES_FOLDER):
        if not filename.endswith('.json'):
            continue

        path = os.path.join(MATCHES_FOLDER, filename)
        with open(path, 'r', encoding='utf-8') as f:
            matches = json.load(f)

        output_json = {'data': {'full_text': {}}}
        text_index = 0

        for match in matches:
            # Предположим, что OCR-текст уже записан в 'text_label' и 'number_label'
            # Если нет, нужно добавить вызов OCR здесь

            text = match.get('text_label', '').strip()
            number = match.get('number_label', '').strip()

            if not text or not number:
                continue

            # Индексация с 22 (как было у тебя)
            index = 22 + text_index
            output_json['data']['full_text'][str(index)] = {
                'text': text,
                'number': number
            }
            text_index += 1

        out_path = os.path.join(TEXTS_FOLDER, filename)
        with open(out_path, 'w', encoding='utf-8') as f:
            json.dump(output_json, f, ensure_ascii=False, indent=2)

        logging.info(f"Итоговый JSON сохранён: {out_path}")

if __name__ == "__main__":
    main()
