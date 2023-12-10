
import pandas as pd
df = pd .read_csv('whisky.csv')

df['price'] = df['price'].str.replace(' ', '').str.replace(',', '.').astype(float)
df_sorted = df.sort_values(['price', 'rating'], ascending=[True,False])

print(df_sorted.get(['name', 'price']))
