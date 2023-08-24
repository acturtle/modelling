from cashflower import variable
from input import assumption, main


@variable()
def age(t):
    return main.get("age_at_entry") + duration(t)


@variable()
def claims(t):
    return main.get("sum_assured") * pols_death(t)


@variable()
def commissions(t):
    return premiums(t) if duration(t) == 0 else 0

def discount(t):
    rate = assumption["disc_rate_ann"].loc[duration(t)]["zero_spot"]
    return (1 + rate)**(-t/12)

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
    return assumption["mort_table"].loc[age(t)][min(duration(t), 5)]


@variable()
def mort_rate_mth(t):
    return 1 - (1-mort_rate(t))**(1/12)


@variable()
def net_cf(t):
    return premiums(t) - claims(t) - expenses(t) - commissions(t)
#
#
# @variable()
# def net_premium_pp():
#     return pv_claims() / pv_pols_if()
#
#
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


# TODO shoould be time-dependent
@variable()
def pv_claims():
    return sum(claims(t) * discount(t) for t in range(settings["T_MAX_CALCULATION"]))


# @variable()
# def pv_commissions():
#     return sum(list(commissions(t) for t in range(proj_len())) * disc_factors()[:proj_len()])
#
#
# @variable()
# def pv_expenses():
#     return sum(list(expenses(t) for t in range(proj_len())) * disc_factors()[:proj_len()])
#
#
# @variable()
# def pv_net_cf():
#     return pv_premiums() - pv_claims() - pv_expenses() - pv_commissions()
#
#
# @variable()
# def pv_pols_if():
#     return sum(list(pols_if(t) for t in range(proj_len())) * disc_factors()[:proj_len()])
#
#
# @variable()
# def pv_premiums():
#     return sum(list(premiums(t) for t in range(proj_len())) * disc_factors()[:proj_len()])
