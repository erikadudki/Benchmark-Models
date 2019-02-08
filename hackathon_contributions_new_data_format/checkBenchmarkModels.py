#!/usr/bin/env python3

import os

model_list = os.listdir()
model_list = sorted(model_list)
print(model_list)

for benchmark_model in model_list:
    if '.MD' not in benchmark_model and '.py' not in benchmark_model:
        os.system("cd {} && petablint.py -v -n {} ".format(benchmark_model,benchmark_model))
        print('='*100) # just for output readability
