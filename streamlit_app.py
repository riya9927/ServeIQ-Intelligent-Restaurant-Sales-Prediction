import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Page config
st.set_page_config(page_title="ServeIQ Dashboard", layout="wide")
st.title("📊 ServeIQ Sales Analytics Dashboard")

# Load merged dataset
merged_df = pd.read_csv("C:/Users/Riya/jupyter notebook/Capstone/merged_data.csv")
merged_df['date'] = pd.to_datetime(merged_df['date'])
merged_df['total_sales'] = merged_df['price'] * merged_df['item_count']

# Helper to display matplotlib figures
def show_fig(fig):
    st.pyplot(fig)

# 📈 Total Sales Over Time
st.subheader("📈 Total Sales Over Time")
daily_sales = merged_df.groupby('date')['total_sales'].sum().reset_index()
fig, ax = plt.subplots(figsize=(14, 5))
sns.lineplot(data=daily_sales, x='date', y='total_sales', ax=ax)
ax.set_title("Total Sales Over Time"); ax.set_xlabel("Date"); ax.set_ylabel("Total Sales")
ax.tick_params(axis='x', rotation=45)
ax.grid(True)
show_fig(fig)

# 📊 Weekly Sales
st.subheader("📆 Sales by Day of the Week")
merged_df['day_of_week'] = merged_df['date'].dt.day_name()
week_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
weekly_sales = merged_df.groupby('day_of_week')['total_sales'].sum().reindex(week_order).reset_index()
fig, ax = plt.subplots(figsize=(10, 6))
sns.barplot(data=weekly_sales, x='day_of_week', y='total_sales', palette='viridis', ax=ax)
ax.set_title("Total Sales by Day of Week"); ax.set_xlabel("Day"); ax.set_ylabel("Total Sales")
show_fig(fig)

# 📅 Monthly Sales
st.subheader("📅 Monthly Sales Trend")
merged_df['month'] = merged_df['date'].dt.month_name()
merged_df['month_num'] = merged_df['date'].dt.month
monthly_sales = merged_df.groupby(['month', 'month_num'])['total_sales'].sum().reset_index()
monthly_sales = monthly_sales.sort_values('month_num')
fig, ax = plt.subplots(figsize=(12, 6))
sns.barplot(data=monthly_sales, x='month', y='total_sales', palette='magma', ax=ax)
ax.set_title("Sales Trend by Month"); ax.set_xlabel("Month"); ax.set_ylabel("Total Sales")
ax.tick_params(axis='x', rotation=45)
show_fig(fig)

# 📉 Quarterly Average
st.subheader("📊 Average Quarterly Sales")
merged_df['quarter'] = merged_df['date'].dt.quarter
merged_df['year'] = merged_df['date'].dt.year
quarterly_sales = merged_df.groupby(['year', 'quarter'])['total_sales'].sum().reset_index()
avg_quarterly_sales = quarterly_sales.groupby('quarter')['total_sales'].mean().reset_index()
fig, ax = plt.subplots(figsize=(8, 5))
sns.barplot(data=avg_quarterly_sales, x='quarter', y='total_sales', palette='cubehelix', ax=ax)
ax.set_title("Avg Quarterly Sales Across Years"); ax.set_xlabel("Quarter"); ax.set_ylabel("Average Sales")
ax.set_xticklabels(['Q1', 'Q2', 'Q3', 'Q4'])
show_fig(fig)

# 🍴 Sales per Restaurant
st.subheader("🏪 Total Sales per Restaurant")
sales_per_restaurant = merged_df.groupby('store_name')['total_sales'].sum().reset_index().sort_values('total_sales', ascending=False)
fig, ax = plt.subplots(figsize=(10, 5))
sns.barplot(data=sales_per_restaurant, x='store_name', y='total_sales', palette='Set2', ax=ax)
ax.set_title("Total Sales by Restaurant"); ax.set_xlabel("Restaurant"); ax.set_ylabel("Sales")
ax.tick_params(axis='x', rotation=45)
show_fig(fig)

# 🔁 Yearly Sales by Restaurant
st.subheader("📆 Yearly Sales by Restaurant")
yearly_sales = merged_df.groupby(['store_name', 'year'])['total_sales'].sum().reset_index()
fig, ax = plt.subplots(figsize=(12, 6))
sns.lineplot(data=yearly_sales, x='year', y='total_sales', hue='store_name', marker='o', ax=ax)
ax.set_title("Yearly Sales by Restaurant"); ax.set_xlabel("Year"); ax.set_ylabel("Sales")
ax.grid(True)
show_fig(fig)

# 🔄 Monthly Sales by Restaurant
st.subheader("📈 Monthly Sales by Restaurant")
monthly_store_sales = merged_df.groupby(['store_name', 'month'])['total_sales'].sum().reset_index()
month_order = ['January', 'February', 'March', 'April', 'May', 'June',
               'July', 'August', 'September', 'October', 'November', 'December']
monthly_store_sales['month'] = pd.Categorical(monthly_store_sales['month'], categories=month_order, ordered=True)
monthly_store_sales = monthly_store_sales.sort_values('month')
fig, ax = plt.subplots(figsize=(14, 6))
sns.lineplot(data=monthly_store_sales, x='month', y='total_sales', hue='store_name', marker='o', ax=ax)
ax.set_title("Monthly Sales by Restaurant"); ax.set_xlabel("Month"); ax.set_ylabel("Sales")
ax.tick_params(axis='x', rotation=45)
show_fig(fig)

# 📅 Daily Sales by Restaurant
st.subheader("🗓️ Day of Week Sales by Restaurant")
daily_sales_rest = merged_df.groupby(['store_name', 'day_of_week'])['total_sales'].sum().reset_index()
daily_sales_rest['day_of_week'] = pd.Categorical(daily_sales_rest['day_of_week'], categories=week_order, ordered=True)
daily_sales_rest = daily_sales_rest.sort_values('day_of_week')
fig, ax = plt.subplots(figsize=(12, 5))
sns.lineplot(data=daily_sales_rest, x='day_of_week', y='total_sales', hue='store_name', marker='o', ax=ax)
ax.set_title("Day-wise Sales by Restaurant"); ax.set_xlabel("Day"); ax.set_ylabel("Sales")
show_fig(fig)

# 🔝 Top 5 Items per Restaurant
st.subheader("🔥 Top 5 Selling Items per Restaurant")
item_sales = merged_df.groupby(['store_name', 'item_name'])['total_sales'].sum().reset_index()
top_items = item_sales.sort_values(['store_name', 'total_sales'], ascending=[True, False])
top5 = top_items.groupby('store_name').head(5)
fig, ax = plt.subplots(figsize=(14, 7))
sns.barplot(data=top5, x='total_sales', y='item_name', hue='store_name', dodge=False, ax=ax)
ax.set_title("Top 5 Items by Restaurant"); ax.set_xlabel("Sales"); ax.set_ylabel("Item")
ax.legend(title="Restaurant")
show_fig(fig)

# 🌡️ Heatmap: Day of Week vs Month
st.subheader("🌡️ Sales Heatmap: Day of Week vs Month")
heatmap_df = merged_df.copy()
heatmap_df['month'] = heatmap_df['date'].dt.month_name()
heatmap_df['day_of_week'] = heatmap_df['date'].dt.day_name()
heatmap_data = heatmap_df.groupby(['day_of_week', 'month'])['total_sales'].sum().reset_index()
heatmap_pivot = heatmap_data.pivot(index='day_of_week', columns='month', values='total_sales')
heatmap_pivot = heatmap_pivot.reindex(index=week_order, columns=month_order)
fig, ax = plt.subplots(figsize=(12, 6))
sns.heatmap(heatmap_pivot, cmap='YlOrBr', annot=True, fmt='.0f', linewidths=0.5, ax=ax)
ax.set_title("Heatmap: Sales by Day and Month")
show_fig(fig)
