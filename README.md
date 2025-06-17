# 📊 Inventory and Sales Data Analysis


[![Python 3.x](https://img.shields.io/badge/Python-3.x-blue.svg)](https://www.python.org/downloads/)
[![Project Status](https://img.shields.io/badge/Status-Completed-brightgreen)](https://github.com/your-username/your-repo-name)

Welcome to the Inventory and Sales Data Analysis project! 🚀 This repository houses a robust set of Python scripts designed to provide deep insights into a company's inventory, purchases, sales, and vendor performance. By transforming raw data into a comprehensive vendor summary table, we unlock crucial metrics like profitability, stock turnover, and freight costs, empowering data-driven strategic decisions.




## 🏗️ Project Structure

Our project is organized for clarity and efficiency:

![Project Structure Diagram](https://github.com/user-attachments/assets/29dc60dd-8dc1-4cda-b3d2-eb6e5c5e4db1)

---

## 🗃️ Data

The `data/` directory contains the raw CSV files that serve as the foundation for our analysis. These include:

* `begin_inventory.csv`: Records of initial inventory levels.
* `end_inventory.csv`: Records of final inventory levels.
* `purchase_prices.csv`: Detailed information on product purchase prices.
* `purchases.csv`: Comprehensive records of all vendor purchase transactions.
* `sales.csv`: All sales transaction data.
* `vendor_invoice.csv`: Vendor invoice details, crucial for freight cost analysis.

> ⚠️ **Important Note on Data Availability:**
> The datasets used in this project were obtained from a paid source and are **not included** in this GitHub repository. To replicate the analysis, you would need to acquire similar inventory and sales data.

---

## 📝 Log Files

The `logs/` directory stores `ingestion_db.log`, capturing detailed insights into the data ingestion and summary table creation processes. This helps in monitoring and debugging.
*Screenshot of Ingestion Log:*
![Ingestion Log Snippet](https://github.com/user-attachments/assets/98728664-ff1e-43c5-b6f2-f2130aefc3b1)

---

## ✨ Key Features

This project provides a comprehensive solution for inventory and sales analysis, featuring:

* **Data Ingestion 📥:** Efficiently loads raw CSV files into an SQLite database (`inventory.db`) for structured storage.
* **Robust Database Management 🗄️:** Leverages `sqlite3` and `sqlalchemy` for seamless database operations, complemented by `pandas` for data manipulation.
* **Comprehensive Summary Table Creation 📊:** Joins various operational tables (`purchases`, `purchase_prices`, `vendor_invoice`, `sales`) to construct a holistic `final_summary_table` (aliased as `vendor_summary` in the DB). This table integrates:
    * Vendor purchase transaction details
    * Sales transaction data
    * Per-vendor freight costs
    * Actual product prices from vendors
* **Intelligent Data Cleaning & Transformation 🧹:**
    * Converts data types (e.g., `Volume` to `float64`) for accurate calculations.
    * Fills missing values with 0 to maintain data integrity.
    * Strips leading/trailing spaces from string columns (`VendorName`, `Description`) for consistency.
* **Key Performance Indicator (KPI) Calculation 📈:** Derives crucial analytical metrics:
    * `GrossProfit`
    * `ProfitMargin`
    * `StockTurnover`
    * `SalesToPurchaseRatio`
* **Thorough Exploratory Data Analysis (EDA) 🔍:** Delivers detailed statistical summaries, distribution plots (histograms, box plots), and correlation heatmaps to reveal data characteristics, patterns, and relationships.
* **Actionable Targeted Analysis & Insights 🎯:** Identifies specific business opportunities and challenges, including:
    * Brands requiring promotional or pricing adjustments (low sales, high profit margins).
    * Top-performing vendors and brands based on sales revenue.
    * Vendors contributing most to total procurement cost (via Pareto analysis).
    * The direct impact of bulk purchasing on unit price.
    * Vendors with low inventory turnover and high unsold inventory value, indicating potential overstocking.
* **Rigorous Hypothesis Testing ✅:** Conducts statistical tests (e.g., Two-Sample t-test) to validate insights, such as significant differences in profit margins between top-performing and low-performing vendors.
* **Detailed Logging ✍️:** Provides comprehensive logs of all ingestion and data processing steps for transparency and traceability.

---

## 📜 Scripts

This project is powered by several interconnected Python scripts, each serving a distinct purpose in the data pipeline.

### `ingestion_DB.py`

This script is the entry point for raw data loading. It systematically ingests all CSV files from the `data/` directory into the SQLite database.

### `eda.py`

This script focuses on initial data exploration within the database. It demonstrates how to query and inspect the ingested tables, perform basic aggregations, and understand the raw data structure.

### `get_summary_table.py`

This is the core data processing script. It's responsible for joining disparate tables and calculating the derived KPIs to build the comprehensive `vendor_summary` table, which is then stored back in the database for analysis.

### `visualanalysis.py`

The powerhouse of insights! This script performs in-depth statistical analysis and generates a suite of visualizations from the `vendor_summary` table, helping to answer key business questions and validate hypotheses.

---

## 📈 Visual Insights

`visualanalysis.py` generates various charts to provide a clear picture of the inventory and sales data.

### Numerical Columns Distributions (Histograms and Box Plots)

These plots help us understand the spread, central tendency, and outliers for key numerical variables like Purchase Price, Actual Price, Gross Profit, etc.

*Histograms showing the frequency distribution of various numerical columns:*
![Numerical Columns Histograms 1](https://github.com/user-attachments/assets/5b16e2ea-c255-4a5b-a7ed-025fe35d05d4)
![Numerical Columns Histograms 2](https://github.com/user-attachments/assets/836e14d1-eb4a-4dab-9452-7a1f7a14b6c7)

*Box plots highlighting the spread and potential outliers in numerical columns:*
![Numerical Columns Box Plots 1](https://github.com/user-attachments/assets/f0fc82db-b735-499d-9d5b-7d8f8c597391)
![Numerical Columns Box Plots 2](https://github.com/user-attachments/assets/60b9cc05-e01f-47c2-b491-a568754e8345)

---

### Categorical Data Frequency

Understand the most frequent vendors and product descriptions.

*Frequency of Top Vendors and Product Descriptions:*
![Top Categorical Frequencies](https://github.com/user-attachments/assets/6f88bcdf-cfc6-4424-8fe4-5e1cd3f01f3d)

---

### Correlation Heatmap

Visualize the relationships between different numerical variables. A strong positive correlation (closer to 1) means they move in the same direction, while a strong negative correlation (closer to -1) means they move in opposite directions.

*Correlation Matrix for Numerical Columns:*
![Correlation Heatmap](https://github.com/user-attachments/assets/cfed4dc2-ba26-4e09-b5d8-a64b57e7bb9a)

---

### Brands for Promotional or Pricing Adjustments

Identifying brands with low sales but high profit margins—prime candidates for strategic adjustments.

*Scatter plot showing brands for potential promotional or pricing adjustments:*
![Brands for Promo/Pricing Adjustments](https://github.com/user-attachments/assets/d42c3909-acc9-4ef3-b860-1bd5cf07b45f)

---

### Top Sales Performance: Vendors & Brands

Highlighting the top contributors to total sales dollars.

*Bar charts showcasing the Top 10 Vendors and Top 10 Brands by Total Sales Dollars:*
![Top Vendors and Brands Sales](https://github.com/user-attachments/assets/f18933b3-c6ad-4424-8fe4-5e1cd3f01f3d)

---

### Vendor Procurement Cost Contribution (Pareto & Donut Charts)

Analyzing which vendors contribute most to total purchase costs and the cumulative impact.

*Pareto Chart illustrating Vendor Purchase Contribution and Cumulative Contribution:*
![Vendor Purchase Pareto Chart](https://github.com/user-attachments/assets/6695e028-8029-42f4-9883-74d722f54798)

*Donut Chart displaying the Top 10 Vendor's contribution to total procurement cost:*
![Vendor Procurement Donut Chart](https://github.com/user-attachments/assets/692ea7b3-94a1-4921-83c4-ded20ff8cb39)

---

### Bulk Purchasing Impact on Unit Price

Investigating if larger order sizes lead to reduced unit costs.

*Box plot demonstrating the relationship between order size (Small, Medium, Large) and Unit Price:*
![Unit Price by Order Size Box Plot](https://github.com/user-attachments/assets/824c6906-f835-40eb-b920-148a394aeaa1)

---

### Profit Margin Comparison (Top vs. Low-Performing Vendors)

A statistical comparison of profit margins between vendors with high and low sales performance.

*Histogram comparing the distribution and confidence intervals of profit margins for top vs. low-performing vendors:*
![Profit Margin Confidence Interval Comparison](https://github.com/user-attachments/assets/516a5b81-a9f8-45ff-8178-5a21e6463943)
*(Note: Please ensure the correct URL for this image. The one provided previously was a placeholder.)*



## 🗄️ Database Schema

The `final_summary_table` (which is stored as `vendor_summary` in the database) has the following structure:

```sql
CREATE TABLE final_summary_table (
    VendorNumber INTEGER,
    VendorName VARCHAR(100),
    Brand INTEGER,
    Description VARCHAR(100),
    PurchasePrice DECIMAL(10, 2),
    ActualPrice DECIMAL(10, 2),
    Volume FLOAT,
    TotalPurchaseQuantity INTEGER,
    TotalPurchaseDollars DECIMAL(10, 2),
    TotalSalesQuantity INTEGER,
    TotalSalesDollars DECIMAL(15, 2),
    TotalSalesPrice DECIMAL(15, 2),
    TotalExciseTax DECIMAL(15, 2),
    FreightCost DECIMAL(15, 2),
    GrossProfit DECIMAL(15, 2),
    ProfitMargin DECIMAL(15, 2),
    StockTurnover DECIMAL(15, 2),
    SalesToPurchaseRatio DECIMAL(15, 2),
    PRIMARY KEY (VendorNumber, Brand)
);



