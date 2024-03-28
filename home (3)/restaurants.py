from datetime import datetime

# Author(s):
# Team:
# Date Edited:

class Menu:
    """
    Class variable:
    None
    
    Instance variable for each object:
    - dishes - intialize an empty dictionary to represents the restaurant's dishes
    - drinks - intialize an empty dictionary to represents the restaurnat's drinks
    """

    def __init__(self) -> None:
        """
        Initialises a menu.
        """
        self.dishes = {}
        self.drinks = {}

    def get_dishes(self) -> dict:
        """
        Returns the dishes in the restaurant 

        Arguments:
        None

        Returns:
        - self.dishes - returns the dictionary of dishes
        """
        return self.dishes

    def get_drinks(self) -> dict:
        """
        Returns the drinks in the restaurant 

        Arguments:
        None

        Returns:
        - self.drinks - returns the dictionary of drinks
        """
        return self.drinks

    def set_dishes(self, dishes: list, price: list) -> None:
        """
        Modifies the instance variable, dishes by storing the dishes and price as a key-value pair 

        Arguments:
        - dishes: represents the dishes in the restaurant 
        - price : represents the price of the dish

        Returns:
        None
        """
        for i in range(len(dishes)):
            self.dishes[dishes[i]] = price[i]

    def set_drinks(self, drinks: list, price: list) -> None:
        """
        Modifies the instance variable, drinks by storing the drinks and price as a key-value pair 

        Arguments:
        - drinks: represents the drinks in the restaurant 
        - price : represents the price of the drink

        Returns:
        None
        """
        self.drinks = {}
        for i in range(len(drinks)):
            self.drinks[drinks[i]] = price[i]

    def display_menu(self, currency_symbol: str = "RM") -> None:
        """
        Displays every item in the menu.
        The currency_symbol is set to "RM" by default.
        """
        minimum_spaces_item = 0
        minimum_spaces_price = 0
        #Finding maximum length of words
        for words in self.get_dishes().keys():
            length_words = len(words) #for each key find the length of words and store in length_words
            if int(length_words) > minimum_spaces_item: #if length of words is longer than minimum_spaces_item 
                minimum_spaces_item = length_words #update minimum_spaces_item so it equals to the length of the word

        #Finding maximum length of words
        for words in self.get_drinks().keys():
            length_words = len(words) #for each key find the length of words and store in length_words
            if int(length_words) > minimum_spaces_item: #if length of words is longer than minimum_spaces_item
                minimum_spaces_item = length_words #update minimum_spaces_item so it equals to the length of the word

        #Find maximum length of price
        for value in self.get_dishes().values():
            length_value = len(str(value)) #for each value find the length of value and store in length_value
            if int(length_value) > minimum_spaces_price: #if length of value is longer than minimum_spaces_price
                minimum_spaces_price = length_value #update minimum_spaces_price so it equals to the length of the price

        #Find maximum length of price
        for value in self.get_drinks().values():
            length_value = len(str(value)) #for each value find the length of value and store in length_value
            if int(length_value) > minimum_spaces_price: #if length of value is longer than minimum_spaces_price
                minimum_spaces_price = length_value #update minimum_spaces_price so it equals to the length of the price

        print("\nDishes") #Print an empty line and then Dishes
        counter = 0  
        for key in self.get_dishes().keys():
            counter += 1 
            spaces_dish = " " * (minimum_spaces_item - len(key)) #Finds the spaces it needs to print after the dish 
            spaces_price = " " * (minimum_spaces_price - len(str(self.get_dishes().get(key)))) #Finds the spaces it needs to print between RM and the price of the dish
            string = "{}{} RM {}{}".format(key.title(), spaces_dish, spaces_price, self.get_dishes().get(key)) #format the information into a variable
            if counter == 1:
                divider = "-" * len(string) #determine the amount of dashes needed (multiplied by the maximum char)
                print(divider) #Print the divider
            print(string) #Print the variable string
        print() #Print empty line 
        print("Drinks")
        counter = 0
        for key in self.get_drinks().keys():
            counter += 1
            spaces_drink = " " * (minimum_spaces_item - len(key)) #Finds the spaces it needs to print after each drink
            spaces_price = " " * (minimum_spaces_price - len(str(self.get_drinks().get(key)))) #Finds the spaces it needs to print between RM and the price of the dish
            string = "{}{} RM {}{}".format(key.title(), spaces_drink, spaces_price, self.get_drinks().get(key)) #format the information into a variable
            if counter == 1:
                divider = "-" * len(string) #determine the amount of dashes needed (multiplied by the maximum char)
                print(divider) #Print the divider
            print(string) #Print the variable string


class Restaurant:
    """
    Class variables:
    - name - String represents the name of the restaurant 
    - opening_time - String represents the opening time of the restaurant in 24 hour format
    - closing_time - String represents the closing time of the restaurant in 24 hour format

    Instance variable for each object:
    - menu - represents the menu of the restaurant
    - restaurant_name - String represents the restaurant's name
    - opening_time - String represents the opening time of the restaurant
    - closing_time - String represents the closing time of the restaurant
    - number_of_staff - Integer represents the number of staff in the restaurant
    - net_worth - Float represents the net worth of the restaurant
    - occupancy - Interger represents the occupancy of the restaurant
    """
    name = "A Slice of Py"
    opening_time = "08:00"
    closing_time = "22:00"

    def __init__(self, menu: Menu) -> None:
        """
        Initialises a restaurant with the given data.
        """
        self.menu = menu
        self.restaurant_name = "A Slice of Py"
        self.opening_time = "08:00"
        self.closing_time = "22:00"
        self.number_of_staff = 0
        self.net_worth = 0.0
        self.occupancy = 0

    def get_net_worth(self) -> float:
        """
        Returns the net worth of the restaurant 

        Arguments:
        None

        Returns:
        - self.net_worth - returns the net worth of the restaurant as a float
        """
        return self.net_worth

    def set_restaurant_name(self, restaurant_name: str) -> None:
        """
        Modifies the instacne variable by assigning a name to the restaurant 

        Arguments:
        restaurant_name - String representing the name of the restaurant 

        Returns:
        None
        """
        self.resturant_name = restaurant_name

    def set_restaurant_hours(self, opening_time: str, closing_time: str) -> None:
        """
        Modifies the instance variables by assigning the value to opening and closing time 

        Arguments:
        opening_time - String representing the opening time of the restaurant 
        closing_time - String representing the closing time of the restaurant 

        Returns:
        None
        """
        self.opening_time = opening_time
        self.closing_time = closing_time

    def set_number_of_staff(self, number_of_staff: int) -> None:
        """
        Modifies the instance variable by assigning the amount of staff working in the restaurant 

        Arguments:
        number_of_staff - Integer representing the amount of staff in the restaurant

        Returns:
        None
        """
        self.number_of_staff = number_of_staff

    def set_net_worth(self, net_worth: float) -> None:
        """
        Modifies the instancee variable by assigning a net worth to the restaurant

        Arguments:
        net_worth - float representing the net worth of the restaurant 

        Returns:
        None
        """
        self.net_worth = net_worth

    def set_occupancy(self, occupancy: int) -> None:
        """
        Modifies the instance variable by assigning the number of people in the restaurant

        Arguments:
        occupancy - integer to represent the occupancy of the restaurant
        
        Returns:
        None
        """
        self.occupancy += occupancy

    def display_details(self) -> None:
        """
        Display the necessary details for the menu of the restaurant

        Arguments:
        None
        
        Returns:
        None
        """
        opening = datetime.strptime(self.opening_time, "%H:%M") #parse the representation of the opening time (String) to chnage to a date time format
        open_restaurant = opening.strftime("%I:%M") #Change the opening time into 12 hour format 
        closing = datetime.strptime(self.closing_time, "%H:%M") #parse the representation of the closing time (String) to chnage to a date time format
        close = closing.strftime("%I:%M") #Change the closing time into 12 hour format 

        print(f"Welcome to {self.restaurant_name}!") #Print and format welcome to the restaurant
        print(f"Operating Hours: {open_restaurant} AM to {close} PM") #Print and format opening and closing tiem of the restaurant
        self.menu.display_menu() #Call the display_menu function from the menu class to display the rest of the menu

    def __str__(self) -> None:
        """
        Return the formatted string for each category

        Arguments:
        None
        
        Returns:
        A string containing the restaurant name, occupancy of the restaurant, the amount of staff and the net worth of the restaurant 
        """
        return f"{self.restaurant_name} (Occupancy: {self.occupancy}, Staff: {self.number_of_staff}, Net Worth: RM{self.net_worth})"


if __name__ == "__main__":
    # Test your function here

    dishes = ["ayam percik", "nasi lemak", "lamb rendang", "apam balik", "mee goreng"]
    dishes_prices = ["12.33", "8.80", "16.22", "1.20", "6.00"]

    drinks = ["teh tarik", "iced milo", "kopi o"]
    drinks_prices = ["2.10", "3.00", "2.20"]

    menu = Menu()
    menu.set_dishes(dishes, dishes_prices)
    menu.set_drinks(drinks, drinks_prices)

    restaurant = Restaurant(menu)
    restaurant.set_restaurant_hours("11:00", "20:00")
    restaurant.display_details()
