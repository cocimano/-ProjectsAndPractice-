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
print(pd.set_option('display.max_rows', 5)) #~> to show only 5 rows
print(wine_reviews.country)  #~> to show only the country column
#also works: wine_reviews['country']
print(wine_reviews['country'][0]) #~> to show the first country

#Index-based selection
print(wine_reviews.iloc[0]) #~> to show the first row
#Note: Both loc and iloc are row-first, column-second. 
# This is the opposite of what we do in native Python, which is column-first, row-second.
print(wine_reviews.iloc[:, 0]) #~> to show the first column
print(wine_reviews.iloc[:3, 0]) #~> to show the first 3 rows of the first column
print(wine_reviews.iloc[1:3, 0]) #~> to show the second and third rows of the first column
print(wine_reviews.iloc[[0, 1, 2], 0]) #~> to show the first, second and third rows of the first column
print(wine_reviews.iloc[-5:]) #~> to show the last 5 rows

#Label-based selection
reviews = wine_reviews
print(reviews.loc[0, 'country']) #~> to show the country of the first row
print(reviews.loc[:, ['taster_name', 'taster_twitter_handle', 'points']]) #~> to show the taster_name, taster_twitter_handle and points columns
#Note: loc includes the first and last elements of the range, iloc only includes the first

#Manipulating the index
print(reviews.set_index("title")) #~> to set the index to the title column

#Conditional selection
print(reviews.country == 'Italy') #~> to show a boolean series
print(reviews.loc[reviews.country == 'Italy']) #~> to show the rows where the country is Italy
print(reviews.loc[(reviews.country == 'Italy') & (reviews.points >= 90)]) #~> & is the and operator
print(reviews.loc[(reviews.country == 'Italy') | (reviews.points >= 90)]) #~> | is the or operator
print(reviews.loc[reviews.country.isin(['Italy', 'France'])]) #~> to show the rows where the country is Italy or France. isin as 'is in the list'
print(reviews.loc[reviews.price.notnull()]) #~> to show the rows where the price is not null

#Assigning data
reviews['critic'] = 'everyone' #~> to add a new column with the value 'everyone'
print(reviews.critic)
# With an iterable of values:
reviews['index_backwards'] = range(len(reviews), 0, -1) #~> to add a new column with the index backwards
print(reviews.index_backwards)

#Renaming and Combining
reviews.rename(columns={'points': 'score'}) #~> to rename the points column to score

