#!/usr/bin/env python3
"""
Wrapper to move repository files into the new structure created by the organize branch.
This script does not run in CI here; it's used to record the planned moves and to apply
safe, linear moves via the GitHub API (already executed by the assistant where possible).
"""
moves = [
    # scripts
    ("ceremony_hrv_experiment.py", "scripts/ceremony_hrv_experiment.py"),
    ("disaster_alert_network.py", "scripts/disaster_alert_network.py"),
    ("duvida_pre_ignicao.py", "scripts/duvida_pre_ignicao.py"),
    ("workspace_demo.py", "scripts/workspace_demo.py"),
    ("real_hrv_experiment.py", "scripts/real_hrv_experiment.py"),
    # data
    ("fantasia_Y1_RR_intervals.txt", "data/raw/fantasia_Y1_RR_intervals.txt"),
    ("fantasia_Y2_RR_intervals.txt", "data/raw/fantasia_Y2_RR_intervals.txt"),
    ("fantasia_Y3_RR_intervals.txt", "data/raw/fantasia_Y3_RR_intervals.txt"),
    ("fantasia_Y1_RR_intervals-1.txt", "data/raw/fantasia_Y1_RR_intervals-1.txt"),
    ("fantasia_O1_RR_intervals.txt", "data/raw/fantasia_O1_RR_intervals.txt"),
    ("fantasia_O2_RR_intervals.txt", "data/raw/fantasia_O2_RR_intervals.txt"),
    ("fantasia_Y1_RR_intervals-2.txt", "data/raw/fantasia_Y1_RR_intervals-2.txt"),
]
# other planned moves: PDFs -> manuscripts, images -> figures
print("Planned moves:")
for a, b in moves:
    print(f"{a} -> {b}")
