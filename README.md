REINVENT 3.2 - Benchmarking
===========================

To run first create a conf.yaml file that can be executed by the repo. To run a script that creates an example configuration execute:

```
$ python create_config_examples/create_config_RL1_QSAR.py
```

Then you just execute the input.py script and point it to the configuration file

```
$ python python input.py --run_config ~/REINVENT_RL_QSAR_demo/RL_QSAR_input.json
```