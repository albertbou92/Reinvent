#!/usr/bin/env python3

import os
import pandas as pd
from pytorchrl.agent.env import load_baselines_results


def process_pytorch_results(path):

    # Read monitor files
    data = load_baselines_results(os.path.join(path, "monitor_logs/train"))

    # Rank monitor files by reward
    data = data.sort_values("r", ascending=False)

    # Filter data
    data = data[data["molecule"] != "invalid_smile"]
    data = data[data["molecule"].duplicated() == False]

    return data


def process_libinvent_results(path):

    # Read monitor files
    scaffold_memory_path = os.path.join(path, 'results/scaffold_memory.csv')
    data = pd.read_csv(scaffold_memory_path)

    # Filter data
    data = data[data["SMILES"].duplicated() == False]

    return data


def generate_comparison(pytorchrl_path, libinvent_path):

    py_data = process_pytorch_results(pytorchrl_path)
    lib_data = process_libinvent_results(libinvent_path)

    import ipdb; ipdb.set_trace()


if __name__ == "__main__":

    generate_comparison(
        pytorchrl_path="/tmp/genchem_ppo_3/",
        libinvent_path="/home/abou/REINVENT_RL_QSAR_demo",
    )
