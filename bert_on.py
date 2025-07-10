from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
import sys

model_path = "bert_russian_model"
model = AutoModelForSequenceClassification.from_pretrained(model_path)
tokenizer = AutoTokenizer.from_pretrained(model_path)

if len(sys.argv) > 1:
    input_text = sys.argv[1]
else:
    input_text = input("Введите текст для оценки: ")

inputs = tokenizer(input_text, return_tensors="pt", padding=True, truncation=True, max_length=128)

model.eval()
with torch.no_grad():
    outputs = model(**inputs)
    score = outputs.logits.item()

print(f"Предсказанная оценка: {score:.2f}")