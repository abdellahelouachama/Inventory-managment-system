import unittest
from Supplier_Management import Supplier
from db_conncetion import create_connection, get_cursor, close_connection

connection = create_connection()
mycursor = get_cursor(connection)

class SupplierTest(unittest.TestCase):
    def setUp(self):
        self.connection = create_connection()
        self.mycursor = get_cursor(self.connection)

    def test_add_supplier(self):
        result = Supplier.add_supplier("jane", "jane@gmail.com", "iphone")
        self.assertEqual(result, "Supplier Inserted Successfully")

        result2 = Supplier.add_supplier("jack", "jack@gmail.com", "Product A")
        self.assertEqual(result2, "No Product Found Matching This Product!")

    def test_update(self):
        result = Supplier.update("jane", "012345678")    
        self.assertEqual(result, "Supplier Contact Infomation Updated Successfully")

        result2 = Supplier.update("Supplier A", "012345678")
        self.assertEqual(result2, "No Suppplier Found Matching This Name!")

    def test_view_suppliers(self):    
        result = Supplier.view_suppliers()    
        self.assertEqual(result, "Suppliers exist")

    def test_delete_supplier(self):
        result = Supplier.delete_supplier("leva")
        self.assertEqual(result, "Supplier Deleted Successfully")

        result2 = Supplier.delete_supplier("Supplier A")
        self.assertEqual(result2, "No Supplier Found Matching This Name!")    

    def tearDown(self):
        close_connection(self.mycursor, self.connection)   


if __name__ == '__main__':
    unittest.main()