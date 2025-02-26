import argparse
import os, sys, datetime
import time

from pyuac import main_requires_admin

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
                        default=60)
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
                        default=0)
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

def wait_five_minutes():
    wait_duration = 300  # 5 minutes in seconds
    end_time = datetime.datetime.now().timestamp() + wait_duration
    while True:
        remaining = int(end_time - datetime.datetime.now().timestamp())
        if remaining <= 0:
            break
        print(f"Waiting: {remaining} seconds remaining...", end="\r")
        time.sleep(1)
    print()  # Move to next line after countdown is complete.

@main_requires_admin
def main():
    args = cli()
    #experiments = []
    #if "all" in args.experiments:
    #    experiments = get_experiments()
    #else:
    #    for experiment in args.experiments:
    #        e = Experiment(experiment)
    #        if e.enabled:
    #            experiments.append(e)
#
    #if not os.path.isabs(args.output):
    #    args.output = os.path.join(os.getcwd(), args.output, sys.platform)
    #args.output = os.path.join(args.output, datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S"))
    #run(experiments, args)4

    groups = [
        # Group 1: Decoding 480p (H.264 & H.265)
        ["decode_480p_h264", "decode_480p_h265"],
        # Group 2: Decoding 720p (H.264 & H.265)
        ["decode_720p_h264", "decode_720p_h265"],
        # Group 3: Decoding 1080p (H.264 & H.265)
        ["decode_1080p_h264", "decode_1080p_h265"],
        # Group 4: Decoding 2kp (H.264 & H.265)
        ["decode_2kp_h264", "decode_2kp_h265"]
    ]
    
    # Process each group in order.
    for index, group in enumerate(groups, start=1):
        print(f"Starting Group {index}...")
        experiments = []
        for name in group:
            exp = Experiment(name)  # This loads experiments/<name>/config.yml
            if exp.enabled:
                experiments.append(exp)
            else:
                print(f"Experiment {name} is not enabled; skipping.")
        if experiments:    

            experiment_type_dir = os.path.join(args.output, group[0].split('_')[1])
            if not os.path.exists(experiment_type_dir):
                os.makedirs(experiment_type_dir)
            
            # Create timestamped directory inside the experiment type directory
            timestamp_dir = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
            args.output = os.path.join(experiment_type_dir, timestamp_dir)
            if not os.path.exists(args.output):
                os.makedirs(args.output)

            run(experiments, args)
        else:
            print(f"No enabled experiments found for Group {index}.")

        
        # If not the last group, wait 5 minutes (300 seconds) before the next group.
        if index < len(groups):
            print("Group completed. Waiting 5 minutes before the next group...")
            wait_five_minutes()

    #if not os.path.isabs(args.output):
    #    args.output = os.path.join(os.getcwd(), args.output, sys.platform)
    #args.output = os.path.join(args.output, datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S"))
    
    print("All experiment groups completed.")


if __name__ == '__main__':
    main()