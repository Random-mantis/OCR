from symspellpy.symspellpy import SymSpell, Verbosity
import os
import json

# --- Конфигурация ---
INPUT_FOLDER = 'texts'           # Папка с json файлами после инференса (2 этап)
OUTPUT_FOLDER = 'texts_corrected'  # Папка для исправленных json файлов
DICTIONARY_PATH = 'russian.txt'    # Путь к словарю SymSpell
MAX_EDIT_DISTANCE = 2
PREFIX_LENGTH = 7

# --- Инициализация SymSpell ---
sym_spell = SymSpell(MAX_EDIT_DISTANCE, PREFIX_LENGTH)

if not sym_spell.load_dictionary(DICTIONARY_PATH, term_index=0, count_index=1):
    print(f"❌ Не удалось загрузить словарь {DICTIONARY_PATH}")
    exit(1)

# --- Создаём папку для результатов ---
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

def correct_text(text, sym_spell):
    corrected_words = []
    for word in text.split():
        suggestions = sym_spell.lookup(word, Verbosity.CLOSEST, max_edit_distance=MAX_EDIT_DISTANCE)
        if suggestions:
            corrected_words.append(suggestions[0].term)
        else:
            corrected_words.append(word)
    return ' '.join(corrected_words)

# --- Обработка файлов ---
for filename in os.listdir(INPUT_FOLDER):
    if not filename.lower().endswith('.json'):
        continue

    input_path = os.path.join(INPUT_FOLDER, filename)
    with open(input_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Проверяем структуру и исправляем тексты
    full_text = data.get('data', {}).get('full_text', {})
    for key in full_text:
        original_text = full_text[key].get('text', '')
        corrected = correct_text(original_text, sym_spell)
        full_text[key]['text'] = corrected

    # Сохраняем исправленный json
    output_path = os.path.join(OUTPUT_FOLDER, filename)
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"✅ Исправлен файл {filename}")

print("Все файлы обработаны и исправлены.")