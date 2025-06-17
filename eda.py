import pandas as pd
import sqlite3

# Database connection
conn = sqlite3.connect('inventory.db')
conn = sqlite3.connect('D:/Python-DataAnalysis/inventory.db')
conn.execute("PRAGMA temp_store = MEMORY;")  # Use RAM instead of disk for temp storage

tables = pd.read_sql_query("SELECT name FROM sqlite_master WHERE type='table'", conn)
print("Tables in the database:")
print(tables)

for table in tables['name']:
  print('-'*50 , f'{table}', '-'*50)
  print('Count of records: ', pd.read_sql(f"select count(*) as count from {table}", conn)['count'].values[0])
  print(pd.read_sql(f"select * from {table} limit 5", conn))


purchases = pd.read_sql("select * from purchases where VendorNumber = 4466", conn)
print(purchases)

purchase_prices = pd.read_sql("select * from purchase_prices where VendorNumber = 4466", conn)
print(purchase_prices)

vendor_invoice = pd.read_sql("select * from vendor_invoice where VendorNumber = 4466", conn)
print(vendor_invoice)

sales = pd.read_sql("select * from sales where VendorNo = 4466", conn)
print(sales)


print(purchases.groupby(['Brand' , 'PurchasePrice'])[['Quantity', 'Dollars']].sum())

print(vendor_invoice['PONumber'].nunique())

print(sales.groupby(['Brand'])[['SalesPrice', 'SalesDollars', 'SalesQuantity']].sum())


'''
What the tables contain:

Purchases table:
Stores data about what vendors bought — like purchase date, product/brand name, price paid, and quantity.

Purchase_prices table:
Lists the actual and expected prices of each product, grouped by vendor and brand.

Vendor_invoice table:
Summarizes purchase data — total quantity, total amount paid, and freight charges — grouped by vendor and purchase order.

Sales table:
Shows actual sales — which brands were sold, how many, at what price, and total revenue earned.

What the summary table should include:

Vendor purchase transaction details

Sales transaction data

Freight costs for each vendor

Actual product prices from vendors
'''

freight_summary = pd.read_sql(""" select VendorNumber, SUM(Freight) as TotalFreight FROM vendor_invoice GROUP BY VendorNumber """, conn )
print(freight_summary)


summary_table_1 = pd.read_sql_query("""
    SELECT 
        p.VendorNumber, 
        p.VendorName, 
        p.Brand, 
        p.PurchasePrice, 
        pp.Volume, 
        pp.Price AS ActualPrice, 
        SUM(p.Quantity) AS TotalPQuantity, 
        SUM(p.Dollars) AS TotalPDollars
    FROM purchases p
    JOIN PURCHASE_PRICES pp 
        ON p.Brand = pp.Brand
    WHERE p.PurchasePrice > 0
    GROUP BY 
        p.VendorNumber, 
        p.VendorName, 
        p.Brand, 
        p.PurchasePrice, 
        pp.Volume, 
        pp.Price
    ORDER BY TotalPDollars
""", conn)

print(summary_table_1)


summary_table_2 = pd.read_sql_query("""
    SELECT 
      VendorNo,
      Brand,
      SUM(SalesDollars) AS TotalSalesDollars,
      SUM(SalesPrice) AS TotalSalesPrice,
      SUM(SalesQuantity) AS TotalSalesQuantity,
      SUM(ExciseTax) AS TotalExciseTax
      FROM sales                           
      GROUP BY VendorNo, 
      Brand 
      ORDER BY TotalSalesDollars""", conn)

print(summary_table_2)



import time
start = time.time()
final_summary_table = pd.read_sql_query("""
WITH FreightSummary AS (
    SELECT
        VendorNumber,
        SUM(Freight) AS FreightCost
    FROM vendor_invoice
    GROUP BY VendorNumber
),

PurchaseSummary AS (
    SELECT
        p.VendorNumber,
        p.VendorName,
        p.Brand,
        p.Description,
        p.PurchasePrice,
        pp.Price AS ActualPrice,
        pp.Volume,
        SUM(p.Quantity) AS TotalPurchaseQuantity,
        SUM(p.Dollars) AS TotalPurchaseDollars
    FROM purchases p
    JOIN purchase_prices pp
        ON p.VendorNumber = pp.VendorNumber
        AND p.Brand = pp.Brand
    GROUP BY p.VendorNumber, p.VendorName, p.Brand, p.Description, p.PurchasePrice, pp.Price, pp.Volume
),

SalesSummary AS (
    SELECT
        VendorNo,
        Brand,
        SUM(SalesQuantity) AS TotalSalesQuantity,
        SUM(SalesDollars) AS TotalSalesDollars,
        SUM(SalesPrice) AS TotalSalesPrice,
        SUM(ExciseTax) AS TotalExciseTax
    FROM sales
    GROUP BY VendorNo, Brand
)

SELECT
    ps.VendorNumber,
    ps.VendorName,
    ps.Brand,
    ps.Description,
    ps.PurchasePrice,
    ps.ActualPrice,
    ps.Volume,
    ps.TotalPurchaseQuantity,
    ps.TotalPurchaseDollars,
    ss.TotalSalesQuantity,
    ss.TotalSalesDollars,
    ss.TotalSalesPrice,
    ss.TotalExciseTax,
    fs.FreightCost
FROM PurchaseSummary ps
LEFT JOIN SalesSummary ss
    ON ps.VendorNumber = ss.VendorNo
    AND ps.Brand = ss.Brand
LEFT JOIN FreightSummary fs
    ON ps.VendorNumber = fs.VendorNumber
ORDER BY ps.TotalPurchaseDollars DESC

""", conn)
end = time.time()

print(final_summary_table)
print(f"Time taken to execute the final summary table query: {end - start} seconds")



"""This query creates a summary of sales and purchases for each vendor. It's useful because:

Performance Benefits:

It handles big data with complex joins and calculations for sales and purchases.

It saves already calculated results to avoid doing the same heavy work again.

It helps compare sales, purchases, and prices between different vendors and brands.

This saved data can be reused later for faster dashboard loading and reports.

Instead of running slow queries every time, dashboards can quickly get the data from the pre-made summary (vendor_sales_summary)."""

# Changing the dtype of Volume column to float64
final_summary_table['Volume'] = final_summary_table['Volume'].astype('float64')


# Replacing the missing values with 0
final_summary_table.fillna(0, inplace=True)

# Removing spaces from the VendorName column
final_summary_table['VendorName'] = final_summary_table['VendorName'].str.strip()

# Checking inconsistencies in the data 
final_summary_table_dtype = final_summary_table.dtypes
print("Data types in the final summary table:")
print(final_summary_table_dtype)

# Checking for missing values in the final summary table
missing_values = final_summary_table.isnull().sum()
print("Missing values in the final summary table:")
print(missing_values)


# Checking for spaces in the last of vendor names
vendor_name_spaces = final_summary_table['VendorName'].unique()
print("Unique vendor names with potential spaces:")
print(vendor_name_spaces)





# Making new columns which helps in further analysis
final_summary_table['GrossProfit'] = final_summary_table['TotalSalesDollars'] - final_summary_table['TotalPurchaseDollars']

final_summary_table['ProfitMargin'] = (final_summary_table['GrossProfit'] / final_summary_table['TotalSalesDollars'])*100

final_summary_table['StockTurnover'] = final_summary_table['TotalSalesQuantity'] / final_summary_table['TotalPurchaseQuantity']

final_summary_table['SalesToPurchaseRatio'] = final_summary_table['TotalSalesDollars'] / final_summary_table['TotalPurchaseDollars']


cursor = conn.cursor()
# Create a new table to store the final summary
cursor.execute(""" CREATE TABLE final_summary_table (
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
);""")

# Insert the final summary table into the new table
final_summary_table.to_sql('final_summary_table', conn, if_exists='replace', index=False)

# Print the final summary table
print("Final summary table created and data inserted successfully.")
print_table = pd.read_sql("select * from final_summary_table", conn)
print(print_table)