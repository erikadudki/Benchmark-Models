import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

DataFilePath = "https://raw.githubusercontent.com/LoosC/Benchmark-Models/" \
               "hackathon/hackathon_contributions_new_data_format/" \
               "Isensee_JCB2018/measurementData_Isensee_JCB2018.tsv"

ConditionFilePath = "https://raw.githubusercontent.com/LoosC/" \
                    "Benchmark-Models/hackathon/hackathon_contributions_" \
                    "new_data_format/Isensee_JCB2018/" \
                    "experimentalCondition_Isensee_JCB2018.tsv"

VisualizationFilePath = "/home/simon/Benchmark-Models/hackathon_contributions"\
                        "_new_data_format/Isensee_JCB2018/visualizationSpecific"\
                        "ation_Isensee_JCB2018.tsv"

# import measurement data
measurement_data= pd.DataFrame.from_csv(
        DataFilePath, sep="\t", index_col=None)

# import experimental condition
experimental_condition= pd.DataFrame.from_csv(
        ConditionFilePath, sep="\t", index_col=None)

# import visualization specification
visualization_specification = pd.DataFrame.from_csv(
        VisualizationFilePath, sep="\t", index_col=None)

# Set Colormap
cmap = ['#8c510a','#bf812d','#dfc27d','#f6e8c3','#c7eae5','#80cdc1','#35978f','#01665e']


# get unique plotIDs
plotIds, plotInd=np.unique(visualization_specification.plotId, return_index=True)
print(plotIds)
print(plotInd)

for i_plotId, var_plotId in enumerate(plotIds):
    print(i_plotId)
    print(var_plotId)
    ind_plot = visualization_specification['plotId']==var_plotId
    print(visualization_specification[ind_plot])
    for i in visualization_specification[ind_plot].index.values:
        # get datasetID and independent variable of first entry of plot1
        datasetId=visualization_specification.datasetId[i]
        indepVar=visualization_specification.independentVariable[i]

        # define index to reduce measurement_data to data linked to datasetId
        ind_dataset = measurement_data['datasetId'] == datasetId
        print(measurement_data[ind_dataset])

        # Case seperation indepParameter custom, time or condition
        if indepVar not in ['time', "condition"]:
            print(datasetId)
            print(indepVar)

            # gather simulationConditionIds belonging to datasetId
            conditionIds=np.unique(measurement_data[ind_dataset].simulationConditionId)
            print(conditionIds)

            # extract conditions (plot input) from condition file
            ind_cond=experimental_condition['conditionId'].isin(conditionIds)
            conditions=experimental_condition[ind_cond][indepVar]
            print(conditions)

            # create empty dataframe for means and SDs
            ms = pd.DataFrame(columns = ['mean', 'sd'], index=conditionIds)
            print(ms)

            # group measurement values for each conditionId
            for ID in conditionIds:
                meas=measurement_data['simulationConditionId']==ID
                print(ID)
                print(measurement_data[meas].measurement)
                print(np.mean(measurement_data[meas].measurement))
                print(np.std(measurement_data[meas].measurement))
                ms.at[ID,'mean']= np.mean(measurement_data[meas].measurement)
                ms.at[ID,'sd']= np.std(measurement_data[meas].measurement)

            print(ms)

            plt.errorbar(conditions, ms['mean'], ms['sd'], linestyle='-', marker='.',
                         color=cmap[min(7,i-plotInd[i_plotId])],
                         label=visualization_specification[ind_plot].legendEntry[i]
                         )
            plt.legend()
        elif indepVar=='time':
            plt.plot()
    plt.xlabel(visualization_specification.independentVariableName[i_plotId])
    plt.show()