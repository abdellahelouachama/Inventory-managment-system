import unittest
from Sales_Transactions import Sales
from db_conncetion import create_connection, get_cursor, close_connection

connection = create_connection()
mycursor = get_cursor(connection)

class SalesTest(unittest.TestCase):
    def setUp(self):
        self.connection = create_connection()
        self.mycursor = get_cursor(self.connection)

    def test_add_transaction(self):    
        result = Sales.record_sales_transaction("labtop", 5, "2023-08-01")
        result2 = Sales.record_sales_transaction("table", 200, "2023-08-01")
        result3 = Sales.record_sales_transaction("A", 200, "2023-08-01")

        self.assertEqual(result, "Sale inserted successfully")
        self.assertEqual(result2, "Insufficient Stock")
        self.assertEqual(result3, "No product found matching this name!")

    def test_view_transactions(self):    
        result = Sales.view_sales_history()
        self.assertEqual(result, "Sales exist")


    def tearDown(self):
        close_connection(self.mycursor, self.connection)    

if __name__ == '__main__':
    unittest.main()