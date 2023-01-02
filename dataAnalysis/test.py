import pandas as pd

a = pd.DataFrame({"A":[0,1,0], "B":[2,0,5]}, columns=list('AB'))
print(a)
isAZero = a["A"] == 0
a.loc[isAZero, 'B'] = "a"
print(a)