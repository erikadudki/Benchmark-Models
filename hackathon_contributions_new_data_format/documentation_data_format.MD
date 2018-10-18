# Documentation
## This Documentation explains the data format used for the benchmark collection


## Condition data

A tab-separated value text file with condition specific parameters. Column names are 
condition names as referenced in the measurement table below. Row names are 
parameter names as given in the SBML model. These parameters will override any
parameter values specified in the model.

```
conditionID       conditionID1 conditionID2 ...
conditionName       conditionName1  conditionName2  ...
constantName1       1             2        ...
constantName2       3             4        ...
...                ...           ...       ...
```

All parameters listed here are expected to have been turned into fixed 
parameters during AMICI model generation.


## Measurements

A text file (tab separated values) containing all measurements to be used for
model training.

Expected to have the following named columns in any (but preferably this) order:

- `observable` [STRING, NOT NULL, REFERENCES(sbml.observableID)]
  
  Observable name matching the ID of the respective parameter in the SBML
    model (`observable_...`) 

- `conditionRef` [STRING, REFERENCES(conditionsTable.conditionID)]
 
  The reference condition to be used for preequilibration. E.g. for drug 
  treatments the model would be preequilibrated with the no-drug condition.
  Empty for no preequlibration.
  
  **NOTE**: Should be left empty for now until preequilibration is fully 
  supported . Will probably be separated into `conditionReference` and 
  `conditionPreequilibration`. The former will provide information on data 
  normalization, the latter will be used to toggle preequilibration.
  
- `condition` [STRING, NOT NULL, REFERENCES(conditionsTable.conditionID)]
  
  Condition name as provided in the condition data table, specifying the 
    fixed parameters used for the simulation 
  
- `measurement` [NUMERIC, NOT NULL]

  The measured value.
  
- `time` [STRING, NOT NULL]

  Time point of the measurement in seconds, float or `Inf` for steady-state 
  measurements. `Inf` will be replaced by a large $t$ during import.
  
- `scaling` [STRING]

  List of scaling parameters to be used for 
  hierarchical optimization as well as any other condition-specific parameters.
  
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

- `offset` [STRING]

  List of offset parameters to be used for 
  hierarchical optimization as well as any other condition-specific parameters.
  
  This field allows introducing condition-specific versions of the parameters
  defined in the model. Parameters listed here must be named
  `${modelParameterName}_${suffix}`. `${modelParameterName}` must be a parameter 
  name present in the model, `${suffix}` is any suffix not containing "_". 
  This extends the optimization parameter vector without
  changing the model itself. This name can occur in multiple lines to model e.g.
  batch-specific or cell line-specific parameters. The corresponding index 
  mapping of parameters to simulation parameters is written to the file, and 
  will be performed before each individual simulation.
  
  Offset parameters are expected to start with `offset_`.
  
  *NOTE*: Currently only a single offset parameter can be 
  used for hierarchical optimization. The one occurring first will be selected.
  A sigma parameter may be provided in addition.
  
- `sigma` [STRING]

  The measurement variance or `NaN` if the corresponding sigma is a model 
  parameter.
