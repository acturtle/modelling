import pandas as pd
from cashflower import Runplan, ModelPointSet, CSVReader


runplan = Runplan(data=pd.DataFrame({"version": [1]}))

main = ModelPointSet(data=pd.read_csv("input/model_point_table.csv"))

assumption = {
    "disc_rate_ann": CSVReader("input/disc_rate_ann.csv"),
    "mort_table": CSVReader("input/mort_table.csv"),
    "loading_prem": 0.5,
    "expense_acq": 300,
    "expense_maint": 60,
    "inflation_rate": 0.01,
}
