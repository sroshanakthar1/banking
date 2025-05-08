import datetime

acc_file = "accounts.txt"
trans_file = "transactions.txt"

#Timestamp
def get_timestamp():
    return datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")

#Create a new account
def create_account():
    name = input("Enter customer name: ")
    initial_balance = float(input("Enter initial balance (>= 0): "))
    if initial_balance < 0:
        print("Initial balance cannot be negative.")
        return

    acc_no = get_new_account_number()

    with open(acc_file, "a") as file:
        file.write(f"{acc_no},{name},{initial_balance}\n")

    with open(trans_file, "a") as file:
        file.write(f"{acc_no},Deposit   ,{initial_balance},{get_timestamp()}\n")

    print(f"Account created successfully! Account Number: {acc_no}")

# Generate a unique account number
def get_new_account_number():
    try:
        with open(acc_file, "r") as file:
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
    updated = False
    new_data = []
    try:
        with open(acc_file, "r") as file:
            for line in file:
                acc, name, bal = line.strip().split(",")
                if acc == acc_no:
                    bal = float(bal)
                    if amount < 0 and amount > bal:
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
        with open(acc_file, "w") as file:
            file.writelines(new_data)
        with open(trans_file, "a") as t_file:
            t_file.write(f"{acc_no},Deposit   ,{amount},{get_timestamp()}\n")
        print("Deposit successful.")
    else:
        print("Account not found.")

# Withdraw money
def withdraw_money():
    acc_no = input("Enter account number: ")
    amount = float(input("Enter amount to withdraw: "))
    if amount <= 0:
        print("Amount must be positive.")
        return
    updated = False
    new_data = []
    try:
        with open(acc_file, "r") as file:
            for line in file:
                acc, name, bal = line.strip().split(",")
                if acc == acc_no:
                    bal = float(bal)
                    if amount < 0 and amount > bal:
                        print("Insufficient balance.")
                        return
                    bal -= amount
                    updated = True
                    new_data.append(f"{acc},{name},{bal}\n")
                else:
                    new_data.append(line)
    except FileNotFoundError:
        print("Account file not found.")
        return

    if updated:
        with open(acc_file, "w") as file:
            file.writelines(new_data)
        with open(trans_file, "a") as t_file:
            t_file.write(f"{acc_no},Withdrawal,{amount},{get_timestamp()}\n")
        print("Withdrawal successful.")
    else:
        print("Account not found.")

# Check balance
def check_balance():
    acc_no = input("Enter account number: ")
    try:
        with open(acc_file, "r") as file:
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
        print("===================================================")
        print("     Date & Time      |     Type       |    Amount")
        print("===================================================")
        with open(trans_file, "r") as file:
            for line in file:
                acc, t_type, amount, timestamp = line.strip().split(",")
                if acc == acc_no:
                    print(f"{timestamp}   |   {t_type}   |    {amount}")
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
        with open(acc_file, "r") as file:
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
        with open(acc_file, "w") as file:
            file.writelines(new_data)
        timestamp = get_timestamp()
        with open(trans_file, "a") as t_file:
            t_file.write(f"{from_acc},TransferOut,{amount},{timestamp}\n")
            t_file.write(f"{to_acc},TransferIn,{amount},{timestamp}\n")
        print("Transfer successful.")
    else:
        print("Sender account not found.")

# Main menu
def main():

    while True:
        print("")
        print("===================================================")
        print("                 Banking System Menu")
        print("===================================================")
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

main()