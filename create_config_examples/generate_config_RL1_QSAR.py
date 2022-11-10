# load dependencies
import os
import re
import json
import tempfile

########################################################################################################################

# --------- change these path variables as required
reinvent_dir = os.path.expanduser("/home/abou/Reinvent/")
output_dir = os.path.expanduser("/home/abou/REINVENT_RL_QSAR_demo")
ipynb_path = os.getcwd()

# if required, generate a folder to store the results
try:
    os.mkdir(output_dir)
except FileExistsError:
    pass

########################################################################################################################

# initialize the dictionary
configuration = {
    "version": 3,
    "model_type": "lib_invent",
    "run_type": "reinforcement_learning"
}

########################################################################################################################

configuration["logging"] = {
    "wandb_key": "",
    "agent_name": "original_code",
    "experiment_name": "benchmarking_libinvent",
    "sender": "",  # only relevant if "recipient" is set to "remote"
    "recipient": "local",  # either to local logging or use a remote REST-interface
    "logging_path": output_dir,  # load this folder in tensorboard
    "result_folder": output_dir,  # output directory for results
    "job_name": "Reinforcement learning QSAR demo",  # set an arbitrary job name for identification
    "job_id": "n/a"  # only relevant if "recipient" is set to "remote"
}

########################################################################################################################

# add the "parameters" block
configuration["parameters"] = {}
configuration["parameters"] = {
    "actor": os.path.join(ipynb_path, "models/library_design.prior"),
    "critic": os.path.join(ipynb_path, "models/library_design.prior"),
    "scaffolds": ["[*:0]N1CCN(CC1)CCCCN[*:1]"],
    "n_steps": 100000,
    "learning_rate": 0.0001,
    "batch_size": 128,
    "randomize_scaffolds": True,
    "learning_strategy": {
        "name": "dap",
        "parameters": {
        "sigma": 120
        }
    }
}

########################################################################################################################

configuration["parameters"]["scoring_strategy"] = {
    "name": "lib_invent"  # Do not change
}

########################################################################################################################

configuration["parameters"]["scoring_strategy"]["diversity_filter"] =  {
    "name": "NoFilterWithPenalty",
}

########################################################################################################################

configuration["parameters"]["scoring_strategy"]["reaction_filter"] =  {
    "type":"selective",
    "reactions":[] # no reactions are imposed.
}

########################################################################################################################

scoring_function = {
    "name": "custom_sum",
    "parallel": False,  # Do not change

    "parameters": [
        {
            "component_type": "predictive_property",
            "name": "DRD2",
            "weight": 1,
            "specific_parameters": {
                "model_path": os.path.join(ipynb_path, "../models/scoring/drd2.pkl"),
                "scikit": "classification",
                "descriptor_type": "ecfp",
                "size": 2048,
                "radius": 3,
                "transformation": {
                    "transformation_type": "no_transformation"
                }
            }
        },
        {
            "component_type": "custom_alerts",
            "name": "Custom alerts",
            "weight": 1,
            "specific_parameters": {
                "smiles": [
                    "[*;r8]",
                    "[*;r9]",
                    "[*;r10]",
                    "[*;r11]",
                    "[*;r12]",
                    "[*;r13]",
                    "[*;r14]",
                    "[*;r15]",
                    "[*;r16]",
                    "[*;r17]",
                    "[#8][#8]",
                    "[#6;+]",
                    "[#16][#16]",
                    "[#7;!n][S;!$(S(=O)=O)]",
                    "[#7;!n][#7;!n]",
                    "C#C",
                    "C(=[O,S])[O,S]",
                    "[#7;!n][C;!$(C(=[O,N])[N,O])][#16;!s]",
                    "[#7;!n][C;!$(C(=[O,N])[N,O])][#7;!n]",
                    "[#7;!n][C;!$(C(=[O,N])[N,O])][#8;!o]",
                    "[#8;!o][C;!$(C(=[O,N])[N,O])][#16;!s]",
                    "[#8;!o][C;!$(C(=[O,N])[N,O])][#8;!o]",
                    "[#16;!s][C;!$(C(=[O,N])[N,O])][#16;!s]"
                ]
            }
        }]
}

configuration["parameters"]["scoring_strategy"]["scoring_function"] = scoring_function

########################################################################################################################

# write out the configuration to disc
configuration_JSON_path = os.path.join(output_dir, "RL_QSAR_input.json")
with open(configuration_JSON_path, 'w') as f:
    json.dump(configuration, f, indent=4, sort_keys=True)

########################################################################################################################
