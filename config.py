#!/usr/bin/python3

import os
import multiprocessing
import config
import sys

if True:
    # exp machine setup
    RESULTS_ROOT = "/home/rmalmain/2024-07-02_104552.771254"
else:
    # toka setup
    RESULTS_ROOT = "/home/rmalmain/2024-07-02_104552.771254"

MAX_TIME = 300
STATE_PARSER = "../state_parser"

def parse(log_file):
    with open(log_file) as f:
        all_lines = f.readlines()
        for line in all_lines:
            if "Client Heartbeat" in line:
                perc = line.split("edges: ")[1].split("%")[0]
                print(perc)
                ret = float(perc)
                return ret
    return 0

def process_task(fuzzer, result_dir_template, mm, trial, t, task_id):
    task_dir = f"./task_{task_id}"
    os.makedirs(task_dir, exist_ok= True)

    os.system(f"cp {STATE_PARSER} {task_dir}/state_parser")
    os.system(f"cp {fuzzer} {task_dir}/{fuzzer}")

    workdir = os.path.join(task_dir, "workdir")
    os.makedirs(workdir, exist_ok=True)

    RESULT_DIR = result_dir_template.format(mm, trial)
    print(f"Processing {RESULT_DIR} in {task_dir}")

    os.system(f"cd {task_dir} && {STATE_PARSER} -t {t} -w ./workdir -s {RESULT_DIR}")
    os.system(f"cd {task_dir} && {fuzzer} --cores {task_id % multiprocessing.cpu_count()} > tmp.txt; tail -n 10 tmp.txt > log.txt")

    log_file = os.path.join(task_dir, "log.txt")
    name = mm + trial + str(t)
    result = parse(log_file)

    return {
        f"{mm}_{trial}_{t}": result
    }

def run(fuzzer, result_dir_template):
    print(f"fuzzer is {fuzzer}")
    trials = ["t0", "t1", "t2", "t3", "t4"]

    if len(sys.argv) > 1 and sys.argv[1] == 'mm':
        mms = ["mm"]
    else:
        mms = ["no_mm"]

    os.system("rm -rf task_*")

    tasks = [(fuzzer, result_dir_template, mm, trial, t, i) for i, (mm, trial, t) in enumerate([(mm, trial, t) for mm in mms for trial in trials for t in range(60, MAX_TIME + 1, 60)])]
    res = dict()
    with multiprocessing.Pool() as pool:
        for result in pool.starmap(process_task, tasks):
            res.update(result)

    print(res)

    with open(f"result_{mms[0]}.txt", 'w') as f:
        f.write(str(res))
