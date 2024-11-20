import csv
'''mylist = []
with open("practice.csv",'r') as file :
    myFile = csv.reader(file)
    for row in myFile :
        mylist.append(row)
for i in mylist :
    print(i)
new_value = float(input("Enter new value for sweater price here:"))
mylist[1][2] = new_value

for i in mylist :
    print(i)
with open('practice.csv','w+') as file :
    myFile = csv.writer(file)
    for i in range(len(mylist)) :
        myFile.writerow(mylist[i])'''

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

def buy_or_return_items() : #gets the item number and the amount of items and returns in a tuple
    item_stuff = input("Please enter the item number and how many items you are buying/returning separated with a comma:")
    item_stuff = item_stuff.split(',')
    transaction_info = (item_stuff[0],item_stuff[1])
    return transaction_info

def not_in_stock(item_num) : #use as an error message when the items bought exceeds items in stock
    print(f"There are not enough of item number {item_num}, please try again with less items.")

def item_not_found() : #when customer tries to buy an item that the store doesn't carry
    print("There is no such item in the inventory")

def update_selling_price() : #update the selling price of an item
    item_info = input("Please enter item number and new price separated with a comma:")
    item_info = item_info.split(',')
    item_number = item_info[0]
    new_price = (item_info[1])
    mylist = read_file()
    header_row = mylist[0]
    price_index = header_row.index('Item Price(Selling)')
    x = None
    for i in range(len(mylist)):
        if item_number in mylist[i]:
            x = i
        print(mylist[i])
    if x != None:
        new_value = new_price
        mylist[x][price_index] = new_value
        for i in mylist:
            print(i)
        write_file(mylist)
    else:
        item_not_found()

def add_item_to_inventory(): #add a new item to the inventory
    item_info = input("Please enter item code, item name, item price, and item quantity all separated by commas:")
    new_item = item_info.split(',')
    mylist = read_file()
    for i in range(len(mylist)) :
        print(mylist[i])
    mylist.append(new_item)
    write_file(mylist)
    for i in range(len(mylist)) :
        print(mylist[i])

def add_inventory(): #use when customer returns an item
    item_number, amount = buy_or_return_items()
    amount = int(amount)
    mylist = read_file()
    header_row = mylist[0]
    quantity_index = header_row.index('Quantity of Items')

    x = None
    for i in range(len(mylist)):
        if item_number in mylist[i]:
            x = i
        print(mylist[i])
    if x != None :
        new_value = int(mylist[x][quantity_index]) + amount
        mylist[x][quantity_index] = new_value
        for i in mylist :
            print(i)
        write_file(mylist)
    else :
        item_not_found()


def subtract_inventory(): #use this when customer tries to buy something to display before and after of inventory
    item_number, amount = buy_or_return_items()
    amount = int(amount)
    mylist = []
    mylist = read_file()
    header_row = mylist[0]
    quantity_index = header_row.index('Quantity of Items')

    x = None
    for i in range(len(mylist)):
        if item_number in mylist[i] :
            x = i
        print(mylist[i])
    if x != None :
        new_value = int(mylist[x][quantity_index]) - amount
        mylist[x][quantity_index] = new_value
        if new_value >= 0 :
            for i in mylist :
                print(i)
            write_file(mylist)
        else :
            not_in_stock(item_number)
    else :
        item_not_found()














