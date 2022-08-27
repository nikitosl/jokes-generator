#!/bin/bash
python t5_finetune_span_masks/run_span_mask_train_flax.py t5_finetune_span_masks/config.json
python test_t5_generation.py
