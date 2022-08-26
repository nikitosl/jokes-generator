#!/bin/bash
python t5_finetune_span_masks/run_span_mask_train_flax.py t5_finetune_span_masks/config.json

for i in {1..5}
do
   echo "Fine-tune Step $i"
   python t5_finetune_generation/run_conditional_generation_train_flax.py t5_finetune_generation/config_setup_punch.json
   python t5_finetune_generation/run_conditional_generation_train_flax.py t5_finetune_generation/config_mark.json
done
