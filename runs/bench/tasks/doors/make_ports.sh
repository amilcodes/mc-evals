#!/bin/sh
# Port and hidden-rule tasks (run after gen_matrix.py). One kernel at a time.
set -x
CHG='{"repeater_unit": 3, "observer_delay": 3}'
python3 gen_port.py w1-fable-a "$CHG" --retime-search
python3 gen_port.py w8-3x3-chg-b-opus '{}' --retime-search
python3 gen_port.py w5-3x3p-fable-a '{}' --retime-search
python3 gen_port.py w8-3x3-chg-c-opus '{}' --retime-search
python3 gen_port.py w4-3x2-fable-a '{"observer_pulse": 3}' --retime-search
python3 gen_port.py w4-3x2-opus-b '{"observer_pulse": 3}' --retime-search
python3 gen_port.py w3-opus-d '{"observer_pulse": 1}' --retime-search
python3 gen_port.py w4-4x4-opus-e "$CHG" --retime-search
python3 gen_port.py w2-4x4-fable-a "$CHG" --retime-search
python3 gen_port.py w4-3x2-opus-a '{"observer_pulse": 3}' --hidden --retime-search
python3 gen_port.py w1-fable-a '{"observer_delay": 3}' --hidden --retime-search
python3 gen_port.py w4-4x4-opus-e '{"repeater_unit": 3}' --hidden --retime-search
