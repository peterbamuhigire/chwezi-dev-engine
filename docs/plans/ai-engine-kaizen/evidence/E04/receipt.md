# AC-E04 release diagnostics

Run the public example with python -B skills/languages/python-ml-predictive/examples/release-diagnostics/diagnose.py and compare its output to trace.json. Run python -B -m unittest discover -s tests -p test_kaizen_release_diagnostics.py -v for the control cases.

The initial draft reported skew even after the serving vector was set equal to the training vector. The repaired check derives its classification from the vectors. The tests also restore the reference input lengths and verify that the shift alarm clears. The frozen shift with delayed labels defers accuracy. The release gate rejects the candidate for vocabulary order and adapter-base mismatches. Interruption before index promotion leaves all G1 components intact. The same promotion ID yields one completed restoration across retry; a different payload under that ID raises a conflict.

All values and timings are synthetic. The simulation models atomic publication in memory. Process-crash durability, production rollout and real quality or latency are unassessed.
