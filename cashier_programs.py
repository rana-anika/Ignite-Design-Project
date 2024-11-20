import csv
import numpy as np
def read_file(file_name = "practice.csv") : #reads the csv file and returns the contents in a 2d list
    mylist = []
    with open(file_name, 'r') as file:
        myfile = csv.reader(file)
        for row in myfile:
            mylist.append(row)
    return mylist

def write_file(mylist, file_name = "practice.csv") : #same as read_file, writes the updated values back to file
    with open(file_name, 'w+') as file:
        myfile = csv.writer(file)
        for i in range(len(mylist)):
            myfile.writerow(mylist[i])
def display_transaction(item_number,item_name,total_items_bought,item_price) : #display transaction for cashier
    total_price = int(total_items_bought) * float(item_price)
    transaction_log = {'Item Number':item_number,'Item Name':item_name,'Total Items Bought':total_items_bought,'Item Price': item_price, 'Total Price':total_price}
    #print("Here is the transaction information:")
    #print(transaction_log)
    return transaction_log
def buy_items() : #gets the item number and the amount of items and returns in a tuple
    while True :
        item_stuff = input("Please enter the item number and how many items you are buying separated with a comma:")
        item_stuff = item_stuff.split(',')
        try :
            check = int(item_stuff[1])
            if check >= 0 :
                transaction_info = (item_stuff[0],item_stuff[1])
                return transaction_info
            else :
                print("You entered a negative value or float.")
                continue
        except :
            print("Please enter a positive integer")
            continue
def return_items() :
    while True:
        item_stuff = input("Please enter the item number and how many items you are returning separated with a comma:")
        item_stuff = item_stuff.split(',')
        try:
            check = int(item_stuff[1])
            if check >= 0:
                transaction_info = (item_stuff[0], item_stuff[1])
                return transaction_info
            else:
                print("You entered a negative value or float.")
                continue
        except:
            print("Please enter a positive integer")
            continue

def restock_start() : #use in the beginning of restock function for a more personalized message
    while True:
        item_stuff = input("Please enter the item number and how many items you are restocking separated with a comma:")
        item_stuff = item_stuff.split(',')
        try:
            check = int(item_stuff[1])
            if check >= 0:
                transaction_info = (item_stuff[0], item_stuff[1])
                return transaction_info
            else:
                print("You entered a negative value or float.")
                continue
        except:
            print("Please enter a positive integer")
            continue
def how_many_things_are_you_going_to_buy() :
    while True :
        try :
            number = int(input("Please enter how many types of items you are checking out:"))
            if number >= 0 :
                return number
            else :
                print("Enter a positive integer.")
                continue
        except :
            print("Please enter an integer value")
            continue
def how_many_things_are_you_going_to_return() :
    while True :
        try :
            number = int(input("Please enter how many types of items you are returning:"))
            if number >= 0 :
                return number
            else :
                print("Enter a positive integer.")
                continue
        except :
            print("Please enter an integer value")
            continue

def not_in_stock(item_num) : #use as an error message when the items bought exceeds items in stock
    print(f"There are not enough of item number {item_num}, please try again with less items.")

def item_not_found() : #when customer tries to buy an item that the store doesn't carry
    print("There is no such item in the inventory")

def update_selling_price() : #update the selling price of an item
    while True :
        try :
            item_info = input("Please enter item number and new price separated with a comma:")
            item_info = item_info.split(',')
            item_number = item_info[0]
            new_price = float(item_info[1])
            if new_price >= 0.0 :
                break
            else :
                print("Enter valid price")
                continue
        except :
            print("Enter a valid float variable")
            continue

    mylist = read_file()
    header_row = mylist[0]
    price_index = header_row.index('Item Price(Selling)')
    x = None
    print("Original Prices")
    for i in range(len(mylist)):
        if item_number in mylist[i]:
            x = i
        print(mylist[i])
    if x is not None:
        new_value = new_price
        mylist[x][price_index] = new_value
        print("New Prices")
        for i in mylist:
            print(i)
        write_file(mylist)
    else:
        item_not_found()

def add_new_item_to_inventory(): #add a new item to the inventory
    new_item = []
    mylist = read_file()
    print("Old inventory")
    for i in mylist :
        print(i)
    while True : #check if item is already in the inventory
        item_num = input("Please enter the unique item code:")
        id_check = False
        for i in mylist :
            if item_num in i :
                print("Item already in inventory, try again")
                id_check = True
        if id_check is False :
            new_item.append(item_num)
            break
    item_name = input("Please enter the item name:")#name can be anything so don't really have to check
    new_item.append(item_name)
    while True : #check if price is valid
        try :
            item_info = input("Please enter item price:")
            new_price = float(item_info)
            if new_price >= 0.0 :
                new_item.append(new_price)
                break
            else :
                print("Enter valid price")
                continue
        except :
            print("Enter a valid float variable")
            continue
    while True: #check if amount is valid
        try:
            number = int(input("Please enter how many items you are adding to stock:"))
            if number >= 0:
                new_item.append(number)
                break
            else:
                print("Enter a positive integer.")
                continue
        except:
            print("Please enter an integer value")
            continue
    mylist.append(new_item)
    write_file(mylist)
    print("New Inventory")
    for i in range(len(mylist)) :
        print(mylist[i])

def append_transaction_log_checkout(transaction_list,file_name = "transaction_log.csv",newline='') : #need to fix
    thelist = ["Purchase"]
    with open(file_name,'a') as file:
        myfile = csv.writer(file)
        myfile.writerow(thelist)
        myfile.writerows(transaction_list)
        myfile.writerow([])
def append_transaction_log_return(transaction_list,file_name = "transaction_log.csv",newline='') : #need to fix
    thelist = ["Return"]
    with open(file_name,'a') as file:
        myfile = csv.writer(file)
        myfile.writerow(thelist)
        myfile.writerows(transaction_list)
        myfile.writerow([])

def add_back_to_inventory(): #use when customer returns an item
    while True :
        item_number, amount = return_items()
        amount = int(amount)
        mylist = read_file()
        header_row = mylist[0]
        quantity_index = header_row.index('Quantity of Items')

        x = None
        for i in range(len(mylist)):
            if item_number in mylist[i]:
                x = i
            #print(mylist[i])
        if x is not None :
            new_value = int(mylist[x][quantity_index]) + amount
            mylist[x][quantity_index] = new_value
            #for i in mylist :
                #print(i)
            write_file(mylist)
            return_row = mylist[x]
            return_row[quantity_index] = amount
            return return_row
        else :
            item_not_found()
            print("Our store does not carry this item, please try again")
            continue


def subtract_inventory(): #use this when customer tries to buy something to display before and after of inventory
    while True :
        item_number, amount = buy_items()
        amount = int(amount)
        mylist = []
        mylist = read_file()
        header_row = mylist[0]
        quantity_index = header_row.index('Quantity of Items')
        name_index = header_row.index('Item Name')
        price_index = header_row.index('Item Price(Selling)')


        x = None
        for i in range(len(mylist)):
            if item_number in mylist[i] :
                x = i
            #print(mylist[i])
        if x is not None :
            new_value = int(mylist[x][quantity_index]) - amount
            mylist[x][quantity_index] = new_value
            if new_value >= 0 :
                #for i in mylist :
                    #print(i)
                write_file(mylist)
                item_price = mylist[x][price_index]
                item_name = mylist[x][name_index]
                display_transaction(item_number, item_name, amount, item_price)
                return display_transaction(item_number, item_name, amount, item_price)
            else :
                not_in_stock(item_number)
                continue
        else :
            item_not_found()
            continue

##############################################################################################################

def checkout(): #cashier uses this for checkout
    number_of_items = how_many_things_are_you_going_to_buy()
    total_transaction = []
    valid_transactions = []
    total_price = []
    for item_type in range(number_of_items) :
        transaction = subtract_inventory()
        if transaction is not None :
            total_transaction.append(transaction)
            price = transaction['Total Price']
            total_price.append(price)
            for key,value in transaction.items() :
                valid_transactions.append(value)
    official_transactions = np.array(valid_transactions).reshape(number_of_items,5)
    for j in total_transaction :
        print(j)
    print(f'Your total price is ${sum(total_price)}')
    append_transaction_log_checkout(official_transactions, file_name="transaction_log.csv")


#################################################################################################################
def restock() : #when cashier wants to restock an amount
    item_number, amount = restock_start()
    amount = int(amount)
    mylist = read_file()
    header_row = mylist[0]
    quantity_index = header_row.index('Quantity of Items')

    x = None
    print("Before Restock")
    for i in range(len(mylist)):
        if item_number in mylist[i]:
            x = i
        print(mylist[i])
    if x is not None:
        new_value = int(mylist[x][quantity_index]) + amount
        mylist[x][quantity_index] = new_value
        print("After Restock")
        for i in mylist:
            print(i)
        write_file(mylist)
    else:
        print("Restock failed")
        item_not_found()
##################################################################################################################
def return_function() :
    number_of_items = how_many_things_are_you_going_to_return()
    total_transaction = []
    for item_type in range(number_of_items):
        transaction = add_back_to_inventory()
        total_transaction.append(transaction)
    official_transaction = np.array(total_transaction).reshape(number_of_items,4)
    print("Successful return")
    append_transaction_log_return(official_transaction, file_name="transaction_log.csv")



checkout()
return_function()
#buttons and which functions they would correspond to:
#checkout button corresponds with checkout()
#restock button corresponds with restock()
#add new item corresponds with add_new_item_to_inventory()
#return corresponds with return_function()


