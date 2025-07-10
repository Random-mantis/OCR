import os
import json
import pandas as pd


TEXTS_FOLDER = 'texts'      
SCORES_FOLDER = 'jsons'     
OUTPUT_CSV = 'dataset.csv'   

score_data = {}
for file in os.listdir(SCORES_FOLDER):
    if file.lower().endswith('.json'):
        with open(os.path.join(SCORES_FOLDER, file), 'r', encoding='utf-8') as f:
            record = json.load(f)
            # Здесь предполагается, что есть ключ "id" и "total" в файле оценок
            task_id = record.get("id")
            total_score_str = record.get("total")  # Формат: "1(3)0(3)0(3)..." 
            if task_id is not None and total_score_str:
                # Преобразуем строку в числовой балл
                # Формат: "1(3)" значит 1 из 3, считаем сумму выставленных баллов
                total_score = 0
                for part in total_score_str.split('0'):
                    if '(' in part:
                        try:
                            score_val = int(part.split('(')[0])
                            total_score += score_val
                        except Exception:
                            pass
                score_data[task_id] = total_score


combined_data = []
for file in os.listdir(TEXTS_FOLDER):
    if file.lower().endswith('.json'):
        with open(os.path.join(TEXTS_FOLDER, file), 'r', encoding='utf-8') as f:
            text_record = json.load(f)
            # Структура: data -> full_text -> {номер задания: {text: "..."}}
            full_texts = text_record.get('data', {}).get('full_text', {})
            for task_num, text_dict in full_texts.items():
                text = text_dict.get('text', '')
                score = score_data.get(task_num)
                if score is not None:
                    combined_data.append({
                        'text': text,
                        'score': score,
                        'task_id': task_num,
                       
                    })


df = pd.DataFrame(combined_data)
df.to_csv(OUTPUT_CSV, index=False, encoding='utf-8')
print(f"✅ Объединено записей: {len(df)}")
print(f"✅ CSV сохранён в {OUTPUT_CSV}")
