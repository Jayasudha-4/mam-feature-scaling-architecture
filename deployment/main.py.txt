from workflows.awf1_binary import run_awf1
from workflows.awf2_multiclass import run_awf2
from config.proposed_model_config import PROPOSED_MODEL_CONFIG

def main():
    graph = run_awf1("CBIS-DDSM", PROPOSED_MODEL_CONFIG)
    graph = run_awf2(graph, ["MIAS", "VinDr-Mammo"], PROPOSED_MODEL_CONFIG)

if __name__ == "__main__":
    main()
