# Description
Process manager to keep your minecraft server healthy and running.

# Example
python launcher.py --hostname localhost ^
                   --port 25565 ^
                   --working-directory "C:\Users\MyName\rl_craft" ^
                   --server-jar server.jar ^
                   --jvm-args "-Dfml.readTimeout=300 -Xmx6g -Xms6g -XX:+UseParallelGC" ^
                   --health-check-strategy simple_latency_strategy ^
                   --health-check-strategy-args "{\"health_checks_queue_size\": 6}" ^
                   --health-check-delay 5 ^
                   --time-to-sleep-after-start 60 ^
                   --ping-socket-connection-timeout 1 ^
                   --gui

# OS
Only tested on Windows

# Change log
10/31/2019 initial commit