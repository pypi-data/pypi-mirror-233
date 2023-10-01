#!/usr/bin/env python

import os
from typing import Union
from subprocess import PIPE, run

class CompletedProcess():
    def __init__(self, returncode: int, output: str, errors: str):
        self.returncode = returncode
        self.stdout = output
        self.stderr = errors
        return None

def execute_cli_sync(command: str, env_vars=os.environ.copy()) -> CompletedProcess:
    try:
        result = run(command, stdout=PIPE, stderr=PIPE, universal_newlines=True, shell=True, env=env_vars)
    except Exception as e:
        return CompletedProcess(1, '', f'cli execution exception: {e}')
    
    return CompletedProcess(result.returncode, result.stdout, result.stderr)