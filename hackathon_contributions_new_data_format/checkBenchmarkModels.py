#!/usr/bin/env python3.6

import os

model_list = os.listdir()
model_list = sorted(model_list)
print(model_list)

for benchmark_model in model_list:
    if '.MD' not in benchmark_model and '.py' not in benchmark_model:
        condition_filename = os.path.join(benchmark_model, f'experimentalCondition_{benchmark_model}.tsv')
        measurement_filename = os.path.join(benchmark_model, f'measurementData_{benchmark_model}.tsv')
        parameter_filename = os.path.join(benchmark_model, f'parameters_{benchmark_model}.tsv')
        sbml_model_file = os.path.join(benchmark_model, f'model_{benchmark_model}.xml')
        model_name = f'model_{benchmark_model}'
        model_output_dir = f'deleteme-{model_name}'
        if os.path.isfile(condition_filename) and os.path.isfile(measurement_filename) and  \
                os.path.isfile(parameter_filename) and os.path.isfile(sbml_model_file):
            print(benchmark_model)
            os.system("petablint.py -s {} -m {} -c {} -p {}".format(sbml_model_file,
                                                                    measurement_filename,
                                                                    condition_filename,
                                                                    parameter_filename))
        else:
            print(benchmark_model+" skipped")
