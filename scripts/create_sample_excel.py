import pandas as pd

# Create sample data for Consol PL sheet
pl_data = {
    'Item': ['Revenue', 'Cost of Sales', 'Gross Profit', 'Other Income', 'Distribution Costs', 
             'Administrative Expenses', 'Other Expenses', 'Profit Before Tax', 'Income Tax Expense', 
             'Profit/(Loss) for the Period'],
    'FY2025': [1000000, -400000, 600000, 50000, -150000, -200000, -25000, 275000, 0, 275000],
    'FY2024': [950000, -380000, 570000, 45000, -140000, -190000, -20000, 260000, 0, 260000]
}

# Create sample data for Consol BS sheet
bs_data = {
    'Item': ['Cash and Cash Equivalents', 'Trade and Other Receivables', 'Inventories', 'Other Current Assets',
             'Total Current Assets', '', 'Property, Plant and Equipment', 'Intangible Assets', 'Other Non-current Assets',
             'Total Non-current Assets', '', 'TOTAL ASSETS', '', 'Trade and Other Payables', 'Provisions', 
             'Other Current Liabilities', 'Total Current Liabilities', '', 'Borrowings', 'Provisions', 
             'Other Non-current Liabilities', 'Total Non-current Liabilities', '', 'Total Liabilities', '', 
             'Share Capital', 'Reserves', 'Retained Earnings', 'Total Equity', '', 'TOTAL EQUITY AND LIABILITIES'],
    'FY2025': [150000, 200000, 100000, 50000, 500000, '', 800000, 100000, 100000, 1000000, '', 1500000, '', 
               150000, 50000, 100000, 300000, '', 500000, 100000, 100000, 700000, '', 1000000, '', 200000, 0, 
               300000, 500000, '', 1500000],
    'FY2024': [120000, 180000, 90000, 40000, 430000, '', 750000, 100000, 90000, 940000, '', 1370000, '', 
               140000, 45000, 90000, 275000, '', 480000, 95000, 95000, 670000, '', 945000, '', 200000, 0, 
               25000, 425000, '', 1370000]
}

# Create DataFrames
pl_df = pd.DataFrame(pl_data)
bs_df = pd.DataFrame(bs_data)

# Create a Pandas Excel writer using XlsxWriter as the engine
with pd.ExcelWriter('sample_entity_management_report.xlsx', engine='xlsxwriter') as writer:
    # Write each DataFrame to a different worksheet
    pl_df.to_excel(writer, sheet_name='Consol PL', index=False)
    bs_df.to_excel(writer, sheet_name='Consol BS', index=False)
    # Create an empty sheet for Consol CFS
    pd.DataFrame().to_excel(writer, sheet_name='Consol CFS', index=False)

print("Sample Excel file created: sample_entity_management_report.xlsx")