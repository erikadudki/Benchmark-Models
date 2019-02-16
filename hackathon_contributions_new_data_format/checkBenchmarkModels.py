#!/usr/bin/env python3

import os

model_list = os.scandir()
model_list = sorted(f.name  for f in model_list if f.is_dir())

for benchmark_model in model_list:
    os.system("cd {} && petablint.py -v -n {} ".format(benchmark_model,benchmark_model))
    print('='*100) # just for output readability
