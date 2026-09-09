import sys
import pandas as pd 
print('arguments', sys.argv)

month = int(sys.argv[1])

df = pd.DataFrame({'Day':[1,2], "number_passengers":[3,4]})
df['Month'] = month


df.to_parquet(f"output_{month}.parquet")