from scripts.db_conncetion import create_connection, get_cursor, close_connection
connection = create_connection()
mycursor = get_cursor(connection)
class Product:
    @staticmethod
    def add_product(name, category, price, stock_level):  
        """
        Adds a product to the database.

        Args:
            name (str): The name of the product.
            category (str): The category of the product.
            price (float): The price of the product.
            stock_level (int): The initial stock level of the product.

        Returns:
            str: A message indicating whether the product was added successfully.

        """
        sql = "INSERT INTO Products (name, category, price, stock_level) VALUES (%s, %s, %s, %s)"
        val = (name, category, price, stock_level)
                
        mycursor.execute(sql, val)
        connection.commit()

        print("Product added successfully.")
        return "Product added successfully."
        
    @staticmethod
    def update_product(name, colomun, new_value):
        """
        Updates a product in the database.

        Args:
            name (str): The name of the product to be updated.
            colomun (str): The column to be updated (price, category, or stock level).
            new_value (str or int or float): The new value of the column.

        Returns:
            str: A message indicating whether the product was updated successfully.

        """
        mycursor.execute("SELECT * FROM Products WHERE name = %s",name)
        result = mycursor.fetchone()

        if result:
            if colomun == 'price':
                sql = "UPDATE Products SET price = %s WHERE name = %s"
                val = (new_value, name)
            elif colomun == 'category':
                sql = "UPDATE Products SET category = %s WHERE name = %s"
                val = (new_value, name)
            elif colomun == 'stock level':
                sql = "UPDATE Products SET stock_level = %s WHERE name = %s"
                val = (new_value, name) 

            mycursor.execute(sql, val)
            connection.commit()
            print("Product updated successfully.")
            # return "Product updated successfully."
        else:
            print("No product found matching this name!")
            # return "No product found matching this name!"
        
    @staticmethod
    def remove_product(product):
        """
        Removes a product from the database.

        Args:
            product (str): The name of the product to be removed.

        Returns:
            str: A message indicating whether the product was removed successfully.

        """
        mycursor.execute("SELECT * FROM Products WHERE name = %s",product)
        result = mycursor.fetchone()

        if result:
            sql = "DELETE FROM Products WHERE name = %s"
            val = (product,)

            mycursor.execute(sql, val)
            connection.commit()

            print("Product deleted successfully.")
            # return "Product deleted successfully."
        else:
            print("No product found matching the name!")    
            # return "No product found matching the name!"

    @staticmethod
    def view_products():
        """
        Prints all products in the database.

        Returns:
            str: A message indicating whether products exist in the database.

        """
        
        mycursor.execute("SELECT * FROM Products")
        result = mycursor.fetchall()
        
        if result:
            print("Products catalog:")
            for row in result:
                print(f"Product name: {row[1]}, Category: {row[2]}, Price: {row[3]}, Stock level: {row[4]}.")
            # return "products exist"    
        else:
            print("No products found.")
            # return "No products found."
        
    @staticmethod
    def search(criteria, value):
        """
    Searches for a product in the database based on the given criteria.

    Args:
        criteria (str): The criteria to search by. Options are 'id', 'name', 
                        'category', 'price', or 'stock level'.
        value: The value of the criteria to search for.

    Returns:
        Prints the details of the found product if a match is found,
        otherwise prints a message indicating no match was found.
        """
        if criteria == 'id':
            sql = "SELECT * FROM Products WHERE id = %s"
            val = (value,)
        elif criteria == 'name':
            sql = "SELECT * FROM Products WHERE name = %s"
            val = (value,)
        elif criteria == 'category':
            sql = "SELECT * FROM Products WHERE category = %s"
            val = (value,)
        elif criteria == 'price':
            sql = "SELECT * FROM Products WHERE price = %s"
            val = (value,)
        elif criteria == 'stock level':
            sql = "SELECT * FROM Products WHERE stock_level = %s"
            val = (value,)
        mycursor.execute(sql, val)
        result = mycursor.fetchone()
        
        if result:
            print(f"Found, Product name : {result[1]}, Category: {result[2]}, Price: {result[3]}, Stock level: {result[4]}")
            # return f"Found, Product name : {result[1]}, Category: {result[2]}, Price: {result[3]}, Stock level: {result[4]}"
        else:
            print("No product found matching this value!")
            # return "No product found matching this value!"
def product_menu():  
    """
    Displays the product management menu and handles user operations.

    The menu includes options to add, update, delete, view, and search for products.
    The user is prompted to select an operation and enter the necessary details for 
    the chosen operation. The function continuously runs until the user chooses to exit.

    Operations:
        - Add product: Adds a new product to the database.
        - Update product: Updates the details of an existing product.
        - Delete product: Removes a product from the database.
        - View products catalog: Displays all products.
        - Search for a product: Searches for a product based on specified criteria.
        - Exit: Closes the connection and exits the menu.

    Raises:
        ValueError: If user input is invalid.
    """
    operations = ['Add product', 'Update product', 'Delete product', 'View products catalog', "Search for a product", "Exit"]
    print("Menu: ")
    for operation in operations:
        print(operation)

    while True:
        try:   
            chosen_operation = input("Choose an operation: ").lower().strip()

            if chosen_operation == (operations[0].lower().strip()):     
                while True:
                    try:
                        name = input("Entre The Product Name You Want To Add: ").lower().strip()  
                        category = input("Entre The Product Category: ").lower().strip()
                        price = input("Entre The Product Price: ")
                        stock_level = input("Entre The Product Stock Level: ")

                        if not name.isalpha() or not category.isalpha() or not price.isdecimal() or not stock_level.isnumeric():
                            raise ValueError ("Please Entre a Valid Inputs!")                    
                        Product.add_product(name, category, price, stock_level)
                        break
                    except ValueError as e:
                        print(e)

            elif chosen_operation == (operations[1].lower().strip()):     
                while True:
                    product_name = input("What Product You Want To Update: ").lower().strip()

                    try:                   
                        updated_colomun = input("Which Value You Want To Update (Price, Category, Stock Level): ").lower().strip()
                        if updated_colomun not in ['Price', 'Category', 'Stock Level']:
                            raise ValueError ("Please Entre a Valid Input!")
                    
                        new_value = input(f"Set, {updated_colomun.capitalize()} : ").lower().strip() 
                        if updated_colomun == 'price' and not new_value.isdecimal():
                            raise ValueError ("Please Entre a Valid Price!")
                        if updated_colomun == 'stock level' and not new_value.isnumeric():
                            raise ValueError ("Please Entre a Valid Stock Level!")
                        if updated_colomun == 'category' and not new_value.isalpha():
                            raise ValueError ("Please Entre a Valid Category!")                     
                         
                        Product.update_product(product_name, updated_colomun, new_value)
                        break
                    except ValueError as e:
                        print(e)
            
            elif chosen_operation == (operations[2].lower().strip()):
                while True:
                    product_name = input("Entre the product you want to delete: ")

                    try:
                        if not product_name.isalpha():
                            raise ValueError ("Please entre a valid input!")                   
                        Product.remove_product(product_name)
                        break

                    except ValueError as e:
                        print(e)
            
            elif chosen_operation == (operations[3].lower().strip()):
                Product.view_products()

            elif chosen_operation == (operations[4].lower().strip()):             
                while True:
                    try:
                        criteria = input("Which Criteria You Want To Search By (ID, Name, Category, Price, Stock Level): ").lower().strip()
                    
                        if criteria not in ['id', 'name', 'category', 'price', 'stock level']:
                            raise ValueError ("Please Entre a Valid Criteria")
                     
                        value = input(f"Entre The Value You Want To Search With: ") 
                        Product.search(criteria, value) 
                        break

                    except ValueError as e:
                        print(e)
            

            elif chosen_operation == (operations[5].lower().strip()):        
                close_connection(mycursor, connection)
                break
    
            else:
                raise ValueError ("Please Entre a Valid Operation!")        
        except ValueError as e:
            print(e)
        
        

            