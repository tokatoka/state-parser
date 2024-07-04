#!/usr/bin/python3
import os
import config

FUZZER = "./string_to_double_fuzzer"
RESULT_DIR_TEMPLATE = os.path.join(config.RESULTS_ROOT, "{}/double-conversion/queue_power\,desyscall\,multi_machine/string_to_double_fuzzer/{}/")

config.run(FUZZER, RESULT_DIR_TEMPLATE)

