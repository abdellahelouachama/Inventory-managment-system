import unittest
from scripts.Reports_Analytics import Reports
from scripts.db_conncetion import create_connection, get_cursor, close_connection

class ReportsTest(unittest.TestCase):
    def setUp(self):
        """
        Set up a database connection and cursor for use in test cases.
       """
        self.connection = create_connection()
        self.mycursor = get_cursor(self.connection)

    def test_revenue_reports(self):
        
        """
        Test the revenue_report function with different date ranges
        """
        # test providing valid date range
        response = Reports.revenue_report('2024-10-23', '2024-10-25')
        self.assertEqual(response, 'OK')
        # test provding invalid date range
        response = Reports.revenue_report('2000-10-23', '2010-10-25')
        self.assertEqual(response, 'No Sales Found For The Selected Date Range.')
        # test providing no date range
        response = Reports.revenue_report()
        self.assertEqual(response, 'Please Provide a Date range!')

    
    def test_best_selling_products_reports(self):
        """
        Test the best_selling_product_report function with different date ranges
        """
        # test providing a vaild date range
        response = Reports.best_selling_product_report('2024-10-23', '2024-10-25')
        self.assertEqual(response, 'Date Range OK')
        # test providing unvialid  datae range
        response = Reports.best_selling_product_report('2000-10-23', '2010-10-25')
        self.assertEqual(response, 'No Product Found')
        # test providing no date rane
        response = Reports.best_selling_product_report()
        self.assertEqual(response, 'OK')
        
    def test_low_stock_alerts_reports(self):          
        """
        Test the low_stock_alerts function.
        The method doesn't take an inputs so we test one case
        """    
        response = Reports.low_stock_alerts()
        self.assertEqual(response, 'OK')
    
    def test_forecast_stock_demand(self):
        """
        Test the forecast_stock_demand function.
        The method doesn't take an inputs so we test one case
        """    
        response = Reports.forecast_stock_demand()
        self.assertEqual(response, 'OK')

    def tearDown(self):
        """
        Close the database connection and cursor after each test case to free up resources and prevent file descriptor leaks.
        """
        close_connection(self.mycursor, self.connection) 

if __name__ == "__main__":
    unittest.main()