from cashflower import variable
from input import assumption, main, runplan
from settings import settings


@variable()
def duration(t):
    return t // 12


@variable()
def mortality_rate_annual(t):
    if t > 0 and duration(t) == duration(t-1):
        return mortality_rate_annual(t-1)

    age = main.get("age_at_entry") + duration(t)
    return assumption["mort_table"].loc[age][min(duration(t), 5)]


@variable()
def mortality_rate_monthly(t):
    return 1 - (1 - mortality_rate_annual(t))**(1/12)


@variable()
def pols_death(t):
    return pols_if(t) * mortality_rate_monthly(t)


@variable()
def pols_if(t):
    if t == 0:
        return 1
    return pols_if(t - 1) - pols_lapse(t - 1) - pols_death(t - 1) - pols_maturity(t)


@variable()
def lapse_rate(t):
    return max(0.1 - 0.02 * duration(t), 0.02)


@variable()
def pols_lapse(t):
    return (pols_if(t) - pols_death(t)) * (1 - (1 - lapse_rate(t))**(1/12))


@variable()
def pols_maturity(t):
    if t == main.get("policy_term") * 12:
        return pols_if(t - 1) - pols_lapse(t - 1) - pols_death(t - 1)
    else:
        return 0


@variable()
def discount(t):
    rate = assumption["disc_rate_ann"].loc[duration(t)]["zero_spot"]
    return (1 + rate)**(-t/12)


@variable()
def claims(t):
    return pols_death(t) * main.get("sum_assured")


@variable()
def inflation_factor(t):
    return (1 + assumption["inflation_rate"])**(t/12)


@variable()
def pv_pols_if():
    return sum(pols_if(t) * discount(t) for t in range(settings["T_MAX_CALCULATION"]))


@variable()
def pv_claims():
    return sum(claims(t) * discount(t) for t in range(settings["T_MAX_CALCULATION"]))


@variable()
def net_premium_pp():
    return pv_claims() / pv_pols_if()


@variable()
def expenses(t):
    expenses = 0
    if t == 0:
        expenses += assumption["expense_acq"] * pols_if(t)
    expenses += assumption["expense_maint"]/12 * inflation_factor(t) * pols_if(t)
    return expenses


@variable()
def premium_pp():
    return round((1 + assumption["loading_prem"]) * net_premium_pp(), 2)


@variable()
def premiums(t):
    return premium_pp() * pols_if(t)


@variable()
def pv_premiums():
    return sum(premiums(t) * discount(t) for t in range(settings["T_MAX_CALCULATION"]))


@variable()
def pv_expenses():
    return sum(expenses(t) * discount(t) for t in range(settings["T_MAX_CALCULATION"]))


@variable()
def commissions(t):
    if duration(t) == 0:
        return premiums(t)
    return 0


@variable()
def pv_commissions():
    return sum(commissions(t) * discount(t) for t in range(settings["T_MAX_CALCULATION"]))


@variable()
def net_cf(t):
    return premiums(t) - claims(t) - expenses(t) - commissions(t)


@variable()
def pv_net_cf():
    return pv_premiums() - pv_claims() - pv_expenses() - pv_commissions()
