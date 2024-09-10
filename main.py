
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



# -------------------------------------------------Example Analysis Code----------------------------------------------------------
final_data = cleared_data


# Define the specific statuses to exclude from sales calculations
specific_statuses = [
    'Cancelled', 'Shipped - Returned to Seller', 'Shipped - Rejected by Buyer',
    'Shipped - Lost in Transit', 'Shipped - Damaged'
]

# Filter out rows with these specific statuses
valid_sales_data = final_data[~final_data['Status'].isin(specific_statuses)]


# Sales over time (excluding invalid statuses)
sales_over_time = valid_sales_data.groupby('Date')['Amount'].sum().reset_index()

# Plotting sales trends (with valid data only)
plt.figure(figsize=(10, 6))
sns.lineplot(x='Date', y='Amount', data=sales_over_time)
plt.title('Sales Performance Over Time (Excluding Cancelled/Returned Orders)')
plt.xlabel('Date')
plt.ylabel('Total Sales Amount')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()


# Product category distribution
category_distribution = valid_sales_data.groupby('Category')['Qty'].sum().reset_index()

# Plotting product distribution
plt.figure(figsize=(8, 5))
sns.barplot(x='Qty', y='Category', data=category_distribution)
plt.title('Product Category Distribution (Excluding Invalid Orders)')
plt.xlabel('Quantity Sold')
plt.ylabel('Category')
plt.tight_layout()
plt.show()


# Size analysis
size_distribution = valid_sales_data.groupby('Size')['Qty'].sum().reset_index()

# Plotting size distribution
plt.figure(figsize=(8,5))
sns.barplot(x='Qty', y='Size', data=size_distribution)
plt.title('Product Size Distribution')
plt.xlabel('Quantity Sold')
plt.ylabel('Size')
plt.tight_layout()
plt.show()


# Fulfillment method analysis
fulfillment_distribution = valid_sales_data['fulfilled-by'].value_counts().reset_index()
fulfillment_distribution.columns = ['Fulfilled By', 'Count']

# Plotting fulfillment methods
plt.figure(figsize=(8,5))
sns.barplot(x='Count', y='Fulfilled By', data=fulfillment_distribution)
plt.title('Fulfillment Methods Distribution')
plt.xlabel('Number of Orders')
plt.ylabel('Fulfilled By')
plt.tight_layout()
plt.show()


# Fulfilled vs. unfulfilled orders
status_distribution = valid_sales_data['Status'].value_counts().reset_index()
status_distribution.columns = ['Status', 'Count']

# Plotting order statuses
plt.figure(figsize=(8,5))
sns.barplot(x='Count', y='Status', data=status_distribution)
plt.title('Order Fulfillment Status')
plt.xlabel('Number of Orders')
plt.ylabel('Status')
plt.tight_layout()
plt.show()


# Customer segmentation based on quantity purchased
customer_segmentation = valid_sales_data.groupby('ship-city')['Qty'].sum().reset_index()

# Plotting customer segmentation by city
plt.figure(figsize=(10,6))
sns.barplot(x='Qty', y='ship-city', data=customer_segmentation.sort_values(by='Qty', ascending=False).head(10))
plt.title('Top 10 Cities by Quantity Purchased')
plt.xlabel('Quantity')
plt.ylabel('City')
plt.tight_layout()
plt.show()


# Customer segmentation by state
state_segmentation = valid_sales_data.groupby('ship-state')['Qty'].sum().reset_index()

# Plotting customer segmentation by state
plt.figure(figsize=(10,6))
sns.barplot(x='Qty', y='ship-state', data=state_segmentation.sort_values(by='Qty', ascending=False).head(10))
plt.title('Top 10 States by Quantity Purchased')
plt.xlabel('Quantity')
plt.ylabel('State')
plt.tight_layout()
plt.show()


# Sales by city
city_sales = valid_sales_data.groupby('ship-city')['Amount'].sum().reset_index()

# Plotting top cities by sales
plt.figure(figsize=(10,6))
sns.barplot(x='Amount', y='ship-city', data=city_sales.sort_values(by='Amount', ascending=False).head(10))
plt.title('Top 10 Cities by Sales Amount')
plt.xlabel('Total Sales')
plt.ylabel('City')
plt.tight_layout()
plt.show()


# Sales by state
state_sales = valid_sales_data.groupby('ship-state')['Amount'].sum().reset_index()

# Plotting top states by sales
plt.figure(figsize=(10,6))
sns.barplot(x='Amount', y='ship-state', data=state_sales.sort_values(by='Amount', ascending=False).head(10))
plt.title('Top 10 States by Sales Amount')
plt.xlabel('Total Sales')
plt.ylabel('State')
plt.tight_layout()
plt.show()


# Filter data based on specific statuses
status_filtered_data = final_data[final_data['Status'].isin(specific_statuses)]

# Group the filtered data by Category and Status
category_status_distribution = status_filtered_data.groupby(['Category', 'Status'])['Qty'].sum().reset_index()

# Create a separate plot for each status
for status in specific_statuses:
    # Filter data for each status
    status_data = category_status_distribution[category_status_distribution['Status'] == status]

    # Plotting the product distribution for each status
    plt.figure(figsize=(8, 5))
    sns.barplot(x='Qty', y='Category', data=status_data)
    plt.title(f'Product Distribution for Status: {status}')
    plt.xlabel('Quantity')
    plt.ylabel('Product Category')
    plt.tight_layout()
    plt.show()




