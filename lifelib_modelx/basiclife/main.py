import modelx as mx
import datetime
import time
import pandas as pd

# User settings
APPROACH = 2
MODEL = "BasicTerm_SE"

proj = mx.read_model(MODEL).Projection
pd.set_option('display.precision', 8)
timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")

if APPROACH == 1:
    # One policy
    proj.point_id = 581
    horizon = [*range(720)]
    result = pd.DataFrame({
        "t": [t for t in horizon],
        "duration_mth": [proj.duration_mth(t) for t in horizon],
        "inflation_factor": [proj.inflation_factor(t) for t in horizon],
        "premium_pp": [proj.premium_pp() for t in horizon],
        "duration": [proj.duration(t) for t in horizon],
        "pols_new_biz": [proj.pols_new_biz(t) for t in horizon],
        "pols_if_init": [proj.pols_if_init() for t in horizon],
        "age": [proj.age(t) for t in horizon],
        "lapse_rate": [proj.lapse_rate(t) for t in horizon],
        "discount": [proj.disc_factors()[t] for t in range(len(proj.disc_factors()))] + [0 for _ in range(len(horizon)-len(proj.disc_factors()))],
        "mort_rate_mth": [proj.mort_rate_mth(t) for t in horizon],
        "mort_rate": [proj.mort_rate(t) for t in horizon],
        "pols_death": [proj.pols_death(t) for t in horizon],
        "pols_if_at_bef_decr": [proj.pols_if_at(t, "BEF_DECR") for t in horizon],
        "pols_if_at_bef_mat": [proj.pols_if_at(t, "BEF_MAT") for t in horizon],
        "pols_if_at_bef_nb": [proj.pols_if_at(t, "BEF_NB") for t in horizon],
        "pols_lapse": [proj.pols_lapse(t) for t in horizon],
        "pols_maturity": [proj.pols_maturity(t) for t in horizon],
        "claims": [proj.claims(t) for t in horizon],
        "premiums": [proj.premiums(t) for t in horizon],
        "expenses": [proj.expenses(t) for t in horizon],
        "pols_if": [proj.pols_if(t) for t in horizon],
        "commissions": [proj.commissions(t) for t in horizon],
        "pv_claims": [proj.pv_claims() for t in horizon],
        "pv_pols_if": [proj.pv_pols_if() for t in horizon],
        "pv_expenses": [proj.pv_expenses() for t in horizon],
        "pv_premiums": [proj.pv_premiums() for t in horizon],
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
        if i % 1_000 == 0:
            print("i =", i)

    result = pd.DataFrame(pv_net_cf, columns=["pv_net_cf"])

    print("End =",  time.strftime("%H:%M:%S", time.localtime()))
    fin = time.time()
    print("Elapsed seconds =", fin - beg)

result.to_csv(f"output/{timestamp}_output_{MODEL}_{APPROACH}.csv", index=False)
