import pandas as pd
from cashflower import Runplan, ModelPointSet


runplan = Runplan(data=pd.DataFrame({"version": [1]}))

main = ModelPointSet(data=pd.read_csv("input/model_point_samples.csv"))

assumption = dict()
