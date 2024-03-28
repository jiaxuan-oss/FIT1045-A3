#Author(s): Yew Jin Ruo, Teh Jia Xuan, Tan Jian Hao, Sam Leong
#Team: Musang King
#Date Edited: 30/1/2023

from preprocess import *
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
from preprocess import * 
from collections import OrderedDict
        
class FeatureExtractor:
    
    def extract_common_words(self, reviews: list, num: int = 15) -> list:
        """
        Extracts the top num occuring words from a list of reviews. 
        num is set to 15 by default.

        Arguments:
            - reviews: A list of pre-processed customer reviews. 

        Returns:
            - common_words: A list of tuples containing the word and the number of occurence.
        """ 
        reviews = ' '.join(reviews) #join the reviews into a single string
        reviews = reviews.split() #seperate each one into individual words for iteration purpose
        review_dict = {}
        count_of_words = []
        common_words = []
        
        review_dict = {i : reviews.count(i) for i in reviews if i not in review_dict} #for each word, count how many are there. 'not in review_dict' so that it don't repeat

        for idx in range(num): 
            count_of_word = max(list(review_dict.values())) #find what the max count is for each time
            key = list(review_dict)[list(review_dict.values()).index(count_of_word)] #by using index of the count_of_word to find the key
            common_words.append((key,count_of_word))
            del review_dict[key] #delete item to make sure no repeat

        return common_words

        #raise NotImplementedError

class ReviewSummariser:

    def calculate_word_weights(self, review: str, words_to_ignore: list) -> dict:
        """
        Determines the weight of each word in a review by counting it's occurence and dividing the total occurences with the highest frequency. 

        Arguments:
            - review: An individual review.
            - words_to_ignore: A list that consists of words to ignore (weight of word will be 0).

        Returns:
            - weighted_words: A dictionary containing the weights of every word in the review. 
        """
        word_lst = []
        weighted_words = {}
        p = PreProcess()
        review = p.convert_lowercase(p.remove_special_characters(review))

        for word in review.split():
            if word not in words_to_ignore:                
                word_lst.append(review.split().count(word)) #Initialise word_lst with weight of each word

        weight = max(word_lst) #find the max weight

        #a function that will calculate the weight of the word
        value = lambda word, review, words_to_ignore, weight : 0 if word in words_to_ignore else float(review.split().count(word))/weight

        weighted_words = {word : value(word, review, words_to_ignore, weight) for word in review.split()} #initialize weighted word with weight

        return weighted_words        
        

    def calculate_sentence_weights(self, review: str, selected_words: dict, words_to_ignore: list) -> dict:
        """
        Determines the weight of each sentence by adding weighted frequencies of the words that occur in that particular sentence.

        Arguments:
            - review: An individual review.
            - selected_words: A dictionary that stores extra weight to priotise certain words.
            - words_to_ignore: A list that consists of words to ignore (weight of word will be 0).

        Returns:
            - weighted_sentences: A dictionary containing the weights of every sentence in the review. 
        """

        p = PreProcess()
        review_key = review #review_key is a seperate review that is used for initialising weighted_sentences without the original text altered
        review = p.convert_lowercase(review)
        weighted_sentences = {}

        review_split = review.split('.')
        review_split = [string for string in review_split if string != ''] #remove empty string
        review_key = review_key.split('.')
        review_key = [string for string in review_key if string != ''] #remove empty string
        weighted_words = self.calculate_word_weights(review, words_to_ignore) #initialize dictionary with words and its corresponding weights
        
        #test
        #print(weighted_words)

        for r in range(len(review_split)):
            token_review = p.tokenize_reviews(p.remove_special_characters(review_split[r])) 
            accum = 0
            
            for i in token_review:
                if i in weighted_words.keys():
                    if i in selected_words.keys():
                        accum += selected_words.get(i) #only if word is in selected word, increment with the corresponding value
                    accum += weighted_words.get(i) #otherwise, increment with the initial value calculated
                    
            
            weighted_sentences[review_key[r].strip()] = accum #initialise weighted_sentences with it's key and weight
        
        return weighted_sentences

    def generate_summary(self, review: str, n: int, selected_words: list, words_to_ignore: list) -> str:
        """
        Generates a summary of a review by taking the top n sentences with the highest scores.

        Arguments:
            - review: An individual review.
            - n: An integer representing how many sentences should be combined.
            - selected_words: A dictionary that stores extra weight to priotise certain words.
            - words_to_ignore: A list that consists of words to ignore (weight of word will be 0).

        Returns:
            - review_summary: A summary of a review. 
        """
        review_summary = []
        sent_weight = self.calculate_sentence_weights(review, selected_words, words_to_ignore)
        review = review.split('.')

        for sentence in range(n):
            idx = list(sent_weight.values()).index(max(list(sent_weight.values()))) #find the index of the sentence of the highest weight value
            review_summary.append(review[idx]) #append review_summary with the review with the index of highest weight
            del sent_weight[list(sent_weight.keys())[idx]] #remove from the dictionary to make sure no repeat
            review.remove(review[idx]) #remove from the review list as well so that indexing will stay in order

        review_summary = '.'.join(review_summary)+"." #join the sentences together into a single line of string

        return review_summary
       
class SentimentAnalyser:

    def get_customer_sentiment(self, reviews: list) -> list:
        """
        Determines the sentiment possibilities of every review.
        Implements Sentiment Analysis from the NLTK module: https://www.nltk.org/howto/sentiment.html

        Arguments:
            - reviews: A list of pre-processed customer reviews. 

        Returns:
            - sentiments: A list containing dictionaries of review sentiments which consists of compound, negative, neutral, and positive probablities.  
        """
        sentiment_analyzer = SentimentIntensityAnalyzer() #create object
        sentiments = [] 
        for sentence in reviews: #loop through reviews list
            possibilities_review = sentiment_analyzer.polarity_scores(sentence) #use NLTK library to determine sentiment possibilities
            sentiments.append(possibilities_review) #add possibilities to sentiments list

        return sentiments #return sentiments


    def insert_customer_sentiment(self, reviews: list, locations: list) -> tuple:
        """
        Determines the sentiment of every review depending on the highest probability and sets the sentiment to: (0:Negative, 1:Positive, 2:Neutral)

        Arguments:

            - reviews: A list of pre-processed customer reviews (follow csv file order).
            - locations: A list of all franchise locations (follow csv file order). 

        Returns:
            - compounds: The compound rate of the review. 
            - reviews_with_locations_sentiments: A nested dictionary containing lists that consists of the customer's reviews and the sentiment (0, 1, or 2).
        """
        probabilities_review_dict = self.get_customer_sentiment(reviews)
        compounds = []
        dict_without_location = {}
        reviews_with_locations_sentiments = {}
        probabilities_reviews_list = []
        p = PreProcess()

        #get compounds of each reviews
        for probabilities in probabilities_review_dict:
            compounds_probability = probabilities.get("compound")#get compound probabilities of each review 
            compounds.append(compounds_probability)#append to compound list
   
        #get review with probabilties in a list
        for index in range (len(reviews)):
            temp_list = [] #create temporary list
            probabilities_reviews_list.append([])# append [] into the list to create list in a list
            temp_list.append(reviews[index]) #append to list in list 
            probabilities_review_dict[index].pop("compound") #remove compound before get max
            maximum_probability = max(probabilities_review_dict[index].values()) #get maximum probabilities of pos neg and neu
            #determine it is neg pos or neu
            result = [k for k,v in probabilities_review_dict[index].items() if v == maximum_probability] #compare if maximum_probability same as neu, pos, or neg 's probability
            if "neu" in result:# if is neutral
                result_probabilties = 2 #then is 2

            elif "pos" in result: #if is positive
                result_probabilties = 1 #then is 1

            elif "neg" in result: #if is negative then 
                result_probabilties = 0 #is 0
            temp_list.append(result_probabilties) #eg ['joy eat aeroplan food hour journey australia warn', 2]
            probabilities_reviews_list[index] = temp_list # add all reviews and result_probabilties into probabilities_reviews_list eg [[review,result_probabilties],[review, result_probabilties]]
        
        reviews_with_locations_sentiments = p.assign_review_location(probabilities_reviews_list, locations) #generate location with reviews
        
        return compounds, reviews_with_locations_sentiments #return
        
if __name__ == "__main__":
    # Test your function here
    test = ReviewSummariser()
    #review = "This restaurant serves really authentic cuisine from Malaysia which is really a rare find in Wales. Many of the dishes were spicy, aromatic and reminds me of my hometown of Penang. Dined here with a group of friends and we all ENJOYED the dishes. All dishes were freshly prepared and absolutely delicious. Reasonably priced too. We loved the rendang and even went back for a second serving. The menu is extensive, and it is even possible to buy laksa and rendang frozen. What a hidden gem."
   # selected_words = {"authentic": 4, 'loved': 3, 'cuisine': 2, 'food': 2} 
    #words_to_ignore =  ['the', 'a', 'was', 'other', 'this', 'and', 'from', 'is', 'were', 'and', 'of', 'which', 'in']
   # print(test.calculate_sentence_weights(review, selected_words, words_to_ignore))
    


    



