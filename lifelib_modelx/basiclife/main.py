import modelx as mx
import time
import pandas as pd

proj = mx.read_model(r"BasicTerm_S").Projection
pd.set_option('display.precision', 8)

APPROACH = 1

if APPROACH == 1:
    # One policy
    proj.point_id = 1

    horizon = [*range(720)]

    result = pd.DataFrame({
        "t": [t for t in horizon],
        "age": [proj.age(t) for t in horizon],
        "pols_death": [proj.pols_death(t) for t in horizon],
        "mort_rate": [proj.mort_rate(t) for t in horizon],
        "mort_rate_mth": [proj.mort_rate_mth(t) for t in horizon],
        "claim_pp": [proj.claim_pp(t) for t in horizon],
        "claims": [proj.claims(t) for t in horizon],
        "pv_claims": [proj.pv_claims() for t in horizon],
        "discount": list(proj.disc_factors()) + [0 for _ in range(720 - len(proj.disc_factors()))]
    })
    # print(result)
    result.to_csv("output/basic_term_output_one_policy.csv")


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

    df = pd.DataFrame(pv_net_cf, columns=["pv_net_cf"])
    df.to_csv("basic_term_output.csv")

    print("End =",  time.strftime("%H:%M:%S", time.localtime()))
    fin = time.time()
    print("Elapsed seconds =", fin - beg)
