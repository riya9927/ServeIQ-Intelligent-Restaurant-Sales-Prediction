# ServeIQ-Intelligent-Restaurant-Sales-Prediction

## 🧠 Project Overview
In today’s competitive and fast-changing market, predicting future sales is crucial for business planning and decision-making. The ServeIQ project aims to leverage historical sales data to build accurate forecasting models that predict item-wise sales across multiple restaurants. The insights gained help businesses optimize inventory, staffing, and production planning to improve efficiency and profitability.

## 🎯 Problem Statement
Fresh Analytics, a data analytics firm, is tasked with understanding and forecasting item-level demand across a network of restaurants. The challenge is to accurately predict future sales trends from past data to enable restaurant managers to make better operational decisions.

## 🔍 Objectives
- Analyze historical sales patterns at different time granularities: daily, weekly, monthly, and quarterly
- Identify best-performing restaurants and top-selling items
- Determine sales trends and seasonality across multiple locations
- Build machine learning and deep learning models to forecast future item sales
- Evaluate model performance and generate accurate forecasts for practical business use

## 📁 Datasets Used
- `restaurants.csv` — Contains information about each restaurant including store ID and name
- `items.csv` — Item-level details such as item name, calories, and cost
- `sales.csv` — Date-wise transactional records containing item name, price, and item count sold

## 🛠 Project Phases

---

### 🧪 Step 1: Data Analysis

### 1. Preliminary Analysis
#### ✅ Objective:
Prepare the data for further exploration by loading, inspecting, and merging datasets.
#### 🔍 Actions Performed:
- Imported datasets using pandas
- Inspected shape, structure, and missing values
- Merged all datasets on appropriate keys (`item_name`, `store_id`, etc.)
- Created a unified DataFrame with the following columns:
  - `date`, `item_id`, `item_name`, `store_id`, `store_name`, `kcal`, `cost`, `item_count`, `price`
  - 
#### 2. Exploratory Data Analysis (EDA)
#####  a. Date-wise Sales Trend
- Aggregated total sales over time
- Visualized sales trends using line plots
- Observed seasonal spikes and drops in demand

##### b. Day-of-Week Analysis
- Extracted weekday from `date`
- Analyzed sales patterns for each day of the week
- Identified high and low performing weekdays

##### c. Monthly Sales Trends
- Grouped sales by month to analyze trends
- Identified months with consistent high or low sales

##### d. Quarterly Sales Distribution
- Extracted quarter from dates
- Averaged sales across quarters for pattern identification
- Useful to inform quarterly business planning

##### e. Restaurant Performance Comparison
- Aggregated sales by restaurant
- Analyzed sales across years, months, and days per restaurant
- Identified top-performing and underperforming stores

##### Interactive Dashboard
Explore the sales trends and forecasts interactively using our Streamlit app:

[ServeIQ Sales Forecasting Dashboard](https://serveiq-intelligent-restaurant-sales-prediction.streamlit.app/)



