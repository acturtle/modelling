from cashflower import variable
from input import assumption, main
from settings import settings


@variable()
def age(t):
    return main.get("age_at_entry") + duration(t)


@variable()
def sum_assured():
    return main.get("sum_assured")


@variable()
def claims(t):
    return main.get("sum_assured") * pols_death(t)


@variable()
def commissions(t):
    return premiums(t) if duration(t) == 0 else 0


@variable()
def discount_ann(t):
    if t > 0 and duration(t-1) == duration(t):
        return discount_ann(t-1)
    return assumption["disc_rate_ann"].loc[duration(t)]["zero_spot"]


@variable()
def discount(t):
    return (1 + discount_ann(t))**(-t/12)


@variable()
def duration(t):
    return t//12


@variable()
def expenses(t):
    maint = pols_if(t) * assumption["expense_maint"]/12 * inflation_factor(t)

    if t == 0:
        return assumption["expense_acq"] + maint
    else:
        return maint


@variable()
def inflation_factor(t):
    return (1 + assumption["inflation_rate"])**(t/12)


@variable()
def lapse_rate(t):
    return max(0.1 - 0.02 * duration(t), 0.02)


@variable()
def mort_rate(t):
    if t > 0 and age(t-1) == age(t) and duration(t-1) == duration(t):
        return mort_rate(t-1)
    return assumption["mort_table"].loc[age(t)][min(duration(t), 5)]


@variable()
def mort_rate_mth(t):
    return 1 - (1-mort_rate(t))**(1/12)


@variable()
def net_cf(t):
    return premiums(t) - claims(t) - expenses(t) - commissions(t)


@variable()
def net_premium_pp():
    return pv_claims(0) / pv_pols_if(0)


@variable()
def pols_death(t):
    return pols_if(t) * mort_rate_mth(t)


@variable()
def pols_if(t):
    if t == 0:
        return 1
    elif t > main.get("policy_term") * 12:
        return 0
    else:
        return pols_if(t-1) - pols_lapse(t-1) - pols_death(t-1) - pols_maturity(t)


@variable()
def pols_lapse(t):
    return (pols_if(t) - pols_death(t)) * (1-(1 - lapse_rate(t))**(1/12))


@variable()
def pols_maturity(t):
    if t == main.get("policy_term") * 12:
        return pols_if(t-1) - pols_lapse(t-1) - pols_death(t-1)
    else:
        return 0


@variable()
def premium_pp():
    return round((1 + assumption["loading_prem"]) * net_premium_pp(), 2)


@variable()
def premiums(t):
    return premium_pp() * pols_if(t)


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
