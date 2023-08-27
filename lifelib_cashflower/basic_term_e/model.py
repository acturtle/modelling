import math
from cashflower import variable
from input import assumption, main
from settings import settings


@variable()
def proj_len():
    return max(12 * main.get("policy_term") - main.get("duration_mth") + 1, 0)


@variable()
def age(t):
    return main.get("age_at_entry") + duration(t)


@variable()
def claims(t):
    if t >= proj_len():
        return 0

    return main.get("sum_assured") * pols_death(t)


@variable()
def commissions(t):
    if duration(t) == 0:
        return premiums(t)
    else:
        return 0


@variable()
def discount_ann(t):
    if t > 0 and (t-1)//12 == t//12:
        return discount_ann(t-1)
    return assumption["disc_rate_ann"].loc[t//12]["zero_spot"]


@variable()
def discount(t):
    return (1 + discount_ann(t))**(-t/12)


@variable()
def duration(t):
    return duration_mth(t) // 12


@variable()
def duration_mth(t):
    if t == 0:
        return main.get("duration_mth")
    else:
        return duration_mth(t-1) + 1


@variable()
def expenses(t):
    if t >= proj_len():
        return 0

    return (assumption["expense_acq"] * pols_new_biz(t) + pols_if_at_bef_decr(t) * assumption["expense_maint"]/12
            * inflation_factor(t))


@variable()
def inflation_factor(t):
    return (1 + assumption["inflation_rate"])**(t/12)


@variable()
def lapse_rate(t):
    return max(0.1 - 0.02 * duration(t), 0.02)


@variable()
def mort_rate(t):
    if t > 0 and age(t-1) == age(t) and (duration(t-1) == duration(t) or duration(t) > 5):
        return mort_rate(t-1)
    age_t = max(min(age(t), 120), 18)
    return assumption["mort_table"].loc[age_t][min(duration(t), 5)]


@variable()
def mort_rate_mth(t):
    return 1-(1-mort_rate(t))**(1/12)


@variable()
def net_cf(t):
    return premiums(t) - claims(t) - expenses(t) - commissions(t)


@variable()
def net_premium_pp():
    if math.isclose(pv_pols_if(0), 0):
        return 0
    return pv_claims(0) / pv_pols_if(0)


@variable()
def pols_death(t):
    return pols_if_at_bef_decr(t) * mort_rate_mth(t)


@variable()
def pols_if(t):
    return pols_if_at_bef_mat(t)


@variable()
def pols_if_at_bef_mat(t):
    if t == 0:
        return pols_if_init()
    else:
        return pols_if_at_bef_mat(t-1) - pols_lapse(t-1) - pols_death(t-1)


@variable()
def pols_if_at_bef_decr(t):
    return pols_if_at_bef_nb(t) + pols_new_biz(t)


@variable()
def pols_if_at_bef_nb(t):
    return pols_if_at_bef_mat(t) - pols_maturity(t)


@variable()
def pols_if_init():
    if duration_mth(0) > 0:
        return main.get("policy_count")
    else:
        return 0


@variable()
def pols_lapse(t):
    return (pols_if_at_bef_decr(t) - pols_death(t)) * (1-(1 - lapse_rate(t))**(1/12))


@variable()
def pols_maturity(t):
    if duration_mth(t) == main.get("policy_term") * 12:
        return pols_if_at_bef_mat(t)
    else:
        return 0


@variable()
def pols_new_biz(t):
    if duration_mth(t) == 0:
        return main.get("policy_count")
    else:
        return 0


@variable()
def premium_pp():
    premium_rate = assumption["premium_table"].loc[(main.get("age_at_entry"), main.get("policy_term"))]["premium_rate"]
    return round(main.get("sum_assured") * premium_rate, 2)


@variable()
def premiums(t):
    if t >= proj_len():
        return 0

    return premium_pp() * pols_if_at_bef_decr(t)


@variable()
def pv_claims(t):
    if t == settings["T_MAX_CALCULATION"]:
        return claims(t) * discount(t)
    return claims(t) * discount(t) + pv_claims(t+1)


@variable()
def pv_commissions(t):
    if t == settings["T_MAX_CALCULATION"]:
        return commissions(t) * discount(t)
    return commissions(t) * discount(t) + pv_commissions(t+1)


@variable()
def pv_expenses(t):
    if t == settings["T_MAX_CALCULATION"]:
        return expenses(t) * discount(t)
    return expenses(t) * discount(t) + pv_expenses(t+1)


@variable()
def pv_premiums(t):
    if t == settings["T_MAX_CALCULATION"]:
        return premiums(t) * discount(t)
    return premiums(t) * discount(t) + pv_premiums(t+1)


@variable()
def pv_pols_if(t):
    if t == settings["T_MAX_CALCULATION"]:
        return pols_if(t) * discount(t)
    return pols_if(t) * discount(t) + pv_pols_if(t+1)


@variable()
def pv_net_cf(t):
    return pv_premiums(t) - pv_claims(t) - pv_expenses(t) - pv_commissions(t)
