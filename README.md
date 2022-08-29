# jokes-generator
Generate jokes with NLP model

## Task
The main goal is to build model to generate jokes from setup.
Using datasets where for each setup there are ~200 punches. For each pair (setup, punch) there is a mark (number of likes).

## Previous approaches (didn't show significant results)
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


## Current workflow
From previous experience I decided to train one model for all tasks (mark prediction and punch generation). 
For this task T5 model published by Google is very suitable cause it reverts all tasks into text-to-text tasks 
and handle multitask fitting (by adding task-specific prefix to input: "Generate punch:" / "Mark joke:" /...). 

1. Take pretrained T5 model: "sberbank-ai/ruT5-base".
2. Fine-tune model on unsupervised task on new corpus of texts (anecdotes, complete jokes, humor texts).
3. Fine-tune model on two supervised tasks - generation punch from setup and punch score prediction.

## Next plan
Add "inspiration" in punch generation pipeline. Every setup has infinity punches, so it's difficult for model 
to learn generation task, because it can see only one punch for one setup during training. 
But we can introduce inspiration into the pipeline, and it will show the direction for punch for current setup!
   1. Each setup has multiple inspirations.
   2. Each setup-inspiration pair has only one punch.
   3. Model to generate inspiration. 
      1. Retrieve inspiration from punch. 
         1. [M-RAKE](https://github.com/vgrabovets/multi_rake). 
         2. TF-IDF.
         3. YAKE.
      2. Train inspiration model (another task for same t5 model?) to generate inspiration from setup.
   4. Train model to generate punch from setup and inspiration.


# Run T5 finetune process
```
cd jokes-generator/
bash setup_linux.sh
(uncomment in run_train.sh suitable script)
bash run_train.sh >> log.txt
```



