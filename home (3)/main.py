from analyse_reviews import *
from preprocess import *
from restaurants import *
from franchises import *
from visualise_data import *
import random
from collections import OrderedDict

class Start:
    """
    Runs full program.

    Class variables:
    - None

    Instance variables:
    - p: Object of class PreProcess
    - s: Object of class SentimentAnalyser
    - f: Object of class FeatureExtractor
    - r: Object of class ReviewSummariser
    - chosen_location: String indicating user's choice of processing all reviews or only for 1 location
    - chosen_location_reviews: List that stores reviews for the chosen location only
    - franchise_locations: List of all franchise locations
    - franchises: List of all Franchise objects
    - franchise_menus: List of FranchiseMenu objects

    """
    """
    Example review analysis:
    Location chosen: Malaysia
    Using FeatureExtractor to extract common words,the bar chart shows that 'food', 'servic', 'get', 'dinner', 'tabl' 
    and 'time' were the top 6 most reoccuring words in Malaysia franchise's reviews. From the words generated, it is hard to determine whether they are
    positive or negative feedback. 
    The sunburst chart generated also shows that most of the review sentiments for Malaysia franchise were 2, which were categorized as neutral.
    Using ReviewSummariser to summarise reviews for Malaysia franchise, features that are bothering customers include
    long waiting time, bad service and attitude from staff and low quality food. ie. there were reviews complaining about taking an hour to get food,
    lack of attention given by waiters and that customers found hair in their food or found the ribeye steak to be disatisfactory. There were also reviews 
    comparing the franchise's food to street vendor food, which they found tastier than what they had at the Malaysia franchise.
    Appropriate actions to be carried out include hiring more waiters to cope with rush hours, giving proper training to staff
    to ensure service quality and ensure the attitude and service given by all staff. It is also neccessary to make sure that the kitchen 
    staff are well-trained to cook all items on the menu to avoid putting out low quality dishes, or remove a few menu items to ensure quality on
    a small range of dishes. 
    """

    def __init__(self):
        #Instantiating all instance variables
        self.p = PreProcess()
        self.s = SentimentAnalyser()
        self.f = FeatureExtractor()
        self.r = ReviewSummariser()
        self.chosen_location = "Default"
        self.chosen_location_reviews = []
        franchise_locations, franchises, franchise_menus = create_menu_and_restaurant_instances()
        self.franchise_locations = franchise_locations
        self.franchises = franchises
        self.franchise_menus = franchise_menus
        
        #start of program
        self.choose()
        
    def options(self)->int:
        """
        Lets user choose type of action between [0] View Franchise Details [1] Analyse Data [2] Generate New Review [3] Display reviews and locations and [4] Quit. 
        
        Arguments:
        - None

        Returns:
        - choice: Integer representing type of action chosen by user.
        """
        choice = int(input("\n[0] View Franchise Details\n[1] Analyse Data\n[2] Generate New Review\n[3] Display reviews and locations\n[4] Quit\n"))
        return choice

    def analyse_options(self)-> int:
        """
        Lets user choose type of analyser between [0] SentimentAnalyser [1] FeatureExtractor and [2] ReviewSummariser. 
        
        Arguments:
        - None 

        Returns:
        - choice: Integer representing type of action chosen by user.
        """
        choice = int(input("\n[0] SentimentAnalyser\n[1] FeatureExtractor\n[2] ReviewSummariser\n"))
        return choice
        
    def location_options(self, type_of_location = "Default")->str:
        """
        display locations for user to choose depends of optional parameter type_of_location

        Arguments
        -type_of_location: string representing types of location list (eg. "Default" is all location list
                           "Review" is location with reviews)

        Return:
        -chosen_location: string representing location chosen by the user
        """
        flag = True
        list_chosen = self.franchise_locations

        if type_of_location == "Review": #if type_of_location change to review 
            list_chosen = self.location_with_reviews() #then change to locations that have reviews

        for i in range(len(list_chosen)): #loop through the list chosen
            print(f"[{i}] {list_chosen[i]}\n") #output list of location for user to choose
        location = int(input("Please choose a franchise location from the list above. ")) #ask user to choose
        #catch error 
        while flag == True:
            try:
                chosen_location = list_chosen[location] #assign chosen location to chosen_location 
                flag = False#stop loop

            except IndexError:#if invalid input from user then output error msg and ask again
                print("Invalid input, please choose again.") #error msg
                location = int(input("Please choose a franchise location from the list above. ")) #ask user to choose

        print("Chosen Location:", chosen_location) #print chosen location
        return chosen_location

    def location_with_reviews(self)->list:
        """
        Delete repeated location in location list

        Arguments: 
        - None

        Return:
        -unique_locations- List with no repeated location
        """
        unique_locations = list(OrderedDict.fromkeys(self.p.locations)) #delete all the repeated location with collections library
        unique_locations.sort() #sort it with alphabetical order
        return unique_locations #return the list

    def options_SentimentAnalyser(self):
        """
        Display options for user to choose while using SentimentAnalyser.

        Arguments
        -None

        Return
        -choice: Integer representing choice of user 
        """
        choice = int(input("[0] Get customer review sentiments\n[1] Get compound values, customer review and sentiment\n")) #ask for user input
        flag = False
        #catch error
        while(flag == False):
            try:
                assert choice == 0 or choice == 1 #assert choice could be 1 or 0 
                flag = True
            except AssertionError: #if assert wrong then print error msg and ask user to choose again
                print("Please choose a valid option.") #error msg
                choice = int(input("[0] Get customer review sentiments\n[1] Get compound values, customer review and sentiment\n")) #ask user choose again
 
        return choice # return user's choice

    def pick_location(self, type_of_location: str = "Default")-> str:
        """
        an assisting function for user to pick location

        Arguments
        -type_of_location(optional parameter: "Default" by default): "Default" -> all locations, "Review" -> only location with reviews

        Return
        -chosen_location: string representing location that chosen by user
        """
        choice = self.location_options(type_of_location) #call location_options function to ask user to choose
        flag = False
        #catch error 
        while (flag == False):
            try:
                if type_of_location == "Default": #if optional parameter is default 
                    assert choice in self.franchise_locations  #then location list is franchise_locations-> representing all location 
                    flag = True
                elif type_of_location == "Review":#if optional parameter is review 
                    assert choice in self.location_with_reviews() #then location list is location with reviews -> representing only location with reviews
                    flag = True

            except AssertionError: #if error input then output error msg ask user to choose again
                print("Please input a valid franchise location.") #output error msg
                choice = self.location_options(type_of_location) #ask user to choose again

        self.chosen_location = choice #assign chosen location
        
        self.get_reviews_by_location(self.chosen_location) #call get_reviews_by_location function to get all reviews for that location
    
        return self.chosen_location #return

    def pick_analyse_way(self)-> None:
        """
        an assisting function to assist program to let user to choose
        which analyser method user prefers

        Arguments
        -None

        Return
        -None
        """
        choice = self.analyse_options() #call function
        flag = False
        #catch error
        while (flag == False):
            try:
                assert choice >= 0 and choice <= 2 #assert value enter by user
                flag = True
            except AssertionError: #if assert wrong the output error msg then pick again
                print("Please pick a valid way to analyse data.")
                choice = self.analyse_options()
                
        if choice == 0: #if user choose sentiment analyser 
            location = self.pick_all_or_location("Review") #get location, user wants to analyse
            self.use_SentimentAnalyser(location) #call analyser function

        elif choice == 1: #if user choose feature extractor analyser
            location = self.pick_all_or_location("Review") #get location , user wants to analyse
            self.use_FeatureExtractor(location) #call the analyser function

        else: #if user choose review summariser analyser
            location = self.pick_all_or_location("Review") #get location, user wants to analyse
            self.use_ReviewSummariser(location) #call the analyser function

    def pick_all_or_location(self, type_of_location = "Default")->str:
        """
        an assisting function to assist program to let user to choose 
        whether analyse all location or only analyse a particular location

        Arguments
        -type_of_location(optional parameter "Default" by default): "Default" -> all locations, "Review" -> only location with reviews

        Returns
        -location: string representing location choose by user

        """
        flag = False
        #catch user error
        while(flag == False):
            try:
                choice = int(input("[0]Review all locations\n[1] Review specific location\n")) #ask user analyse all location or a particular location
                assert choice == 0 or choice == 1 #assert user input
                flag = True
            except AssertionError: #if assert wrong output error msg and ask again
                print("Please choose a valid option.") #error msg
                
        if choice == 0: #set location to default when user choose all location
            location = "Default"
        elif choice == 1 and type_of_location == "Default": #ask user to pick location if it is true 
            location = self.pick_location() #call pick location function

        elif choice == 1 and type_of_location == "Review":  #if user wants to analyse particular location then set type_of_location to "Review"
            location = self.pick_location("Review") #ask user to choose location from the location list
 
        return location # return location

    
    def get_reviews_by_location(self, location: str)->list:
        """
        get all the reviews of that particular location

        Arguments
        -location: string representing location

        Return:
        -chosen_location_reviews: list representing all the reviews of that location
        """
        review_lst = [self.p.reviews[index] for index in range(len(self.p.reviews)) if self.p.locations[index] == location] #getting location's review
        self.chosen_location_reviews = review_lst #assign
        return self.chosen_location_reviews#return

    def choose_view_bar_chart(self)->int:
        """
        an assisting function to ask user for viewing bar chart

        Arguments:
        -None

        Returns:
        -choice: integer representing yes or no to view bar chart
        """
        flag = False
        #catch error
        while (flag == False):
            try:
                choice = int(input("Would you like to view bar chart?\n[0] No\n[1] Yes\n")) #ask user to choose 
                assert choice == 0 or choice == 1 #assert 1 or 0 
                flag = True #jump out of loop if assertion correct
            except AssertionError: # if assertion failed then print error msg and choose again
                print("Please choose from options given.")#error msg

        return choice#return user input

    def choose_view_pie_or_grouped_bar_chart(self)-> int:
        """
        assisting function to ask user for viewing groupbar chart or pie chart

        Arguments:
        -None

        Returns
        -choice: integer representing yes or no for viewing chart
        """
        flag = False
        #catch error
        while (flag == False):
            try:
                choice = int(input("Would you like to view pie or grouped barchart?\n[0] No\n[1] Yes\n"))#ask user for input
                assert choice == 0 or choice == 1#assert 1 or 0
                flag = True#jump out of loop when assertion correct
            except AssertionError:#assertion failed
                print("Please choose from options given.")#output error msg

        return choice#return choice

    def choose_pie_or_grouped_bar_chart(self)->int:
        """
        assisting function to ask user for viewing bar chart or pie chart

        Arguments:
        -None

        Returns
        -choice: integer representing pie chart or grouped barchart
        """
        flag = False
        while (flag == False):
            try:
                choice = int(input("[0] View pie chart\n[1] View grouped bar chart\n"))#ask user for input
                assert choice == 0 or choice == 1#assert 1 or 0
                flag = True #jump out of loop when assertion correct
            except AssertionError: #assertion failed
                print("Please choose from options given.")#output error msg

        return choice #return choice of user

            
    def use_SentimentAnalyser(self, location: str)->None: 
        """
        user Sentiment analyser

        Arguments 
        -location: string representing type of location (eg. all location or particular location)

        Return
        -None
        """
        choice = self.options_SentimentAnalyser()
        if location == "Default":#if user choose all franchise location 
            if choice == 0:#if user choose to get customer sentiment
                print(self.s.get_customer_sentiment(self.p.reviews))# then get customer sentiment based on all franchise location
            else:#if choose to insert customer sentiment then
                compounds, reviews_with_locations_sentiments = self.s.insert_customer_sentiment(self.p.reviews, self.p.locations) #then insert customer sentiment based on all franchise location
                print(f"Compounds: {compounds}\nReviews with locations sentiments: {reviews_with_locations_sentiments}") #output
        else: #if user choose a particular location then
            if choice == 0: #if user choose to get customer sentiment
                print(self.s.get_customer_sentiment(self.chosen_location_reviews))# then get customer sentiment based on that particular franchise location
            else:#if choose to insert customer sentiment then
                location_list = [location]*len(self.chosen_location_reviews) #duplicate that location into a list which same length as the location's review in order to enter the function
                compounds, reviews_with_locations_sentiments = self.s.insert_customer_sentiment(self.chosen_location_reviews, location_list)#then insert customer sentiment based on all franchise location
                print(f"Compounds: {compounds}\nReviews with locations sentiments: {reviews_with_locations_sentiments}")

        #choose to view pie chart or grouped_bar_chart
        choice = self.choose_view_pie_or_grouped_bar_chart()#ask user wanted to see chart or not
        if choice == 1: #if user wanted to view then
            choice = self.choose_pie_or_grouped_bar_chart() #ask user to choose pie or group bar chart
            if choice == 0: #if user wanted to see pie chart
                generate_pie_chart(self.p) #show pie chart
            elif choice == 1: #if user wanted to see another chart
                generate_extra_chart(self.p) #then show 

        self.choose()#back to main menu
  
    def use_FeatureExtractor(self, location: str)->None:
        """
        Feature extractor analyser

        Arguments
        -location: String represents type of location (eg.all location or particular location)

        Return
        -None
        """
        flag = True
        number_of_words = self.manipulate_num_word() #ask user input number of words to be displayed
        if location == "Default": #if location is default
            common_words = self.f.extract_common_words(self.p.reviews, number_of_words) #then use all location's review
            self.common_words = common_words 
            print(common_words) #display common words
        else:#if a location is given then 
            review_lst = self.get_reviews_by_location(location) #get review of that location
            while flag == True:
                try:
                    common_words = self.f.extract_common_words(review_lst, number_of_words)#extract the common words
                    flag = False #jump out of loop

                except ValueError:#catch error 
                    print("Input exceeds maximum words, Please try again.")#output error msg, if user input's value exceeds maximum common words
                    number_of_words = self.manipulate_num_word()#ask again 

            print(common_words)#display for user to see
        
        #choose to view bar chart
        choice = self.choose_view_bar_chart()     
        if choice == 1 and location == "Default": #if choose to all location then
            generate_bar_chart(self.p.reviews, number_of_words) #generate a bar chart based on all location
        elif choice == 1 and location != "Default": #if choose a particular location
            generate_bar_chart(self.chosen_location_reviews, number_of_words)#then generate a bar chart for that particular location

        self.choose()#back to main menu
    
    def manipulate_n_summariser(self)->int:
        """
        Ask user to input n_value for review summariser
        (indicates lines to be displayed)

        Arguments
        -None

        Return
        -n_value: integer represents number of line to be display while using review summariser
        """
        flag = True
        n_value = 0
        
        while flag == True:
            try:
                input_n = int(input("Number of sentences you would like to see: "))
                assert input_n > 0 
                n_value = input_n
                flag = False
                
            except ValueError:
                print("Only integer accepted")

            except AssertionError:
                print("Please positive integer")

                
        return n_value

    def use_ReviewSummariser(self, location: str)->None:
        """
        Use ReviewSummariser to analyse data.

        Arguments
        -location: String representing types of location list to use

        Return
        -None
        """
        flag = True
        selected_words = self.manipulate_selected_words() #ask user to input selected_words
        words_to_ignore = self.manipulate_words_to_ignore() #ask user to input words_to_ignore
        n_value = self.manipulate_n_summariser() #ask user to input number of line to display
        all_reviews_str = "" 
        
        #pick chosen location review
        if location == "Default":
            for index in range(len(self.p.locations)):
                all_reviews_str += (" {}.".format(self.p.reviews[index])) #combine all same location review into a str

        else:
            for index in range(len(self.p.locations)):
                if self.p.locations[index] == location: #comparing location
                    all_reviews_str += (" {}.".format(self.p.reviews[index])) #combine all same location review into a str
        while flag == True:
            try:
                summary = self.r.generate_summary(all_reviews_str, n_value, selected_words, words_to_ignore) #generate a summary 
                flag = False
            except ValueError: #if n_value invalid then return error and ask user to input again
                print("Input exceeds maximum words, Please try a smaller value") #error msg
                n_value = self.manipulate_n_summariser() #ask user to input again
                
        print(summary) #output summary for user to see

        self.choose() #back to main menu after display summary
    
    def choose(self)-> None:
        """
        Acts as a main menu for the user to choose which step they want to go to.
        Will always return to this method until user decides to quit the program.

        Arguments
        -None

        Return
        -None
        """
        flag = False
        while (flag == False):
            try:
                choice = self.options()#call option function to let user choose step
                assert choice >= 0 and choice <= 4
                flag = True
            except AssertionError: #if invalid input show error and choose again
                print("Please select from options given.")#error msg
        
        if choice == 0: #if display franchise details chosen
            location = self.pick_location() #ask user to pick location
            self.display_franchise_details(location) #display
        elif choice == 1: #if user choose to analyse then
            self.pick_analyse_way() #ask user to choose ways to analyse
        elif choice == 2: #if user choose generate_reviews then 
            self.generate_reviews()#generate review
        elif choice == 3: #if user choose to get list of reviews and their locations
            self.assign_review_location(self.p.reviews) #display all reviews and their locations
        else:
            return #if nothing above return nothing
            
    def manipulate_words_to_ignore(self)->list:
        """
        ask user to input words to ignore while using analyser

        Arguments
        -None

        Return
        -word_list: list representing words to ignore while using analyser
        """
        word_list = []
        flag = True
        #ask for words to ignore 
        while flag == True:
            words_to_ignore = input('Words to ignore(Enter [0] to stop): ')
            if words_to_ignore.isdigit():#if appropriate value
                flag = False #then jump out of loop
            
            else:
                word_list.append(words_to_ignore) #add words to ignore to list if it is appropriate
        return word_list #return

    def manipulate_selected_words(self)-> dict:
        """
        ask user for selected words and its point for review summariser analyser

        Arguments
        -None

        Returns
        -selected_words: dict representing words and its points
        """
        selected_words = {}
        flag = True
        
        while flag == True:
            #ask for selected words
            selected_words_input = input("Selected words (Enter [0] to stop): ")#ask for input
            if (selected_words_input == "0"): #end asking if 0 is entered
                flag = False

            #check for appropriate value
            elif (selected_words_input.isalpha()) == False:
                selected_words_input = print("Please enter appropriate input")
            
            elif(selected_words_input.isalpha()): #check appropriate input then
                selected_words_point = input("Points: ") #ask for points for that word
                #check for appropriate value
                if selected_words_point.isdigit():
                    selected_words[selected_words_input] = selected_words_point
                
                else: 
                    print("Please enter appropriate input") #if not appropriate value print error msg

        return selected_words #return
    
    def manipulate_num_word(self)-> int:
        """
        ask user for number of words needed to be display
        while using feature analyser

        Arguments
        -None

        Returns
        -number_of_words: integer representing number of words needed to be display
        """
        number_of_words = 0
        flag = True
        while flag == True:
            try:
                input_num_words = int(input("Number of words: "))# ask for number of words
                assert input_num_words >= 0#assert it more than 0
                number_of_words = input_num_words #assign and stop loop if assert correct
                flag = False
            #catch error
            except ValueError: #if assertion failed then output error msgs and ask again
                print("Only integer accepted, Please try again")#error msg

            except AssertionError:
                print("Please enter number between 1 to {}".format(maximum_num_words)) #error msg

        return number_of_words

    def calculate_words_weight(self, reviews:str, words_to_ignore:list)-> dict:
        """
        assisting function to call calculate word weight function from review ReviewSummariser

        Arguments
        -reviews: list representing individual review
        -words_to_ignore: list representing words that is not counted while calculate words weight

        return
        -words_weight: dictionary representing each word's point
        """
        reviewSummariser = ReviewSummariser()
        words_weight = reviewSummariser.calculate_word_weights(reviews, words_to_ignore)
        return words_weight

    def calculate_sentence_weights(self, review: str, selected_words: dict, words_to_ignore: list)->dict:
        """
        assisting function to call calculate sentence weight function from review ReviewSummariser

        Arguments
        -reviews: String representing individual review
        -selected words: dictionary represents selected words and its Points (eg loved : 4)
        -words_to_ignore: list representing words that is not counted while calculate sentence weight

        return
        -sentence_weight: dictionary represents each sentence's point
        """
        reviewSummariser = ReviewSummariser() 
        sentence_weight = reviewSummariser.calculate_sentence_weights(review, selected_words, words_to_ignore)#calling function
        return sentence_weight#return
    
    def generate_reviews(self)->list:
        """
        generate fake reviews

        Arguments
        -None

        Returns
        -new_reviews: list representing all the fake reviews that created by the user
        """
        starters, features, linking_verbs, adjectives, number_review = self.generate_reviews_component() #get all the component needed by calling generate_reviews_compenent
        new_reviews = self.p.generate_new_reviews(self.p.reviews, starters, features, linking_verbs, adjectives, number_review) #generate fake review
        self.assign_location_for_new_reviews(number_review)#randomly assign location for the fake reviews
        self.view_location_with_review_option() #ask user whether want to display or back to main menu
        return new_reviews #return all the fake reviews

    def view_location_with_review_option(self)-> None:
        """
        assisting function to ask user to choose, display review with location 
        or back to main menu

        Arguments
        -None

        Returns
        -None
        """
        flag = True
        while flag == True:
            try:
                option = int(input("[0] Display review with location\n[1] Main Menu"))#ask for input from user
                assert option == 1 or option == 0 #assert to be 0 or 1

                if option == 0: #if user choose display review with location
                    flag = False #jump out of loop
                    self.assign_review_location(self.p.review) #call assign review location to display
                    

                elif option == 1: #if user want to back to main menu
                    flag = False #jump out of loop
                    self.choose() #back to main menu
                    
            #catch error
            except AssertionError:#output error if assertion failed
                print("Please input only 1 or 0") #error msg

        
    def generate_reviews_component(self):
        """
        ask for starters, features, linking_verbs, adjective for generating reviews
        and total number of review needs to be generated

        Arguments
        -None

        Returns
        -starters = list representing starters used by generating reviews
        -features = list representing features used by generating reviews
        -linking_verbs = list representing linking verbs used by generating reviews
        -adjectives = list representing adjectives used by generating reviews
        -number_review = integer representing number of review needs to be generated
        """
        #initialise and declaration
        flag = True
        starters = ["In my opinion", "To me", "Honestly"]
        features = ["occupancy", "menu items", "opening hours", "staff"]
        linking_verbs = ["is", "are", "was", "were"]
        adjectives = ["insufficient", "not enough", "inadequate", "short"]
        number_review = 0 

        #getting starters
        while flag == True:
            starters_input = input("Starters (eg.In my opinion)[Enter 0 to stop]: ")#ask for input 
            if starters_input == "0":#if user enter 0 then stop asking
                flag = False#jump out of loop
                    
            else:
                starters.append(starters_input)#add to starters list
        

        #getting features
        flag = True
        while flag == True:
            features_input = input("Features (eg.Opening hours, stuff)[Enter 0 to stop]: ") #ask for opening hours
            if features_input== "0": #if user enter 0 then stop asking
                flag = False
                    
            else:
                features.append(features_input)#add to feature list

        #getting linking_verbs
        flag = True
        while flag == True:
            linking_verbs_input = input("Linking verbs (eg.is, are)[Enter 0 to stop]: ") #ask for linking verbs
            if linking_verbs_input == "0":
                flag = False
                    
            else:
                linking_verbs.append(linking_verbs_input)#add to linking verbs list

        #getting adjectives
        flag = True
        while flag == True:
            adjectives_input = input("Adjectives (eg.insufficient)[Enter 0 to stop]: ")#ask for adjectives
            if adjectives_input == "0":
                flag = False
                    
            else:
                adjectives.append(adjectives_input) #add to list
        
        #getting num of review
        flag = True
        while flag == True:
            try: 
                input_num_reviews = int(input("Number of reviews: ")) #ask for number of review needed to be generated
                assert input_num_reviews >= 0 #assert 
                number_review = input_num_reviews
                flag = False#jump out of loop if assertion success

            #catch error, output error msg if failed assertion
            except ValueError:
                print("Only integer accepted, Please try again")#error msg

            except AssertionError:
                print("Please enter positive integer")#error msg
        
        return starters, features, linking_verbs, adjectives, number_review
                
    def assign_location_for_new_reviews(self, number_review:int)-> None:
        """
        randomly assign location for new reviews

        Arguments
        -number_reviews: integer representing number of new review that needed to assign location

        Returns
        -None
        """
        for number in range(number_review): #loop through
            random_location = random.choice(self.franchise_locations) #randomly choose location from location list
            self.p.locations.append(random_location) #add location into existing location list


    def assign_review_location(self, reviews:list)-> None:
        """
        Assign each review to the appropriate franchise location.

        Arguments
        -reviews: list representing reviews of franchise location

        Returns:
        -None
        """
        location_review_dict = self.p.assign_review_location(reviews, self.p.locations) #call assign review location function from preprocess
        for keys, values in location_review_dict.items(): #output keys and value from the dictionary that return by assign review location
            print("\n{}: {}".format(keys, values))

        self.choose()

    def display_franchise_details(self, location: str)->None:
        """
        Display franchise's details (eg, menu, operating hrs etc)

        Arguments
        -location: string representing location

        Returns
        -None

        """
        index = self.franchise_locations.index(location)#get location's index in the location list
        print(self.franchises[index].__str__())#print details franchise (eg operating hours, net worth etc)
        self.franchises[index].display_details() #display details like menu, price etc
        self.choose()        #back to main menu to let user choose his next step

if __name__ == "__main__":
    start = Start()    
   # generate_pie_chart(start.p)
    
    

    
