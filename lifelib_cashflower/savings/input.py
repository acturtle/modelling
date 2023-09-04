import pandas as pd
from cashflower import Runplan, ModelPointSet, CSVReader


runplan = Runplan(data=pd.DataFrame({
    "version": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
    "scen_id": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
}))

model_point_table = pd.read_csv("input/model_point_samples.csv")
product_spec_table = pd.read_csv("input/product_spec_table.csv")
main_data = pd.concat([model_point_table, product_spec_table], axis=1, join="inner")
main = ModelPointSet(data=main_data)

assumption = {
    "disc_rate_ann": pd.read_csv("input/disc_rate_ann.csv", index_col="year"),
    "mort_table": pd.read_csv("input/mort_table.csv", index_col="Age"),
    "surr_charge_table": pd.read_csv("input/surr_charge_table.csv", index_col="duration"),
    "std_norm_rand": CSVReader("input/std_norm_rand.csv", num_row_label_cols=2),
    "expense_acq": 5000,
    "expense_maint": 500,
    "inflation_rate": 0.01,
}
