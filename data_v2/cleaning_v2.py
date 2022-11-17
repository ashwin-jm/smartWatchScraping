import pandas as pd

data = pd.read_csv("smartwatch_data_v1.csv")

indexes = data[ data['Sale_price'] == 'No price available'].index
data.drop(indexes, inplace=True)
data.to_csv("smartwatch_data_v2.csv", index=False)