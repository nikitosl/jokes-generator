from transformers import T5Tokenizer, T5ForConditionalGeneration
import pandas as pd

# model_name, model_type = "sberbank-ai/ruT5-base", "pytorch"
model_name, model_type = "naltukhov/joke-generator-rus-t5", "flax"
tokenizer = T5Tokenizer.from_pretrained(model_name, from_flax=model_type=="flax")
model = T5ForConditionalGeneration.from_pretrained(model_name, from_flax=model_type=="flax")
print(f'Loaded model {model_name}')

# Punch generation
print('(1/2) Punch Generation task')
df = pd.read_csv('data/agg-setup-punch-dataset/agg-setup-punch-dataset-test.csv')
df['setup'] = 'Generate punch:' + df['setup']
for i in range(3):
    setup, punch = df.sample().values[0]
    print(f'\tExample {i + 1}:')
    print('\t\tSetup:', setup)
    print('\t\tPunch:', punch)
    input_ids = tokenizer(setup, return_tensors="pt").input_ids

    predict_ids = model.generate(input_ids)
    predict = tokenizer.decode(predict_ids[0], skip_special_tokens=True)
    print('\t\tPredict:', predict)

# Mark generation
print('(2/2) Mark Generation task')
df = pd.read_csv('data/agg-marked-joke-dataset/agg-marked-joke-dataset-test.csv')
df['joke'] = 'Mark joke:' + df['joke']
for i in range(3):
    joke, mark = df.sample().values[0]
    print(f'\tExample {i + 1}:')
    print('\t\tJoke:', joke)
    print('\t\tMark:', mark)
    input_ids = tokenizer(joke, return_tensors="pt").input_ids

    predict_ids = model.generate(input_ids)
    predict = tokenizer.decode(predict_ids[0], skip_special_tokens=True)
    print('\t\tPredict:', predict)
