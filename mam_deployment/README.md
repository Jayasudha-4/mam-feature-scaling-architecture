# MAM Deployment

Modular Adaptive Mining (MAM) base implementation: Data Lakehouse (DLH)
-> Central Graph (CG) -> Analytical Workflow 1 (binary classification, CG -> CG')
-> Analytical Workflow 2 (BI-RADS multi-class classification, CG' -> Final Central
Graph FG), with min-cut based subgraph mining, incremental graph evolution, and
computation (KPI) evaluation.

## Folder structure

```
mam_deployment/
├── config/                     # All configuration files
│   ├── base_config.py          # Project-wide base settings (logging, lakehouse paths)
│   ├── proposed_model_config.py# Central Graph + AWF-1 / AWF-2 feature & task config
│   ├── model_config.py         # CatBoost / XGBoost ensemble hyper-parameters
│   └── experiment_config.py    # Environments (E1/E2/E3), KPI settings, reference results
├── data_lakehouse/
│   └── dlh.py                  # DLH: loads CSVs
├── graph/
│   ├── central_graph.py        # Central Graph (nodes=features, edges=associations)
│   └── subgraph_miner.py       # Min-cut based subgraph mining / expansion
├── preprocessing/
│   └── metadata_pipeline.py    # AWF-1 preprocessing + AWF-2 harmonization pipelines
├── models/
│   └── ensemble_classifier.py  # CatBoost + XGBoost soft-voting ensemble
├── workflows/
│   ├── awf1_binary.py          # AWF-1: CBIS-DDSM binary classification (CG -> CG')
│   └── awf2_multiclass.py      # AWF-2: cross-dataset BI-RADS classification (CG' -> FG)
├── metrics/
│   └── kpi_evaluator.py        # RT / WT / NT / QL computation evaluation
├── main.py                     # Entry point wiring the full pipeline
└── requirements.txt
```

## Setup

```bash
pip install -r requirements.txt
```

## Run

```bash
python main.py
```

## Results 

| Workflow | Task                     | Accuracy |
|----------|--------------------------|----------|
| AWF-1    | Binary (Benign/Malignant)| 0.97     |
| AWF-2    | BI-RADS (multi-class)    | 0.95     |

Computation KPIs (Read/Write Throughput, Node Transition, Query Latency) are
measured live on the running Central Graph across three simulated
environments (E1: 8vCores/32GB, E2: 16vCores/64GB, E3: 32vCores/128GB) and
printed alongside the paper's reference results in `main.py`'s output.
