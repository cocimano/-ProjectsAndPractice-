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
reviews.rename(index={0: 'firstEntry', 1: 'secondEntry'}) #~> rename the first and second rows index
print(reviews.rename_axis("wines", axis='rows').rename_axis("fields", axis='columns')) #~> rename both the row index and the column index
#Combining
canadian_youtube = pd.read_csv("./CAvideos.csv")
british_youtube = pd.read_csv("./GBvideos.csv")
pd.concat([canadian_youtube, british_youtube]) #~> to concatenate the two dataframes
left = canadian_youtube.set_index(['title', 'trending_date'])
right = british_youtube.set_index(['title', 'trending_date'])
left.join(right, lsuffix='_CAN', rsuffix='_UK') #~> to join the two dataframes.
#Note: lsuffix and rsuffix are used to specify the suffixes to use for overlapping columns

#Summary Functions and Maps
print(f'Describe points:\n{reviews.points.describe()}')
print(f'{reviews.taster_name.describe()}')
print(f'{reviews.points.mean()}')
print(f'{reviews.taster_name.unique()}') #~> to show the unique values
print(f'{reviews.taster_name.value_counts()}') #~> to show the number of times each value appears
#Map
review_points_mean = reviews.points.mean()
print(f'{reviews.points.map(lambda p: p - review_points_mean)}') #~> to subtract the mean from each value
def remean_points(row):
    row.points = row.points - review_points_mean
    return row

reviews.apply(remean_points, axis='columns')
print(reviews.head(1))

review_points_mean = reviews.points.mean()
reviews.points - review_points_mean #~> to subtract the mean from each value
reviews.country + " - " + reviews.region_1 #~> to concatenate the country and the region_1

#I'm an economical wine buyer. Which wine is the "best bargain"? Create a variable bargain_wine with the title of the wine with the highest points-to-price ratio in the dataset.
bargain_wine = reviews.title[(reviews.points / reviews.price).idxmax()]

#Grouping and Sorting
print(reviews.groupby('points').points.count()) #~> to group by points and count the number of times each value appears
print(reviews.groupby('points').price.min()) #~> to group by points and show the minimum price
print(reviews.groupby('winery').apply(lambda df: df.title.iloc[0])) #~> to group by winery and show the first title of each group
reviews.groupby(['country', 'province']).apply(lambda df: df.loc[df.points.idxmax()]) #~> to group by country and province and show the row with the maximum points
print(reviews.groupby(['country']).price.agg([len, min, max])) #~> to group by country and show the length, minimum and maximum price
#Multi-indexes
countries_reviewed = reviews.groupby(['country', 'province']).description.agg([len])
print(countries_reviewed)
mi = countries_reviewed.index
print(mi) #~> to show the multi-index
print(countries_reviewed.reset_index())#~> to reset the index
#Sorting
countries_reviewed = countries_reviewed.reset_index()
print(countries_reviewed.sort_values(by='len')) #~> to sort by len
print(countries_reviewed.sort_values(by='len', ascending=False)) #~> to sort by len in descending order
print(countries_reviewed.sort_index()) #~> to sort by index
print(countries_reviewed.sort_values(by=['country', 'len'])) #~> to sort by country and len

#Data Types and Missing Values
print(reviews.price.dtype) #~> to show the data type of the price column
print(reviews.dtypes) #~> to show the data type of all columns
print(reviews.points.astype('float64')) #~> to change the data type of the points column to float64
print(reviews.index.dtype) #~> to show the data type of the index
reviews[pd.isnull(reviews.country)] #~> to show the rows where the country is null
reviews.region_2.fillna("Unknown") #~> to fill the null values with "Unknown"
reviews.taster_twitter_handle.replace("@kerinokeefe", "@kerino") #~> to replace the values

