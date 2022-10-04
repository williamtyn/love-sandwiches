import gspread
from google.oauth2.service_account import Credentials
from pprint import pprint

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('love_sandwiches')

def get_sales_data():
    """
    Get sales figures input from the user and while loop if the data is not valid until
    user input correct values
    """
    while True:
        print('Please enter sales data from the last market ')
        print('Data should be six numbers separated by comma')
        print('Example: 10,20,30,40,50,60\n')

        data_str = input('Enter your data here:')

        sales_data = data_str.split(',')
        
        if validate_data(sales_data):
            print('Data is OK')
            break
    return sales_data

def validate_data(values):
    """
    Inside the try, converts all strings into integers
    Raises ValueError if strings cannot be converted into int,
    or if there isn´t exaclty 6 values
    """
    
    try:
        [int(value) for value in values]
        if len(values) != 6:
            raise ValueError(
                f'exactly 6 values required and you provided {len(values)}'
            )
    except ValueError as e:
        print(f'Invalid data: {e}, Please try again.\n')
        return False
    return True
"""
def update_sales_worksheet(data):
   
    print('updating sales worksheet')
    sales_worksheet = SHEET.worksheet('sales')
    sales_worksheet.append_row(data)
    print('Sales worksheet updated succesfully!\n')

def update_surplus_worksheet(data):
    
    print('Updating surplus worksheet..')
    surplus_worksheet = SHEET.worksheet('surplus')
    surplus_worksheet.append_row(new_surplus_data)
    print(f'Surplus worksheet updated with following values: {new_surplus_data}!\n')
"""
def update_worksheet(data,worksheet):
    """
    Recives a list with integers to update worksheet rows
    Update the relevant worksheet with the data provided 
    """
    print(f'Updating {worksheet} worksheet\n')
    worksheet_to_update = SHEET.worksheet(worksheet)
    worksheet_to_update.append_row(data)
    print(f'{worksheet} updated succesfully!\n')

def calculate_surplus_data(sales_row):
    """
    Calculate stock minus sales to calculate surplus for each item

    The surplus is defined as the sales figure subtracted form the stock:
    - Positive surplus indicates waste.
    - Negative surplus indicates extramade when stock runned out. 
    """
    print('Calculating surplus data..')
    stock = SHEET.worksheet('stock').get_all_values()
    stock_row = stock.pop()
    
    surplus_data = []
    for stock, sales in zip(stock_row, sales_row):
        surplus = int(stock) - sales
        surplus_data.append(surplus)
    
    return surplus_data    

def get_last_5_entries_sales():
    """
    Collects the 5 last entries of sales for each sandwich in worksheet
    """
    sales = SHEET.worksheet('sales')

    columns = []
    for ind in range(1,7):
        column = sales.col_values(ind)
        columns.append(column[-5:])
    return columns

def calculate_stock_data(data):
    """
    Calculate stock data by taking 5 last entries and add them together
    then adding 10% to that
    """
    print('Calculating stock data..\n')
    new_stock_data = []

    for column in data:
        int_column = [int(num)for num in column]
        avarage = sum(int_column) / len(int_column)
        stock_num = avarage * 1.1
        new_stock_data.append(round(stock_num))

    return new_stock_data


def main():
    """
    Run all program functions
    """
    data = get_sales_data()
    sales_data = [int(num) for num in data]
    update_worksheet(sales_data, 'sales')
    new_surplus_data = calculate_surplus_data(sales_data)
    update_worksheet(new_surplus_data, 'surplus')
    sales_columns = get_last_5_entries_sales()
    stock_data = calculate_stock_data(sales_columns)
    update_worksheet(stock_data,'stock')

print('Welcome to Love Sandwiches Data Automation')
main()
