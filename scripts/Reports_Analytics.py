from scripts.db_conncetion import create_connection, get_cursor, close_connection
from datetime import datetime

connection = create_connection()
mycursor = get_cursor(connection)
class Reports:
    @staticmethod
    def revenue_report(from_date=None, to_date=None):
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
    print("Enter Date Range: ")
    while True:
        from_date = str(input("From (YYYY-MM-DD): ")).strip()
        to_date = str(input("To (YYYY-MM-DD): ")).strip()
        
        try:
            # Validate and parse the dates
        
            from_date_obj = datetime.strptime(from_date, "%Y-%m-%d")
            to_date_obj = datetime.strptime(to_date, "%Y-%m-%d")
            
            # Ensure from_date is not after to_date
            if from_date_obj > to_date_obj:
                raise ValueError("The 'from' date must not be after the 'to' date.")
        except ValueError as e:
            print(f"Error: {e}. Please enter the dates in the format (YYYY-MM-DD).")
        else:
            # Return the valid dates
            return from_date_obj, to_date_obj
  

def reports_menu():
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
        
        




                    

