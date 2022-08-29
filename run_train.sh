#!/bin/bash

:: Finetune sberbank-ai/ruT5-base on span mask and then finetune on punch-mark-generation task
:: python t5_finetune_span_masks/run_span_mask_train_flax.py t5_finetune_span_masks/config.json
:: python t5_finetune_generation/run_conditional_generation_train_flax.py t5_finetune_generation/config_generation.json

:: Finetune naltukhov/joke-generator-rus-t5 in loop by one epoch punch generation and mark generation tasks
:: for i in {1..20}
:: do
::    echo "===================================Fine-tune Step $i========================================="
::    python t5_finetune_generation/run_conditional_generation_train_flax.py t5_finetune_generation/config_setup_punch.json
::    python t5_finetune_generation/run_conditional_generation_train_flax.py t5_finetune_generation/config_mark.json
::    python test_t5_generation.py
:: done
