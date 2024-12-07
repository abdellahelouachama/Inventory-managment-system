from db_conncetion import create_connection, get_cursor, close_connection
connection = create_connection()
mycursor = get_cursor(connection)
class Supplier:

    @staticmethod
    def add_supplier(name, contact_info, provided_products):  
        mycursor.execute("SELECT name FROM Products WHERE name = %s",provided_products)
        result = mycursor.fetchone()
        if result:
            sql = "INSERT INTO suppliers (name, contact_info) VALUES (%s, %s)"
            val = (name, contact_info)

            mycursor.execute(sql, val)
            connection.commit()
            print("Supplier Inserted Successfully")

            mycursor.execute("SELECT id FROM suppliers WHERE name = %s", name)
            supplier_id = mycursor.fetchone()
            Supplier.link_supplier_to_product(provided_products, supplier_id)

            return "Supplier Inserted Successfully"
        else:
            print("No Product Found Matching This Product!")
            return "No Product Found Matching This Product!"

    @staticmethod
    def update(name, new_value):
        mycursor.execute("SELECT * FROM suppliers WHERE name = %s",name)
        result = mycursor.fetchone()

        if result:
            sql = "UPDATE suppliers SET contact_info = %s WHERE name = %s"
            val = (new_value, name)
 
            mycursor.execute(sql, val)
            connection.commit()
        
            print("Supplier Contact Infomation Updated Successfully")
            return "Supplier Contact Infomation Updated Successfully"
        else:
            print("No Suppplier Found Matching This Name!")
            return "No Suppplier Found Matching This Name!"
    @staticmethod
    def link_supplier_to_product(provided_products, supplier_id):
        sql = "UPDATE Products SET supplier_id = %s WHERE name = %s"
        val = (supplier_id, provided_products)

        mycursor.execute(sql, val)
        connection.commit()
     
    @staticmethod
    def view_suppliers():
        mycursor.execute("SELECT s.name, s.contact_info, p.name FROM suppliers s JOIN Products p ON s.id = p.supplier_id ")
        result = mycursor.fetchall()
        if result:
            print("Suppliers List: ")
            for row in result:
            
                print(f"Supplier name: {row[0]}, Contact infomations: {row[1]}, Provided products: {row[2]}")
            return "Suppliers exist"    
        else:
            print("No Suppliers Found ")
        

    @staticmethod
    def delete_supplier(name):
        mycursor.execute("SELECT * FROM suppliers WHERE name = %s",name)
        result = mycursor.fetchone()

        if result:
            mycursor.execute("UPDATE Products SET supplier_id = NULL WHERE supplier_id = (SELECT id FROM suppliers WHERE name = %s)", name)
            sql = "DELETE FROM suppliers WHERE name = %s"
            val = (name)

            mycursor.execute(sql, val)
            connection.commit()

            print("Supplier Deleted Successfully")
            return "Supplier Deleted Successfully"
        else:
            print("No Supplier Found Matching This Name!")
            return "No Supplier Found Matching This Name!"
            
def supplier_menu():
    operations = ['Add supplier', 'Update supplier Contact infomation', 'View suppliers', 'Delete supplier', 'Exit']
    print("Menu: ")
    for operation in operations:
        print(operation)

    while True:
        chosen_operation = input("Choose an operation: ").lower().strip()
        try:

            if chosen_operation == (operations[0].lower().strip()):
                while True:
                    try:

                        name = input("What is the supplier name: ").lower().strip()
                        contact_info = input("Provide contact information of this supplier (email/phone number): ").lower().strip()
                        provided_product = input("What is the product this supplier provide: ").lower().strip()
           
                        if not name.isalpha() or not provided_product.isalpha():
                            raise ValueError ("Please provide valid inputs!")
                    
                        Supplier.add_supplier(name, contact_info, provided_product)
                        break

                    except ValueError as e:
                        print(e)

            elif chosen_operation == (operations[1].lower().strip()):
                print("You only can update in contact information!")

                while True:
                    try:
                        name = input("Entre the supplier name you want to update his contact information : ").lower().strip()        

                        if not name.isalpha():
                            raise ValueError ("Please entre a valid name!")
                        new_value = input("New value: ").lower().strip()

                        Supplier.update(name, new_value)
                        break
                    except ValueError as e:
                        print(e)
                    
            elif chosen_operation == (operations[2].lower().strip()):
                Supplier.view_suppliers()

            elif chosen_operation == (operations[3].lower().strip()):
                while True:
                    name = input("Entre the supplier name you want to delete: ").lower().strip()

                    try:
                        if not name.isalpha():
                            raise ValueError ("Please entre a valid name!")
                    
                        Supplier.delete_supplier(name)
                        break
                    except ValueError as e:
                        print(e)

            elif chosen_operation == (operations[4].lower().strip()):
                close_connection(connection, mycursor)
                break

            else:
                raise ValueError ("Please entre a valid operation")         
        except ValueError as e:
            print(e)            
                 
        