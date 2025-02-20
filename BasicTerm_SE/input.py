import os
import pandas as pd
from cashflower import ModelPointSet

# Paths
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
model_point_table_path = os.path.join(PROJECT_ROOT, "input_csv", "model_point_table.csv")
disc_rate_ann_path = os.path.join(PROJECT_ROOT, "input_csv", "disc_rate_ann.csv")
mort_table_path = os.path.join(PROJECT_ROOT, "input_csv", "mort_table.csv")
premium_table_path = os.path.join(PROJECT_ROOT, "input_csv", "premium_table.csv")

model_point = ModelPointSet(data=pd.read_csv(model_point_table_path, nrows=1))

assumption = {
    "disc_rate_ann": pd.read_csv(disc_rate_ann_path, index_col="year"),
    "mort_table": pd.read_csv(mort_table_path, index_col="Age"),
    "premium_table": pd.read_csv(premium_table_path),
    "loading_prem": 0.5,
    "expense_acq": 300,
    "expense_maint": 60,
    "inflation_rate": 0.01,
}
