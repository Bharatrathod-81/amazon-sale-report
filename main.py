from typing import final

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the dataset
data = pd.read_csv('data/Amazon Sale Report.csv')


# Define the known date formats
date_formats = ['%m-%d-%Y', '%m-%d-%y', '%Y-%m-%d', '%d-%m-%Y']  # Add more formats as needed

def parse_multiple_formats(date):
    """
    Try multiple date formats until one works. If none match, return NaT.
    """
    for fmt in date_formats:
        try:
            return pd.to_datetime(date, format=fmt)
        except (ValueError, TypeError):
            continue
    return pd.NaT  # Return NaT if no format matches

# Apply the function only to rows where Date is still NaT after initial parsing
data['Date'] = data['Date'].apply(parse_multiple_formats)


# Remove rows where 'Amount' is missing (likely due to canceled/incomplete orders)
cleared_data = data.dropna(subset=['Amount'])

# Remove duplicate rows
cleared_data = cleared_data.drop_duplicates()



# Filter out unfulfilled orders
unfulfilled_orders = cleared_data[cleared_data['Status'] != 'Fulfilled']
cleared_data.drop(unfulfilled_orders.index) # Drop unfulfilled orders


# Drop unnecessary columns ex: New and Pendings
cleared_data = cleared_data.drop(columns=['New', 'PendingS'])

# Fill missing values in the 'fulfilled-by' column with 'Unknown'
cleared_data['fulfilled-by'] = cleared_data['fulfilled-by'].fillna('No Easy Ship')

# Drop rows with missing shipping information
cleared_data = cleared_data.dropna(subset=['ship-city', 'ship-state', 'ship-postal-code', 'ship-country'])


print(cleared_data.info())
print(cleared_data.isnull().sum())



# Example Analysis Code

final_data = cleared_data

# Group data by date and calculate total sales per day
daily_sales = final_data.groupby('Date')['Amount'].sum()

# Create a new figure with customized height
fig, ax = plt.subplots(figsize=(13, 8))
daily_sales.plot(kind='line', title='Sales Over Time', ax=ax)
ax.set_xlabel('Date')
ax.set_ylabel('Total Sales')
plt.show()


# Sales quantity by product category
category_sales = final_data.groupby('Category')['Qty'].sum().sort_values(ascending=False)

# Create a new figure with customized height
fig, ax = plt.subplots(figsize=(13, 8))
category_sales.plot(kind='bar', title='Quantity Sold by Product Category', ax=ax)
ax.set_xlabel('Product Category')
ax.set_ylabel('Quantity Sold')
plt.show()


# Total sales by state
sales_by_state = final_data.groupby('ship-state')['Amount'].sum().sort_values(ascending=False)

# Create a new figure with customized height
fig, ax = plt.subplots(figsize=(13, 8))
sales_by_state.plot(kind='bar', title='Total Sales by State', ax=ax)
ax.set_xlabel('State')
ax.set_ylabel('Total Sales')
plt.show()


# Sales by fulfillment method
fulfillment_sales = final_data.groupby('fulfilled-by')['Amount'].sum().sort_values(ascending=False)

# Create a new figure with customized height
fig, ax = plt.subplots(figsize=(13, 8))
fulfillment_sales.plot(kind='bar', title='Sales by Fulfillment Method', ax=ax)
ax.set_xlabel('Fulfillment Method')
ax.set_ylabel('Total Sales')
plt.show()
