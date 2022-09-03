from transformers import T5Tokenizer, T5ForConditionalGeneration
import pandas as pd

# model_name, model_type = "sberbank-ai/ruT5-base", "pytorch"
model_name, model_type = "naltukhov/joke-generator-t5-rus-finetune", "flax"
tokenizer = T5Tokenizer.from_pretrained(model_name, from_flax=model_type == "flax",
                                        force_download=False, use_auth_token=True)
model = T5ForConditionalGeneration.from_pretrained(model_name, from_flax=model_type == "flax",
                                                   force_download=False, use_auth_token=True)
print(f'Loaded model {model_name}')

inspiration_prefix = 'Сгенерировать вдохновение: '
mark_prefix = 'Сгенерировать оценку: '
punch_prefix = 'Сгенерировать шутку: '


def inference(input):
    setup = input.split(':')[1].split('|')[1]

    # Generate inspirations
    setup_ids = tokenizer(inspiration_prefix + setup, return_tensors="pt").input_ids
    predict_inspiration_ids = model.generate(setup_ids,
                                             num_beams=5,
                                             top_k=10,
                                             max_length=50,
                                             early_stopping=True,
                                             no_repeat_ngram_size=2,
                                             num_return_sequences=3).tolist()
    predict_inspirations = [tokenizer.decode(p, skip_special_tokens=True) for p in predict_inspiration_ids]

    result_list = list()
    for predict_inspiration in predict_inspirations:
        result_dict = dict()
        result_dict['setup'] = setup
        result_dict['inspiration'] = predict_inspiration
        input_ids = tokenizer(punch_prefix + predict_inspiration + '|' + setup, return_tensors="pt").input_ids
        predict_punches_ids = model.generate(input_ids,
                                             num_beams=5,
                                             top_k=10,
                                             max_length=50,
                                             early_stopping=True,
                                             no_repeat_ngram_size=2,
                                             num_return_sequences=3).tolist()
        predict_punches = [tokenizer.decode(p, skip_special_tokens=True) for p in predict_punches_ids]
        result_dict['punches'] = predict_punches
        result_list.append(result_dict)
    return result_list


# Punch generation
df = pd.read_csv('data/agg-generation-dataset/agg-generation-dataset-test.csv')
df = df.loc[df.input.str.startswith(punch_prefix)]
for i in range(10):
    input, output = df.sample().values[0]
    print(f'\tExample {i + 1}:')

    predicts = inference(input)
    print(*predicts)
