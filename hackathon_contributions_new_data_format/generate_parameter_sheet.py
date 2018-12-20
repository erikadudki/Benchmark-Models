import os
import numpy as np
import pandas as pd

# INPUT - PLEASE INSERT FITTING PATH TO GENERAL INFO
folder = r"C:\Users\phili\Benchmark-Models\hackathon_contributions_new_data_format\Boehm_JProteomeRes2014"


# ALGORITHM STARTS
basename = os.path.basename(folder)
filepath = os.path.join(folder, 'General_info.xlsx')


def new_format(filepath):
    old_format = pd.read_excel(filepath, sheet_name="Parameters")
    return (old_format)


output_new_format = new_format(filepath)


# print(output_new_format)

def transform_format(y):
    a = pd.DataFrame({'parameterID': y.parameter,  # no brackets around y.---
                      'parameterName': y.parameter,
                      'parameterScale': y.loc[:, 'analysis at log-scale'],
                      'lowerBound': y.loc[:, 'lower boundary'],  # not correct with nor without brackets
                      'upperBound': y.loc[:, 'upper boundary'],  # y.values[:,3:4],
                      'nominalValue': y.value,
                      'estimate': y.estimated})
    # 'priorType': [], 'priorParameter': [], 'hierarchicalOptimization (optional)': []})
    return (a)


y = output_new_format
output_transformed_format = transform_format(y)


# print(output_transformed_format)

def changing_ID(w):
    for iCount in range(len(w.parameterID)):
        if w.iloc[iCount, 0].startswith('log10('):
            d = w.iloc[iCount, 0].lstrip('log10(')
            w.iloc[iCount, 0] = d.rstrip(')')
        else:
            w.iloc[iCount, 0] = w.iloc[iCount, 0]
    return (w)


def changing_Name(w):
    for iCount in range(len(w.parameterID)):
        if w.iloc[iCount, 1].startswith('log10('):
            d = w.iloc[iCount, 1].lstrip('log10(')
            w.iloc[iCount, 1] = d.rstrip(')')
        else:
            w.iloc[iCount, 1] = w.iloc[iCount, 1]
    return (w)


def changing_Scale(w):
    for iCount in range(len(w.parameterID)):
        a = w.iloc[iCount, 2]
        b = np.asarray(['lin', 'log10'])  # create array with 'lin' and 'log10'
        w.iloc[iCount, 2] = b[a]
    return (w)


def changing_Estimate(w):
    for iCount in range(len(w.parameterID)):
        if w.iloc[iCount, 6].startswith('yes'):
            d = w.iloc[iCount, 6].lstrip('yes')
            w.iloc[iCount, 6] = d + '1'
        else:
            d = w.iloc[iCount, 6].lstrip('fixed')
            w.iloc[iCount, 6] = d + '0'
    return (w)


def changing_All(w):
    w1 = changing_ID(w)
    w2 = changing_Name(w1)
    w3 = changing_Scale(w2)
    w4 = changing_Estimate(w3)
    return (w4)

w = output_transformed_format
final_table = changing_All(w)
print(final_table)


#Save created file in same ordner as general info file
final_table.to_csv(path_or_buf= os.path.join(folder,'parameters_%s_gen.tsv' % basename), sep='\t')
