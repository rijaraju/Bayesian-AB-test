import requests
import numpy as np
import pandas as pd
from scipy import stats

# get data
df = pd.read_csv("advertisement_click.csv")
a = df[df["advertisement_id"] == "A"]
b = df[df["advertisement_id"] == "B"]
a = a["action"].values
b = b["action"].values

print("a.mean:", a.mean())
print("b.mean:", b.mean())


i = 0
j = 0
count = 0
while i < len(a) and j < len(b):
    # quit when there's no data left for either ad
    r = requests.get("http://localhost:8888/get_ad")
    # print(r.content)
    r = r.json()
    if r["advertisement_id"] == "A":
        action = a[i]
        i += 1
    else:
        action = b[j]
        j += 1

    if action == 1:
        # only click the ad if our dataset determines that we should
        requests.post(
            "http://localhost:8888/click_ad",
            data={"advertisement_id": r["advertisement_id"]},
        )

    # log some stats
    count += 1
    if count % 50 == 0:
        print("Seen %s ads, A: %s, B: %s" % (count, i, j))
