from cashflower import variable
from input import main
from settings import settings


@variable()
def age(t):
    return main.get("age_at_entry") + duration(t)


@variable()
def av_at_bef_mat(t):
    return av_pp_at(t, "BEF_PREM") * pols_if_at(t, "BEF_MAT")


@variable()
def av_at_bef_nb(t):
    return av_pp_at(t, "BEF_PREM") * pols_if_at(t, "BEF_NB")


@variable()
def av_at_bef_fee(t):
    return av_pp_at(t, "BEF_FEE") * pols_if_at(t, "BEF_DECR")


@variable()
def av_change(t):
    if t == settings["T_MAX_CALCULATION"]:
        return 0
    return av_at_bef_mat(t+1) - av_at_bef_mat(t)


@variable()
def av_pp_at_bef_prem(t):
    if t == 0:
        return main.get("av_pp_init")
    else:
        return av_pp_at_bef_inv(t-1) + inv_income_pp(t-1)


@variable()
def av_pp_at_bef_fee(t):
    return av_pp_at_bef_prem(t) + prem_to_av_pp(t)


@variable()
def av_pp_at_bef_inv(t):
    return av_pp_at_bef_fee(t) - maint_fee_pp(t) - coi_pp(t)


@variable()
def av_pp_at_mid_mth(t):
    return av_pp_at_bef_inv(t) + 0.5 * inv_income_pp(t)


@variable()
def claim_pp_death(t):
    return max(sum_assured(), av_pp_at_mid_mth(t))


@variable()
def claim_pp_lapse(t):
    return av_pp_at_mid_mth(t)


@variable()
def claim_pp_maturity(t):
    return av_pp_at_bef_prem(t)


@variable()
def claims_death(t):
    return claim_pp_death(t) * pols_death(t)


@variable()
def claims_lapse(t):
    return claims_from_av(t, "LAPSE") - surr_charge(t)


@variable()
def claims_maturity(t):
    return claims_from_av(t, "MATURITY")


@variable()
def claims(t):
    return claims_death(t) + claims_lapse(t) + claims_maturity(t)
