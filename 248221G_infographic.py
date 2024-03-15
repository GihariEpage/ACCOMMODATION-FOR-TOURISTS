# -*- coding: utf-8 -*-
"""infographic.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1BOlR1qREKgPdncx1CURvOjoBGYbwTJbw
"""

# read the given dataset
import pandas as pd

# Read the dataset
df = pd.read_csv('/content/Information for Accommodation.csv')

# Print the first few rows of the dataset
df.head(10)

#check the data types of each columns
df.dtypes

numeric_cols = df.select_dtypes(include=['number']).columns
print(numeric_cols)

non_numeric_cols = df.select_dtypes(exclude=['number']).columns
print(non_numeric_cols)

df[non_numeric_cols].info()

num_missing = df.isna().sum()
num_missing

missing_values = df.isnull().sum().div(df.shape[0]) * 100
for column, missing in missing_values.items():
    print(f"Column: {column}, Missing Values: {missing:.2f}%")

"""**Missing value analysis**"""

import seaborn as sns
import matplotlib.pyplot as plt

plt.figure(figsize=(10,8))

cols = df.columns
colours = ['#000099', '#ffff00'] # specify colours: yellow - missing. blue - not missing
sns.heatmap(df[cols].isna(), cmap=sns.color_palette(colours))

# obtain the distinct category of Type column wise missing values of columns as percentage with respect to category totals in Type column
missing_percentages = {}
for category in df['Type'].unique():
  category_df = df[df['Type'] == category]
  missing_counts = category_df.isna().sum()
  missing_percentages[category] = (missing_counts / category_df.shape[0]) * 100

missing_percentages_df = pd.DataFrame.from_dict(missing_percentages, orient='index')
missing_percentages_df.columns = df.columns
missing_percentages_df.index.name = 'Type'

# Create a stacked bar chart
ax = missing_percentages_df.plot(kind='bar', stacked=False, figsize=(10, 6))

# Add labels and title
ax.set_xlabel('Type')
ax.set_ylabel('Missing Values (%)')
ax.set_title('Missing Values by Category (%)')

# Add grid and legend
ax.grid(True)
ax.legend(loc='upper right')

# Show the plot
plt.show()

"""100% missing in Grades for Boutique Hotels, Boutique Villas, Tourist Hotels
Grade, AGA Division, PS/MC/UC, Longitude and Latitude have missing values.  
Since District column doesn’t contain any missing values and we can get location information from District column rather than analyzing the data into AGA Divisional wise or PS/MC/UC wise. Also, Longitude and Latitude gives the exact location, and it contains more than 30% missing values data, we can ignore those two columns since we can get the location information from district level.
Deeper analyzing the missing values under Grade column, it was identified that the Boutique Hotels, Boutique Villas, Tourist Hotels has no Grading values appears in the dataset. Hence it was decided to impute the Grading value as “Not_Graded”.         

"""

df['Grade'].fillna('Not_Graded', inplace=True)

missing_values = df.isnull().sum().div(df.shape[0]) * 100
for column, missing in missing_values.items():
    print(f"Column: {column}, Missing Values: {missing:.2f}%")

#Univariate Analysis
grouped_data = df.groupby('Type')['Type'].count()
print(grouped_data)

total_records = df.shape[0]
percentage_data = (grouped_data / total_records) * 100
for category, percentage in percentage_data.items():
    print(f"Accomodation Type: {category}, Percentage: {percentage:.2f}%")

grouped_data = df.groupby('Type')['Type'].count()
print(grouped_data)

total_records = df.shape[0]
percentage_data = (grouped_data / total_records) * 100
#pie chart

labels = df['Type'].value_counts().index.to_list()
plt.figure(figsize=(15, 8))
plt.pie(df['Type'].value_counts(), labels=labels, autopct='%.2f%%')
plt.title('Accommodation Types', fontsize=16)
plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
plt.show()

"""There are 11 types of accommodation placesin Sri Lanka in 2018 and there are 2130 rooms available for accommodations for tourists. Most popular accommodation places are low- luxury accommodation types. Guest houses, which is categorized as low luxury accommodation type are the most common type of accommodation for tourists in Sri Lanka & among them most guest houses in Sri Lanka hold Grade A classification, ensuring high standards of quality."""

grouped_data = df.groupby('District')['District'].count()
print(grouped_data)

total_records = df.shape[0]
percentage_data = (grouped_data / total_records) * 100

#bar chart
grouped_data.plot(kind='bar')
plt.xlabel("District")
plt.ylabel("Number of Accomodation Places")
plt.title("Accomodation Places by District")
plt.show()

grouped_data = df.groupby('Name')['Name'].count()
print(grouped_data)
#This variable contains unique values

grouped_data = df.groupby('Address')['Address'].count()
print(grouped_data)
#Thia variable also contains unique values

grouped_data = df.groupby('AGA Division')['AGA Division'].count()
print(grouped_data)

grouped_data = df.groupby('PS/MC/UC')['PS/MC/UC'].count()
print(grouped_data)

sns.histplot(df['Rooms'], bins=50)
plt.xlabel('Number of Rooms')
plt.ylabel('Frequency')
plt.title('Distribution of Number of Rooms')
plt.show()

sns.boxplot(x=df['Rooms'])
plt.xlabel('Rooms')
plt.ylabel('Value')
plt.title('Boxplot of Rooms')
plt.show()

"""There can be high no of rooms avaible in some Accommodations

"""

highest_rooms = df['Rooms'].max()
highest_rooms_name = df[df['Rooms'] == highest_rooms]['Name'].values[0]

print(f"Name of the accommodation with the highest number of rooms: {highest_rooms_name}")

filtered_df = df[df['Rooms'] > 400]
accommodation_types = filtered_df['Type'].unique()

for accommodation_type in accommodation_types:
    print("Accommodation Types which has the high number of rooms:", accommodation_type)

"""**Bivariate** **analysis**"""

sns.boxplot(x = 'Type', y = 'Rooms', data = df)
plt.xlabel('Type')
plt.ylabel('Rooms')
plt.title('Type wise Rooms Box Plot')
plt.xticks(rotation = 90)
plt.show()

"""High no of rooms offered by Classification hotels (1-5 star) and tourist hotels"""

import colorcet as cc
# Group the data by Type and District
grouped_data = df.groupby(['Type', 'District']).size().unstack()

# Calculate percentages
grouped_data_pct = grouped_data.apply(lambda x: 100 * x / x.sum(), axis=1)

# Create a 100% stacked clustered bar chart
fig, ax = plt.subplots(figsize=(10, 6))
colors = sns.color_palette(cc.glasbey, n_colors=25)
grouped_data_pct.plot(kind='bar', stacked=True, ax=ax, width=0.8, color=colors)

# Add labels and title
ax.set_xlabel('Accomodation Type')
ax.set_ylabel('Percentage of Accommodation Places')
ax.set_title('Accommodation Places by Type and District (100% Stacked)')

# Add legend
ax.legend(title='District', bbox_to_anchor=(1.05, 1), loc='upper left')

# Show the plot
plt.show()

df_bungalow = df[df['Type'] == 'Bangalows']
#df_boutique_hotels = df[df['Type'] == 'Boutique Hotels'] --since Grade is missing
#df_boutique_villas = df[df['Type'] == 'Boutique Villas'] --since Grade is missing
df_star_hotel = df[df['Type'] == 'Classified Hotels( 1-5 Star)']
df_guest_house = df[df['Type'] == 'Guest Houses']
#df_heritage_bungalow = df[df['Type'] == 'Heritage Bungalows'] --since Grade is missing
df_heritage_homes = df[df['Type'] == 'Heritage Homes']
df_home_stay = df[df['Type'] == 'Home Stay Units']
df_apartments = df[df['Type'] == 'Rented Apartments']
df_rented_homes = df[df['Type'] == 'Rented Homes']
df_hotels = df[df['Type'] == 'Tourist Hotels']

grouped_data = df_bungalow.groupby('Grade')['Grade'].count()
total_records = df_bungalow.shape[0]
percentage_data = (grouped_data / total_records) * 100

#bar chart
grouped_data.plot(kind='bar')
plt.xlabel("Grade")
plt.ylabel("Number of Accomodation Places")
plt.title("Accomodation Places by Grade - Bungalows")
plt.show()

grouped_data = df_star_hotel.groupby('Grade')['Grade'].count()
total_records = df_star_hotel.shape[0]
percentage_data = (grouped_data / total_records) * 100

#bar chart
grouped_data.plot(kind='bar')
plt.xlabel("Grade")
plt.ylabel("Number of Accomodation Places")
plt.title("Accomodation Places by Grade - Classified Hotels( 1-5 Star)")
plt.show()

grouped_data = df_guest_house.groupby('Grade')['Grade'].count()
total_records = df_guest_house.shape[0]
percentage_data = (grouped_data / total_records) * 100

#bar chart
grouped_data.plot(kind='bar',colormap='Accent')
plt.xlabel("Grade")
plt.ylabel("Number of Accomodation Places")
plt.title("Accomodation Places by Grade - Guest Houses")
plt.show()

grouped_data = df_heritage_homes.groupby('Grade')['Grade'].count()
total_records = df_heritage_homes.shape[0]
percentage_data = (grouped_data / total_records) * 100

#bar chart
grouped_data.plot(kind='bar')
plt.xlabel("Grade")
plt.ylabel("Number of Accomodation Places")
plt.title("Accomodation Places by Grade - Heritage Homes")
plt.show()

grouped_data = df_home_stay.groupby('Grade')['Grade'].count()
total_records = df_home_stay.shape[0]
percentage_data = (grouped_data / total_records) * 100

#bar chart
grouped_data.plot(kind='bar')
plt.xlabel("Grade")
plt.ylabel("Number of Accomodation Places")
plt.title("Accomodation Places by Grade - Home Stay Units")
plt.show()

grouped_data = df_apartments.groupby('Grade')['Grade'].count()
total_records = df_apartments.shape[0]
percentage_data = (grouped_data / total_records) * 100

#bar chart
grouped_data.plot(kind='bar')
plt.xlabel("Grade")
plt.ylabel("Number of Accomodation Places")
plt.title("Accomodation Places by Grade - Rented Apartments")
plt.show()

grouped_data = df_rented_homes.groupby('Grade')['Grade'].count()
total_records = df_rented_homes.shape[0]
percentage_data = (grouped_data / total_records) * 100

#bar chart
grouped_data.plot(kind='bar')
plt.xlabel("Grade")
plt.ylabel("Number of Accomodation Places")
plt.title("Accomodation Places by Grade - Rented Homes")
plt.show()

"""Further Graphs are plotted using Power BI"""