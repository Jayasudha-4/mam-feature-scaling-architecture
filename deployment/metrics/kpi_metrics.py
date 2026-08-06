import time

def compute_kpis(start_time, end_time, read_ops, write_ops):
    duration = end_time - start_time
    return {
        "RT": read_ops / duration,
        "WT": write_ops / duration,
        "QL": duration * 1000
    }
