import pandas as pd
data_frame_int = pd.DataFrame({'Yes': [50, 21], 'No': [131, 2]})
print(data_frame_int)
data_frame_str = pd.DataFrame({'Bob': ['I liked it.', 'It was awful.'], 
                               'Sue': ['Pretty good.', 'Bland.']},
                              index=['Product A', 'Product B'])
print(data_frame_str)
series = pd.Series([1, 2, 3, 4, 5])
print(series)
series_index = pd.Series([30, 35, 40], index=['2015 Sales', '2016 Sales', '2017 Sales'], name='Product A')
print(series_index) #~> Note: I can also specify data type with dtype=...

wine_reviews = pd.read_csv("./winemag-data-130k-v2.csv")
print(wine_reviews.shape) #~> out: (q.rows, q.columns)
print(wine_reviews.head()) #~> out: first 5 rows
#~> to show all columns:
pd.set_option('display.max_columns', None)
print(wine_reviews.head())

wine_reviews = pd.read_csv("./winemag-data-130k-v2.csv", index_col=0) #~> to use the first column as index
print(wine_reviews.head())