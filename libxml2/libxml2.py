#!/usr/bin/python3
import os
import config

FUZZER = "./xml"
RESULT_DIR_TEMPLATE = os.path.join(config.RESULTS_ROOT, "{}/libxml2/queue_power\,desyscall\,multi_machine/xml/{}/")

config.run(FUZZER, RESULT_DIR_TEMPLATE)

