#!/bin/sh
# Repair tasks. One kernel at a time; each line boots one kernel under the door's own physics.
set -x
python3 gen_repair.py w2-2x2-haiku-a 2,3
python3 gen_repair.py w2-2x2-sonnet-a 2,4
python3 gen_repair.py w2-2x2-haiku-b 3
python3 gen_repair.py w4-3x2-fable-a 2
python3 gen_repair.py w4-3x2-fable-b 3
python3 gen_repair.py w4-3x2-opus-a 3
python3 gen_repair.py w4-3x2-opus-b 4
python3 gen_repair.py w4-3x2-sonnet-a 2
python3 gen_repair.py w4-3x2-haiku-a 3
python3 gen_repair.py w1-fable-a 2,3
python3 gen_repair.py w3-opus-d 3
python3 gen_repair.py w8-3x3-chg-b-opus 2
python3 gen_repair.py w5-3x3p-fable-a 4
python3 gen_repair.py w4-4x4-opus-e 2,3
python3 gen_repair.py w2-4x4-fable-a 3
