#!/usr/bin/env python3

import os
import sys
import re

def ensure_file_exists(filename):
    if not os.path.isfile(filename):
        print(f'\tERROR: Missing file {filename}')

script_dir = os.path.split(__file__)[0]
for directory in os.listdir(script_dir):
    if not os.path.isdir(directory):

        continue

    print(directory)

    if not re.match(r'^[A-Z][a-z]+_\w+\d{4}$', directory):
        print(f'WARNING: Not a valid model directory name: {directory}')

    model_name = directory
    condition_filename = os.path.join(model_name,
                                      f'experimentalCondition_{model_name}.tsv')
    measurement_filename = os.path.join(model_name,
                                        f'measurementData_{model_name}.tsv')
    parameter_filename = os.path.join(model_name,
                                      f'parameters_{model_name}.tsv')
    sbml_model_file = os.path.join(model_name,
                                   f'model_{model_name}.xml')

    ensure_file_exists(condition_filename)
    ensure_file_exists(measurement_filename)
    ensure_file_exists(parameter_filename)
    ensure_file_exists(sbml_model_file)

    print()

