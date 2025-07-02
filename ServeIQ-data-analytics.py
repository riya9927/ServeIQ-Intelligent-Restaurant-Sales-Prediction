import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="ServeIQ Dashboard", layout="wide")
st.title("📊 ServeIQ Sales Analytics Dashboard")

merged_df = pd.read_csv("C:/Users/Riya/jupyter notebook/Capstone/merged_data.csv")

merged_df['date'] = pd.to_datetime(merged_df['date'])
merged_df['total_sales'] = merged_df['price'] * merged_df['item_count']

restaurants = merged_df['store_name'].unique().tolist()

restaurants.sort()

st.sidebar.header("Filter Options")

# Create restaurant options with "All Restaurants" as first option
restaurant_options = ["All Restaurants"] + restaurants
selected_restaurant = st.sidebar.selectbox("Select Restaurant", options=restaurant_options, index=0)

min_date = merged_df['date'].min()
max_date = merged_df['date'].max()

selected_date_range = st.sidebar.date_input("Select Date Range", value=(min_date, max_date),min_value=min_date, max_value=max_date)

if len(selected_date_range) == 2:
    start_date, end_date = selected_date_range
else:
    start_date = min_date
    end_date = max_date

# Filter data based on restaurant selection
if selected_restaurant == "All Restaurants":
    filtered_data = merged_df[
        (merged_df['date'] >= pd.to_datetime(start_date)) &
        (merged_df['date'] <= pd.to_datetime(end_date))
    ]
    st.info(f"📍 Showing data for: **All Restaurants** ({len(restaurants)} restaurants)")
else:
    filtered_data = merged_df[
        (merged_df['store_name'] == selected_restaurant) &
        (merged_df['date'] >= pd.to_datetime(start_date)) &
        (merged_df['date'] <= pd.to_datetime(end_date))
    ]
    st.info(f"📍 Showing data for: **{selected_restaurant}**")

def show_fig(fig):
    st.pyplot(fig)

# 📈 Total Sales Over Time
st.subheader("📈 Total Sales Over Time")
daily_sales = filtered_data.groupby('date')['total_sales'].sum().reset_index()
fig, ax = plt.subplots(figsize=(14, 5))
sns.lineplot(data=daily_sales, x='date', y='total_sales', ax=ax)
ax.set_title("Total Sales Over Time")
ax.set_xlabel("Date")
ax.set_ylabel("Total Sales")
ax.tick_params(axis='x', rotation=45)
ax.grid(True)
show_fig(fig)

# 📊 Weekly Sales
st.subheader("📆 Sales by Day of the Week")
filtered_data['day_of_week'] = filtered_data['date'].dt.day_name()
week_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
weekly_sales = filtered_data.groupby('day_of_week')['total_sales'].sum().reindex(week_order).reset_index()
fig, ax = plt.subplots(figsize=(10, 6))
sns.barplot(data=weekly_sales, x='day_of_week', y='total_sales', palette='viridis', ax=ax)
ax.set_title("Total Sales by Day of Week")
ax.set_xlabel("Day")
ax.set_ylabel("Total Sales")
show_fig(fig)

# 📅 Monthly Sales
st.subheader("📅 Monthly Sales Trend")
filtered_data['month'] = filtered_data['date'].dt.month_name()
filtered_data['month_num'] = filtered_data['date'].dt.month
monthly_sales = filtered_data.groupby(['month', 'month_num'])['total_sales'].sum().reset_index()
monthly_sales = monthly_sales.sort_values('month_num')
fig, ax = plt.subplots(figsize=(12, 6))
sns.barplot(data=monthly_sales, x='month', y='total_sales', palette='magma', ax=ax)
ax.set_title("Sales Trend by Month")
ax.set_xlabel("Month")
ax.set_ylabel("Total Sales")
ax.tick_params(axis='x', rotation=45)
show_fig(fig)

# 📉 Quarterly Average
st.subheader("📊 Average Quarterly Sales")
filtered_data['quarter'] = filtered_data['date'].dt.quarter
filtered_data['year'] = filtered_data['date'].dt.year
quarterly_sales = filtered_data.groupby(['year', 'quarter'])['total_sales'].sum().reset_index()
avg_quarterly_sales = quarterly_sales.groupby('quarter')['total_sales'].mean().reset_index()
fig, ax = plt.subplots(figsize=(8, 5))
sns.barplot(data=avg_quarterly_sales, x='quarter', y='total_sales', palette='cubehelix', ax=ax)
ax.set_title("Avg Quarterly Sales Across Years")
ax.set_xlabel("Quarter")
ax.set_ylabel("Average Sales")
ax.set_xticklabels(['Q1', 'Q2', 'Q3', 'Q4'])
show_fig(fig)

# 🍴 Sales per Restaurant (only show if "All Restaurants" is selected)
if selected_restaurant == "All Restaurants":
    st.subheader("🏪 Total Sales per Restaurant")
    sales_per_restaurant = filtered_data.groupby('store_name')['total_sales'].sum().reset_index().sort_values('total_sales', ascending=False)
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.barplot(data=sales_per_restaurant, x='store_name', y='total_sales', palette='Set2', ax=ax)
    ax.set_title("Total Sales by Restaurant")
    ax.set_xlabel("Restaurant")
    ax.set_ylabel("Sales")
    ax.tick_params(axis='x', rotation=45)
    show_fig(fig)
    # 🔁 Yearly Sales by Restaurant
    st.subheader("📆 Yearly Sales by Restaurant")
    yearly_sales = filtered_data.groupby(['store_name', 'year'])['total_sales'].sum().reset_index()
    fig, ax = plt.subplots(figsize=(12, 6))
    sns.lineplot(data=yearly_sales, x='year', y='total_sales', hue='store_name', marker='o', ax=ax)
    ax.set_title("Yearly Sales by Restaurant")
    ax.set_xlabel("Year")
    ax.set_ylabel("Sales")
    ax.grid(True)
    show_fig(fig)
    # 🔄 Monthly Sales by Restaurant
    st.subheader("📈 Monthly Sales by Restaurant")
    month_order = ['January', 'February', 'March', 'April', 'May', 'June','July', 'August', 'September', 'October', 'November', 'December']
    monthly_store_sales = filtered_data.groupby(['store_name', 'month'])['total_sales'].sum().reset_index()
    monthly_store_sales['month'] = pd.Categorical(monthly_store_sales['month'], categories=month_order, ordered=True)
    monthly_store_sales = monthly_store_sales.sort_values('month')
    fig, ax = plt.subplots(figsize=(14, 6))
    sns.lineplot(data=monthly_store_sales, x='month', y='total_sales', hue='store_name', marker='o', ax=ax)
    ax.set_title("Monthly Sales by Restaurant")
    ax.set_xlabel("Month")
    ax.set_ylabel("Sales")
    ax.tick_params(axis='x', rotation=45)
    show_fig(fig)
    # 📅 Daily Sales by Restaurant
    st.subheader("🗓️ Day of Week Sales by Restaurant")
    daily_sales_rest = filtered_data.groupby(['store_name', 'day_of_week'])['total_sales'].sum().reset_index()
    daily_sales_rest['day_of_week'] = pd.Categorical(daily_sales_rest['day_of_week'], categories=week_order, ordered=True)
    daily_sales_rest = daily_sales_rest.sort_values('day_of_week')
    fig, ax = plt.subplots(figsize=(12, 5))
    sns.lineplot(data=daily_sales_rest, x='day_of_week', y='total_sales', hue='store_name', marker='o', ax=ax)
    ax.set_title("Day-wise Sales by Restaurant")
    ax.set_xlabel("Day")
    ax.set_ylabel("Sales")
    show_fig(fig)

# 🔝 Top 5 Items (for selected restaurant or all restaurants)
if selected_restaurant == "All Restaurants":
    st.subheader("🔥 Top 5 Selling Items per Restaurant")
    item_sales = filtered_data.groupby(['store_name', 'item_name'])['total_sales'].sum().reset_index()
    top_items = item_sales.sort_values(['store_name', 'total_sales'], ascending=[True, False])
    top5 = top_items.groupby('store_name').head(5)
    fig, ax = plt.subplots(figsize=(14, 7))
    sns.barplot(data=top5, x='total_sales', y='item_name', hue='store_name', dodge=False, ax=ax)
    ax.set_title("Top 5 Items by Restaurant")
    ax.set_xlabel("Sales")
    ax.set_ylabel("Item")
    ax.legend(title="Restaurant")
    show_fig(fig)
else:
    st.subheader(f"🔥 Top 10 Selling Items - {selected_restaurant}")
    item_sales = filtered_data.groupby('item_name')['total_sales'].sum().reset_index()
    top_items = item_sales.sort_values('total_sales', ascending=False).head(10)
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(data=top_items, x='total_sales', y='item_name', palette='viridis', ax=ax)
    ax.set_title(f"Top 10 Items - {selected_restaurant}")
    ax.set_xlabel("Sales")
    ax.set_ylabel("Item")
    show_fig(fig)

# 🌡️ Heatmap: Day of Week vs Month
st.subheader("🌡️ Sales Heatmap: Day of Week vs Month")
heatmap_data = filtered_data.groupby(['day_of_week', 'month'])['total_sales'].sum().reset_index()
heatmap_pivot = heatmap_data.pivot(index='day_of_week', columns='month', values='total_sales')
month_order = ['January', 'February', 'March', 'April', 'May', 'June','July', 'August', 'September', 'October', 'November', 'December']
# Only reindex with months that exist in the data
existing_months = [month for month in month_order if month in heatmap_pivot.columns]
heatmap_pivot = heatmap_pivot.reindex(index=week_order, columns=existing_months)
fig, ax = plt.subplots(figsize=(12, 6))
sns.heatmap(heatmap_pivot, cmap='YlOrBr', annot=True, fmt='.0f', linewidths=0.5, ax=ax)
ax.set_title("Heatmap: Sales by Day and Month")
show_fig(fig)

# import pandas as pd

# sales_df = pd.read_csv('sales.csv')
# restaurants_df = pd.read_csv('resturants.csv')
# items_df = pd.read_csv('items.csv')

# sales_df.head(), restaurants_df.head(), items_df.head()

# sales_shape = sales_df.shape
# restaurants_shape = restaurants_df.shape
# items_shape = items_df.shape

# sales_info = sales_df.info()
# restaurants_info = restaurants_df.info()
# items_info = items_df.info()

# sales_desc = sales_df.describe()
# items_desc = items_df.describe()
# rest_desc = restaurants_df.describe()

# sales_shape, restaurants_shape, items_shape, sales_desc, items_desc, rest_desc

# restaurants_df.rename(columns={'id': 'store_id', 'name': 'store_name'}, inplace=True)
# items_df.rename(columns={'id': 'item_id', 'name': 'item_name'}, inplace=True)

# merged_df = sales_df.merge(items_df, on='item_id', how='left')
# merged_df = merged_df.merge(restaurants_df, on='store_id', how='left')
# merged_df['date'] = pd.to_datetime(merged_df['date'])
# merged_df.head()

# import matplotlib.pyplot as plt
# import seaborn as sns

# merged_df['total_sales'] = merged_df['price'] * merged_df['item_count']
# daily_sales = merged_df.groupby('date')['total_sales'].sum().reset_index()
# plt.figure(figsize=(14, 5))
# sns.lineplot(data=daily_sales, x='date', y='total_sales')
# plt.title('Total Sales Over Time')
# plt.xlabel('Date')
# plt.ylabel('Total Sales')
# plt.tight_layout()
# plt.grid(True)
# plt.xticks(rotation=45)
# plt.show()

# merged_df['day_of_week'] = merged_df['date'].dt.day_name()
# weekly_sales = merged_df.groupby('day_of_week')['total_sales'].sum().reindex([
#     'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'
# ]).reset_index()
# plt.figure(figsize=(10, 6))
# sns.barplot(data=weekly_sales, x='day_of_week', y='total_sales', palette='viridis')
# plt.title('Total Sales by Day of the Week')
# plt.xlabel('Day of the Week')
# plt.ylabel('Total Sales')
# plt.xticks(rotation=45)
# plt.tight_layout()
# plt.show()

# merged_df['month'] = merged_df['date'].dt.month_name()
# merged_df['month_num'] = merged_df['date'].dt.month
# monthly_sales = merged_df.groupby(['month', 'month_num'])['total_sales'].sum().reset_index()
# monthly_sales = monthly_sales.sort_values('month_num')
# plt.figure(figsize=(12, 6))
# sns.barplot(data=monthly_sales, x='month', y='total_sales', palette='magma')
# plt.title('Total Sales Trend Across Months')
# plt.xlabel('Month')
# plt.ylabel('Total Sales')
# plt.xticks(rotation=45)
# plt.tight_layout()
# plt.show()

# merged_df['year'] = merged_df['date'].dt.year
# merged_df['quarter'] = merged_df['date'].dt.quarter
# quarterly_sales = merged_df.groupby(['year', 'quarter'])['total_sales'].sum().reset_index()
# average_quarterly_sales = quarterly_sales.groupby('quarter')['total_sales'].mean().reset_index()
# plt.figure(figsize=(8, 5))
# sns.barplot(data=average_quarterly_sales, x='quarter', y='total_sales', palette='cubehelix')
# plt.title('Average Quarterly Sales Across Years')
# plt.xlabel('Quarter')
# plt.ylabel('Average Total Sales')
# plt.xticks([0, 1, 2, 3], ['Q1', 'Q2', 'Q3', 'Q4'])
# plt.tight_layout()
# plt.show()

# total_sales_restaurant = merged_df.groupby('store_name')['total_sales'].sum().sort_values(ascending=False).reset_index()
# plt.figure(figsize=(10, 5))
# sns.barplot(data=total_sales_restaurant, x='store_name', y='total_sales', palette='Set2')
# plt.title('Total Sales per Restaurant')
# plt.xlabel('Restaurant')
# plt.ylabel('Total Sales')
# plt.xticks(rotation=45)
# plt.tight_layout()
# plt.show()

# yearly_sales = merged_df.groupby(['store_name', 'year'])['total_sales'].sum().reset_index()
# plt.figure(figsize=(12, 6))
# sns.lineplot(data=yearly_sales, x='year', y='total_sales', hue='store_name', marker='o')
# plt.title('Yearly Sales per Restaurant')
# plt.xlabel('Year')
# plt.ylabel('Total Sales')
# plt.grid(True)
# plt.tight_layout()
# plt.show()

# monthly_sales = merged_df.groupby(['store_name', 'month'])['total_sales'].sum().reset_index()
# month_order = ['January', 'February', 'March', 'April', 'May', 'June', 
#                'July', 'August', 'September', 'October', 'November', 'December']
# monthly_sales['month'] = pd.Categorical(monthly_sales['month'], categories=month_order, ordered=True)
# monthly_sales = monthly_sales.sort_values('month')
# plt.figure(figsize=(14, 6))
# sns.lineplot(data=monthly_sales, x='month', y='total_sales', hue='store_name', marker='o')
# plt.title('Monthly Sales per Restaurant')
# plt.xlabel('Month')
# plt.ylabel('Total Sales')
# plt.xticks(rotation=45)
# plt.tight_layout()
# plt.show()

# day_sales = merged_df.groupby(['store_name', 'day_of_week'])['total_sales'].sum().reset_index()
# day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
# day_sales['day_of_week'] = pd.Categorical(day_sales['day_of_week'], categories=day_order, ordered=True)
# day_sales = day_sales.sort_values('day_of_week')
# plt.figure(figsize=(12, 5))
# sns.lineplot(data=day_sales, x='day_of_week', y='total_sales', hue='store_name', marker='o')
# plt.title('Day of Week Sales per Restaurant')
# plt.xlabel('Day of the Week')
# plt.ylabel('Total Sales')
# plt.xticks(rotation=45)
# plt.tight_layout()
# plt.show()

# item_sales = merged_df.groupby(['store_name', 'item_name'])['total_sales'].sum().reset_index()
# top_items = item_sales.sort_values(['store_name', 'total_sales'], ascending=[True, False])
# top_5_items_per_restaurant = top_items.groupby('store_name').head(5)
# plt.figure(figsize=(14, 7))
# sns.barplot(data=top_5_items_per_restaurant, x='total_sales', y='item_name', hue='store_name', dodge=False)
# plt.title('Top 5 Selling Items per Restaurant (by Revenue)')
# plt.xlabel('Total Sales')
# plt.ylabel('Item Name')
# plt.legend(title='Restaurant')
# plt.tight_layout()
# plt.show()

# heatmap_df = merged_df.copy()
# heatmap_df['month'] = heatmap_df['date'].dt.month_name()
# heatmap_df['day_of_week'] = heatmap_df['date'].dt.day_name()
# heatmap_data = heatmap_df.groupby(['day_of_week', 'month'])['total_sales'].sum().reset_index()
# month_order = ['January', 'February', 'March', 'April', 'May', 'June', 
#                'July', 'August', 'September', 'October', 'November', 'December']
# day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
# heatmap_pivot = heatmap_data.pivot(index='day_of_week', columns='month', values='total_sales')
# heatmap_pivot = heatmap_pivot.reindex(index=day_order, columns=month_order)
# plt.figure(figsize=(12, 6))
# sns.heatmap(heatmap_pivot, cmap='YlOrBr', annot=True, fmt='.0f', linewidths=0.5)
# plt.title('Sales Heatmap: Day of Week vs Month')
# plt.xlabel('Month')
# plt.ylabel('Day of Week')
# plt.tight_layout()
# plt.show()
