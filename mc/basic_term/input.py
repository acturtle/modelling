import pandas as pd
from cashflower import Runplan, ModelPointSet


runplan = Runplan(data=pd.DataFrame({"version": [1]}))

main = ModelPointSet(data=pd.read_csv("./input/model_point_table.csv"))

assumption = dict()
assumption["mort_table"] = pd.read_csv("./input/mort_table.csv", index_col="Age")
assumption["disc_rate_ann"] = pd.read_csv("./input/disc_rate_ann.csv", index_col="year")
assumption["inflation_rate"] = 0.01
assumption["expense_acq"] = 300
assumption["expense_maint"] = 60
assumption["loading_prem"] = 0.5
