import pandas as pd
import numpy as np
from ksif import Portfolio, columns
from ksif.core.columns import CODE, DATE, B_P, E_P, MOM12_1, GP_A, VOL_3M, RET_1
from tabulate import tabulate

INFORMATION_RATIO = 'information_ratio'
ALL = 'all'
VALUE_MOMENTUM = 'value+momentum'
VOLATILITY = 'volatility'
QUALITY = 'quality'
MOMENTUM = 'momentum'
VALUE = 'value'
std = 'std_'

pf = Portfolio()
universe = pf.loc[
           (pf[columns.MKTCAP] >= 50000000000) &
           (~np.isnan(pf[RET_1])) &
           (~np.isnan(pf[B_P])) &
           (~np.isnan(pf[E_P])) &
           (~np.isnan(pf[MOM12_1])) &
           (~np.isnan(pf[GP_A])) &
           (~np.isnan(pf[VOL_3M])), :
           ]
universe = universe.periodic_standardize(factor=B_P)
universe = universe.periodic_standardize(factor=E_P)
universe[VALUE] = (universe[std + B_P] + universe[std + E_P]) / 2
universe = universe.periodic_standardize(factor=MOM12_1)
universe[MOMENTUM] = universe[std + MOM12_1]
universe = universe.periodic_standardize(factor=GP_A)
universe[QUALITY] = universe[std + GP_A]
universe = universe.periodic_standardize(factor=VOL_3M)
universe[VOLATILITY] = universe[std + VOL_3M]

universe[VALUE_MOMENTUM] = universe[VALUE] + universe[MOMENTUM]
universe[ALL] = universe[VALUE] + universe[MOMENTUM] + universe[QUALITY] + universe[VOLATILITY]

# %% Table 3. Low Factor Exposure 2 Factor
signal_blend = universe.periodic_percentage(min_percentage=0, max_percentage=0.5, factor=VALUE_MOMENTUM)
signal_blend_outcome = signal_blend.outcome()
signal_blend_information_ratio = signal_blend_outcome[INFORMATION_RATIO]

value_portfolio = universe.periodic_percentage(min_percentage=0, max_percentage=0.5, factor=VALUE)
value_portfolio_outcome = value_portfolio.outcome()
momentum_portfolio = universe.periodic_percentage(min_percentage=0, max_percentage=0.5, factor=MOMENTUM)
momentum_portfolio_outcome = momentum_portfolio.outcome()
portfolio_blend_information_ratio = (value_portfolio_outcome[INFORMATION_RATIO] +
                                     momentum_portfolio_outcome[INFORMATION_RATIO]) / 2

print("Table 3. Portfolio Comparison - Low Factor Exposure: Performance")
print(" - KOSPI + KOSDAQ 시총 500억 이상, May 2002-July 2018")
print(tabulate([['Signal Blend', None, None, signal_blend_information_ratio],
                ['Portfolio Blend', None, None, portfolio_blend_information_ratio]],
               headers=['Name', 'Active Return', 'Active Risk', 'Information Ratio']))

#%% Table 8. High Factor Exposure 2 Factor
signal_blend = universe.periodic_percentage(min_percentage=0, max_percentage=0.15, factor=VALUE_MOMENTUM)
signal_blend_outcome = signal_blend.outcome()
signal_blend_information_ratio = signal_blend_outcome[INFORMATION_RATIO]

value_portfolio = universe.periodic_percentage(min_percentage=0, max_percentage=0.05, factor=VALUE)
value_portfolio_outcome = value_portfolio.outcome()
momentum_portfolio = universe.periodic_percentage(min_percentage=0, max_percentage=0.05, factor=MOMENTUM)
momentum_portfolio_outcome = momentum_portfolio.outcome()
portfolio_blend_information_ratio = (value_portfolio_outcome[INFORMATION_RATIO] +
                                     momentum_portfolio_outcome[INFORMATION_RATIO]) / 2

print("Table 8. Portfolio Comparison - High Factor Exposure: Performance")
print(" - KOSPI + KOSDAQ 시총 500억 이상, May 2002-July 2018")
print(tabulate([['Signal Blend', None, None, signal_blend_information_ratio],
                ['Portfolio Blend', None, None, portfolio_blend_information_ratio]],
               headers=['Name', 'Active Return', 'Active Risk', 'Information Ratio']))