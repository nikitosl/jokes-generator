## Problem
Can AI generate jokes?  
How many data it need?  
Which model architecture is best suited?  

## Task
Model create for jokes generation task on Russian language.
Generate jokes from scratch is too difficult task. Too make it easier jokes was splitted into setup and punch pairs.
Each setup can produce infinite number of punches so inspiration was also introduced,
which means main idea (or main word) of punch for given setup. In the real world, jokes come in different qualities (bad, good, funny, ...).
Therefore, in order for the models to distinguish them from each other, a mark was introduced. It ranges from 0 (not a joke) to 5 (golden joke).

## Data
A huge amount of work has been done to create a dataset. Jokes were copied from different sites or from  
Telegram channels containing jokes, anecdotes, memes with comments and so on. I don't want to post certain links here.  
Parsing was done by selenium robots, page parsing and manual search.  
The size of the complete data set is about 1.5 million jokes.  

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

## Current workflow
From previous experience I decided to train one model for all tasks (mark prediction and punch generation). 
For this task T5 model published by Google is very suitable because it reverts all tasks into text-to-text tasks 
and handle multitask fitting (by adding task-specific prefix to input: "Generate punch:" / "Mark joke:" /...). 

Model trained using flax on huge dataset with jokes and anekdots on different tasks:
1. Span masks (dataset size: 850K)
2. Conditional generation: generate inspiration by given setup (dataset size: 230K)
3. Conditional generation: generate punch by given setup and inspiration (dataset size: 240K)
4. Conditional generation: generate mark by given setup and punch (dataset size: 200K)

## Run T5 finetune process
```
cd jokes-generator/
bash setup_linux.sh
(uncomment in run_train.sh suitable script)
bash run_train.sh >> log.txt
```



