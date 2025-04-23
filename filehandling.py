acc_num = input("name of file: ")

with open (acc_num + "transact.txt", 'w') as file:
    file.write("Transaction history for account number: " + acc_num + "\n")
    file.write("Date\t\tTransaction Type\tAmount\n")
    file.write("-------------------------------------------------\n")
    
    

with open (acc_num + "transact.txt", 'r') as file: pass
