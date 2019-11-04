# Description
Process manager to keep your minecraft server healthy and running.

# How to run

Requires setuptools which can be installed from pip.

```
python -m pip install -U pip
pip install setuptools
```

Requires git which can installed from

```
https://git-scm.com/book/en/v2/Getting-Started-Installing-Git
```

Now build and install the distribution.

```
git clone https://github.com/Cameron-Alberts/MinecraftProcessManager
python setup.py build
python setup.py install
start_process_manager --hostname localhost ^
                      --port 25565 ^
                      --working-directory "C:\rl_craft" ^
                      --server-jar server.jar ^
                      --jvm-args "-Dfml.readTimeout=300 -Xmx6g -Xms6g -XX:+UseParallelGC" ^
                      --health-check-strategy simple_latency_strategy ^
                      --health-check-strategy-args "{\"health_checks_queue_size\": 6}" ^
                      --health-check-delay 5 ^
                      --time-to-sleep-after-start 60 ^
                      --ping-socket-connection-timeout 1 ^
                      --gui
```

For additional help with commands.

```
start_process_manager --help
```

# System requirements

## Python version
Python >= 3.0

## Operating Systems
Only tested on Windows

# Change log
11/3/2019 added setuptools for distribution
10/31/2019 initial commit