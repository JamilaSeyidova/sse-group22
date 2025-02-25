import argparse
import os, sys, datetime

from src.experiment import get_experiments, Experiment
from src.runner import run


def cli():
    experiments = get_experiments()
    parser = argparse.ArgumentParser(
        description="Execute EnergiBridge experiments.",
        add_help=False,
        prog="EnergiBridge")
    parser.add_argument("--iterations",
                        help="Number of interations to run.",
                        dest="iterations",
                        type=int,
                        nargs='?',
                        default=30)
    parser.add_argument("--sleep",
                        help="sleep time between runs.",
                        dest="sleep",
                        type=int,
                        nargs='?',
                        default=30)
    parser.add_argument("-i", "--interval",
                        help="Interval between measurements.",
                        dest="interval",
                        type=int,
                        nargs='?',
                        default=200)
    parser.add_argument("--warmup",
                        help="Warmup time.",
                        dest="warmup",
                        type=int,
                        nargs='?',
                        default=20)
    parser.add_argument("-o", "--output",
                        help="Output directory.",
                        dest="output",
                        type=str,
                        nargs='?',
                        default="results")
    parser.add_argument("-e", "--experiments",
                        help="List of experiments to run.",
                        dest="experiments",
                        choices=["all"] + [e.name for e in experiments],
                        type=str,
                        nargs='*',
                        default=["all"])
    return parser.parse_args()

def main():
    args = cli()
    experiments = []
    if "all" in args.experiments:
        experiments = get_experiments()
    else:
        for experiment in args.experiments:
            e = Experiment(experiment)
            if e.enabled:
                experiments.append(e)

    if not os.path.isabs(args.output):
        args.output = os.path.join(os.getcwd(), args.output, sys.platform)
    args.output = os.path.join(args.output, datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S"))
    run(experiments, args, 'videos')


if __name__ == '__main__':
    main()