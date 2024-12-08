from scripts.db_conncetion import create_connection, get_cursor, close_connection
from datetime import datetime

connection = create_connection()
mycursor = get_cursor(connection)

class Sales:
    @staticmethod
    def record_sales_transaction(product_name, quantity_sold, sale_date):
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
        mycursor.execute("SELECT P.name, S.quantity, S.sale_date, S.revenue FROM sales S JOIN Products P ON P.id = S.product_id")
        result = mycursor.fetchall()

        if result: 
           print("Sales History: ")
           for row in result:
                print(f"Product name: {row[0]}, Quantity sold: {row[1]}, Sale date: {row[2]}, Revenue: {row[3]}")
            
        #    return "Sales exist"    
        else:
            print("No Sales Found ")
            # return "No Sales Found "
def sales_menu():
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
        
        