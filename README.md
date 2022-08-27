# jokes-generator
Generate jokes with NLP model

The main goal is to build model to generate jokes from setup.
Using datasets where for each setup there are ~200 punches. For each pair (setup, punch) there is a mark (number of likes).

As we have dataset with jokes markup, first idea was to train model to markup jokes (simple regression model).
Methods already tried for joles markup model:
  1. Catboost regression model over sentence embeddings for setup and punch. 
    Tried regression and even classification into two classes (good joke or bad). 
    No approach showed sofisticated results. Train loss is reducing on each step, but eval loss stay unchanged.
    Fixed embeddings are not able to handle such complex task.
    
  2. Pretrained by sber T5 model. Setup to encoder, punch to decoder. 
    Decoder output to fully-connected layer. Trained with MSEloss on Google Colab.
    No sofisticated results. Train loss and eval loss are not reducing during epochs.
    Can't generalize the mark function at all.

 
I think, it's too hard to separate tasks into two models (markup model and jokes generation model). 
Because for jokes markup need an understanding how to build joke and visa versa.

Next plan is:
1. Take pretrained T5 model.
2. Fine-tune model on unsupervised task on new corpus of texts (anecdotes, complete jokes, humor texts).
3. Fine-tune model on supervised task - generation punch from setup.
4. Fine-tune model on supervised task - punch score prediction.
5. Repeat steps 3 and 4. Model will be trained on two independent tasks, but in same field (humor). 
6. That's should make model be robust.


Another ideas:
- Reinforcement learning + transformer for text generation. Research paper: https://arxiv.org/pdf/2101.04229.pdf


# Run T5 finetune process
### Run complete finetune in loop:
```
cd jokes-generator/
bash setup_linux.sh
bash run_train.sh >> log.txt
```
### Run finetune semi-manually:
```
cd jokes-generator/
bash setup_linux.sh
bash run_finetune_span_maks_from_scratch.sh
bash run_finetune_generation_loop.sh
```

### Run finetune manually:
```
cd jokes-generator/
bash setup_linux.sh
python t5_finetune_span_masks/run_span_mask_train_flax.py t5_finetune_span_masks/config.json
python t5_finetune_generation/run_conditional_generation_train_flax.py t5_finetune_generation/config_setup_punch.json
python t5_finetune_generation/run_conditional_generation_train_flax.py t5_finetune_generation/config_mark.json
```

# Model versions
93c99f8 - fine-tuned on span-masks (20 epochs)