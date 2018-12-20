import numpy as np
import pandas as pd

filepath = 'C:\\Users\\phili\\Benchmark-Models\\hackathon_contributions_new_data_format\\Boehm_JProteomeRes2014\\General_info.xlsx'

def new_format(filepath):
    old_format = pd.read_excel(filepath, sheet_name="Parameters")
    return(old_format)
output_new_format = new_format(filepath)
print(output_new_format)

def transform_format(y):
    a = pd.DataFrame({'parameterID': y.parameter,       #no brackets around y.---
                    'parameterName': y.parameter,
                   'parameterScale': y.loc[:,'analysis at log-scale'],
                   'lowerBound': y.loc[:,'lower boundary'],       #not correct with nor without brackets
                   'upperBound': y.loc[:,'upper boundary'],                       #y.values[:,3:4],
                   'nominalValue': y.value,
                   'estimate': y.estimated})
                   #'priorType': [], 'priorParameter': [], 'hierarchicalOptimization (optional)': []})
    return(a)

y = output_new_format
output_transformed_format = transform_format(y)
print(output_transformed_format)

def changing_stuff(w):
    if w.parameterID.startswith('log10('):
        d = w.parameterID.lstrip('log10(')
        e = d.rtsrip(')')
        print(e)
    else:
        e = w.parameterID
        print(e)

    return(e)

w = output_transformed_format
last_step = changing_stuff(w)
print(last_step)

np.vectorize

# NOTIZEN:

#if pd.DataFrame.startswith('log10('):
 #   pd.DataFrame[len('log10('):]
#if pd.DataFrame.endswith(')'):
 #   pd.DataFrame[len(')'):]

#if x.startswith('log10('):
 #   y = x.lstrip('log10(')
  #  z = y.rstrip(')')
   # print(z)
#else:
 #   print('No')
