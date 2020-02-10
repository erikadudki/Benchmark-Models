# -*- coding: utf-8 -*-

import os
import numpy as np
import pandas as pd


# INPUT - PLEASE INSERT FITTING PATH AND NAME
# TO GENERAL INFO INTO FUNCTION 'generateParameterSheet'
def generateParameterSheet(filepath, filename):
    # Example: filepath = r"C:\Benchmark-Models\hackathon_contributions_new_data_format\Boehm_JProteomeRes2014" # noqa: E501
    #          filename = r"General_info.xlsx"
    whole_filepath = filepath + '/' + filename  # Whole string
    modelname = filepath.split('\\')[-1]  # Last part 'filepath' == model name

    # Transformation of old excel sheet into new one
    output_new_format = new_excel_sheet(whole_filepath)

    output_transformed_format = transform_format(output_new_format)

    # Table with all input - printed in Python Console
    final_excel_sheet = final_form(output_transformed_format)
    print(final_excel_sheet)
    final_excel_sheet.to_csv(
        path_or_buf=os.path.join(
            filepath,      # Save created file as '.tsv'
            'parameters_%s.tsv' % modelname
        ), sep='\t',
        index=False
    )     # in same folder as 'General_info' file


# Read in old excel sheet 'General_info'
def new_excel_sheet(filepath):
    old_excel_sheet = pd.read_excel(filepath, sheet_name="Parameters")
    return (old_excel_sheet)


# Change headlines of all columns and
# fill with selected input of 'old_excel_sheet'
def transform_format(y):
    a = pd.DataFrame({'parameterID': y.parameter,
                      'parameterName': y.parameter,
                      'parameterScale': y.loc[:, 'analysis at log-scale'],
                      'lowerBound': y.loc[:, 'lower boundary'],
                      'upperBound': y.loc[:, 'upper boundary'],
                      'nominalValue': y.value,
                      'estimate': y.estimated})
    return (a)


# Change column 'parameterID' from old form into new form
def changing_ID(w):
    for iCount in range(len(w.parameterID)):
        if w.iloc[iCount, 0].startswith('log10('):
            d = w.iloc[iCount, 0].lstrip('log10(')
            w.iloc[iCount, 0] = d.rstrip(')')
        else:
            w.iloc[iCount, 0] = w.iloc[iCount, 0]
    return (w)


# Change column 'parameterName' from old form into new form
def changing_Name(w):
    for iCount in range(len(w.parameterID)):
        if w.iloc[iCount, 1].startswith('log10('):
            d = w.iloc[iCount, 1].lstrip('log10(')
            w.iloc[iCount, 1] = d.rstrip(')')
        else:
            w.iloc[iCount, 1] = w.iloc[iCount, 1]
    return (w)


# Change column 'parameterScale' from old form into new form
def changing_Scale(w):
    for iCount in range(len(w.parameterID)):
        a = w.iloc[iCount, 2]
        b = np.asarray(['lin', 'log10'])  # create array with 'lin' and 'log10'
        w.iloc[iCount, 2] = b[a]
    return (w)


# Change column 'estimate' from old form into new form
def changing_Estimate(w):
    for iCount in range(len(w.parameterID)):
        if w.iloc[iCount, 6].startswith('yes'):
            d = w.iloc[iCount, 6].lstrip('yes')
            w.iloc[iCount, 6] = d + '1'
        else:
            d = w.iloc[iCount, 6].lstrip('fixed')
            w.iloc[iCount, 6] = d + '0'
    return (w)


# All previous changes are connected in 'final_form'
def final_form(w):
    w1 = changing_ID(w)
    w2 = changing_Name(w1)
    w3 = changing_Scale(w2)
    w4 = changing_Estimate(w3)
    return (w4)
