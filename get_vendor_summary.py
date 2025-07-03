import sqlite3
import pandas as pd
import logging
from ingestion_db import ingest_db 

# Configure logging
logging.basicConfig(
    filename="logs/get_vendor_summary.log",
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
    filemode="a"
)

def create_vendor_summary(conn):
    '''
    This function merges data from multiple tables to create 
    a comprehensive vendor sales summary with additional calculated columns.
    '''
    vendor_sales_summary = pd.read_sql_query("""
        WITH FreightSummary AS (
            -- Calculate total freight cost for each vendor
            SELECT 
                VendorNumber,
                SUM(Freight) AS FreightCost
            FROM vendor_invoice
            GROUP BY VendorNumber
        ),

        PurchaseSummary AS (
            -- Summarize purchase details for each vendor and brand
            -- Includes vendor info, brand, description, prices, volume, quantity, and total dollars
            SELECT 
                p.VendorNumber,
                p.VendorName,
                p.Brand,
                p.Description,
                pp.PurchasePrice,
                pp.Price AS ActualPrice,
                pp.Volume,
                SUM(p.Quantity) AS TotalPurchaseQuantity,
                SUM(p.Dollars) AS TotalPurchaseDollars
            FROM purchases p
            JOIN purchase_prices pp ON p.Brand = pp.Brand
            WHERE p.PurchasePrice > 0  -- Only include valid purchases
            GROUP BY 
                p.VendorNumber, p.VendorName, 
                p.Brand, p.Description,
                p.PurchasePrice, pp.Price, pp.Volume
        ),

        SalesSummary AS (
            -- Summarize total sales data for each vendor and brand
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

        -- Final result: Join all summaries into one view
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
            ON ps.VendorNumber = ss.VendorNo AND ps.Brand = ss.Brand
        LEFT JOIN FreightSummary fs
            ON ps.VendorNumber = fs.VendorNumber
        ORDER BY ps.TotalPurchaseDollars DESC;
    """, conn)

    return vendor_sales_summary


def clean_data(df):
    '''This function will clean the data'''
    # Changing datatype to float
    df['Volume'] = df['Volume'].astype('float')

    # filling missing value with 0.
    df.fillna(0, inplace = True)

    # removing spaces from categorical data.
    df['VendorName'] = df['VendorName'].str.strip()
    df['Description'] = df['Description'].str.strip()

    # Creating new column for better analysis.
    vendor_sales_summary['GrossProfit'] = vendor_sales_summary['TotalSalesDollars'] - vendor_sales_summary['TotalPurchaseDollars']

    vendor_sales_summary['ProfitMargin'] = (vendor_sales_summary['GrossProfit'] / vendor_sales_summary['TotalSalesDollars'])*100

    vendor_sales_summary['StockTurnover'] = vendor_sales_summary['TotalSalesQuantity'] / vendor_sales_summary['TotalPurchaseQuantity']

    vendor_sales_summary['SalestoPurchaseRatio'] = vendor_sales_summary['TotalSalesDollars'] / vendor_sales_summary['TotalPurchaseDollars']

    return df

if __name__ == '__main__':
    # Creating database connection
    conn = sqlite3.connect('inventory.db')

    logging.info('Creating Vendor Summary Table.....')
    summary_df = create_vendor_summary(conn)
    logging.info(summary_df.head())

    logging.info('Cleaning data.....')
    clean_df = clean_data(summary_df)
    logging.info(clean_df.head())

    logging.info('Ingesting data.....')
    ingest_db(clean_df, 'vendor_sales_summary', conn)
    logging.info('Completed')