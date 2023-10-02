from argparse import ArgumentParser
from pathlib import Path

from lkmeans.examples.experiment import run_experiment
from lkmeans.examples.experiment_data import get_experiment_data

parser = ArgumentParser()

parser.add_argument(
    '--path',
    type=Path,
    default=Path('experiments'),
    help='Path to save results'
)

parser.add_argument(
    '--num-clusters',
    type=int,
    default=2
)


def main():
    args = parser.parse_args()
    experiments_path = args.path

    minkowski_parameter = [0.2, 0.6, 1, 1.5, 2, 3, 5]
    T_parameter = [0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]
    repeats = 100
    n_points = [100, 500, 1000]

    dimension = 20
    n_clusters, prob, mu_list, cov_matrices = get_experiment_data(
        num_clusters=args.num_clusters, dimension=dimension)

    for points in n_points:
        experiment_name = f'Clusters:{n_clusters}, points:{points}'
        output_path = experiments_path / f'exp_{args.num_clusters}_points_{points}'

        run_experiment(
            n_clusters=n_clusters,
            distance_parameters=T_parameter,
            minkowski_parameters=minkowski_parameter,
            repeats=repeats,
            n_points=points,
            cov_matrices=cov_matrices,
            prob=prob,
            mu_list=mu_list,
            experiment_name=experiment_name,
            output_path=output_path
        )


if __name__ == '__main__':
    main()
