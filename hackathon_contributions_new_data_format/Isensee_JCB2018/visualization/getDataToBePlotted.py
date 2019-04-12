import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

def getDataToBePlotted(visualization_specification, measurement_data, condition_ids, i, clmn_name_unique):

    '''
    group the data, which should be plotted and save it in dataframe called 'ms'

    Parameters:
    ----------

    visualization_specification: pandas data frame contains defined data format (visualization file)
    measurement_data: panda data frame contains defined data format (measurement file)
    conditionIds: array containing all unique condition IDs which should be plotted in one figure (can be found in
                    measurementData file, column simulationConditionId)
    i: current index (row number) of row which should be plotted in visualizationSpecification file
    clmn_name_unique: the name of the column in visualization file, which entries should be unique (depends on condition
                        in column independentVariableName)

    Return:
    ----------

    ms: panda data frame containing the data which should be plotted (Mean and Std)
    '''


    # create empty dataframe for means and SDs
    ms = pd.DataFrame(columns=['mean', 'sd', 'sem','repl'], index=condition_ids)

    # if visualization_specification.independentVariable[i] == 'time':
    for var_cond_id in condition_ids:
        ind_meas = ((measurement_data[clmn_name_unique] == var_cond_id) &
                    (measurement_data['datasetId'] == visualization_specification.datasetId[i]))

        ms.at[var_cond_id, 'mean'] = measurement_data[ind_meas].measurement.mean()
        ms.at[var_cond_id, 'sd'] = np.std(measurement_data[ind_meas].measurement)
        ms.at[var_cond_id, 'sem'] = np.std(measurement_data[ind_meas].measurement) / np.sqrt(
            len(measurement_data[ind_meas].measurement))  # Standard Error of Mean
        ms.at[var_cond_id, 'repl'] = measurement_data[ind_meas].measurement


    return ms
