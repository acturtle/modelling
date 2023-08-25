import modelx as mx
import time
import pandas as pd

proj = mx.read_model(r"BasicTerm_S").Projection

# 1st policy
proj.point_id = 1
print(proj.pv_net_cf())  # 910.92066093366

# Full portfolio
print("Start =",  time.strftime("%H:%M:%S", time.localtime()))

N = 10_000
pv_net_cf = [None for _ in range(N)]
for i in range(1, N+1):
    proj.point_id = i
    pv_net_cf[i-1] = proj.pv_net_cf()
    if i % 1_000 == 0:
        print("i =", i)

df = pd.DataFrame(pv_net_cf, columns=["pv_net_cf"])
df.to_csv("basic_term_output.csv")

print("End =",  time.strftime("%H:%M:%S", time.localtime()))
