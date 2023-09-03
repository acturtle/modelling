import modelx as mx
import datetime
import time
import pandas as pd

# User settings
APPROACH = 2
MODEL = "CashValue_SE"

proj = mx.read_model(MODEL).Projection
pd.set_option('display.precision', 8)
timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")

if APPROACH == 1:
    # One policy
    proj.point_id = 1
    horizon = [*range(720)]
    result = pd.DataFrame({
        "t": [t for t in horizon],
    })
else:
    # Full portfolio
    print("Start =",  time.strftime("%H:%M:%S", time.localtime()))
    beg = time.time()

    N = 4
    pv_net_cf = [None for _ in range(N)]
    for i in range(1, N+1):
        # Full portfolio
        proj.point_id = i
        pv_net_cf[i-1] = proj.pv_net_cf()
        if i % 1_000 == 0:
            print("i =", i)

    result = pd.DataFrame(pv_net_cf, columns=["pv_net_cf"])

    print("End =",  time.strftime("%H:%M:%S", time.localtime()))
    fin = time.time()
    print("Elapsed seconds =", fin - beg)

result.to_csv(f"output/{timestamp}_output_{MODEL}_{APPROACH}.csv", index=False)
