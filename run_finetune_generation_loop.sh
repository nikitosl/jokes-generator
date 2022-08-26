#!/bin/bash
python test_t5_generation.py
for i in {1..20}
do
   echo "===================================Fine-tune Step $i========================================="
   python t5_finetune_generation/run_conditional_generation_train_flax.py t5_finetune_generation/config_setup_punch.json
   python t5_finetune_generation/run_conditional_generation_train_flax.py t5_finetune_generation/config_mark.json
   python test_t5_generation.py
done
