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
    # One model_point
    proj.point_id = 1
    horizon = [*range(720)]
    result = pd.DataFrame({
        "t": [t for t in horizon],
        "inv_return_mth": [proj.inv_return_mth(t) for t in horizon],
        "premiums": [proj.premiums(t) for t in horizon],
        "inv_income": [proj.inv_income(t) for t in horizon],
        "claims": [proj.claims(t) for t in horizon],
        "expenses": [proj.expenses(t) for t in horizon],
        "commissions": [proj.commissions(t) for t in horizon],
        "av_change": [proj.av_change(t) for t in horizon],
        "pv_expenses": [proj.pv_expenses() for t in horizon],
        "pv_net_cf": [proj.pv_net_cf() for t in horizon],
    })
else:
    # Full portfolio
    print("Start =",  time.strftime("%H:%M:%S", time.localtime()))
    beg = time.time()

    N = 10_000
    pv_net_cf = [None for _ in range(N)]
    for i in range(1, N+1):
        # Full portfolio
        proj.point_id = i
        pv_net_cf[i-1] = proj.pv_net_cf()
        if i % 100 == 0:
            print("i =", i)

    result = pd.DataFrame(pv_net_cf, columns=["pv_net_cf"])

    print("End =",  time.strftime("%H:%M:%S", time.localtime()))
    fin = time.time()
    print("Elapsed seconds =", fin - beg)

result.to_csv(f"output/{timestamp}_output_{MODEL}_{APPROACH}.csv", index=False)
