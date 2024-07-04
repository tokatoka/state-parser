#!/usr/bin/python3
import os
import config

FUZZER = "./hevc_dec_fuzzer"
RESULT_DIR_TEMPLATE = os.path.join(config.RESULTS_ROOT, "{}/libhevc/queue_power\,desyscall\,multi_machine/hevc_dec_fuzzer/{}/")

config.run(FUZZER, RESULT_DIR_TEMPLATE)
