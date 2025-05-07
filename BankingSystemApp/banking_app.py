import datetime
import os

# Utility to get current timestamp
def get_timestamp():
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# Automatically add interest if a new month has started
def auto_add_interest():
    today = datetime.date.today()

    # If file doesn't exist or is empty or invalid, initialize and add interest
    if not os.path.exists("last_interest.txt"):
        with open("last_interest.txt", "w") as f:
            f.write(str(today))
        add_interest()
        return

    with open("last_interest.txt", "r") as f:
        content = f.read().strip()

    # Handle empty or invalid content
    try:
        last_date = datetime.datetime.strptime(content, "%Y-%m-%d").date()
    except ValueError:
        last_date = today  # Treat as first run
        with open("last_interest.txt", "w") as f:
            f.write(str(today))
        add_interest()
        return

    # Add interest if new month
    if today.month != last_date.month or today.year != last_date.year:
        add_interest()
        with open("last_interest.txt", "w") as f:
            f.write(str(today))
            
# Add 1% interest to all accounts
def add_interest():
    new_data = []
    try:
        with open("accounts.txt", "r") as file:
            for line in file:
                acc, name, bal = line.strip().split(",")
                bal = float(bal)
                interest = round(bal * 0.01, 2)
                bal += interest
                new_data.append(f"{acc},{name},{bal}\n")
                with open("transactions.txt", "a") as trans_file:
                    trans_file.write(f"{acc},Interest,{interest},{get_timestamp()}\n")
    except FileNotFoundError:
        return
    with open("accounts.txt", "w") as file:
        file.writelines(new_data)
    print("Monthly interest added automatically.")

# Create a new account
def create_account():
    name = input("Enter customer name: ")
    initial_balance = float(input("Enter initial balance (>= 0): "))
    if initial_balance < 0:
        print("Initial balance cannot be negative.")
        return

    acc_no = get_new_account_number()

    with open("accounts.txt", "a") as acc_file, open("customer.txt", "a") as cust_file:
        acc_file.write(f"{acc_no},{name},{initial_balance}\n")
        cust_file.write(f"{acc_no},{name}\n")

    with open("transactions.txt", "a") as trans_file:
        trans_file.write(f"{acc_no},Deposit,{initial_balance},{get_timestamp()}\n")

    print(f"Account created successfully! Account Number: {acc_no}")

# Generate a unique account number
def get_new_account_number():
    try:
        with open("accounts.txt", "r") as file:
            lines = file.readlines()
            if not lines:
                return 1001
            last_line = lines[-1]
            last_acc_no = int(last_line.split(",")[0])
            return last_acc_no + 1
    except FileNotFoundError:
        return 1001

# Deposit money
def deposit_money():
    acc_no = input("Enter account number: ")
    amount = float(input("Enter amount to deposit: "))
    if amount <= 0:
        print("Amount must be positive.")
        return
    update_balance(acc_no, amount, "Deposit")

# Withdraw money
def withdraw_money():
    acc_no = input("Enter account number: ")
    amount = float(input("Enter amount to withdraw: "))
    if amount <= 0:
        print("Amount must be positive.")
        return
    update_balance(acc_no, -amount, "Withdrawal")

# Update balance utility
def update_balance(acc_no, amount, transaction_type):
    updated = False
    new_data = []
    try:
        with open("accounts.txt", "r") as file:
            for line in file:
                acc, name, bal = line.strip().split(",")
                if acc == acc_no:
                    bal = float(bal)
                    if transaction_type == "Withdrawal" and amount < 0 and abs(amount) > bal:
                        print("Insufficient balance.")
                        return
                    bal += amount
                    updated = True
                    new_data.append(f"{acc},{name},{bal}\n")
                else:
                    new_data.append(line)
    except FileNotFoundError:
        print("Account file not found.")
        return

    if updated:
        with open("accounts.txt", "w") as file:
            file.writelines(new_data)
        with open("transactions.txt", "a") as trans_file:
            trans_file.write(f"{acc_no},{transaction_type},{abs(amount)},{get_timestamp()}\n")
        print(f"{transaction_type} successful.")
    else:
        print("Account not found.")

# Check balance
def check_balance():
    acc_no = input("Enter account number: ")
    try:
        with open("accounts.txt", "r") as file:
            for line in file:
                acc, name, bal = line.strip().split(",")
                if acc == acc_no:
                    print(f"Account Holder: {name}\nBalance: {bal}")
                    return
        print("Account not found.")
    except FileNotFoundError:
        print("Account file not found.")

# View transaction history
def view_transactions():
    acc_no = input("Enter account number: ")
    found = False
    try:
        with open("transactions.txt", "r") as file:
            for line in file:
                acc, t_type, amount, timestamp = line.strip().split(",")
                if acc == acc_no:
                    print(f"{t_type}: {amount} on {timestamp}")
                    found = True
        if not found:
            print("No transactions found.")
    except FileNotFoundError:
        print("Transactions file not found.")

# Transfer money
def transfer_money():
    from_acc = input("Enter sender's account number: ")
    to_acc = input("Enter receiver's account number: ")
    amount = float(input("Enter amount to transfer: "))
    if from_acc == to_acc:
        print("Sender and receiver account cannot be the same.")
        return
    if amount <= 0:
        print("Amount must be positive.")
        return

    updated = False
    new_data = []
    try:
        with open("accounts.txt", "r") as file:
            for line in file:
                acc, name, bal = line.strip().split(",")
                if acc == from_acc:
                    bal = float(bal)
                    if amount > bal:
                        print("Insufficient balance.")
                        return
                    bal -= amount
                    updated = True
                    new_data.append(f"{acc},{name},{bal}\n")
                elif acc == to_acc:
                    bal = float(bal) + amount
                    new_data.append(f"{acc},{name},{bal}\n")
                else:
                    new_data.append(line)
    except FileNotFoundError:
        print("Account file not found.")
        return

    if updated:
        with open("accounts.txt", "w") as file:
            file.writelines(new_data)
        timestamp = get_timestamp()
        with open("transactions.txt", "a") as trans_file:
            trans_file.write(f"{from_acc},TransferOut,{amount},{timestamp}\n")
            trans_file.write(f"{to_acc},TransferIn,{amount},{timestamp}\n")
        print("Transfer successful.")
    else:
        print("Sender account not found.")

# Main menu
def main():
    auto_add_interest()  # Check and apply monthly interest automatically

    while True:
        print("\n----- Banking System Menu -----")
        print("1. Create Account")
        print("2. Deposit Money")
        print("3. Withdraw Money")
        print("4. Check Balance")
        print("5. Transaction History")
        print("6. Transfer Money")
        print("7. Exit")
        choice = input("Enter your choice: ")

        if choice == '1':
            create_account()
        elif choice == '2':
            deposit_money()
        elif choice == '3':
            withdraw_money()
        elif choice == '4':
            check_balance()
        elif choice == '5':
            view_transactions()
        elif choice == '6':
            transfer_money()
        elif choice == '7':
            print("Thank you for using the banking system.")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
