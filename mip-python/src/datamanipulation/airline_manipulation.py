"""
Insert code here for all the transformations you are going to do
"""
import pandas as pd
import numpy as np
from sklearn import preprocessing

# Read the data/flights.csv dataset into Python
flights_df = pd.read_csv('../../data/flights.csv', sep=',', encoding='utf8')
#print (flights_df)

# Remove the column "DAY_OF_WEEK"
df_deleted = flights_df.drop(['DAY_OF_WEEK'], 1)
#print(df_deleted)

# Rename the column "WHEELS_OFF" to "HAS_WHEELS"
updated_df  = flights_df.rename(index=str, columns={"WHEELS_OFF": "HAS_WHEELS"})
#print (updated_df.describe())

# Slice the dataset row-wise into 4 equal-sized chunks
df1,df2,df3,df4 = np.array_split(updated_df, 4)
#print(df1)
#print(df2)
#print(df3)
#print(df4)


# Concatenate back the chucks produced above into 1 dataset
df_concatenated = pd.concat([df1,df2,df3,df4])
#print(df_concatenated)

# Get the slice of the dataset that is only relevant to the airline AA
airline_is_AA = updated_df.AIRLINE == 'AA'
df_aa = updated_df[airline_is_AA]
#print(df_aa)

# Get the slice of the dataset where delay is <10 and destination is PBI
delay_lt_10 = updated_df.DEPARTURE_DELAY < 10
dest_PBI =  updated_df.DESTINATION_AIRPORT == 'PBI'
df_delay_lt_10_and_dest_PBI = updated_df[delay_lt_10 & dest_PBI]
#print(df_delay_lt_10_and_dest_PBI)
#print(updated_df.describe)

# Fill the blanks in the AIR_SYSTEM_DELAY column with the average of the column itself
mean_AIR_SYSTEM_DELAY = updated_df.AIR_SYSTEM_DELAY.mean()
updated_df.AIR_SYSTEM_DELAY.fillna(mean_AIR_SYSTEM_DELAY,inplace = True)
#print(updated_df.describe)


# Create a column "has_A", which contains 1 if the airline name contains the letter 'A', 0 otherwise
has_A = updated_df.apply(lambda row : 1 if 'A' in row.AIRLINE else 0, axis =1)
print(has_A )

# Get a random sample of the rows in the data frame
sample_row = updated_df.sample()
#print (sample_row)

# Normalise the column "DEPARTURE_DELAY" to the range 0-1 with Min Max normalisation
df_DEPARTURE_DELAY = updated_df[['DEPARTURE_DELAY']].dropna().values
min_max_scaler = preprocessing.MinMaxScaler()
x_scaled = min_max_scaler.fit_transform(df_DEPARTURE_DELAY)
df_normalized = pd.DataFrame(x_scaled)
#print(df_normalized)

# Binarise the column "ORIGIN_AIRPORT"
binarize_ORIGIN_AIRPORT = pd.get_dummies(updated_df.ORIGIN_AIRPORT)
print(binarize_ORIGIN_AIRPORT)


