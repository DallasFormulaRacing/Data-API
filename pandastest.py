import pandas as pd

with open("./example_csv.csv") as file:
    df = pd.read_csv(file)
    print(df.loc[0, 'First Name'])