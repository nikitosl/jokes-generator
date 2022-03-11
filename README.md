# jokes-generator
Research a challeging task - generating jokes with NLP models.

The main goal is to build model to generate jokes from setup.
Using datasets where for each setup there are ~200 punches. For each pair (setup, punch) there is a mark (number of likes).

As we have dataset with jokes markup, first idea was to train model to markup jokes (simple regression model).
Methods already tried for joles markup model:
  1. Catboost regression model over sentence embeddings for setup and punch. 
    Tried regression and even classification into two classes (good joke or bad). 
    No approach showed sofisticated results. Train loss is reducing on each step, but eval loss stay unchanged.
    Fixed embeddings are not able to handle such complex task.
    
  2. T5 model pretrained on russian corpus. Setup to encoder, punch to decoder. 
    Decoder output to fully-connected layer. Trained with MSEloss on Google Colab.
    No sofisticated results. Train loss and eval loss are not reducing during epochs.
    Can't generalize the mark function at all.

 
Hard to separate task into two models (markup model and jokes generation model). 
Because for jokes markup need unerstanding how to build joke and visa versa.

TODO:
1. - Finetune T5 model on big corpus of russian anekdots. 
   - Train T5 model from previous step to generate punch by given setup.
   - Train T5 model from previous step to mark joke by given setup and punch.

2. Reinforcement learning + transformer for text generation.
      Research paper: https://arxiv.org/pdf/2101.04229.pdf
      

