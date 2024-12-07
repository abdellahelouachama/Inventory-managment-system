from scripts.Product_Management import product_menu
from scripts.Supplier_Management import supplier_menu
from scripts.Sales_Transactions import sales_menu
from scripts.Reports_Analytics import reports_menu

print("Welcome to the Inventory Management System!")
print("What would you like to do?")

operations = ['Product Management', 'Supplier Management', 'Sales Transactions', 'Reports and Analytics', 'Exit']
for operation in operations:
    print(operation)

while True:
    choosen_operation = input("Select an operation: ").lower().strip()

    try:
        if choosen_operation == (operations[0].lower().strip()):
            product_menu()

        elif choosen_operation == (operations[1].lower().strip()):
            supplier_menu()

        elif choosen_operation == (operations[2].lower().strip()):
            sales_menu()

        elif choosen_operation == (operations[3].lower().strip()):
            reports_menu()

        elif choosen_operation == (operations[4].lower().strip()):
            print("Thanks for using the Inventory Management System!")
            break

        else:
            raise ValueError ("Please entre a valid operation!")

    except ValueError as e:
        print(e)            
