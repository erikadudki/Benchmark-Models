#!/usr/bin/env python3
"""Update models from SBML observables to separate observables table"""

from petab import *
from petab.migrations import sbml_observables_to_table


def update(model_name: str) -> None:
    """Update model"""
    model_dir = f'{model_name}/'
    yaml_file = f'{model_name}/{model_name}.yaml'
    yaml_config = load_yaml(yaml_file)

    if is_composite_problem(yaml_config):
        print(f"SKIPPING {model_name}: Cannot handle PEtab problems with "
              "multiple models yet")
        return

    problem = Problem.from_yaml(yaml_file)
    sbml_observables_to_table(problem)

    # save updated files
    p = yaml_config['problems'][0]
    for field in [SBML_FILES, CONDITION_FILES, MEASUREMENT_FILES,
                  VISUALIZATION_FILES]:
        if field in p and not len(p[field]) <= 1:
            raise NotImplementedError(f"Cannot handle multiple {field}")

    problem.to_files(
        sbml_file=model_dir + p[SBML_FILES][0],
        # condition_file=model_dir + p[CONDITION_FILES][0],
        measurement_file=model_dir + p[MEASUREMENT_FILES][0],
        # parameter_file=model_dir + yaml_config[PARAMETER_FILE]
        observable_file=model_dir + f"observables_{model_name}.tsv",
    )
    # if VISUALIZATION_FILES in p and len(p[VISUALIZATION_FILES]):
    #    write_visualization_df(problem.visualization_df,
    #                           model_dir + p[VISUALIZATION_FILES][0])


def main():
    model_list = os.scandir()
    model_list = sorted(f.name for f in model_list if f.is_dir())

    model_list.remove('Casaletto_PNAS2019') # no yaml
    model_list.remove('Merkle_PCB2016') # no yaml

    for benchmark_model in model_list:
        print('# ', benchmark_model)
        try:
            update(benchmark_model)
        except RuntimeError as e:
            print(e)

        print('='*100)
        # break


if __name__ == '__main__':
    main()
