import sys
all_categories = {}
letters = ["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z","-"]
file = open("output.txt","w")

def print_to_file_and_terminal(text):  # this function is for printing to the terminal and output.txt
    print(text,file=file)
    print(text)

def create_category(input_line):
    category = input_line.split(" ")[1]
    if category in all_categories:
        print_to_file_and_terminal("Warning: Cannot create the category for the second time. The stadium has already {}.".format(category))
        return
    row_number = int(input_line.split(" ")[2].split("x")[0])
    column_number = int(input_line.split(" ")[2].split("x")[1])
    category_dict = {}  # for storing every category in a dictionary
    for a in range(0,column_number+1):
        row_dict = {}  # for storing every row in a dictionary
        if a==column_number:
            row_dict["-"]=" "  # for non seats i use "-"
            for t in range(row_number):
                row_dict[t]=t  # numbers (column)
        else:    
            row_dict["-"]=letters[column_number-a-1]  # letters (row)
            for b in range(row_number):
                row_dict[b]="X"
        category_dict[letters[row_number-a-1]] = row_dict
    all_categories[category] = category_dict
    all_categories[category]["sold_ticket"] = {"student" : 0, "full" : 0, "ticket" : 0}  # for calculating revenue
    print_to_file_and_terminal("The category {} having {} seats has been created".format(category,row_number*column_number))

def check_for_interval(category,name,seat_interval,type):  # this funciton for selling interval seats like C1-5 
    initial = int(seat_interval[1:].split("-")[0])
    final = int(seat_interval[1:].split("-")[1])
    seat_list_interval = []
    for seat in range(initial,final+1):
        seat_list_interval.append(seat_interval[0]+str(seat))  #creating a list for store seats that one person want to buy
    for seat in seat_list_interval:
        if int(seat[1:]) not in all_categories[category]["-"]:  # checkin for column is in category
            if seat[0] not in all_categories[category]:  # checking for row is in category
                print_to_file_and_terminal("Error: The category {} has less row and column than the specified index {}!".format(category,seat_interval))
            else:
                print_to_file_and_terminal("Error: The category {} has less column than the specified index {}!".format(category,seat_interval))
            return False
        elif seat[0] not in all_categories[category]:
            print_to_file_and_terminal("Error: The category {} has less row than the specified index {}!".format(category,seat_interval))  # checking for row again
            return False
        elif all_categories[category][seat[0]][int(seat[1:])] != "X":  # checking for if the seat is empty or not
            print_to_file_and_terminal("Warning: The seats {} cannot be sold to {} due some of them have already been sold!".format(seat_interval,name))
            return False
        all_categories[category][seat[0]][int(seat[1:])] = type[0].upper()  # storing the fee type
        all_categories[category]["sold_ticket"][type] += 1
    print_to_file_and_terminal("Success: {} has bought {} at {}".format(name,seat_interval,category))

def sell_ticket(input_line):
    name = input_line.split(" ",4)[1]
    first_type = input_line.split(" ",4)[2]
    if first_type=="season": # changing season to ticket because when showing the table, i want to show season tickets as T and its easier when first letter is same
        type = "ticket" 
    else: 
        type = first_type
    category = input_line.split(" ",4)[3]
    seat_list = input_line.split(" ",4)[4].split(" ")
    for seat in seat_list:
        if "-" not in seat:  # this for non interval seats
            if seat[0] not in all_categories[category]:  # checking for row is in category
                if int(seat[1:]) not in all_categories[category]["-"]: # checking for column is in category
                    print_to_file_and_terminal("Error: The category {} has less row and column than the specified index {}!".format(category,seat))
                else:
                    print_to_file_and_terminal("Error: The category {} has less row than the specified index {}!".format(category,seat))
            elif int(seat[1:]) not in all_categories[category]["-"]:
                print_to_file_and_terminal("Error: The category {} has less column than the specified index {}!".format(category,seat))
            elif all_categories[category][seat[0]][int(seat[1:])] != "X":
                print_to_file_and_terminal("Warning: The seat {} cannot be sold to {} since it was already sold!".format(seat,name))
            else:
                all_categories[category][seat[0]][int(seat[1:])] = type[0].upper() # adding seat to the table
                print_to_file_and_terminal("Success: {} has bought {} at {}".format(name,seat,category))
                all_categories[category]["sold_ticket"][type] += 1
            continue
        check_for_interval(category,name,seat,type)

def cancel_ticket(input_line):
    category = input_line.split(" ")[1]
    seat = input_line.split(" ")[2]
    if seat[0] not in all_categories[category]: # checking for row is in category
        if int(seat[1:]) not in all_categories[category]["-"]: # checking for column is in category
            print_to_file_and_terminal("Error: The category {} has less row and column than the specified index {}!".format(category,seat))
        else:
            print_to_file_and_terminal("Error: The category {} has less row than the specified index {}!".format(category,seat))
        return
    elif int(seat[1:]) not in all_categories[category]["-"]:
        print_to_file_and_terminal("Error: The category {} has less column than the specified index {}!".format(category,seat))
        return
    if all_categories[category][seat[0]][int(seat[1:])] == "S": # determining the type
        type="student"
    elif all_categories[category][seat[0]][int(seat[1:])] == "T":
        type = "ticket"
    elif all_categories[category][seat[0]][int(seat[1:])]=="F":
        type = "full"
    else:
        print_to_file_and_terminal("Error: The seat {} at {} has already been free! Nothing to cancel".format(seat,category))
        return
    all_categories[category][seat[0]][int(seat[1:])] = "X"  # cancelling the seat
    print_to_file_and_terminal("Success: The seat {} at {} has been canceled and now ready to sell again".format(seat,category))
    all_categories[category]["sold_ticket"][type]-=1  # removing from revenue

def balance(input_line):
    category = input_line.split(" ")[1]
    sum_of_students = int(all_categories[category]["sold_ticket"]["student"])
    sum_of_full_pay = int(all_categories[category]["sold_ticket"]["full"])
    sum_of_season_ticket = int(all_categories[category]["sold_ticket"]["ticket"])
    revenue = (sum_of_students*10)+(sum_of_full_pay*20)+(sum_of_season_ticket*250)
    report = "Category report of ’{}’".format(category)
    print_to_file_and_terminal(report)
    print_to_file_and_terminal("-"*len(report))
    print_to_file_and_terminal("Sum of students = {}, Sum of full pay = {}, Sum of season ticket = {}, and Revenues = {} Dollars".format(sum_of_students,sum_of_full_pay,sum_of_season_ticket,revenue))


def show_category(input_line):
    category = input_line.split(" ")[1]
    print_to_file_and_terminal("Printing category layout of {}".format(category))
    for row in all_categories[category]:
        for column in all_categories[category][row]:
            if len(str(all_categories[category][row][column]))==1:
                print(all_categories[category][row][column],end="",file=file)
                print(all_categories[category][row][column],end="")
                if all_categories[category][row][column] == 9:  # when the table gets to 10, it will need only 1 space
                    print(" ", end="",file=file)
                    print(" ", end="")
                else:
                    print("  ", end="",file=file)
                    print("  ", end="")
            else:
                print(all_categories[category][row][column],end="",file=file)
                print(all_categories[category][row][column],end="")
                print(" ", end="",file=file)
                print(" ", end="")
        print_to_file_and_terminal("")
        if row =="-":
            break

def read_input():
    global inputs
    file = open(sys.argv[1],"r")  # getting the input from terminal as argumants with sys module
    inputs = file.read().split("\n") # reading and splitting the input
    file.close()

read_input()

for line in inputs:                 #  calling the right function
    command = line.split(" ")[0]
    if command == "CREATECATEGORY":
        create_category(line)
    elif command == "SELLTICKET":
        sell_ticket(line)
    elif command == "CANCELTICKET":
        cancel_ticket(line)
    elif command == "BALANCE":
        balance(line)
    elif command == "SHOWCATEGORY":
        show_category(line)
    
file.close

#Ahmet Şeref Eker
#2210356098
#Bilgisayar Mühendisliği