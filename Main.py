from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QTableWidget, QTableWidgetItem, \
    QDialog, QLineEdit
import pandas as pd

# Function to load and display the DataFrame (Customers Page) with styled buttons
def load_customers_page(local_file_path):
    try:
        # Load the Excel file into a DataFrame
        df = pd.read_excel(local_file_path)

        # Create the table widget to display the DataFrame
        table = QTableWidget()
        table.setRowCount(df.shape[0])
        table.setColumnCount(df.shape[1])
        table.setHorizontalHeaderLabels(df.columns)

        # Populate the table with data
        for i in range(df.shape[0]):
            for j in range(df.shape[1]):
                table.setItem(i, j, QTableWidgetItem(str(df.iat[i, j])))

        # === Button Styling (Matching Sidebar Style) ===
        button_style = """
            QPushButton {
                background-color: #cdcdcd;
                color: black;
                font-weight: bold;
                border-radius: 10px;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: #9f9f9f;
            }
        """

        # Create the button layout (Vertical layout)
        button_layout = QVBoxLayout()
        button_layout.setSpacing(20)  # Add some spacing between the buttons
        button_layout.setContentsMargins(10, 0, 10, 0)  # Consistent margins

        # Add Customer button
        add_customer_button = QPushButton("Add Customer")
        add_customer_button.setStyleSheet(button_style)
        add_customer_button.clicked.connect(lambda: add_customer(df, local_file_path, table))
        button_layout.addWidget(add_customer_button)

        # Remove Customer button
        remove_customer_button = QPushButton("Remove Customer")
        remove_customer_button.setStyleSheet(button_style)
        remove_customer_button.clicked.connect(lambda: remove_customer(df, local_file_path, table))
        button_layout.addWidget(remove_customer_button)

        # Calculate Money button (placeholder)
        calculate_button = QPushButton("Calculate Money (To be implemented)")
        calculate_button.setStyleSheet(button_style)
        button_layout.addWidget(calculate_button)

        # Main layout for the page (Horizontal)
        page_layout = QHBoxLayout()
        page_layout.addWidget(table)  # Add the table
        page_layout.addLayout(button_layout)  # Add the buttons to the right

        # Create a widget to hold the layout and return it
        page_widget = QWidget()
        page_widget.setLayout(page_layout)

        return page_widget
    except Exception as e:
        print(f"Error loading Excel file: {e}")
        return QLabel("Failed to load customers data")


# Function to add a customer (Dialog for input)
def add_customer(df, local_file_path, table):
    dialog = QDialog()
    dialog.setWindowTitle("Add Customer")

    # Create input fields for each of the columns
    name_label = QLabel("Name:")
    name_input = QLineEdit()

    num_accounts_label = QLabel("Number of Accounts:")
    num_accounts_input = QLineEdit()

    last_transaction_label = QLabel("Last Transaction:")
    last_transaction_input = QLineEdit()

    paid_label = QLabel("Paid:")
    paid_input = QLineEdit()

    owes_label = QLabel("Owes:")
    owes_input = QLineEdit()

    total_label = QLabel("Total:")
    total_input = QLineEdit()

    # Create a layout for the dialog
    dialog_layout = QVBoxLayout()
    dialog_layout.addWidget(name_label)
    dialog_layout.addWidget(name_input)
    dialog_layout.addWidget(num_accounts_label)
    dialog_layout.addWidget(num_accounts_input)
    dialog_layout.addWidget(last_transaction_label)
    dialog_layout.addWidget(last_transaction_input)
    dialog_layout.addWidget(paid_label)
    dialog_layout.addWidget(paid_input)
    dialog_layout.addWidget(owes_label)
    dialog_layout.addWidget(owes_input)
    dialog_layout.addWidget(total_label)
    dialog_layout.addWidget(total_input)

    # OK and Cancel buttons
    ok_button = QPushButton("OK")
    ok_button.clicked.connect(lambda: add_customer_to_db(df, name_input.text(), num_accounts_input.text(),
                                                         last_transaction_input.text(), paid_input.text(),
                                                         owes_input.text(), total_input.text(),
                                                         local_file_path, table, dialog))
    dialog_layout.addWidget(ok_button)

    cancel_button = QPushButton("Cancel")
    cancel_button.clicked.connect(dialog.close)
    dialog_layout.addWidget(cancel_button)

    dialog.setLayout(dialog_layout)
    dialog.exec_()


def add_customer_to_db(df, name, num_accounts, last_transaction, paid, owes, total, local_file_path, table, dialog):
    try:
        # Debugging outputs to check values being passed in
        print(f"Name: {name}")
        print(f"Number of Accounts: {num_accounts}")
        print(f"Last Transaction (before conversion): {last_transaction}")
        print(f"Paid: {paid}")
        print(f"Owes: {owes}")
        print(f"Total (before conversion): {total}")

        # Validate and convert inputs as necessary
        num_accounts = int(num_accounts) if num_accounts else 0

        # Convert Last Transaction to datetime, handle errors by assigning NaT (Not a Time) if invalid
        if last_transaction:
            last_transaction = pd.to_datetime(last_transaction, errors='coerce')
        else:
            last_transaction = pd.NaT  # Not a Time (equivalent to NULL for dates)
        print(f"Last Transaction (after conversion): {last_transaction}")

        # Convert Paid, Owes, and Total to float (use 0.0 if invalid or empty)
        paid = float(paid) if paid else 0.0
        owes = float(owes) if owes else 0.0
        total = float(total) if total else 0.0
        print(f"Total (after conversion): {total}")

        # Create a new row as a DataFrame
        new_row = pd.DataFrame({
            "Name": [name],
            "Number of Accounts": [num_accounts],
            "Last Transaction": [last_transaction],
            "Paid": [paid],
            "Owes": [owes],
            "Total": [total]
        })

        # Concatenate the new row to the existing DataFrame
        df = pd.concat([df, new_row], ignore_index=True)
        print("New customer added to DataFrame")

        # Save the updated DataFrame to the Excel file
        df.to_excel(local_file_path, index=False)
        print(f"DataFrame saved to {local_file_path}")

        # Update the table in the UI
        table.setRowCount(df.shape[0])
        for i in range(df.shape[0]):
            for j in range(df.shape[1]):
                table.setItem(i, j, QTableWidgetItem(str(df.iat[i, j])))

        # Close the dialog properly
        dialog.accept()

    except Exception as e:
        print(f"Error: {e}")
        dialog.reject()


# Function to remove the selected customer
def remove_customer(df, local_file_path, table):
    selected_row = table.currentRow()

    if selected_row >= 0:
        # Remove the selected row from the DataFrame
        df = df.drop(df.index[selected_row])
        df.reset_index(drop=True, inplace=True)

        # Save the updated DataFrame to the Excel file
        df.to_excel(local_file_path, index=False)

        # Update the table in the UI
        table.removeRow(selected_row)
