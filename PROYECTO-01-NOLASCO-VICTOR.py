"""
PROJECT 1: LifeStore products report
"""

import sys
from lifestore_file import lifestore_products 
from lifestore_file import lifestore_searches 
from lifestore_file import lifestore_sales



""" the following block is the login code
    check that username and password entered are in the users list
    also handle 2 types of errors: unregistered user and incorrect password
"""
#users_list = [username, password, type]
#type=0 for admins, type=1 for regular users
users_list = [["admin", "password", 0],
              ["javier", "contra", 0],
              ["pedro", "1234", 1], 
              ["maria", "5678", 1]]
login_success = 0   #1=success, -1=incorrect password, 0=unregistered user
while login_success != 1:
    login_success = 0        #necessary for correct error handling
    print("\n---------------------------------------")
    print("\n\t\t\t\tLOGIN")
    print("\nEnter your username and password")
    user = input("-> Username: ")
    password = input("-> Password: ")
    
    for userL in users_list:
        if userL[0] == user:
            if userL[1] == password:
                user_type = userL[2]
                login_success = 1
                print("\n------------ Welcome " + user + " ------------")
            else:
                login_success = -1
                print("\n* Error: Incorrect password ")
            break
    if login_success == 0:
        print("\n* Error: Unregistered user ")

if user_type == 1:
    print("\n* Since you are a regular user, you \n  don't have access " 
          "to the admins' menu")
    input("\nPress enter to accept and close the program.")
    sys.exit()



""" get the total sales, total refunds, average score and total searches
    of every product, this data will be used later and is added to the 
    lifestore_product list, so the list structure will be:
    lifestore_products = [id_product, name, price, category, stock,
                          sales, refunds, avr_score, searches]
"""
for product in lifestore_products:
    sales_counter = 0
    refunds_counter = 0
    score_sum = 0
    searches_counter = 0
    
    for sale in lifestore_sales:
        if sale[1] == product[0]:   #match id_product in both lists 
            sales_counter += 1
            score_sum += sale[2]
            if sale[4] == 1:        #there was a refund
                refunds_counter += 1           
    product.append(sales_counter)
    product.append(refunds_counter)
    if sales_counter != 0:      #to avoid divisions by zero
        product.append(score_sum/sales_counter)     #calculate the average
    else: 
        product.append(0)
        
    for search in lifestore_searches:
        if search[1] == product[0]:     #match id_product in both lists
            searches_counter += 1
    product.append(searches_counter)



"""generate a list of the products by category that will be used later"""
#categories = [category, [products]]
categories = []
for product in lifestore_products:
    ban = 0     #to indicate if the category is alredy in the list
    for category in categories:
        if category[0] == product[3]:
            category[1].append(product)
            ban = 1
            break
    if ban == 0:    #the category is still not in the list
        categories.append([product[3],[product]])



"""generate a product list order by average score that will be used later"""
aux_list = list(lifestore_products)
score_list = []
while aux_list:
    minimum = aux_list[0][7]
    actual_product = aux_list[0]
    for product in aux_list:
        if product[7] < minimum:
            minimum = product[7]
            actual_product = product
    score_list.append(actual_product)
    aux_list.remove(actual_product)
score_list.reverse() 



"""menu"""
opt = -1
while opt != "0":
    print("\n\t\t\tADMINISTRATOR MENU \n")
    print("Choose an option:\n")
    print("1. Show best seller products")
    print("2. Show most searched products")
    print("3. Show less sold products by category")
    print("4. Show less searched products by category")
    print("5. Show best reviewed products")
    print("6. Show worst reviewed products")
    print("7. Show sales and income per month")
    print("0. Exit")
    opt = input("-> Option: ")
    
    if opt == "1":
        
        """display a list with the 50 best selling products"""
        #generate a product list order by total sales
        aux_list = list(lifestore_products)
        sales_list = []
        while aux_list:
            minimum = aux_list[0][5]
            actual_product = aux_list[0]
            for product in aux_list:
                if product[5] < minimum:
                    minimum = product[5]
                    actual_product = product
            sales_list.append(actual_product)
            aux_list.remove(actual_product)
        sales_list.reverse()    
          
        #filter the first 50, and print them in a table form
        print("\n\n\t\t\tTOP 50 BEST-SELLING PRODUCTS\n")
        print("Top \t ID \t Product (short name)\t\t\t Sales\n")
        top = 1     #to count the 50 products
        for product in sales_list:
            #display 50 products max and only those with at least 1 sale
            if top>50 or product[5]<1:     
                break
            else:
                print(top, "  \t", product[0], " \t", product[1][:25], " \t ", 
                      product[5])
                top += 1
        print("\n*Note: Only products with at least 1 sale are displayed")
        
        input("\nPress enter to continue.")
        
        
        
    elif opt == "2":
        
        """display the 50 most searched products"""
        #generate a product list order by total searches 
        aux_list = list(lifestore_products)
        searches_list = []
        while aux_list:
            minimum = aux_list[0][8]
            actual_product = aux_list[0]
            for product in aux_list:
                if product[8] < minimum:
                    minimum = product[8]
                    actual_product = product
            searches_list.append(actual_product)
            aux_list.remove(actual_product)
        searches_list.reverse()  
        
        #filter the first 50 and print them in a table form
        print("\n\n\t\t\tTOP 50 MOST SEARCHED PRODUCTS\n")
        print("Top \t ID \t Product (short name)\t\t\t Searches\n")
        top = 1 #once again to count the 50 products
        for product in searches_list:
            if top>50 or product[8]<1:
                break
            else:
                print(top, "  \t", product[0], " \t", product[1][:25], " \t  ", 
                      product[8])
                top += 1
        print("\n*Note: Only products with at least 1 search are displayed")
        
        input("\nPress enter to continue.")
        
        
        
    elif opt == "3":
        
        """show the less sold products by category"""
        print("\n\n\t\tTOP 5 LESS SOLD PRODUCTS BY CATEGORY")
        #use the categories list created previously
        for category in categories:
            aux_list = list(category[1])
            sales_list = []
            #sort the product list of every category
            while aux_list:
                minimum = aux_list[0][5]
                actual_product = aux_list[0]
                for product in aux_list:
                    if product[5] < minimum:
                        minimum = product[5]
                        actual_product = product
                sales_list.append(actual_product)
                aux_list.remove(actual_product)  
              
            #filter the last 5, and print them in a table form
            print("\n\nCategory: ", category[0].upper())
            print("\nTop \t ID \t Product (short name)\t\t\t Sales\n")
            top = 1     #to count the 5 products
            for product in sales_list:
                if top>5:     
                    break
                else:
                    print(top, "  \t", product[0], " \t", product[1][:25], 
                          " \t ", product[5])
                    top += 1
        print("\n\n*Note: Categories with less than 5 products shown do \n"
              "\t\tnot have enought products")
        
        input("\nPress enter to continue.")
        
        
        
    elif opt == "4":
        
        """show the less searched products by category"""
        print("\n\n\t\tTOP 5 LESS SEARCHED PRODUCTS BY CATEGORY")
        #use the categories list created previously
        for category in categories:
            aux_list = list(category[1])
            searches_list = []
            #sort the product list of every category
            while aux_list:
                minimum = aux_list[0][8]
                actual_product = aux_list[0]
                for product in aux_list:
                    if product[8] < minimum:
                        minimum = product[8]
                        actual_product = product
                searches_list.append(actual_product)
                aux_list.remove(actual_product) 
        
            #filter the last 5 and print them in a table form
            print("\n\nCategory: ", category[0].upper())
            print("\nTop \t ID \t Product (short name)\t\t\t Searches\n")
            top = 1 #once again to count the 5 products
            for product in searches_list:
                if top>5:
                    break
                else:
                    print(top, "  \t", product[0], " \t", product[1][:25], " \t  ", 
                          product[8])
                    top += 1
        
        print("\n\n*Note: Categories with less than 5 products shown do not have"
              "\n \t   enough products")
        
        input("\nPress enter to continue.")
        
        
        
    elif opt == "5":
        
        """ display the 20 products with the best score (average) 
            and the total reviews received
        """        
        #use the score list created previously
        #filter the first 20 and print them in a table form
        print("\n\n\t\t\t\tTOP 20 BEST REVIEWED PRODUCTS\n")
        print("Top \t ID \t Product (short name)\t\t\t Score \t Reviews\n")
        top = 1     #to count the 20 products
        for product in score_list:
            #display 20 products max and only those with score
            if top>20 or product[7]<1:     
                break
            else:
                print(top, "  \t", product[0], " \t", product[1][:25], " \t ",
                      round(product[7],1), " \t  ", product[5])
                top += 1
        print("\n*Note: Only the reviewed products are shown")
        
        input("\nPress enter to continue.")
        
        
        
    elif opt == "6":
        
        """ display the 20 products with the worst score (average), 
            the total reviews received, and the total refunds 
        """
        #use the score list created previously
        #filter the last 20 and print them in a table form
        print("\n\n\t\t\t\t\t\tTOP 20 WORST REVIEWED PRODUCTS\n")
        print("Top \t ID \t Product (short name)\t\t\t Score \t  Reviews \t "
              "Refunds\n")
        top = 1     #to count the 20 products
        for product in reversed(score_list):    #use an invert score_list
            if top>20:     #display 20 products max
                break
            elif product[7]>0:      #just consider products with score>0 
                print(top, "  \t", product[0], " \t", product[1][:25], " \t ",
                      round(product[7],1), " \t\t", product[5], " \t\t", product[6])
                top += 1
        print("\n*Note: Only the reviewed products are shown")
        
        input("\nPress enter to continue.")
        
        
        
    elif opt == "7":

        """ display the sales and income per month, the annual totals
            and annual average
        """
        #months = [month, sales, income]
        months = [["January  ", 0, 0],
                  ["February ", 0, 0],
                  ["March    ", 0, 0],
                  ["April    ", 0, 0],
                  ["May      ", 0, 0],
                  ["June     ", 0, 0],
                  ["July     ", 0, 0],
                  ["August   ", 0, 0],
                  ["September", 0, 0],
                  ["October  ", 0, 0],
                  ["November ", 0, 0],
                  ["December ", 0, 0]]
        
        #iterate the sales list and increase income to the respective month
        for sale in lifestore_sales:
            month = int(sale[3][3:5])   #get the number of the month as integer
            months[month-1][1] += 1       #increment the sale counter
            product_id = sale[1]
            #search the price in the product list
            for product in lifestore_products:
                if product_id == product[0]:
                    months[month-1][2] += product[2]      #increase the income
                    break
            
        #display the info in a table
        print("\n\n\tSALES AND TOTAL INCOME PER MONTH\n")
        print("Month \t\t\t\tSales \t\t Income\n")
        annual_sales = 0
        annual_income = 0
        for month in months:
            annual_sales += month[1]
            annual_income += month[2]
            print(month[0], " \t\t\t", month[1], " \t\t", month[2])
            
        print("\nANNUAL TOTAL: \t\t", annual_sales, " \t\t", annual_income)
        print("MONTHLY AVERAGE: \t", round(annual_sales/12), " \t\t", 
              round(annual_income/12))
        
        input("\nPress enter to continue.")
        
        
        
    elif opt == "0":
        
        """to finish the program"""
        sys.exit()
        
         
    else:
        
        """to catch any other option"""
        print("\n* Error: Invalid option")
        input("Press enter to continue.")
    
    print("\n---------------------------------------------")
