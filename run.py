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

def update_sales_worksheet(data):
    """
    Update sales worksheet, add new row in worksheet with list provided
    """
    print('updating sales worksheet')
    sales_worksheet = SHEET.worksheet('sales')
    sales_worksheet.append_row(data)
    print('Sales worksheet updated succesfully!\n')

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

def main():
    """
    Run all program functions
    """
    data = get_sales_data()
    sales_data = [int(num) for num in data]
    update_sales_worksheet(sales_data)
    new_surplus_data = calculate_surplus_data(sales_data)
    print(new_surplus_data)

print('Welcome to Love Sandwiches Data Automation')
main()