#!/bin/bash
python3 -m cProfile main_module.py | tee  cProfile_results.txt
