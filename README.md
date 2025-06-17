# Inventory and Sales Data Analysis

This repository contains Python scripts for ingesting, analyzing, and summarizing inventory and sales data. The project focuses on creating a comprehensive vendor summary table to gain insights into purchase transactions, sales performance, freight costs, and profitability, followed by in-depth visual and statistical analysis.

## Project Structure
![Project Structure Diagram](https://github.com/user-attachments/assets/29dc60dd-8dc1-4cda-b3d2-eb6e5c5e4db1)

## Data

The `data/` directory contains several CSV files that are used as input for the data ingestion and analysis process. These datasets include:

* `begin_inventory.csv`: Initial inventory records.
* `end_inventory.csv`: Final inventory records.
* `purchase_prices.csv`: Details about product purchase prices.
* `purchases.csv`: Records of vendor purchases.
* `sales.csv`: Records of sales transactions.
* `vendor_invoice.csv`: Vendor invoice details, including freight costs.

**Important Note on Data Availability:** Please be aware that the datasets used in this project were obtained from a paid source and are therefore **not included** in this GitHub repository. To replicate the analysis, you would need to acquire similar inventory and sales data.

## Log Files

The `logs/` directory contains `ingestion_db.log`, which logs the data ingestion and summary table creation processes. Here's a snippet demonstrating the successful ingestion and initial summary table creation:
![Ingestion Log Snippet](https://github.com/user-attachments/assets/98728664-ff1e-43c5-b6f2-f2130aefc3b1)

## Features

* **Data Ingestion:** Efficiently ingests multiple CSV files into an SQLite database (`inventory.db`).
* **Database Management:** Utilizes `sqlite3` and `sqlalchemy` for database operations and `pandas` for data manipulation.
* **Comprehensive Summary Table:** Joins various tables (`purchases`, `purchase_prices`, `vendor_invoice`, `sales`) to create a consolidated `final_summary_table` (stored as `vendor_summary` in the DB) that includes:
    * Vendor purchase transaction details
    * Sales transaction data
    * Freight costs for each vendor
    * Actual product prices from vendors
* **Data Cleaning and Transformation:**
    * Handles data type conversions (e.g., `Volume` to `float64`).
    * Fills missing values with 0.
    * Strips leading/trailing spaces from string columns (`VendorName`, `Description`).
* **Key Performance Indicators (KPIs):** Calculates insightful metrics such as:
    * `GrossProfit`
    * `ProfitMargin`
    * `StockTurnover`
    * `SalesToPurchaseRatio`
* **Exploratory Data Analysis (EDA):** Provides comprehensive statistical summaries, distribution plots (histograms, box plots), and correlation heatmaps to understand data characteristics and relationships.
* **Targeted Analysis & Insights:** Identifies specific business opportunities and challenges, such as:
    * Brands needing promotional or pricing adjustments (low sales, high profit margins).
    * Top-performing vendors and brands by sales dollars.
    * Vendors contributing most to total procurement cost (Pareto analysis).
    * Impact of bulk purchasing on unit price.
    * Vendors with low inventory turnover and high unsold inventory value.
* **Hypothesis Testing:** Conducts statistical tests (e.g., Two-Sample t-test) to validate insights, such as significant differences in profit margins between top and low-performing vendors.
* **Logging:** Provides detailed logging of the ingestion and data processing steps.

## Scripts

### `ingestion_DB.py`

This script is responsible for ingesting the raw CSV data from the `data` directory into the SQLite database.

* **`ingest_db(df, table_name, engine)`:** A utility function to ingest a pandas DataFrame into a specified table in the database, replacing it if it already exists.
* **`load_raw_data()`:** This is the main function that iterates through all `.csv` files found in the `data/` folder. For each CSV, it reads the data into a pandas DataFrame, logs the ingestion process, and then calls `ingest_db` to load the DataFrame into the `inventory.db` database. The table name in the database is derived from the CSV filename (e.g., `purchases.csv` becomes the `purchases` table).
* The script logs the start and end of the ingestion process, including the total time taken.

### `eda.py`

This script performs exploratory data analysis (EDA) and demonstrates how to query and inspect the ingested data within the SQLite database. It shows examples of:

* Listing all tables in the database.
* Counting records and displaying the first 5 rows of each table.
* Querying specific vendor data from `purchases`, `purchase_prices`, `vendor_invoice`, and `sales` tables.
* Performing aggregations (e.g., `groupby` on `Brand` and `PurchasePrice` for purchases).
* Calculating unique purchase order numbers.
* Summarizing sales data by `Brand`.
* Creating intermediate summary tables using SQL queries (`freight_summary`, `summary_table_1`, `summary_table_2`).

### `get_summary_table.py`

This is the core script for generating the comprehensive `vendor_summary` table.

1.  **`create_vendor_summary(conn)`:** This function executes a complex SQL query to join `purchases`, `purchase_prices`, `vendor_invoice`, and `sales` tables. It aggregates data to provide a holistic view of vendor activities, including purchase quantities and dollars, sales quantities and dollars, excise tax, and freight costs.
2.  **`clean_data(df)`:** This function applies several cleaning and transformation steps to the generated summary DataFrame:
    * Casts the `Volume` column to `float64`.
    * Fills any `NaN` values with `0`.
    * Removes leading/trailing whitespace from `VendorName` and `Description`.
    * Calculates new analytical columns: `GrossProfit`, `ProfitMargin`, `StockTurnover`, and `SalesToPurchaseRatio`.
3.  **Main Execution Block (`if __name__ == "__main__":`)**:
    * Establishes a connection to the `inventory.db` database.
    * Calls `create_vendor_summary` to build the initial summary DataFrame.
    * Calls `clean_data` to process and enhance the summary DataFrame.
    * Ingests the final cleaned summary DataFrame into a new table named `vendor_summary` in the `inventory.db` database.
    * Logs the entire process, providing insights into execution steps and data states.

### `visualanalysis.py`

This script performs in-depth statistical and visual analysis on the `final_summary_table` (which is named `vendor_summary` in the database after ingestion by `get_summary_table.py`).

* **Initial Data Overview:**
    * Connects to the `inventory.db` database and fetches the `final_summary_table` (aliased as `vendor_summary` in the database) into a pandas DataFrame.
    * Prints the head of the DataFrame and its summary statistics (`.describe().T`).

* **Exploratory Data Visualization:**
    * Generates histograms and box plots for all numerical columns to visualize their distributions, identify skewness, and detect outliers.
    * **Numerical Columns Distributions (Histograms):** (Visualizations available in the gallery)
        *(Note: These visualizations show distributions for various numerical columns like Purchase Price, Actual Price, Gross Profit, etc.)*

    * **Numerical Columns Distributions (Box Plots):** (Visualizations available in the gallery)
        *(Note: These visualizations display the spread and outliers for numerical columns using box plots.)*

    * Provides a commentary section to interpret insights from these plots, specifically addressing negative/zero values (e.g., in `GrossProfit`, `ProfitMargin`, `TotalSalesQuantity`) and the presence of outliers (e.g., in `Purchase & Actual Prices`, `Freight Cost`, `Stock Turnover`).

* **Data Filtering for Consistency:**
    * Filters the DataFrame to include only rows where `GrossProfit > 0`, `ProfitMargin > 0`, and `TotalSalesQuantity > 0`, to focus on meaningful sales and profitability data.

* **Categorical Data Frequency:**
    * Creates count plots for top categorical columns (`VendorName`, `Description`) to show their frequencies.
    * **Top Categorical Column Frequencies:** (Visualization available in the gallery)
        *(Note: This visualization shows the frequency of top vendors and product descriptions.)*

* **Correlation Analysis:**
    * Generates a correlation heatmap for numerical columns, with annotations to show the strength and direction of relationships between variables (e.g., purchase vs. sales quantities, profit margin vs. sales price, stock turnover vs. profitability).
    * **Correlation Heatmap:** (Visualization available in the gallery)
    * Provides "Rephrased Correlation Insights" to explain the implications of observed correlations.

* **Business Question: Brands for Promotional/Pricing Adjustments:**
    * Aggregates data by `Description` (Brand) to calculate `TotalSalesDollars` and `ProfitMargin`.
    * Identifies brands with `low sales performance` (below the 15th percentile of `TotalSalesDollars`) but `high profit margins` (above the 85th percentile of `ProfitMargin`).
    * Visualizes these target brands on a scatter plot, along with thresholds, to guide strategic decisions.
    * **Brands for Promotional or Pricing Adjustments:** (Visualization available in the gallery)

* **Business Question: Top Sales Performance & Profitability:**
    * Defines a helper function `format_dollars` for better readability of large monetary values.
    * Identifies and prints the top 10 vendors and brands by `TotalSalesDollars`.
    * Visualizes these top performers using side-by-side bar plots with formatted dollar values.
    * **Top 10 Vendors and Brands by Total Sales Dollars:** (Visualization available in the gallery)
        *(Note: This combines the bar plots for top vendors and top brands by sales.)*

* **Business Question: Vendor Procurement Cost Contribution:**
    * Aggregates `TotalPurchaseDollars`, `GrossProfit`, and `TotalSalesDollars` by `VendorName`.
    * Calculates `PurchaseContribution` for each vendor and the cumulative contribution of the top vendors.
    * Generates a **Pareto Chart** to visually represent vendor purchase contributions and their cumulative impact.
    * **Pareto Chart: Vendor Purchase Contribution:** (Visualization available in the gallery)
    * Also creates a **Donut Chart** to show the overall proportion of procurement cost attributed to the top 10 vendors versus others.
    * **Top 10 Vendor Procurement Cost Contribution (Donut Chart):** (Visualization available in the gallery)

* **Business Question: Bulk Purchasing Impact on Unit Price:**
    * Calculates `UnitPrice` from `TotalPurchaseDollars` and `TotalPurchaseQuantity`.
    * Categorizes `TotalPurchaseQuantity` into 'Small', 'Medium', and 'Large' `OrderSize` using `pd.qcut`.
    * Visualizes the mean `UnitPrice` by `OrderSize` using a bar plot and a box plot to show the distribution.
    * **Unit Price by Order Size (Box Plot):** (Visualization available in the gallery)
        *(Note: This visualization illustrates how unit price varies with order size.)*
    * Provides a commentary on the observed cost advantages of larger order sizes.

* **Business Question: Low Inventory Turnover & Unsold Inventory:**
    * Identifies vendors with `StockTurnover` less than 1, indicating slow-moving inventory.
    * Calculates `UnsoldInventoryValue` for each item and aggregates it by `VendorName` to find vendors with the most capital locked in unsold stock.

* **Hypothesis Testing: Profit Margin Difference between Top and Low-Performing Vendors:**
    * Divides vendors into `top_vendors` (top 25% by `TotalSalesDollars`) and `bottom_vendors` (bottom 25% by `TotalSalesDollars`).
    * Defines a `confidence_interval` function to calculate the mean and 95% confidence interval for profit margins.
    * Prints the confidence intervals for both groups.
    * Visualizes the profit margin distributions of top and low vendors using overlaid histograms with confidence interval lines.
    * **Confidence Interval Comparison: Top vs. Low Vendors (Profit Margin):** (Visualization available in the gallery)
        *(Note: The URL for this image was not provided in the last set, so I used a placeholder URL. Please replace with the correct one if available in your full gallery.)*
    * States the **Null (H₀)** and **Alternative (H₁)** Hypotheses for a two-sample t-test.
    * Performs a `ttest_ind` (independent t-test) comparing the profit margins of top and low-performing vendors.
    * Prints the t-statistic and p-value, and interprets the result to determine if there's a statistically significant difference in profit margins.
    * Offers actionable insights based on the confidence interval and hypothesis test results for both top and low-performing vendors.


## 🖼️ Visualizations Gallery

Here you can find all the visualizations generated by `visualanalysis.py`, offering a quick overview of the data insights.


![Numerical Columns Histograms 1](https://github.com/user-attachments/assets/5b16e2ea-c255-4a5b-a7ed-025fe35d05d4)
![Numerical Columns Histograms 2](https://github.com/user-attachments/assets/836e14d1-eb4a-4dab-9452-7a1f7a14b6c7)

![Numerical Columns Box Plots 1](https://github.com/user-attachments/assets/f0fc82db-b735-499d-9d5b-7d8f8c597391)
![Numerical Columns Box Plots 2](https://github.com/user-attachments/assets/60b9cc05-e01f-47c2-b491-a568754e8345)

![Top Categorical Frequencies](https://github.com/user-attachments/assets/6f88bcdf-cfc6-4424-8fe4-5e1cd3f01f3d)

![Correlation Heatmap](https://github.com/user-attachments/assets/cfed4dc2-ba26-4e09-b5d8-a64b57e7bb9a)

![Brands for Promo/Pricing Adjustments](https://github.com/user-attachments/assets/d42c3909-acc9-4ef3-b860-1bd5cf07b45f)

![Top Vendors and Brands Sales](https://github.com/user-attachments/assets/f18933b3-c6ad-4234-a308-6fbe8dfee18e)

![Vendor Purchase Pareto Chart](https://github.com/user-attachments/assets/6695e028-8029-42f4-9883-74d722f54798)

![Vendor Procurement Donut Chart](https://github.com/user-attachments/assets/692ea7b3-94a1-4921-83c4-ded20ff8cb39)

![Unit Price by Order Size Box Plot](https://github.com/user-attachments/assets/824c6906-f835-40eb-b920-148a394aeaa1)




## Database Schema (for `final_summary_table` / `vendor_summary`)

The `final_summary_table` (which is stored as `vendor_summary` in the database) has the following schema:

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
