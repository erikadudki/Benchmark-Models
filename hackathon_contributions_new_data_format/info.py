#!/usr/bin/env python3

import os
import pandas as pd
import yaml


def find_field_general(general_info, needle):
    try:
        return general_info.loc[general_info.iloc[:, 0].str.find(needle) >= 0].iloc[:,1].values[0]
    except IndexError:
        pass


def get_info(model_dir):
    info_file = os.path.join(model_dir, 'General_info.xlsx')
    out_file = os.path.join(model_dir, 'General_info.yml')

    if not os.path.isfile(info_file):
        raise ValueError(f'File {info_file} does not exist.')

    xls = pd.read_excel(info_file,
                        sheet_name=None)

    data = {'general': {}}

    general_info = list(xls.items())[0][1]
    assert general_info.shape[1] == 2
    data['general']['nllh'] = find_field_general(general_info, 'likelihood')
    data['general']['chi2'] = find_field_general(general_info, 'Chi2')


    with open(out_file, 'w') as outfile:
        yaml.dump(data, outfile, default_flow_style=False)


def main():
    model_list = os.scandir()
    model_list = sorted(f.name  for f in model_list if f.is_dir())

    for benchmark_model in model_list:
        print(benchmark_model)
        try:
            get_info(benchmark_model)
        except ValueError as e:
            print(e)

        #print('='*100)
        #break


if __name__ == '__main__':
    main()
