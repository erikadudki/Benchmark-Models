import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

def getDataToBePlotted(visualization_specification, measurement_data, conditionIds, i):

    '''
    group the data, which should be plotted and save it in dataframe called 'ms'

    Parameters:
    ----------

    visualization_specification: panda data frame contains defined data format (visualization file)
    measurement_data: panda data frame contains defined data format (measurement file)
    conditionIds: array containing all unique condition IDs which should be plotted in one figure (can be found in
                    measurementData file, column simulationConditionId)
    i: current index (row number) of row which should be plotted in visualizationSpecification file

    Return:
    ----------

    ms: panda data frame containing the data which should be plotted (Mean and Std)
    '''

    if visualization_specification.plotTypeData[i] == 'MeanAndSD':
        # create empty dataframe for means and SDs
        ms = pd.DataFrame(columns=['mean', 'sd', 'sem'], index=conditionIds)

        if visualization_specification.independentVariable[i] == 'time':
            for ID in conditionIds:
                ind_meas = ((measurement_data['time'] == ID) &
                            (measurement_data['datasetId'] == visualization_specification.datasetId[i]))

                ms.at[ID, 'mean'] = np.mean(measurement_data[ind_meas].measurement)
                ms.at[ID, 'sd'] = np.std(measurement_data[ind_meas].measurement)
                ms.at[ID, 'sem'] = np.std(measurement_data[ind_meas].measurement) / np.sqrt(
                    len(measurement_data[ind_meas].measurement))  # Standard Error of Mean
        else:
            for ID in conditionIds:
                ind_meas = ((measurement_data['simulationConditionId'] == ID) &
                            (measurement_data['datasetId'] == visualization_specification.datasetId[i]))

                ms.at[ID, 'mean'] = np.mean(measurement_data[ind_meas].measurement)
                ms.at[ID, 'sd'] = np.std(measurement_data[ind_meas].measurement)
                ms.at[ID, 'sem'] = np.std(measurement_data[ind_meas].measurement)/np.sqrt(
                    len(measurement_data[ind_meas].measurement))                             # Standard Error of Mean



    return ms