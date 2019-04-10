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

VisualizationFilePath = "https://raw.githubusercontent.com/LoosC/"\
                        "Benchmark-Models/visualization/hackathon_contributions"\
                        "_new_data_format/Isensee_JCB2018/visualizationSpecific"\
                        "ation_Isensee_JCB2018.tsv"

# import measurement data
measurement_data = pd.DataFrame.from_csv(
        DataFilePath, sep="\t", index_col=None)

# import experimental condition
experimental_condition = pd.DataFrame.from_csv(
        ConditionFilePath, sep="\t", index_col=None)

# import visualization specification
visualization_specification = pd.DataFrame.from_csv(
        VisualizationFilePath, sep="\t", index_col=None)

# Set Colormap
cmap = ['#8c510a','#bf812d','#dfc27d','#f6e8c3','#c7eae5','#80cdc1','#35978f','#01665e']


# get unique plotIDs
plotIds, plotInd = np.unique(visualization_specification.plotId, return_index=True)
#print(plotIds)
#print(plotInd)

for i_plotId, var_plotId in enumerate(plotIds):
    #print(i_plotId)
    #print(var_plotId)
    ind_plot = visualization_specification['plotId'] == var_plotId

    counter_cond = 0        # counter for the condition case, (if independentVariable == 'condition')

    #print(visualization_specification[ind_plot])

    for i in visualization_specification[ind_plot].index.values:
        # get datasetID and independent variable of first entry of plot1
        datasetId = visualization_specification.datasetId[i]
        indepVar = visualization_specification.independentVariable[i]

        # define index to reduce measurement_data to data linked to datasetId
        ind_dataset = measurement_data['datasetId'] == datasetId
        #print(measurement_data[ind_dataset])

        # gather simulationConditionIds belonging to datasetId
        conditionIds = np.unique(measurement_data[ind_dataset].simulationConditionId)
        #print(conditionIds)

        # Case seperation indepParameter custom, time or condition
        if indepVar not in ['time', "condition"]:
            #print(datasetId)
            #print(indepVar)

            # gather simulationConditionIds belonging to datasetId
            #conditionIds = np.unique(measurement_data[ind_dataset].simulationConditionId)
            #print(conditionIds)

            # extract conditions (plot input) from condition file
            ind_cond = experimental_condition['conditionId'].isin(conditionIds)
            conditions = experimental_condition[ind_cond][indepVar]
            #print(conditions)

            # create empty dataframe for means and SDs
            ms = pd.DataFrame(columns = ['mean', 'sd'], index=conditionIds)
            #print(conditionIds)

            # group measurement values for each conditionId
            for ID in conditionIds:
                meas = measurement_data['simulationConditionId'] == ID
                #print(ID)
                #print(measurement_data[meas].measurement)
                #print(np.mean(measurement_data[meas].measurement))
                #print(np.std(measurement_data[meas].measurement))
                ms.at[ID,'mean'] = np.mean(measurement_data[meas].measurement)
                ms.at[ID,'sd'] = np.std(measurement_data[meas].measurement)


            plt.errorbar(conditions, ms['mean'], ms['sd'], linestyle='-', marker='.',
                         color=cmap[min(7,i-plotInd[i_plotId])],
                         label=visualization_specification[ind_plot].legendEntry[i]
                         )
            plt.legend()


        elif indepVar == 'condition':
            # if conditionIds == 'control':
            #     # dont have to go in expCondFile, all Cond are 0
            # else:
            #     ind_expCond = experimental_condition.conditionId == conditionIds
            #     #do smth with information in this file
            # get measurement values for each condId

            # create empty dataframe for means and SDs
            ms_c = pd.DataFrame(columns=['mean', 'sd'], index=conditionIds)

            # group measurement values for each conditionId

            for ID in conditionIds:
                #print(conditionIds)
                if conditionIds == 'control':       # datasetId and conditionIds have to coincide, since there are multiple experiments called 'control'
                    # ind_meas = measurement_data.simulationConditionId[ind_dataset] == ID
                    # meas = measurement_data['simulationConditionId'] == ID
                    ms_c.at[ID, 'mean'] = np.mean(measurement_data.measurement[ind_dataset])        # check datasetId is enough
                    ms_c.at[ID, 'sd'] = np.std(measurement_data.measurement[ind_dataset])
                else:
                    meas = measurement_data['simulationConditionId'] == ID
                    ms_c.at[ID, 'mean'] = np.mean(measurement_data[meas].measurement)
                    ms_c.at[ID, 'sd'] = np.std(measurement_data[meas].measurement)
                    print(ms_c)

            bars = ('a','b','c')
            print(conditionIds)
            x_pos = np.arange(len(bars))

            plt.bar(conditionIds,[x_pos[counter_cond], ms_c['mean']])
            counter_cond = counter_cond + 1
            #plt.xticks(x_pos,bars)
            #plt.legend()

        elif indepVar == 'time':

            # obtain unique observation times
            uni_times = np.unique(measurement_data[ind_dataset].time)
            print(uni_times)

            # create empty dataframe for means and SDs
            ms = pd.DataFrame(columns=['mean', 'sd'], index=uni_times)
            print(ms)

            print(measurement_data[ind_dataset].time)
            # group measurement values for each conditionId
            for var_time in uni_times:
                ind_meas = ((measurement_data['time'] == var_time) &
                            (measurement_data['datasetId']==datasetId))
                print(var_time)
                print(measurement_data[ind_meas].measurement)
                print(np.mean(measurement_data[ind_meas].measurement))
                print(np.std(measurement_data[ind_meas].measurement))
                ms.at[var_time, 'mean'] = np.mean(measurement_data[ind_meas].measurement)
                ms.at[var_time, 'sd'] = np.std(measurement_data[ind_meas].measurement)

            print(ms)

            plt.errorbar(uni_times, ms['mean'], ms['sd'], linestyle='-', marker='.',
                         color=cmap[min(7,i-plotInd[i_plotId])],
                         label=visualization_specification[ind_plot].legendEntry[i]
                         )
            plt.legend()


    plt.xlabel(visualization_specification.independentVariableName[i_plotId])
    plt.show()