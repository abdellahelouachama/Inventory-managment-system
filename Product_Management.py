from db_conncetion import create_connection, get_cursor, close_connection
connection = create_connection()
mycursor = get_cursor(connection)
class Product:
    @staticmethod
    def add_product(name, category, price, stock_level):  
        sql = "INSERT INTO Products (name, category, price, stock_level) VALUES (%s, %s, %s, %s)"
        val = (name, category, price, stock_level)
                
        mycursor.execute(sql, val)
        connection.commit()

        print("Product added successfully.")
        return "Product added successfully."
        
    @staticmethod
    def update_product(name, colomun, new_value):
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
            return "Product updated successfully."
        else:
            print("No product found matching this name!")
            return "No product found matching this name!"

        
    @staticmethod
    def remove_product(product):
        mycursor.execute("SELECT * FROM Products WHERE name = %s",product)
        result = mycursor.fetchone()

        if result:
            sql = "DELETE FROM Products WHERE name = %s"
            val = (product,)

            mycursor.execute(sql, val)
            connection.commit()

            print("Product deleted successfully.")
            return "Product deleted successfully."
        else:
            print("No product found matching the name!")    
            return "No product found matching the name!"
    @staticmethod
    def view_products():
        mycursor.execute("SELECT * FROM Products")
        result = mycursor.fetchall()
        
        if result:
            print("Products catalog:")
            for row in result:
                print(f"Product name: {row[1]}, Category: {row[2]}, Price: {row[3]}, Stock level: {row[4]}.")
                pass
            return "products exist"    
        else:
            print("No products found.")
            return "No products found."
        
    @staticmethod
    def search(criteria, value):
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
            return f"Found, Product name : {result[1]}, Category: {result[2]}, Price: {result[3]}, Stock level: {result[4]}"
        else:
            print("No product found matching this value!")
            return "No product found matching this value!"
def product_menu():  
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
                        name = input("Entre the product name you want to add: ").lower().strip()  
                        category = input("Entre the product category: ").lower().strip()

                        price = input("Entre the product price: ")
                        stock_level = input("Entre the product stock level: ")

                        if not name.isalpha() or not category.isalpha() or not price.isdecimal() or not stock_level.isnumeric():
                            raise ValueError ("Please entre a valid inputs!")
                    
                        Product.add_product(name, category, price, stock_level)
                        break

                    except ValueError as e:
                        print(e)

            elif chosen_operation == (operations[1].lower().strip()):     
                while True:
                    product_name = input("What product you want to update: ").lower().strip()

                    try:                   
                        updated_colomun = input("Which value you want to update (Price, Category, Stock Level): ").lower().strip()
                        if updated_colomun not in ['price', 'category', 'stock level']:
                            raise ValueError ("Please entre a valid input!")
                    
                        new_value = input(f"set, {updated_colomun} : ").lower().strip() 

                        if updated_colomun == 'price' and not new_value.isdecimal():
                            raise ValueError ("Please entre a valid price!")
                        if updated_colomun == 'stock level' and not new_value.isnumeric():
                            raise ValueError ("Please entre a valid stock level!")
                        if updated_colomun == 'category' and not new_value.isalpha():
                            raise ValueError ("Please entre a valid category!")                     
                         
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
                        criteria = input("Which criteria you want to search by (ID, Name, Category, Price, Stock Level): ").lower().strip()
                    
                        if criteria not in ['id', 'name', 'category', 'price', 'stock level']:
                            raise ValueError ("Please entre a valid criteria")
                     
                        value = input(f"Entre the value you want to search with: ") 
                        Product.search(criteria, value) 
                        break

                    except ValueError as e:
                        print(e)
            

            elif chosen_operation == (operations[5].lower().strip()):        
                close_connection(mycursor, connection)
                break
    
            else:
                raise ValueError ("Please entre a valid operation!")        
        except ValueError as e:
            print(e)
        
        

            