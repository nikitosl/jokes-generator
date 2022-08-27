from transformers import T5Tokenizer, T5ForConditionalGeneration
import pandas as pd

# model_name, model_type = "sberbank-ai/ruT5-base", "pytorch"
model_name, model_type = "naltukhov/joke-generator-rus-t5", "flax"
tokenizer = T5Tokenizer.from_pretrained(model_name, from_flax=model_type=="flax")
model = T5ForConditionalGeneration.from_pretrained(model_name, from_flax=model_type=="flax")
print(f'Loaded model {model_name}')

# Punch generation
df = pd.read_csv('data/agg-generation-dataset/agg-generation-dataset-test.csv')
for i in range(10):
    setup, punch = df.sample().values[0]
    print(f'\tExample {i + 1}:')
    print('\t\tInput:', setup)
    print('\t\tTarget:', punch)
    input_ids = tokenizer(setup, return_tensors="pt").input_ids

    predict_ids = model.generate(input_ids)
    predict = tokenizer.decode(predict_ids[0], skip_special_tokens=True)
    print('\t\tOutput:', predict)
