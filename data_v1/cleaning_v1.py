import pandas as pd
data = pd.read_csv('smartwatch_data2.csv')
final_data = data.drop_duplicates(subset='Product_url', keep="first")
final_data.to_csv("smartwatch_data_v1.csv", index=False)