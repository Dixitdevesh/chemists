import csv
from datetime import datetime

MEDICINE_FILE = 'medicines.csv'
SALES_FILE = 'sales.csv'
LOW_STOCK_THRESHOLD = 10

def initialize_files():
    try:
        with open(MEDICINE_FILE, mode='x', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['ID', 'Name', 'Category', 'Quantity', 'Price'])
    except FileExistsError:
        pass

    try:
        with open(SALES_FILE, mode='x', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Transaction ID', 'Medicine ID', 'Quantity Sold', 'Total Price', 'Date'])
    except FileExistsError:
        pass

def add_medicine():
    id = input("Enter Medicine ID: ")
    name = input("Enter Medicine Name: ")
    category = input("Enter Medicine Category: ")
    quantity = input("Enter Medicine Quantity: ")
    price = input("Enter Medicine Price: ")

    if quantity.isdigit() and float(price) >= 0:
        with open(MEDICINE_FILE, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([id, name, category, quantity, price])
            print(f"Medicine {name} added successfully!\n")
    else:
        print("Invalid quantity or price entered. Please try again.\n")

def view_medicines():
    """Display all medicines in a user-friendly format."""
    try:
        with open('medicines.csv', mode='r') as file:
            reader = csv.DictReader(file)
            medicines = [row for row in reader]

            
            if not medicines:
                print("\nNo medicines available.\n")
                return

            
            print("\n{:<10} {:<30} {:<15} {:<10} {:<10}".format('ID', 'Name', 'Category', 'Quantity', 'Price'))
            print("=" * 75)

            
            for medicine in medicines:
                print("{:<10} {:<30} {:<15} {:<10} ${:<10.2f}".format(
                    medicine['ID'],
                    medicine['Name'],
                    medicine['Category'],
                    medicine['Quantity'],
                    float(medicine['Price'])
                ))
            print("=" * 75)  

    except FileNotFoundError:
        print("Medicines data file not found. Please ensure the file exists.")
    except Exception as e:
        print(f"An error occurred while viewing medicines: {e}")


def search_medicine():
    id = input("Enter Medicine ID to search: ")
    found = False
    try:
        with open(MEDICINE_FILE, mode='r') as file:
            reader = csv.reader(file)
            next(reader)  # Skip the header
            for row in reader:
                if row[0] == id:
                    print(f"Medicine Found: ID: {row[0]}, Name: {row[1]}, Category: {row[2]}, Quantity: {row[3]}, Price: {row[4]}")
                    found = True
                    check_stock_level(int(row[3]))
                    break
            if not found:
                print("Medicine not found.\n")
    except FileNotFoundError:
        print("No medicine records found.\n")

def check_stock_level(quantity):
    if quantity < LOW_STOCK_THRESHOLD:
        print("Warning: Stock is low!\n")

def update_medicine():
    id = input("Enter Medicine ID to update: ")
    found = False
    updated_rows = []
    
    try:
        with open(MEDICINE_FILE, mode='r') as file:
            reader = csv.reader(file)
            header = next(reader)  # Store header
            updated_rows.append(header)  # Add header to updated_rows
            for row in reader:
                if row[0] == id:
                    found = True
                    print("Leave field blank to keep current value.")
                    new_name = input(f"New Name [{row[1]}]: ") or row[1]
                    new_category = input(f"New Category [{row[2]}]: ") or row[2]
                    new_quantity = input(f"New Quantity [{row[3]}]: ") or row[3]
                    new_price = input(f"New Price [{row[4]}]: ") or row[4]
                    updated_rows.append([id, new_name, new_category, new_quantity, new_price])
                    print(f"Medicine ID {id} updated successfully.\n")
                else:
                    updated_rows.append(row)
        if found:
            with open(MEDICINE_FILE, mode='w', newline='') as file:
                writer = csv.writer(file)
                writer.writerows(updated_rows)
        else:
            print("Medicine ID not found.\n")
    except FileNotFoundError:
        print("No medicine records found.\n")

def batch_update_medicines():
    while True:
        id = input("Enter Medicine ID to update (or type 'done' to finish): ")
        if id.lower() == 'done':
            break
        found = False
        updated_rows = []
        try:
            with open(MEDICINE_FILE, mode='r') as file:
                reader = csv.reader(file)
                header = next(reader)
                updated_rows.append(header)
                for row in reader:
                    if row[0] == id:
                        found = True
                        print("Leave field blank to keep current value.")
                        new_name = input(f"New Name [{row[1]}]: ") or row[1]
                        new_category = input(f"New Category [{row[2]}]: ") or row[2]
                        new_quantity = input(f"New Quantity [{row[3]}]: ") or row[3]
                        new_price = input(f"New Price [{row[4]}]: ") or row[4]
                        updated_rows.append([id, new_name, new_category, new_quantity, new_price])
                        print(f"Medicine ID {id} updated successfully.")
                    else:
                        updated_rows.append(row)
            if found:
                with open(MEDICINE_FILE, mode='w', newline='') as file:
                    writer = csv.writer(file)
                    writer.writerows(updated_rows)
            else:
                print("Medicine ID not found.")
        except FileNotFoundError:
            print("No medicine records found.\n")

def delete_medicine():
    id = input("Enter Medicine ID to delete: ")
    found = False
    updated_rows = []

    try:
        with open(MEDICINE_FILE, mode='r') as file:
            reader = csv.reader(file)
            header = next(reader)  # Store header
            updated_rows.append(header)  # Add header to updated_rows
            for row in reader:
                if row[0] != id:
                    updated_rows.append(row)
                else:
                    found = True
                    print(f"Medicine ID {id} deleted successfully.\n")
        if found:
            with open(MEDICINE_FILE, mode='w', newline='') as file:
                writer = csv.writer(file)
                writer.writerows(updated_rows)
        else:
            print("Medicine ID not found.\n")
    except FileNotFoundError:
        print("No medicine records found.\n")

def record_sale():
    id = input("Enter Medicine ID sold: ")
    quantity_sold = input("Enter Quantity Sold: ")

    if quantity_sold.isdigit():
        quantity_sold = int(quantity_sold)
        found = False
        updated_rows = []

        try:
            with open(MEDICINE_FILE, mode='r') as file:
                reader = csv.reader(file)
                header = next(reader)
                updated_rows.append(header)
                for row in reader:
                    if row[0] == id:
                        found = True
                        current_quantity = int(row[3])
                        if quantity_sold <= current_quantity:
                            new_quantity = current_quantity - quantity_sold
                            total_price = quantity_sold * float(row[4])
                            updated_rows.append([id, row[1], row[2], str(new_quantity), row[4]])
                            record_sale_to_file(id, quantity_sold, total_price)
                            print(f"Sale recorded: {quantity_sold} of {row[1]} sold.")
                        else:
                            print("Insufficient stock to complete the sale.\n")
                    else:
                        updated_rows.append(row)
            if found:
                with open(MEDICINE_FILE, mode='w', newline='') as file:
                    writer = csv.writer(file)
                    writer.writerows(updated_rows)
            else:
                print("Medicine ID not found.\n")
        except FileNotFoundError:
            print("No medicine records found.\n")
    else:
        print("Invalid quantity entered. Please try again.\n")

def record_sale_to_file(medicine_id, quantity_sold, total_price):
    date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    transaction_id = datetime.now().strftime('%Y%m%d%H%M%S')
    with open(SALES_FILE, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([transaction_id, medicine_id, quantity_sold, total_price, date])

def generate_sales_report():
    try:
        with open(SALES_FILE, mode='r') as file:
            reader = csv.reader(file)
            next(reader)  # Skip the header
            sales_data = []
            total_sales = 0
            print("Sales Report:")
            print("Transaction ID, Medicine ID, Quantity Sold, Total Price, Date")
            for row in reader:
                sales_data.append(row)
                total_sales += float(row[3])
                print(", ".join(row))
            print(f"\nTotal Sales: {total_sales}\n")
    except FileNotFoundError:
        print("No sales records found.\n")

def main():
    initialize_files()
    while True:
        print("Welcome to Medical Shop Management System")
        print("1. Add Medicine")
        print("2. View Medicines")
        print("3. Search Medicine")
        print("4. Update Medicine")
        print("5. Batch Update Medicines")
        print("6. Delete Medicine")
        print("7. Record Sale")
        print("8. Generate Sales Report")
        print("9. Exit")
        
        choice = input("Choose an option: ")
        
        if choice == '1':
            add_medicine()
        elif choice == '2':
            view_medicines()
        elif choice == '3':
            search_medicine()
        elif choice == '4':
            update_medicine()
        elif choice == '5':
            batch_update_medicines()
        elif choice == '6':
            delete_medicine()
        elif choice == '7':
            record_sale()
        elif choice == '8':
            generate_sales_report()
        elif choice == '9':
            print("Exiting the system. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.\n")

if __name__ == "__main__":
    main()
