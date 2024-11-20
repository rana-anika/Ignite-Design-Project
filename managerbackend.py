# Cashier Backend

#inventory.csv : Item Number[0], Item Name[1], Quantity of Items[2], Item Price(Selling) [3], Item Price(Production)[4]


reports_file = open('financialreport.csv','r+')

reports = reports_file.read()

# Gets entire inventory
def get_inventory():
    reports_file = open('financialreport.csv','r+')
    reports = []
    for line in reports_file:
        line = str(line)
        linestripped = line.strip('\n')
        new_line = linestripped.split(',')
        reports.append(new_line)
    reports_file.close()
    return reports


def check_index(file,index):
    file_list = file[:]
    try:
        file_list[index][0]
    except:
        print('Item value does not exist.')
        return False


# Get Item Number
def get_item_num(file, index):
    try:    
        reports_list = file[:]
        item_num = reports_list[index][0]
        return item_num
    except:
        return "Invalid input"
# Get Item Name
def get_item_name(file, index):
    try:
        reports_list = file[:]
        item_name = reports_list[index][1]
        return item_name
    except:
        return "Invalid input"
# Gets Transaction Number
def get_transaction_num(file, index):
    try:
        reports_list = file[:]
        transaction_num = reports_list[index][2]
        return transaction_num
    except:
        return "Invalid input"
# Gets Profit
def get_profit(file, index):
    try:
        reports_list = file[:]
        profit = reports_list[index][3]
        return profit
    except:
        return "Invalid input"
# Gets Date Sold
def get_date_sold(file, index):
    try:
        reports_list = file[:]
        date_sold = reports_list[index][4]
        return date_sold
    except:
        return "Invalid input"

# Gets full item info as a list
def get_full_item_info(file, index):
    try:
        reports_list = file[:]
        full_item_info = reports_list[index][0:]
        return full_item_info
    except:
        return "Invalid input"

# Get non file values: Most Sold Item, Least Sold Item, Quantity of items sold for each item
def get_item_counts(file):
    items = {}
    for line in file:
        if file.index(line) == 0:
            pass
        elif line[1] not in items:
            items[line[1]] = 1
        else:
            items[line[1]] +=1
    return items

# Returns item(s) that are sold the most when inputted a dicitionary from get_item_counts, and returns the number of times the item was sold at index -1 of the return value
def get_most_sold(items):
    most_sold_val = 0
    most_sold = ''
    for i in items:
        if items[i] > most_sold_val:
            most_sold = i
            most_sold_val = items[i]
        elif items[i] == most_sold_val:
            most_sold += ' , ' + i
        else:
            pass
    return most_sold, most_sold_val

def get_least_sold(items):
    values = []
    for i in items:
        values.append(items[i])
    least_sold_val = min(values)
    least_sold = ''
    for i in items:
        if items[i] == least_sold_val:
            least_sold = i
        else:
            pass
    return least_sold, least_sold_val

# Gets full inventory
inventory = get_inventory()




# Testing
item_num = get_item_num(inventory, 6)
print(item_num)

item_name = get_item_name(inventory, 4)
print(item_name)

transaction_num = get_transaction_num(inventory, 1)
print(transaction_num)

profit = get_profit(inventory, 4)
print(profit)


item_counts = get_item_counts(inventory) # Gets dictionary of all items and quantity of items sold for each
print(item_counts)

most_sold_item = get_most_sold(item_counts)
print(most_sold_item)

print(get_least_sold(item_counts))

reports_file.close()