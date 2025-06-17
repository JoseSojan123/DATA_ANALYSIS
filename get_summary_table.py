import pandas as pd
import os
from sqlalchemy import create_engine
import logging
import time
from ingestion_DB import ingest_db
import sqlite3

logging.basicConfig(
   filename="logs/ingestion_db.log",
   level = logging.DEBUG,
   format = "%(asctime)s - %(levelname)s - %(message)s",
   filemode = "a"
)

def create_vendor_summary(conn):
  """this function merges different tables to create a summary table of vendor information"""
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
  return final_summary_table

def clean_data(df):
    """This function cleans the data by removing duplicates and filling missing values"""
    # Changing the dtype of Volume column to float64
    df['Volume'] = df['Volume'].astype('float64')


    # Replacing the missing values with 0
    df.fillna(0, inplace=True)

    # Removing spaces from the VendorName column
    df['VendorName'] = df['VendorName'].str.strip()
    df['Description'] = df['Description'].str.strip()

    # Making new columns which helps in further analysis
    df['GrossProfit'] = df['TotalSalesDollars'] - df['TotalPurchaseDollars']

    df['ProfitMargin'] = (df['GrossProfit'] / df['TotalSalesDollars'])*100

    df['StockTurnover'] = df['TotalSalesQuantity'] / df['TotalPurchaseQuantity']

    df['SalesToPurchaseRatio'] = df['TotalSalesDollars'] / df['TotalPurchaseDollars']

    return df

if __name__ == "__main__":
    # Create a database connection
    conn = sqlite3.connect('inventory.db')
    conn = sqlite3.connect('D:/Python-DataAnalysis/inventory.db')
    conn.execute("PRAGMA temp_store = MEMORY;")

    logging.info("Creating vendor summary table")
    summary_df = create_vendor_summary(conn)
    logging.info(summary_df.head())

    logging.info("Cleaning the data")
    clean_df = clean_data(summary_df)
    logging.info(clean_df.head())


    logging.info("Ingesting the cleaned data into the database")
    ingest_db(clean_df, 'vendor_summary', conn)
    logging.info("Vendor summary table created and ingested successfully")

    # Close the database connection
    conn.close()

