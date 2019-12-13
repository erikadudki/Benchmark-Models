# -*- coding: utf-8 -*-

import os
import pandas as pd
import numpy as np

model_list = os.scandir()
model_list = sorted(f.name for f in model_list if f.is_dir())
model_list = [model_list[1]]

for benchmark_model in model_list:

    print(benchmark_model)

    parameter_file_name = (benchmark_model +
                           '/parameters_' +
                           benchmark_model + '.tsv')

    if os.path.isfile(parameter_file_name):
        # create a copy of the original parameter file
        os.system("cp {} {}".format(
            parameter_file_name,
            benchmark_model + '/parametersOriginal_' +
            benchmark_model + '.tsv')
        )
        # read the parameter file
        parameter_df = pd.read_csv(parameter_file_name, sep='\t')

        # loop over rows in parameter data-frame
        for row in range(parameter_df.shape[0]):
            for column_name in ['upperBound', 'lowerBound', 'nominalValue']:
                # set column type to float64
                parameter_df = parameter_df.astype({column_name: 'float64'})
                if parameter_df['parameterScale'][row] in 'log':
                    # exponential of log parameter
                    parameter_df.at[row, column_name] = \
                        np.exp(float(parameter_df[column_name][row]))
                elif parameter_df['parameterScale'][row] in 'log10':
                    # exponential of log10 parameter
                    parameter_df.at[row, column_name] = \
                        np.power(10, float(parameter_df[column_name][row]))

        # write results in parameter file
        parameter_df.to_csv(r'./'+benchmark_model +
                            '/parameters_'+benchmark_model+'.tsv',
                            index=None,
                            header=True,
                            sep='\t')
    else:
        # in case parameter file not found
        print('Parameter file not found in {}'.format(
            benchmark_model)
        )
