#!/usr/bin/python3
import os
import config

FUZZER = "./ossfuzz"
RESULT_DIR_TEMPLATE = os.path.join(config.RESULTS_ROOT, "{}/sqlite3/queue_power\,desyscall\,multi_machine/ossfuzz/{}/")

config.run(FUZZER, RESULT_DIR_TEMPLATE)

