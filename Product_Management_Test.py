import unittest
from Product_Management import Product
from db_conncetion import create_connection, get_cursor, close_connection

connection = create_connection()
mycursor = get_cursor(connection)

class ProductTest(unittest.TestCase):

    def setUp(self):
        self.connection = create_connection()
        self.mycursor = get_cursor(self.connection)
    
    def test_add_product(self):     
        result = Product.add_product("wine", "drinks", "10.45", "300")    
        self.assertEqual(result, "Product added successfully.")

    def test_update_product(self):
        result1 = Product.update_product("milk", "price", "14.99")   
        result2 = Product.update_product("A", "category", "Dairy") 

        self.assertEqual(result1, "Product updated successfully.")
        self.assertEqual(result2, "No product found matching this name!")

    def test_remove_product(self):
        result1 = Product.remove_product("wine")
        result2 = Product.remove_product("A")

        self.assertEqual(result1, "Product deleted successfully.")
        self.assertEqual(result2, "No product found matching the name!")    

    def test_view_products(self):
        result = Product.view_products()

        self.assertEqual(result, "products exist")    
        

    def test_search(self):
        result1 = Product.search("id", "9")    
        r = Product.search("id", "800")
        result2 = Product.search("name", "Product A")
        r1 = Product.search("name", "A")
        result3 = Product.search("category", "houses")
        r3 = Product.search("category", "A")
        result4 = Product.search("price", "10.99")
        r4 = Product.search("price", "00.00")
        result5 = Product.search("stock level", "100")
        r5 = Product.search("stock level", "40000")

        self.assertEqual(result1, "Found, Product name : milk, Category: food, Price: 14.99, Stock level: 0")
        self.assertEqual(r, "No product found matching this value!")

        self.assertEqual(result2, "Found, Product name : Product A, Category: Category A, Price: 10.99, Stock level: 100")
        self.assertEqual(r1, "No product found matching this value!")

        self.assertEqual(result3, "Found, Product name : house, Category: houses, Price: 456.00, Stock level: 67")
        self.assertEqual(r3, "No product found matching this value!")

        self.assertEqual(result4, "Found, Product name : Product A, Category: Category A, Price: 10.99, Stock level: 100")
        self.assertEqual(r4, "No product found matching this value!")

        self.assertEqual(result5, "Found, Product name : labtop, Category: technolgy, Price: 5000.00, Stock level: 100")
        self.assertEqual(r5, "No product found matching this value!")
    def tearDown(self):
        close_connection(self.mycursor, self.connection)  

if __name__ == "__main__":
  unittest.main()       