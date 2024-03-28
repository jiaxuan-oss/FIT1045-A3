#Author(s): Yew Jin Ruo, Teh Jia Xuan, Tan Jian Hao, Sam Leong
#Team: Musang King
#Date Edited: 30/1/2023

import random
import re
import pandas as pd
import nltk
from nltk.stem.porter import PorterStemmer
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
from collections import OrderedDict
import csv

class PreProcess:

    def __init__(self, filename: str = "reviews.csv"):
        """
        Initialise all instance variables.
        """
        review_corpus, locations = self.pre_process_reviews(filename)
        self.reviews = review_corpus
        self.locations = locations
        
    def remove_special_characters(self, raw_review: str) -> str:
        """
        Remove special characters and numbers.
        Implements the re module: https://docs.micropython.org/en/latest/library/re.html

        Arguments: 
            - raw_reviews: an unprocessed raw review.

        Returns:
            - review: A review with special characters removed. 
        """
        pattern = "[^A-Za-z]" #this pattern exclude characters that are not an alphabet

        new_pattern = r" "#then replace them with space
        
        review =" ".join(re.sub(pattern, new_pattern, raw_review).split()) #split and join to make the sentence coherent

        return review

    def convert_lowercase(self, review: str) -> str:
        """
        Converts every character in the review to a lowercase character.

        Arguments:
            - review: A single customer review string (sentence in form of string). 

        Returns:
            - review: A review string with all characters in lowercase. 
        """

        return review.lower()


    def tokenize_reviews(self, review: str) -> list:
        """
        Splits the review into individual words. 

        Arguments:
            - review: A single customer review (sentence in form of string). 

        Returns:
            - review_tokens: A list of every words from a review.   
        """
        review_tokens = word_tokenize(review)
        
        
        return review_tokens


    def remove_stopwords(self, review_tokens: list) -> list:
        """
        Checks to see if there are any stopwords in each review and removes them. 
        A list of stopwords can be found in the documentation for the library of your choosing.
        Please extend the list of stopwords with custom_stopwords = ["due", "all", "on", "to"].

        Arguments:
            - review_tokens: A list of every words from a review. 

        Returns:
            - review_tokens: A list of every words from a review excluding stopwords.
        """
        custom_stopwords = ["due", "all", "on", "to"]

        stop_words = stopwords.words('english') #use stopword of language english
        stop_words.extend(custom_stopwords) #add custom stopwords to the list

        return [i for i in review_tokens if i not in stop_words] #go through review tokens and only return tokens not in list of stopwords


    def stem_words(self, review_tokens: list) -> str:
        """
        Stems all words in every review by removing affixes (eg: hopp(ing) -> hop).
        Implements the PorterStemmer module: https://www.nltk.org/howto/stem.html

        Arguments:
            - review_tokens: A list of every words from a review. 

        Returns:
            - review: A review with all words stemmed.
        """

        stemmer = PorterStemmer()

        review = [stemmer.stem(word) for word in review_tokens]

        return review



    def remove_spam(self, review_corpus: list, locations: list) -> tuple:
        """
        Removes spam reviews in the form of repeated characters such as "aaa aa" or "b b b bbbbb".
        Removes locations of those spam reviews from locations.

        Returns:
            - review_corpus: A list containing pre-processed customer reviews after the spam reviews are removed.
            - locations: A list containing locations after the locations for the spam reviews are removed.
        """
        locations = self.check_location(review_corpus, locations)
        
        review_corpus = self.check_lst_repeat(review_corpus)

        return (review_corpus, locations)


    def check_lst_repeat(self, review_corpus): #this function uses recursion to go through the list 
        """This function uses recursion to go through list review_corpus and check if
        if each review contains repeated characters

        Arguments:
            - review_corpus: a list that contains lines of customer's reviews

        Returns:
            - review_corpus: reviews that does not contain minimum_spaces_item
        """
        if len(review_corpus) == 1: #if only one item, check one last time and return appropriate review
            string = str(review_corpus[0])
            if self.check_repeat(string, 0) == True:              
                return [] #if contain repeating chars, return empty list
            return review_corpus #else return original review

        else:
            string = str(review_corpus[0]) #initialize 'string' as an argument 
            if self.check_repeat(string, 0) == True: 
                return []+self.check_lst_repeat(review_corpus[1:]) #include empty list so can concatenate
            else:
                return review_corpus[:1] + self.check_lst_repeat(review_corpus[1:]) #return current review, then call function again to check for the rest of reviews
    
    def check_location(self, review_corpus, locations):
        """
        This function check for repeating characters and remove the location corresponding to the review

        Arguments:
        - review_corpus: a list that contains all the customer's reviews
        - locations: a list that contains the locations corresponding to each customer's reviews
            
        Returns:
        - locations: a list that contains the locations corresponding to each customer's reviews excluding spams
        """
        if len(locations) == 1:
            string = str(review_corpus[0]) #initialize string as an argument
            if self.check_repeat(string, 0) == True:
                return []
            return locations

        else:
            string = str(review_corpus[0])
            if self.check_repeat(string, 0) == True: #check if current location's review contains spam
                return []+self.check_location(review_corpus[1:], locations[1:]) #check next review and replace current location as an empty list
            else:
                return locations[:1] + self.check_location(review_corpus[1:],locations[1:]) #check next review and return current location
        

    def check_repeat(self, string, count, flag=False):
        """This function go through each char in each review to check for repeating chars
    
        repeating chars are defined as:
            - more than 2 of the same char placed alongside each other, excluding spaces

        then return True if there are repeating characters

            Arguments: 
                - string: a string of review from review_corpus
                - count: an integer to keep track of number of repeating characters
                - flag: a boolean value with default value set as format

            return:
                - flag: a boolean value
        """    
        if len(string) == 1: #check for the count and length of the string
            #count = 0
            if count >2:
                flag = True
            return flag

        else:
            if string[0] == string[1]: #if same as the next char, increment count by 1
                count +=1

            elif string[1] == " " and len(string)>2: #is same as next char that is not a space, increment count by 1
                if string[0] == string[2]:
                    count += 1

            else:
                count = 0 #resets the count value 

            if count > 2:
                flag = True
                return flag

            
            return self.check_repeat(string[1:], count)

    

    def pre_process_reviews(self, filename: str = "reviews.csv") -> tuple:
        """
        Combines all functions created above to pre-process reviews from the file reviews.csv.
        - Read file to extract raw reviews then;
        - Iterate through raw reviews to pre-process reviews following the order:
             1. Remove special characters 
             2. Convert review to lowercase then tokenise each review
             3. Remove any stop words before stemming words in each review
        - Remove spam before returning review_corpus.

        Returns:
            - review_corpus: A list that contains every review after pre-processing. 
            - locations: A list containing locations for the reviews in review_corpus.
        """
        data = open(filename).readlines() #open file as lines of reviews
        locations = []
        review_corpus = []
        for i in data[1:]:
            word = word_tokenize(i)

            if word[1] =="Zealand" or word[1] =="Kingdom": #check if the name of the country has more than 1 characters
                locations.append(' '.join(word[:2])) #add first 2 word to the list location
                review_corpus.append(' '.join(word[2:])) #add the rest as review to list review_corpus

            else:
                locations.append(word[0]) #add first word to the list location
                review_corpus.append(' '.join(word[1:])) #add the rest as review to list review_corpus

        for i in range(len(review_corpus)): #for each review, remove special chars, convert to lowercase, tokenize, remove stopwords and stemming
            review_corpus[i] = ' '.join(self.stem_words(self.remove_stopwords(self.tokenize_reviews(self.convert_lowercase(self.remove_special_characters(review_corpus[i]))))))
       
        review_corpus, locations = self.remove_spam(review_corpus,locations) #finally, remove spam reviews
        
        return (review_corpus, locations)

    def assign_review_location(self, review_corpus: list, locations: list) -> dict:
        """
        Assign each review to the appropriate franchise location.

        Returns:
            - reviews_with_locations: A dictionary with locations as keys with a corresponding 
            value of a dictionary of all reviews from those locations indexed by csv file row.
        """

        set_locations = list(OrderedDict.fromkeys(locations)) #create an ordered list of locations

        reviews_with_locations = {}

        for i in range(len(set_locations)):
            temp_dict = {}
            for u in range(len(locations)): #look for reviews from the same location, add to temp_dict
                if locations[u] == set_locations[i]:
                    temp_dict[u] = review_corpus[u]                    
            reviews_with_locations[set_locations[i]] = temp_dict #add reviews with index of that particular location to reviews_with_location

        return reviews_with_locations

  
    def generate_new_reviews(self, review_corpus: list, starters: list, features: list, linking_verbs: list, adjectives: list, num:int = 4) -> list:
        """
        #Take in an existing review_corpus and extending it to include /num/ new reviews. /num/ is set to 4 by default.
        
        Generates new reviews by randomly selecting and combining the sentences of the input parameters.
        
        For example, if we use:
            starters = ["In my opinion", "To me", "Honestly"]
            features = ["occupancy", "menu items", "opening hours", "staff"]
            linking_verbs = ["is", "are", "was", "were"]
            adjectives = ["insufficient", "not enough", "inadequate", "short"]
        
        [2, 0, 2, 0] forms "Honestly occupancy was insufficient"
        [1, 3, 3, 2] forms "To me staff were not enough"

        Returns:
            - review_corpus: A list containing pre-processed customer reviews after the new reviews are inserted.
        """
        
        for num_reviews in range(num):
            rand_starters = random.randint(0,len(starters)-1) #generate a number number within the range of index
            rand_features = random.randint(0,len(features)-1)
            rand_linking_verbs = random.randint(0,len(linking_verbs)-1)
            rand_adjectives = random.randint(0, len(adjectives)-1)
            new_review = starters[rand_starters]+" "+features[rand_features]+" "+linking_verbs[rand_linking_verbs]+" "+adjectives[rand_adjectives]        
            review_corpus.append(new_review)
       
        self.review = review_corpus
        return review_corpus
        

if __name__ == "__main__":
    # Test your function here
    p = PreProcess()
    review_corpus, locations = p.reviews, p.locations
    review_corpus = ["Great service!", "The food wasn't good"]
    starters      = ["In my opinion", "To me", "Honestly"]
    features      = ["occupancy", "menu items", "opening hours", "staff"]
    linking_verbs = ["is", "are", "was", "were"]
    adjectives    = ["insufficient", "not enough", "inadequate", "short"]
    review_corpus = ["Great service!", "The food wasn't good"]
    new_reviews   = p.generate_new_reviews(p.reviews, starters, features, linking_verbs, adjectives, 3)
    
    
