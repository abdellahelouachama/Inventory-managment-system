from scripts.db_conncetion import create_connection, get_cursor, close_connection
from datetime import datetime
connection = create_connection()
mycursor = get_cursor(connection)

class Sales:
    @staticmethod
    def record_sales_transaction(product_name, quantity_sold, sale_date):
        """
        Records a sale transaction into the database.

        Args:
            product_name (str): The name of the product sold.
            quantity_sold (int): The quantity of the product sold.
            sale_date (datetime): The date of the sale.

        Returns:
            str: A message indicating the result of the operation.
        """
        mycursor.execute("SELECT id, stock_level, price FROM Products WHERE %s = name",product_name)
        result = mycursor.fetchone()
 
        if result:
            id = result[0]
            stock_level = result[1]
            price = result[2] 

            if stock_level >= quantity_sold:
                revenue = price * quantity_sold
                sql = "INSERT INTO sales (product_id, quantity, sale_date, revenue)  VALUES (%s, %s, %s, %s)"
                val = (id, quantity_sold, sale_date, revenue)
                mycursor.execute(sql, val)

                updated_stock_level = stock_level - quantity_sold
                sql = "UPDATE Products SET stock_level = %s WHERE id = %s"
                val = (updated_stock_level, id)
                mycursor.execute(sql, val)    
                connection.commit()
                print("Sale Added Successfully")
                # return "Sale inserted successfully"

            else:
                print("Insufficient Stock")
                # return "Insufficient Stock"
        else:
            print("No Product Found Matching This Name!")   
            # return "No product found matching this name!"    

    @staticmethod 
    def view_sales_history():
        """
        Retrieves and prints all sales in the database.

        The function first retrieves all sales records from the database, then iterates over the result and prints each sale 
        with its corresponding product name, quantity sold, sale date, and revenue. If no sales records are found, the function prints a message indicating this.

        Returns:
            str: A message indicating whether sales records exist in the database.
        """
        mycursor.execute("SELECT P.name, S.quantity, S.sale_date, S.revenue FROM sales S JOIN Products P ON P.id = S.product_id")
        result = mycursor.fetchall()

        if result: 
            print("Sales History: ")
            for row in result:
                print(f"Product name: {row[0]}, Quantity sold: {row[1]}, Sale date: {row[2]}, Revenue: {row[3]}")
            
            # return "Sales exist"    
        else:
            print("No Sales Found ")
            # return "No Sales Found "
def sales_menu():
    """
    Displays the sales transactions menu and handles user operations.

    The menu includes options to record a sale transaction and view sales history. 
    The user is prompted to select an operation and enter the necessary details for the chosen operation. 
    The function continuously runs until the user chooses to exit.

    Operations:
        - Record Sale Transaction: Records a sale transaction into the database.
        - View Sales History: Retrieves and prints all sales in the database.
        - Exit: Closes the connection and exits the menu.

    Raises:
        ValueError: If user input is invalid.
    """
    operations = ["Record Sale Transaction", "View Sales History", "Exit"]
    print("Menu: ")
    for operation in operations:
        print(operation)

    while True:
        chosen_operation = input("Select an operation: ").lower().strip()

        try:
            if chosen_operation == (operations[0].lower().strip()):

                while True:
                    try:
                        product_name = input("What Product You Sold: ").lower().strip()
                        quantity_sold = input("How Many Items Sold: ")

                        if not product_name.isalpha() or not quantity_sold.isnumeric():
                            raise ValueError ("Please entre a valid inputs!")
                    
                        sale_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        Sales.record_sales_transaction(product_name, int(quantity_sold), sale_date)
                        break

                    except ValueError as e:
                        print(e) 

            elif chosen_operation == (operations[1].lower().strip()):
                Sales.view_sales_history()

            elif chosen_operation == (operations[2].lower().strip()):
                close_connection(mycursor, connection)
                break    
            else:
                raise ValueError ("Please entre a valid operation!")

        except ValueError as e:
            print(e)
        
        