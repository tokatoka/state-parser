#!/usr/bin/python3
import os
import config

FUZZER = "./stbi_read_fuzzer"
RESULT_DIR_TEMPLATE = os.path.join(config.RESULTS_ROOT, "{}/stb/queue_power\,desyscall\,multi_machine/stbi_read_fuzzer/{}/")

config.run(FUZZER, RESULT_DIR_TEMPLATE)

