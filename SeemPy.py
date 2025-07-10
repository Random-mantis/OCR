from symspellpy.symspellpy import SymSpell, Verbosity
import os
import json


INPUT_FOLDER = 'texts'           
OUTPUT_FOLDER = 'texts_corrected' 
DICTIONARY_PATH = 'russian.txt'    
MAX_EDIT_DISTANCE = 2
PREFIX_LENGTH = 7

sym_spell = SymSpell(MAX_EDIT_DISTANCE, PREFIX_LENGTH)

if not sym_spell.load_dictionary(DICTIONARY_PATH, term_index=0, count_index=1):
    print(f"❌ Не удалось загрузить словарь {DICTIONARY_PATH}")
    exit(1)


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


for filename in os.listdir(INPUT_FOLDER):
    if not filename.lower().endswith('.json'):
        continue

    input_path = os.path.join(INPUT_FOLDER, filename)
    with open(input_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

   
    full_text = data.get('data', {}).get('full_text', {})
    for key in full_text:
        original_text = full_text[key].get('text', '')
        corrected = correct_text(original_text, sym_spell)
        full_text[key]['text'] = corrected


    output_path = os.path.join(OUTPUT_FOLDER, filename)
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"✅ Исправлен файл {filename}")

print("Все файлы обработаны и исправлены.")
