"""
Insert code here for all the transformations you are going to do
"""
import pandas as pd
import numpy as np
from sklearn import preprocessing
import pygeohash as gh
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA

#from scipy.stats import mstats
from scipy.special import expit as sigmoid

pd.set_option('display.width', 1000)


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
#print(has_A )

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
#print(binarize_ORIGIN_AIRPORT)

# replace NaN with mean for AIR_SYSTEM_DELAY
updated_df.AIR_SYSTEM_DELAY.fillna(updated_df.AIR_SYSTEM_DELAY.mean(),inplace=True)
#print(updated_df.AIR_SYSTEM_DELAY)

#Remove outliers for 'DEPARTURE_DELAY' - remove rows in excess of 3 standard deviations from mean
updated_df1 = updated_df[((updated_df.DEPARTURE_DELAY - updated_df.DEPARTURE_DELAY.mean()) / updated_df.DEPARTURE_DELAY.std()).abs() < 3]
#print(updated_df)

#Remove those rows where (for quantitative variables) any quant variable has value > 3std from mean
#updated_df.dropna(axis = 1,how = 'any', inplace = True)
#print(updated_df.describe())

#numeric_col_names = updated_df.select_dtypes(include=[np.number]).columns
#for num_column in numeric_cols:
#    updated_df = updated_df[((updated_df[[num_column]] - updated_df[[num_column]].mean()) / updated_df[[num_column]].std()).abs() < 3]
#print(updated_df.describe())

#Winsorise all quantitative columns to a 95% upper and lower bound
#numeric_cols_data = updated_df.select_dtypes([np.number])
#winsorize_data = mstats.winsorize(numeric_cols_data, limits=[0.05, 0.05])
#print(winsorize_data)

#log transform the column 'DEPARTURE_DELAY' into a new column 'LOG_DEPARTURE_DELAY'
updated_df['LOG_DEPARTURE_DELAY'] = np.log(updated_df['DEPARTURE_DELAY'])
#print(updated_df)

#Create a "Route" column by merging ORIGIN_AIRPORT and DESTINATION_AIRPORT
updated_df['ROUTE'] = updated_df['ORIGIN_AIRPORT'].str.cat(updated_df['DESTINATION_AIRPORT'], sep = '->')
#print(updated_df)

#Normalise all the quantitative columns with standard normalisation

#Apply the sigmoid function to the column 'ARRIVAL_DELAY'
#print(sigmoid(updated_df.ARRIVAL_DELAY))

#Perform a left join with the dataset airports.csv, on departure_airport
airports_df = pd.read_csv('../../data/airports.csv', sep=',', encoding='utf8')
df_merged = pd.merge(updated_df,airports_df,how='left',left_on='ORIGIN_AIRPORT', right_on='IATA_CODE')
#print(df_merged)

#For each airline, the percentage delay for each dep_airport, over total delay across all dep_airport
dd_sum = flights_df.DEPARTURE_DELAY.sum()
groupby_OA = flights_df.groupby(['ORIGIN_AIRPORT'])['DEPARTURE_DELAY'].sum().apply(lambda x: (x*100)/dd_sum)
#print(groupby_OA)

#Calculate the mean "Departure_delay" for each airline, over the whole dataset
mean_DD = flights_df.groupby(['ORIGIN_AIRPORT'])['DEPARTURE_DELAY'].agg('mean')
#print(mean_DD)
#ABE=7.975610 173

#The mean geohash of "londf['geohash']=df.apply(lambda x: gh.encode(x.latitude, x.longitude, precision=5), axis=1)gitude" and "latitude" for each airline
airports_df['geohash']=airports_df.apply(lambda x: gh.encode(x.LATITUDE, x.LONGITUDE, precision=5), axis=1)
#print(airports_df)

#The percentage of flights leaving before 12pm, over total flights for each airline
flights_b4_12 = flights_df.groupby('AIRLINE')['DEPARTURE_TIME'].apply(lambda x: (x<1200).sum()*100/x.sum())
#print(flights_b4_12)

#Do PCA to reduce the variables 'departure_delay' and 'arrival_delay' to a single component
updated_df = updated_df[np.isfinite(updated_df['DEPARTURE_DELAY'])]
updated_df = updated_df[np.isfinite(updated_df['ARRIVAL_DELAY'])]
#print(updated_df)
features = ['DEPARTURE_DELAY' , 'ARRIVAL_DELAY']
x = StandardScaler().fit_transform(updated_df.loc[:, features].values)
pca = PCA(n_components=1)
principalComponents = pca.fit_transform(x)
print(principalComponents)
