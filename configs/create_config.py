"""From https://github.com/MolecularAI/ReinventCommunity/blob/master/notebooks/Lib-INVENT_RL1_QSAR.ipynb."""

import os
import json

# Define output directory
output_dir = os.path.expanduser(os.path.dirname(__file__))

# initialize the dictionary
configuration = {
    "version": 3,
    "model_type": "lib_invent",
    "run_type": "reinforcement_learning"
}

# add block to specify whether to run locally or not and
# where to store the results and logging
configuration["logging"] = {
    "sender": "",  # only relevant if "recipient" is set to "remote"
    "recipient": "local",  # either to local logging or use a remote REST-interface
    "logging_path": os.path.join(output_dir, "progress.log"),  # load this folder in tensorboard
    "result_folder": os.path.join(output_dir, "results"),  # output directory for results
    "job_name": "Reinforcement learning QSAR demo",  # set an arbitrary job name for identification
    "job_id": "n/a"  # only relevant if "recipient" is set to "remote"
}

# add the "parameters" block
configuration["parameters"] = {}

configuration["parameters"] = {
    "actor": os.path.join(os.path.expanduser(os.path.dirname(__file__)), "models/agents_prior/decorative.prior"),
    "critic": os.path.join(os.path.expanduser(os.path.dirname(__file__)), "models/agents_prior/decorative.prior"),
    "scaffolds": ["[*:0]N1CCN(CC1)CCCCN[*:1]"],
    "n_steps": 100,
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

configuration["parameters"]["scoring_strategy"] = {
    "name": "lib_invent"  # Do not change
}

configuration["parameters"]["scoring_strategy"]["diversity_filter"] = {
    "name": "NoFilterWithPenalty",
}

configuration["parameters"]["scoring_strategy"]["reaction_filter"] = {
    "type": "selective",
    "reactions": []  # no reactions are imposed.
}

scoring_function = {
    "name": "custom_sum",
    "parallel": False,  # Do not change

    "parameters": [
        {
            "component_type": "predictive_property",
            "name": "DRD2",
            "weight": 1,
            "specific_parameters": {
                "model_path": os.path.join(os.path.expanduser(os.path.dirname(__file__)), "models/scoring/drd2.pkl"),
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

# write out the configuration to disc
configuration_JSON_path = os.path.join(output_dir, "RL_QSAR_input.json")
with open(configuration_JSON_path, 'w') as f:
    json.dump(configuration, f, indent=4, sort_keys=True)
