import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Additional Libraries
import folium
from folium.plugins import HeatMap

# Load the dataset
data = pd.read_csv('../data/Amazon Sale Report.csv')

# Define known date formats
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

# Apply the function to parse dates
data['Date'] = data['Date'].apply(parse_multiple_formats)

# Clean the data
cleared_data = data.dropna(subset=['Amount'])  # Remove rows where 'Amount' is missing
cleared_data = cleared_data.drop_duplicates()  # Remove duplicate rows

# Remove unfulfilled orders
cleared_data = cleared_data[cleared_data['Status'] == 'Fulfilled']

# Drop unnecessary columns
cleared_data = cleared_data.drop(columns=['New', 'PendingS'])

# Fill missing values in the 'fulfilled-by' column with 'Unknown'
cleared_data['fulfilled-by'] = cleared_data['fulfilled-by'].fillna('No Easy Ship')

# Drop rows with missing shipping information
cleared_data = cleared_data.dropna(subset=['ship-city', 'ship-state', 'ship-postal-code', 'ship-country'])

# Example Analysis Code
final_data = cleared_data

### 1. Sales Overview

# Sales over time
sales_over_time = final_data.groupby('Date')['Amount'].sum().reset_index()

# Monthly sales trend
sales_over_time['Date'] = pd.to_datetime(sales_over_time['Date'])
sales_over_time.set_index('Date', inplace=True)
monthly_sales = sales_over_time['Amount'].resample('ME').sum()

# Plot monthly sales trend
plt.figure(figsize=(10,6))
sns.lineplot(x=monthly_sales.index, y=monthly_sales.values)
plt.title('Monthly Sales Performance')
plt.xlabel('Month')
plt.ylabel('Total Sales Amount')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

### 2. Product Category Distribution

# Product category distribution
category_distribution = final_data.groupby('Category')['Qty'].sum().reset_index()

# Plot product category distribution
plt.figure(figsize=(8,5))
sns.barplot(x='Qty', y='Category', data=category_distribution)
plt.title('Product Category Distribution')
plt.xlabel('Quantity Sold')
plt.ylabel('Category')
plt.tight_layout()
plt.show()

### 3. Size Analysis

# Size distribution
size_distribution = final_data.groupby('Size')['Qty'].sum().reset_index()

# Plot size distribution
plt.figure(figsize=(8,5))
sns.barplot(x='Qty', y='Size', data=size_distribution)
plt.title('Product Size Distribution')
plt.xlabel('Quantity Sold')
plt.ylabel('Size')
plt.tight_layout()
plt.show()

### 4. Fulfillment Analysis

# Fulfillment method analysis
fulfillment_distribution = final_data['fulfilled-by'].value_counts().reset_index()
fulfillment_distribution.columns = ['Fulfilled By', 'Count']

# Plot fulfillment methods
plt.figure(figsize=(8,5))
sns.barplot(x='Count', y='Fulfilled By', data=fulfillment_distribution)
plt.title('Fulfillment Methods Distribution')
plt.xlabel('Number of Orders')
plt.ylabel('Fulfilled By')
plt.tight_layout()
plt.show()

### 5. Customer Segmentation

# Customer segmentation by city
customer_segmentation = final_data.groupby('ship-city')['Qty'].sum().reset_index()

# Plot customer segmentation by city
plt.figure(figsize=(10,6))
sns.barplot(x='Qty', y='ship-city', data=customer_segmentation.sort_values(by='Qty', ascending=False).head(10))
plt.title('Top 10 Cities by Quantity Purchased')
plt.xlabel('Quantity')
plt.ylabel('City')
plt.tight_layout()
plt.show()

# Customer segmentation by state
state_segmentation = final_data.groupby('ship-state')['Qty'].sum().reset_index()

# Plot customer segmentation by state
plt.figure(figsize=(10,6))
sns.barplot(x='Qty', y='ship-state', data=state_segmentation.sort_values(by='Qty', ascending=False).head(10))
plt.title('Top 10 States by Quantity Purchased')
plt.xlabel('Quantity')
plt.ylabel('State')
plt.tight_layout()
plt.show()

### 6. Geographical Sales Analysis

# Sales by city
city_sales = final_data.groupby('ship-city')['Amount'].sum().reset_index()

# Plot top cities by sales
plt.figure(figsize=(10,6))
sns.barplot(x='Amount', y='ship-city', data=city_sales.sort_values(by='Amount', ascending=False).head(10))
plt.title('Top 10 Cities by Sales Amount')
plt.xlabel('Total Sales')
plt.ylabel('City')
plt.tight_layout()
plt.show()

# Sales by state
state_sales = final_data.groupby('ship-state')['Amount'].sum().reset_index()

# Plot top states by sales
plt.figure(figsize=(10,6))
sns.barplot(x='Amount', y='ship-state', data=state_sales.sort_values(by='Amount', ascending=False).head(10))
plt.title('Top 10 States by Sales Amount')
plt.xlabel('Total Sales')
plt.ylabel('State')
plt.tight_layout()
plt.show()

### 7. Advanced Customer Segmentation (RFM)

# RFM (Recency, Frequency, Monetary) analysis
rfm = final_data.groupby('ship-city').agg({
    'Date': lambda x: (pd.to_datetime('today') - pd.to_datetime(x).max()).days,
    'Order ID': 'count',
    'Amount': 'sum'
}).rename(columns={'Date': 'Recency', 'Order ID': 'Frequency', 'Amount': 'Monetary'})


### 9. Correlation Analysis

# Correlation heatmap
plt.figure(figsize=(10,8))
sns.heatmap(final_data.corr(), annot=True, cmap='coolwarm', fmt='.2f')
plt.title('Correlation Between Key Metrics')
plt.tight_layout()
plt.show()


