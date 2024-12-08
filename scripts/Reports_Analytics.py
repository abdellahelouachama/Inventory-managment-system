from scripts.db_conncetion import create_connection, get_cursor, close_connection
from datetime import datetime
connection = create_connection()
mycursor = get_cursor(connection)

class Reports:
    @staticmethod
    def revenue_report(from_date=None, to_date=None):
        """
        Retrieves and prints the revenue for each product category in the database.

        Args:
            from_date (datetime): The start date of the period for which the revenue is desired.
            to_date (datetime): The end date of the period for which the revenue is desired.

        Returns:
            str: A message indicating whether sales records exist in the database for the selected period and the revenue report.

        Notes:
            If no sales records exist for the selected period, 
            the function prints a message indicating this and returns "No Sales Found For The Selected Date Range."
            If the function is called without providing a date range,
            it prints a message indicating this and returns "Please Provide a Date range!"

        """
        if from_date != None and to_date != None:
            mycursor.execute("""SELECT SUM(S.revenue), P.category 
                         FROM sales S JOIN Products P ON P.id = S.product_id 
                         WHERE S.sale_date BETWEEN %s AND %s  
                         GROUP BY P.category """,
                          (from_date, to_date))
            result = mycursor.fetchall()
        
        
            if result:                
                print(f"Revenue Report From {from_date} To {to_date}:")
                for row in result:
                    print(f"Category: {row[1]}, Revenue: {row[0]}")
                    
                # return "OK"    
            else:
                print("No Sales Found For The Selected Date Range.")        
                # return "No Sales Found For The Selected Date Range."
        else:
            print("Please Provide a Date range!") 
            # return "Please Provide a Date range!"       
        
    @staticmethod
    def best_selling_product_report(from_date=None, to_date=None):
        """
        Retrieves and prints the best selling products in the database.

        Args:
            from_date (datetime): The start date of the period for which the best selling products are desired.
            to_date (datetime): The end date of the period for which the best selling products are desired.

        Notes:
            If no date range is provided, the function prints the best selling products in the database.
            If a date range is provided and no sales records exist for the selected period, 
            the function prints a message indicating this and returns "No Product Found ".
            If a date range is provided and sales records exist for the selected period, 
            the function prints the best selling products for the selected period and returns "Date Range OK".
        """
        if not from_date and not to_date:
            mycursor.execute("""SELECT SUM(s.quantity), p.name 
                          FROM sales s JOIN Products p 
                          ON p.id = s.product_id 
                          GROUP BY product_id
                          ORDER BY SUM(s.quantity) DESC LIMIT 5""")         
            result = mycursor.fetchall()   

            if result:   
                print("Best Selling Products:")
                for row in result:
                   print("Product name: {}, Quantity sold: {}".format(row[1], row[0]))
                    
                # return 'OK'
            else:
                print("No Product Found ")     
                # return 'No Product Found'   
         
        else:
            mycursor.execute("""SELECT SUM(s.quantity), p.name 
                          FROM sales s JOIN Products p 
                          ON p.id = s.product_id 
                          WHERE S.sale_date BETWEEN %s AND %s 
                          GROUP BY product_id
                          ORDER BY SUM(s.quantity) DESC LIMIT 5""",(from_date, to_date))                 
            result = mycursor.fetchall()

            if result:
                print(f"Best Selling Products From {from_date} To {to_date}:")
                for row in result:
                    print("Product name: {}, Quantity sold: {}".format(row[1], row[0]))
                    
                # return 'Date Range OK'    
            else:
                print("No Product Found ") 
                # return 'No Product Found'       

    @staticmethod                
    def low_stock_alerts():
        """
        Retrieves and prints the five products with the lowest stock levels in the database.

        Returns:
            str: A message indicating whether products exist in the database with low stock levels.

        Notes:
            If no products exist in the database with low stock levels, 
            the function prints a message indicating this and returns "No Product Found ".

        """
        mycursor.execute("SELECT name, stock_level FROM Products ORDER BY stock_level LIMIT 5")    
        result = mycursor.fetchall()

        if result:  
            print("Low stock alerts:")
            for row in result:
                print(f"Product name: {row[0]}, Stock level: {row[1]}")
                
            # return 'OK'    
        else:
            print("No Product Found ")        
            
    @staticmethod
    def forecast_stock_demand():
        """
        Retrieves and prints the five products with the highest expected future demand in the database.

        The method forecasts the future demand of products by analyzing the best-selling products in the last period.

        Returns:
            str: A message indicating whether products exist in the database with high expected future demand.

        Notes:
            If no products exist in the database with high expected future demand, 
            the function prints a message indicating this and returns "No Product Found ".

        """
        mycursor.execute("""SELECT SUM(s.quantity), p.name 
                          FROM sales s JOIN Products p 
                          ON p.id = s.product_id 
                          GROUP BY product_id
                          ORDER BY SUM(s.quantity) DESC LIMIT 5""")         
        result = mycursor.fetchall()    

        if result:       
            print("List Of Expected Future Demand For High-Demand Products Based On The Best-Selling Products In The Last Period:")
            for row in result:
                print("Product Name: {}".format(row[1]))
                
            # return 'OK'    
        else:
            print("No Product Found ")  

def get_and_validate_date():
    """
    Prompts the user to input a date range and validates the input.

    The function continuously prompts the user to enter a 'from' date and a 'to' date 
    in the format YYYY-MM-DD. It validates that the dates are correctly formatted and 
    that the 'from' date is not after the 'to' date. If the input is invalid, the user 
    is re-prompted. Once valid dates are provided, the function returns them as 
    datetime objects.

    Returns:
        tuple: A tuple containing two datetime objects representing the start and end 
        dates of the range.

    Raises:
        ValueError: If the dates are not in the correct format or if the 'from' date 
        is after the 'to' date.
    """
    print("Enter Date Range: ")
    while True:
        from_date = str(input("From (YYYY-MM-DD): ")).strip()
        to_date = str(input("To (YYYY-MM-DD): ")).strip()
        
        try:
            from_date_obj = datetime.strptime(from_date, "%Y-%m-%d")
            to_date_obj = datetime.strptime(to_date, "%Y-%m-%d")
            
            if from_date_obj > to_date_obj:
                raise ValueError("The 'from' date must not be after the 'to' date.")
        except ValueError as e:
            print(f"Error: {e}. Please enter the dates in the format (YYYY-MM-DD).")
        else:
            return from_date_obj, to_date_obj

def reports_menu():
    """
    Displays the reports menu and handles user operations.

    The menu includes options to view revenue reports, best selling products, low stock alerts, and forecasted stock demand.
    The user is prompted to select an operation and enter the necessary details for the chosen operation. The function continuously runs until the user chooses to exit.

    Operations:
        - View Revenue Report: Displays revenue report for a specific date range.
        - View Best Selling Products: Displays best selling products for a specific date range.
        - View Low Stock Alerts: Displays products with low stock.
        - View Forecasted Stock Demand: Displays forecasted stock demand.
        - Exit: Closes the connection and exits the menu.

    Raises:
        ValueError: If user input is invalid.
    """
    operations = ["View Revenue Report", "View Best Selling Products", "View Low Stock Alerts", "View Forecasted Stock Demand", "Exit"]
    print("Menu: ")
    for operation in operations:
        print(operation)

    while True:
        chosen_operation = input("Choose An Operation: ").lower().strip()
        try:

            if chosen_operation == (operations[0].lower().strip()):
                
                from_date_obj, to_date_obj = get_and_validate_date()
                Reports.revenue_report(from_date_obj, to_date_obj)

            elif chosen_operation == (operations[1].lower().strip()):
                answer = input("Would You Like To View Best Selling Products In a Specific Date Range (Y/N)? ").lower().strip()

                if answer in ['y', 'yes']:
                    from_date_obj, to_date_obj = get_and_validate_date()
                    Reports.best_selling_product_report(from_date_obj, to_date_obj)
                    
                else:
                    Reports.best_selling_product_report()

            elif chosen_operation == (operations[2].lower().strip()):
                Reports.low_stock_alerts()

            elif chosen_operation == (operations[3].lower().strip()):
                Reports.forecast_stock_demand()

            elif chosen_operation == (operations[4].lower().strip()):
                close_connection(mycursor, connection)
                break  
            else:
                raise ValueError ("Please Entre a Valid Operation!")
            
        except ValueError as e:
            print(e)        
        
        




                    

