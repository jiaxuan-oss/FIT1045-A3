#Author(s): Yew Jin Ruo, Teh Jia Xuan, Tan Jian Hao, Sam Leong
#Team: Musang King
#Date Edited: 30/1/2023

from restaurants import Restaurant, Menu
import random
import re

class FranchiseMenu(Menu):
    
    def __init__(self) -> None:
        """
        Initialise Franchise Menu object using inheritance.

        Arguments:
        -None

        Returns:
        -None
        """
        super().__init__() #call constructor of parent class Menu
        self.location = None
        
    def get_national_dishes(self,filename: str = 'national_dishes.txt') -> dict:
        """
        Read filename and extract all the national dishes from it.

        Arguments:
        - filename: String representing name of the file

        Returns:
        - national_dishes: Dictionary with a country as the key and it's corresponding national dish(s) as the value.
        """

        with open(filename, 'r') as fileref: #open files
            national_dishes = {}
            starting_row = 0
            ending_row = 0
            entire_file = fileref.readlines() #read the entire file
            for row in range (len(entire_file)):
                if "=== A ===" in entire_file[row]:#find this string and set it to starting row in txt file
                    starting_row = row

                if "== Gallery ==" in entire_file[row]: #find ending row
                    ending_row = row

            for row in entire_file[starting_row:ending_row]:
                split_row = re.split('[:]',row.strip()) # use import re to split 
                
                for each in split_row[1:]:
                    split_dish = re.split('[,]', each.strip()) #split by ,
                    strip_left = [x.lstrip() for x in split_dish] #delete left space of all item in list eg.['Afghanistan', ' Kabuli palaw']
                    national_dishes[split_row[0]] = strip_left #to ['Afghanistan', 'Kabuli palaw']

            
            return national_dishes
                
            
        
    def get_national_drinks(self,filename: str = 'national_drinks.txt') -> dict:
        """
        Read filename and extract all the national drinks from it.

        Arguments:
        - filename: String representing the name of the file

        Returns:
        - national_drinks: Dictionary with a country as the key and it's corresponding national drink(s) as the value.
        """
        with open(filename, 'r') as fileref:  #open file
            national_drinks = {}
            starting_row = 0
            ending_row = 0
            entire_file = fileref.readlines() #Read the entire file 
            for row in range (len(entire_file)):
                if "== America ==" in entire_file[row]:#find this string and set it to starting row in txt file
                    starting_row = row

                if "== Gallery ==" in entire_file[row]: #find ending row
                    ending_row = row
           
            for row in entire_file[starting_row:ending_row]: #loop through only the country and drinks
                pattern = '.*:.*'  #pattern of identify key and values in txt
                search_line = re.search(pattern,row) #search the line based on the pattern
                
                if search_line:                     #if it is found then
                    combine = search_line.group()  #group them together
                    split_row = re.split('[:,]',combine.strip()) #then split them based on :,
                    strip_left = [x.lstrip() for x in split_row] #delete the spaces of the word in list
                    national_drinks[strip_left[0]] = strip_left[1:] #assign it to the dictionary
        
            return national_drinks
                    
                
    def update_franchise_menu(self, dishes: list, drinks: list, location: str) -> None:
        """
        Receive dishes and drinks list, and location from input parameters.
        drinks_prices list where the drinks are randomly priced between RM 0.50 to 15.99.
        dishes_prices list where the drinks are randomly priced between RM 5.00 to 75.99.
        Set the dishes, drinks and location attribute accordingly.
        
        Arguments:
        - dishes: List of dishes to be added 
        - drinks: List of drinks to be added
        - location: String representing the location where the menu is updated 

        Returns:
        - None
        """
        drink_list = []
        drink_price_list = []
        dishes_list = []
        dishes_price_list = []
        self.location = location
        
        #Check for the drink and if the location exists 
        if drinks.get(location) != None:
            for drink in drinks.get(location): #get all the drink for that location
                drink_list.append(drink) #add drink to the list
                random_price = round(random.uniform(0.5, 16),2) #generate a random price for the drink
                drink_price_list.append(random_price) #add to price list
            self.set_drinks(drink_list,drink_price_list) #set drinks

        #Check for the dish and if the location exists
        if dishes.get(location) != None: #if the dish exist then
            for dishes in dishes.get(location): #get all the dishes for that location
                dishes_list.append(dishes) #add that dish to list
                random_price = round(random.uniform(5 , 76),2) #generate a random price for the dish
                dishes_price_list.append(random_price) #add random price to list
            self.set_dishes(dishes_list,dishes_price_list) #set dish
        
class Franchise(Restaurant):

    def __init__(self, location: str, franchise_menu: FranchiseMenu) -> None:
        """
        Initialise and update Franchise attributes based on the guidelines:
        
        - 50-50% chance of either:
          Keeping the default restaurant name ("A Slice of Py"),
          or randomly choosing between the options of "Py's Restaurant", "1045 Py Bistro", "Slice of Py", "A Slice of Py Bistro" or "Py 1045";
          
        - 50-50% chance of either:
          Keeping the default opening and closing times of 08:00 and 22:00, or randomly choosing opening
          times and closing times between 08:00-13:00 and 18:00-23:00, respectively;

        - Set the appropriate number of staff accordingly.
          There should be 6 to 10 kitchen staff and 1 waiter is needed for every 10 available seats.
          e.g. an occupancy of 18 may lead to 7 kitchen staff + 2 waiters = 9 staff;
          
        - Set the restaurant's occupancy (available seats) to a randomly generated number between 15 to 35;
          
        - Set the net worth to a randomly generated value between 50000 to 200000;
        
        - Set the franchise menu to the newly created FranchiseMenu object;
        
        - Set the location and menu according to input parameters.

        Arguments:
        - Location - representing the location of the restaurant 
        - franchise_menu - instance variable of the FranchiseMenu class

        Returns:
        None
        """
        #calling constructor of parent class Restaurant
        super().__init__(franchise_menu)
        #generate chance: 50/50 chance of changing franchise attributes
        chance = random.random()
        if (chance < 0.5):
            self.set_restaurant_name(random.choice(["Py's Restaurant", "1045 Py Bistro", "Slice of Py", "A Slice of Py Bistro", "Py 1045"]))#List of restaurant names to pick from 
            hours = random.randint(8,13) #Random opening hours between 8 and 13 
            hours_string = ("0" + str(hours)) if (hours < 10) else str(hours) #Turn integer into a string
            minutes = random.choices([":00", ":15", ":30", ":45"]) #List of opening minutes to choose from 
            opening_time = (hours_string + minutes[0]) 

            hours = str(random.randint(18,23)) #Random closing hour between 18 and 23 
            minutes = random.choices([":00", ":15", ":30", ":45"]) #List of closing minutes to choose from 
            closing_time = (hours + minutes[0])

            self.set_restaurant_hours(opening_time, closing_time)
        
        self.set_occupancy(random.randint(15,35)) #Set a random occupancy between 15 and 35 
        if (self.occupancy <= 10): #Based on the occupancy how many waiters should be working 
            waiter = 1
        elif (self.occupancy > 10) and (self.occupancy <= 20):
            waiter = 2
        elif (self.occupancy > 20) and (self.occupancy <= 30):
            waiter = 3
        else:
            waiter = 4
        self.set_number_of_staff(random.randint(6,10) + waiter) #Set a random number of staff plus the waiter(s)
        self.set_net_worth(random.randint(50000,200000)) #Set a random number between 50000 and 200000 as the net worth of the restaurant
        self.location = location

#Not a method of any class
def create_menu_and_restaurant_instances() -> tuple:
    """
    1. Dynamically creates instances of FranchiseMenu with national_dishes, national_drinks, and locations.
    2. Dynamically creates instances of Franchise. 

        Arguments: 
        -None

        Returns:- 
        - locations: A list of countries that are present in both national_dishes and national_drinks.
        - franchises: A list of franchise instances. 
        - franchise_menus: A list of franchise_menu instances. 
    """
    national_dishes = FranchiseMenu.get_national_dishes("national_dishes.txt")
    national_drinks = FranchiseMenu.get_national_drinks("national_drinks.txt")
    franchise_menus, franchises, franchise_locations = [], [], []

    #add your code here
    #add all the locations into franchise_locations
    for location in national_dishes.keys(): #loop through all the location in national_dishes
        if location in national_drinks.keys(): #compare if location in drinks list 
            franchise_locations.append(location) #then add the location to the list

    #create FranchiseMenu for each location
    for index in range(len(franchise_locations)): #loop through all franchise location
        franchiseMenu_instance = FranchiseMenu() #create object
        franchiseMenu_instance.update_franchise_menu(national_dishes , national_drinks, franchise_locations[index]) #use update function to update the price and set
        franchise_menus.append(franchiseMenu_instance) #add all the menu instance to the list
    
    #create franchises instance 
    for index in range(len(franchise_locations)): #loop through all location
        franchise_instance = Franchise(franchise_locations[index] , franchise_menus[index]) #create all the franchises based on location and menus
        franchises.append(franchise_instance) #add that location in that list

    #Return the lists as a tuple
    return (franchise_locations, franchises, franchise_menus) 

if __name__ == "__main__":
    #franchise_locations, franchises, franchise_menus = create_menu_and_restaurant_instances()
    #print(len(franchise_locations))
    Franchise = create_menu_and_restaurant_instances()
    #print(franchises[5].location)
    #print(franchise_menus[5].location)
    #franchises[5].display_details()

    

    




