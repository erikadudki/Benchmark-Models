# Documentation
## This Documentation explains the data format used for the benchmark collection


## Condition data

A tab-separated value text file with condition specific parameters. Row names are 
condition names as referenced in the measurement table below. Column names are 
parameter names as given in the SBML model. These parameters will override any
parameter values specified in the model.

```
conditionId conditionName constantName1 constantName2 ...
conditionId1  conditionName1  1 2 ...
conditionId2  conditionName2  3 4 ...
... ... ... ... ...
```

All parameters listed here are expected to have been turned into fixed 
parameters during AMICI model generation.


## Measurements

A text file (tab separated values) containing all measurements to be used for
model training.

Expected to have the following named columns in any (but preferably this) order:

- `observableId` [STRING, NOT NULL, REFERENCES(sbml.observableID)]
  
  Observable name matching the ID of the respective parameter in the SBML
    model (`observable_...`) 

- `preequilibrationConditionId` [STRING, REFERENCES(conditionsTable.conditionID)]
 
  The reference condition to be used for preequilibration. E.g. for drug 
  treatments the model would be preequilibrated with the no-drug condition.
  Empty for no preequlibration.
  
  **NOTE**: Should be left empty for now until preequilibration is fully 
  supported . Will probably be separated into `conditionReference` and 
  `conditionPreequilibration`. The former will provide information on data 
  normalization, the latter will be used to toggle preequilibration.
  
- `simulationConditionId` [STRING, NOT NULL, REFERENCES(conditionsTable.conditionID)]
  
  Condition name as provided in the condition data table, specifying the 
    fixed parameters used for the simulation 
  
- `measurement` [NUMERIC, NOT NULL]

  The measured value.
  
- `time` [STRING, NOT NULL]

  Time point of the measurement in seconds, float or `Inf` for steady-state 
  measurements. `Inf` will be replaced by a large $t$ during import.
  
- `observableParameters` [STRING]

  List of observable parameters separated by semicolon.
  
  This field allows introducing condition-specific versions of the parameters
  defined in the model. Parameters listed here must be named
  `${modelParameterName}_${suffix}`. `${modelParameterName}` must be a parameter 
  name present in the model, `${suffix}` is any suffix not containing "_". 
  This extends the optimization parameter vector without
  changing the model itself. This name can occur in multiple lines to model e.g.
  batch-specific or cell line-specific parameters. The corresponding index 
  mapping of parameters to simulation parameters is written to the file, and 
  will be performed before each individual simulation.
  
  Scaling parameters are expected to start with `scaling_`.
  
  *NOTE*: Currently only a single scaling parameter can be 
  used for hierarchical optimization. The one occurring first will be selected.
  A sigma parameter may be provided in addition.
  
  Offset parameters are expected to start with `offset_`.
  
  *NOTE*: Currently only a single offset parameter can be 
  used for hierarchical optimization. The one occurring first will be selected.
  A sigma parameter may be provided in addition.
  
- `noiseParameters` [STRING]

  The measurement variance or `NaN` if the corresponding sigma is a model 
  parameter.

- `observableTransformation` [STRING]

  Transformation of the observable. `lin`, `log` or `log10`.



## Parameter information

A tab-separated value text file containing information on the parameters. One row per parameter

```
parameterId parameterName parameterScale lowerBound  upperBound nominalValue estimated priorType priorParameters hierarchicalOptimization(optional)
...
```
- parameterId has to be identical to the parameter ids specified in the SBML model.
- parameterName will be used for plotting etc. Can be chosen freely.
- parameterScale: scale of parameter. lin/log/log10 etc. The parameters and boundaries in the following fields are expected to be given in this scale.
- lowerBound: lower bound of the parameter used for optimization.
- upperBound: upper bound of the parameter used for optimization.
- nominalValue: Best values found by optimization or the value used for simulation for fixed parameters(see estimated).
- estimated: 1 or 0, depending on, if the parameter is estimated (1) or set to a fixed value(0).
- priorType: Type of prior. Leave empty, if no priors. Normal/ Laplace etc.
- priorParameters: parameters for prior.
- hierarchicalOptimization: 1 if parameter is optimized using hierarchical optimization approach. 0 otherwise.

## SBML files

In the SBML file for the model the observables are indicated by prefix `observable_` followed by the observableId as in the corresponding column of the measurement sheet. In the definition (=assignment rule) of the observable, `observableParameters` (see measurements) can be included, e.g., 
```
observable_pErk = observableParameter1 + observableParameter2*pErk 
```
where `observableParameter1` would be an offset, and `observableParameter2` a scaling parameters. 
For each observable, the noise model needs to be defined in `sigma_observableId`. In the assignment rule for this, the `noiseParameters` (see measurements) are used in the same way as the `observableParameters`. A noise model which accounts for relative and absolute contributions could, e.g., be defined as
```
sigma_pErk = noiseParameter1 + noiseParameter2*pErk 
```
with `noiseParameter1` denoting the absolute and `noiseParameter2` the relative contribution.
