# p value for advertisement A/B

import numpy as np
import pandas as pd
from scipy.stats import chi2, chi2_contingency

# contingency table
#        click       no click
# ------------------------------
# adv A |   a            b
# adv B |   c            d

# chi^2 = (ad - bc)^2 (a + b + c + d) / [ (a + b)(c + d)(a + c)(b + d)]
# degrees of freedom = (#cols - 1) x (#rows - 1) = (2 - 1)(2 - 1) = 1


def get_p_value(T):
    det = T[0, 0] * T[1, 1] - T[0, 1] * T[1, 0]
    c2 = (
        float(det)
        / T[0].sum()
        * det
        / T[1].sum()
        * T.sum()
        / T[:, 0].sum()
        / T[:, 1].sum()
    )
    p = 1 - chi2.cdf(x=c2, df=1)
    return p


# get data
df = pd.read_csv("C:/gitproj/AB_test/CTR_ttest/advertisement_click.csv")
a = df[df["advertisement_id"] == "A"]
b = df[df["advertisement_id"] == "B"]
a = a["action"]
b = b["action"]

A_clk = a.sum()
A_noclk = a.size - a.sum()
B_clk = b.sum()
B_noclk = b.size - b.sum()

T = np.array([[A_clk, A_noclk], [B_clk, B_noclk]])

print(f"p value is {get_p_value(T)}")
