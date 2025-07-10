import pandas as pd
from datasets import Dataset
from transformers import AutoTokenizer, AutoModelForSequenceClassification, Trainer, TrainingArguments
from sklearn.metrics import mean_squared_error
import numpy as np
import matplotlib.pyplot as plt


df = pd.read_csv("dataset.csv")  # Колонки: 'text', 'score'
df = df[['text', 'score']].rename(columns={'score': 'label'})

dataset = Dataset.from_pandas(df)


model_name = "DeepPavlov/rubert-base-cased"  # Русский BERT
tokenizer = AutoTokenizer.from_pretrained(model_name)

def tokenize_function(examples):
    return tokenizer(examples['text'], padding='max_length', truncation=True, max_length=128)

tokenized_dataset = dataset.map(tokenize_function, batched=True)
tokenized_dataset = tokenized_dataset.train_test_split(test_size=0.2)
model = AutoModelForSequenceClassification.from_pretrained(model_name, num_labels=1)
training_args = TrainingArguments(
    output_dir='./bert_russian_model',
    evaluation_strategy='epoch',
    save_strategy='epoch',
    per_device_train_batch_size=8,
    per_device_eval_batch_size=8,
    num_train_epochs=5,
    learning_rate=2e-5,
    weight_decay=0.01,
    load_best_model_at_end=True,
    metric_for_best_model='rmse',
)

def compute_metrics(eval_pred):
    preds, labels = eval_pred
    preds = preds.flatten()
    rmse = mean_squared_error(labels, preds, squared=False)
    return {'rmse': rmse}

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_dataset['train'],
    eval_dataset=tokenized_dataset['test'],
    tokenizer=tokenizer,
    compute_metrics=compute_metrics,
)

train_result = trainer.train()

trainer.save_model('./bert_russian_model')
tokenizer.save_pretrained('./bert_russian_model')

print("✅ Обучение завершено. Модель и токенизатор сохранены.")
history = train_result.metrics
train_losses = []
eval_rmse = []
epochs = []

for log in trainer.state.log_history:
    if 'loss' in log:
        train_losses.append(log['loss'])
    if 'eval_rmse' in log:
        eval_rmse.append(log['eval_rmse'])
        epochs.append(log['epoch'])

import matplotlib.pyplot as plt

plt.figure(figsize=(12,5))
plt.subplot(1,2,1)
plt.plot(train_losses, label='Training Loss')
plt.xlabel('Steps')
plt.ylabel('Loss')
plt.title('Training Loss')
plt.legend()
plt.subplot(1,2,2)
plt.plot(epochs, eval_rmse, marker='o', label='Eval RMSE')
plt.xlabel('Epoch')
plt.ylabel('RMSE')
plt.title('Validation RMSE per Epoch')
plt.legend()

plt.tight_layout()
plt.show()
