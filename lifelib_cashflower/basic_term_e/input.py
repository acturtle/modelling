import pandas as pd
from cashflower import Runplan, ModelPointSet


runplan = Runplan(data=pd.DataFrame({"version": [1]}))

main = ModelPointSet(data=pd.read_csv("input/model_point_table.csv"))

assumption = {
    "disc_rate_ann": pd.read_csv("input/disc_rate_ann.csv", index_col="year"),
    "mort_table": pd.read_csv("input/mort_table.csv", index_col="Age"),
    "premium_table": pd.read_csv("input/premium_table.csv", index_col=("age_at_entry", "policy_term")),
    "loading_prem": 0.5,
    "expense_acq": 300,
    "expense_maint": 60,
    "inflation_rate": 0.01,
}