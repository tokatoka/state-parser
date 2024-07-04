#!/usr/bin/python3
import os
import multiprocessing
import config

MAX_TIME = 300
FUZZER = "./ossfuzz"
RESULT_DIR_TEMPLATE = os.path.join(config.RESULTS_ROOT, "{}/sqlite3/queue_power\,desyscall\,multi_machine/ossfuzz/{}/")
STATE_PARSER = "../state_parser"
print(f"fuzzer is {FUZZER}")
trials = ["t0", "t1", "t2", "t3", "t4"]
mms = ["mm", "no_mm"]

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

def process_task(mm, trial, t, task_id):
    task_dir = f"./task_{task_id}"
    os.makedirs(task_dir, exist_ok= True)

    os.system(f"cp {STATE_PARSER} {task_dir}/state_parser")
    os.system(f"cp {FUZZER} {task_dir}/{FUZZER}")

    workdir = os.path.join(task_dir, "workdir")
    os.makedirs(workdir, exist_ok=True)

    RESULT_DIR = RESULT_DIR_TEMPLATE.format(mm, trial)
    print(f"Processing {RESULT_DIR} in {task_dir}")

    os.system(f"cd {task_dir} && {STATE_PARSER} -t {t} -w ./workdir -s {RESULT_DIR}")
    os.system(f"cd {task_dir} && {RESULT_DIR_TEMPLATE} --cores {task_id % multiprocessing.cpu_count()} > tmp.txt; tail -n 10 tmp.txt > log.txt")

    log_file = os.path.join(task_dir, "log.txt")
    name = mm + trial + str(t)
    result = parse(log_file)

    with open(os.path.join(task_dir, "result.txt"), 'w') as f:
        f.write(name + "\n")
        f.write(str(result))

os.system("rm -rf task_*")

tasks = [(mm, trial, t, i) for i, (mm, trial, t) in enumerate([(mm, trial, t) for mm in mms for trial in trials for t in range(0, MAX_TIME + 1, 30)])]
res = dict()
with multiprocessing.Pool() as pool:
    results = pool.starmap(process_task, tasks)

