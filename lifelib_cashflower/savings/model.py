import math
import numpy as np

from cashflower import discount, variable
from input import assumption, main, runplan
from settings import settings


@variable()
def proj_len():
    return max(12 * policy_term() - duration_mth(0) + 1, 0)


@variable(array=True)
def age():
    return main.get("age_at_entry") + duration()


@variable(array=True)
def av_at_bef_mat():
    return av_pp_at_bef_prem() * pols_if_at_bef_mat()


@variable(array=True)
def av_at_bef_nb():
    return av_pp_at_bef_prem() * pols_if_at_bef_nb()


@variable(array=True)
def av_at_bef_fee():
    return av_pp_at_bef_fee() * pols_if_at_bef_decr()


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


@variable(array=True)
def av_pp_at_mid_mth():
    return av_pp_at_bef_inv() + 0.5 * inv_income_pp()


@variable(array=True)
def claim_pp_death():
    return np.maximum(main.get("sum_assured"), av_pp_at_mid_mth())


@variable(array=True)
def claim_pp_lapse():
    return av_pp_at_mid_mth()


@variable(array=True)
def claim_pp_maturity():
    return av_pp_at_bef_prem()


@variable(array=True)
def claims_death():
    return claim_pp_death() * pols_death()


@variable(array=True)
def claims_lapse():
    return claims_from_av_lapse() - surr_charge()


@variable(array=True)
def claims_maturity():
    return claims_from_av_maturity()


@variable(array=True)
def claims():
    return claims_death() + claims_lapse() + claims_maturity()


@variable(array=True)
def claims_from_av_death():
    return av_pp_at_mid_mth() * pols_death()


@variable(array=True)
def claims_from_av_lapse():
    return av_pp_at_mid_mth() * pols_lapse()


@variable(array=True)
def claims_from_av_maturity():
    return av_pp_at_bef_prem() * pols_maturity()


@variable(array=True)
def claims_over_av():
    return (claim_pp_death() - av_pp_at_mid_mth()) * pols_death()


@variable(array=True)
def coi():
    return coi_pp() * pols_if_at_bef_decr()


@variable(array=True)
def coi_rate():
    return 1.1 * mort_rate_mth()


@variable()
def coi_pp(t):
    return coi_rate(t) * net_amt_at_risk(t)


@variable(array=True)
def commissions():
    return 0.05 * premiums()


@variable()
def yearly_spot_rate(t):
    if t > 0 and (t-1)//12 == t//12:
        return yearly_spot_rate(t - 1)
    return float(assumption["disc_rate_ann"].get_value(str(t // 12), "zero_spot"))


@variable()
def monthly_spot_rate(t):
    return (1+yearly_spot_rate(t))**(1/12)-1


@variable()
def monthly_forward_rate(t):
    if t == 0:
        return 0
    return (1+monthly_spot_rate(t))**t / (1+monthly_spot_rate(t-1))**(t-1) - 1


@variable()
def forward_discount_rate(t):
    return 1/(1+monthly_forward_rate(t))


@variable()
def spot_discount_rate(t):
    return (1 + yearly_spot_rate(t))**(-t / 12)


@variable(array=True)
def duration():
    return duration_mth() // 12


@variable()
def duration_mth(t):
    if t == 0:
        return main.get("duration_mth")
    else:
        return duration_mth(t-1) + 1


@variable(array=True)
def expenses():
    return pols_new_biz() * assumption["expense_acq"] + pols_if_at_bef_decr() * assumption["expense_maint"]/12 * inflation_factor()


@variable()
def inflation_factor(t):
    return (1 + assumption["inflation_rate"])**(t/12)


@variable()
def inv_income(t):
    if t == settings["T_MAX_CALCULATION"]:
        return 0
    return inv_income_pp(t) * pols_if_at_bef_mat(t+1) + 0.5 * inv_income_pp(t) * (pols_death(t) + pols_lapse(t))


@variable()
def inv_income_pp(t):
    return inv_return_mth(t) * av_pp_at_bef_inv(t)


@variable()
def inv_return_mth(t):
    mu = 0.02
    sigma = 0.03
    dt = 1 / 12
    std_norm_rand = float(assumption["std_norm_rand"].get_value((str(runplan.get("scen_id")), str(t)), "std_norm_rand"))
    return math.exp((mu - 0.5 * sigma ** 2) * dt + sigma * dt ** 0.5 * std_norm_rand) - 1


@variable(array=True)
def lapse_rate():
    return np.maximum(0.1 - 0.02 * duration(), 0.02)


@variable(array=True)
def maint_fee():
    return maint_fee_pp() * pols_if_at_bef_decr()


@variable()
def maint_fee_rate():
    return 0.01 / 12


@variable()
def maint_fee_pp(t):
    return maint_fee_rate() * av_pp_at_bef_fee(t)


@variable(array=True)
def margin_expense():
    return main.get("load_prem_rate") * premium_pp() * pols_if_at_bef_decr() + surr_charge() + maint_fee() - commissions() - expenses()


@variable(array=True)
def margin_mortality():
    return coi() - claims_over_av()


@variable()
def mort_rate(t):
    if t > 0 and age(t-1) == age(t) and (duration(t-1) == duration(t) or duration(t) > 5):
        return mort_rate(t-1)
    age_t = str(int(max(min(age(t), 120), 18)))
    duration_t = str(int(max(min(duration(t), 5), 0)))
    return float(assumption["mort_table"].get_value(age_t, duration_t))


@variable()
def mort_rate_mth(t):
    return 1 - (1-mort_rate(t))**(1/12)


@variable()
def net_amt_at_risk(t):
    return max(main.get("sum_assured") - av_pp_at_bef_fee(t), 0)


@variable()
def net_cf(t):
    if t >= proj_len():
        return 0

    return premiums(t) + inv_income(t) - claims(t) - expenses(t) - commissions(t) - av_change(t)


@variable()
def policy_term():
    if main.get("is_wl"):
        return assumption["mort_table_last_age"] - main.get("age_at_entry")
    else:
        return main.get("policy_term")


@variable()
def pols_death(t):
    return pols_if_at_bef_decr(t) * mort_rate_mth(t)


@variable(array=True)
def pols_if():
    return pols_if_at_bef_mat()


@variable()
def pols_if_at_bef_mat(t):
    if t == 0:
        return pols_if_init()
    else:
        return pols_if_at_bef_decr(t-1) - pols_lapse(t-1) - pols_death(t-1)


@variable()
def pols_if_at_bef_nb(t):
    return pols_if_at_bef_mat(t) - pols_maturity(t)


@variable()
def pols_if_at_bef_decr(t):
    return pols_if_at_bef_nb(t) + pols_new_biz(t)


@variable()
def pols_if_init():
    if duration_mth(0) > 0:
        return main.get("policy_count")
    else:
        return 0


@variable()
def pols_lapse(t):
    return (pols_if_at_bef_decr(t) - pols_death(t)) * (1 - (1-lapse_rate(t))**(1/12))


@variable()
def pols_maturity(t):
    if duration_mth(t) == policy_term() * 12:
        return pols_if_at_bef_mat(t)
    else:
        return 0


@variable()
def pols_new_biz(t):
    if duration_mth(t) == 0:
        return main.get("policy_count")
    else:
        return 0


@variable(array=True)
def prem_to_av():
    return prem_to_av_pp() * pols_if_at_bef_decr()


@variable(array=True)
def prem_to_av_pp():
    return (1 - main.get("load_prem_rate")) * premium_pp()


@variable()
def premium_pp(t):
    if main.get("premium_type") == 'SINGLE':
        if duration_mth(t) == 0:
            return main.get("premium_pp")
        else:
            return 0
    elif main.get("premium_type") == 'LEVEL':
        if duration_mth(t) < 12 * policy_term():
            return main.get("premium_pp")
        else:
            return 0


@variable(array=True)
def premiums():
    return premium_pp() * pols_if_at_bef_decr()


@variable(array=True)
def pv_av_change():
    return discount(av_change(), forward_discount_rate())


@variable(array=True)
def pv_claims():
    return discount(claims(), forward_discount_rate())


@variable(array=True)
def pv_commissions():
    return discount(commissions(), forward_discount_rate())


@variable(array=True)
def pv_expenses():
    return discount(expenses(), forward_discount_rate())


@variable(array=True)
def pv_inv_income():
    return discount(inv_income(), forward_discount_rate())


@variable(array=True)
def pv_net_cf():
    return pv_premiums() + pv_inv_income() - pv_claims() - pv_expenses() - pv_commissions() - pv_av_change()


@variable(array=True)
def pv_pols_if():
    return discount(pols_if(), forward_discount_rate())


@variable(array=True)
def pv_premiums():
    return discount(premiums(), forward_discount_rate())


@variable(array=True)
def surr_charge():
    return surr_charge_rate() * av_pp_at_mid_mth() * pols_lapse()


@variable()
def surr_charge_rate(t):
    if main.get("has_surr_charge"):
        if duration(t) > 10:
            return surr_charge_rate(t-1)
        else:
            return float(assumption["surr_charge_table"].get_value(str(int(duration(t))), main.get("surr_charge_id")))
    else:
        return 0
