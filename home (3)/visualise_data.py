from analyse_reviews import *
from preprocess import *
import numpy as np
import pandas as pd
import matplotlib.pyplot as plot
import plotly.express as px
import seaborn as sb

def review_probabilities(reviews, locations):
    """
    Returns a list of sentiments of all reviews in input reviews list.

    Arguments:
    - reviews: List representing all reviews
    - locations: List of all locations

    Returns:
    probabilities_reviews_list: List representing sentiments of all reviews
    """

    #initialising object of SentimentAnalyser
    sentiment = SentimentAnalyser()

    #getting a list containing dictionaries of review sentiments which consists of compound, negative, neutral, and positive probablities.
    probabilities_review_dict = sentiment.get_customer_sentiment(reviews)
    probabilities_reviews_list = []
    #all_location_probabilities = []
    #unique_list = list(OrderedDict.fromkeys(locations))

    for index in range (len(reviews)):
        probabilities_review_dict[index].pop("compound") #remove compound before get max value of each pos, neg, neu
        maximum_probability = max(probabilities_review_dict[index].values())
        #determine it is neg,pos or neu
        result = [k for k,v in probabilities_review_dict[index].items() if v == maximum_probability]
        if "neu" in result:
            result_probabilties = 2

        elif "pos" in result:
            result_probabilties = 1

        elif "neg" in result:
            result_probabilties = 0
        probabilities_reviews_list.append(result_probabilties) #put sentiments of all reviews in a list
    
    return probabilities_reviews_list

def generate_bar_chart(reviews: list, num: int):
    """
    Generates a bar chart from the most common words that exists in customer's review and it's frequencies. 

    Arguments:
    - reviews: List representing all/specific location reviews
    - num: Integer representing number of most reoccuring words

    Returns:
    - None
    """
    #initialising object of class FeatureExtractor
    f = FeatureExtractor()
    #if number of common words needed is indicated/not
    if num == 15:
        common_words = f.extract_common_words(reviews)
    else:
        common_words = f.extract_common_words(reviews, num)

    #list of common words on x axis
    x_axis = [item[0] for item in common_words]
    #list of common word frequencies on y axis
    y_axis = [item[1] for item in common_words]

    #start and end colors of gradient for bar chart
    color1 = "#003153"
    color2 = "#FEF4D2"
    #set figure size
    fig = plot.figure(figsize = (25, 9))
    #plot bar chart
    #color of all bars uses a gradient color list generated using function get_color_gradient
    plot.bar(x_axis, y_axis, width = 0.9, color = get_color_gradient(color1, color2, len(x_axis)))
    plot.title("Most Common Words in Customer's Review")
    plot.xlabel(f"{num} Most Reoccuring Words")
    plot.ylabel("Word Frequencies")

    #save bar chart
    plot.savefig("bar_chart.jpg")
    plot.show()

def generate_pie_chart(p: PreProcess):
    """
    Generates a sunburst chart from customer review sentiments, compounds, and locations. 

    Arguments:
    - p: Object of class PreProcess

    Returns:
    - None 
    """
    #getting the reviews and locations of PreProcess object
    reviews = p.reviews
    locations = p.locations

    #initialising object of SentimentAnalyser
    sentiment = SentimentAnalyser()
    #getting the compounds of each review and their sentiments with their locations using insert_customer_sentiment of SentimentAnalyser class
    compounds, reviews_with_locations_sentiments = sentiment.insert_customer_sentiment(reviews, locations)
    #getting a list of sentiments of all reviews
    probabilities_list = review_probabilities(reviews, locations)

    #add locations, sentiments and compounds to a dictionary to be converted to a pandas dataframe
    data = {
        'Location': locations,
        'Sentiment' : probabilities_list,
        'Compounds' : compounds
    }

    #convert data to a pandas dataframe
    df = pd.DataFrame(data)

    #csv file for checking if data is accurately stored in dataframe
    #x = df.groupby(['Location','Sentiment','Compounds'], as_index= False)
    #df = x.sum()
    #df.to_csv('data.csv', index = False)

    #create a sunburst chart using the dataframe 
    fig = px.sunburst(data_frame = df, path=['Location', 'Sentiment','Compounds'])
    #save sunburst chart
    fig.write_image("sunburst_chart.png") 

def generate_extra_chart(p: PreProcess):
    """
    Generates a grouped bar chart from customer review sentiments, compounds, and the most common word of each review. 

    Arguments:
    - p: Object of class PreProcess

    Returns:
    - None 
    """
    #getting a list of sentiments of all reviews
    probabilities_list = review_probabilities(p.reviews, p.locations)
    #initialising object of FeatureExtractor
    f = FeatureExtractor()
    #list to store the highest frequency word in each review
    word_frequency = []
    for review in p.reviews:
        highest_frequency_word = f.extract_common_words([review], 1) #for each review, extract 1 most common word
        word_frequency.append(highest_frequency_word[0][0]) #append word to word_frequency list

    #initialising object of SentimentAnalyser
    sentiment = SentimentAnalyser()
    #getting the compounds of each review and their sentiments with their locations using insert_customer_sentiment of SentimentAnalyser class
    compounds, reviews_with_locations_sentiments = sentiment.insert_customer_sentiment(p.reviews, p.locations)

    #add highest frequency word of each review, sentiments and compounds to a dictionary to be converted to a pandas dataframe
    data = {
        'Compounds': compounds,
        'Sentiment' : probabilities_list,
        'Highest Frequency Word': word_frequency
    }

    #convert data to a pandas dataframe
    df = pd.DataFrame(data)

    #csv file for checking if data is accurately stored in dataframe
    #x = df.groupby(['Compounds','Sentiment','Highest Frequency Word'], as_index= False)
    #df = x.sum()
    #df.to_csv('data1.csv', index = False)
    
    #set size of figure
    fig = plot.figure(figsize = (45, 15))
    #using seaborn barplot function to create grouped bar chart
    sb.barplot(x='Highest Frequency Word', y='Compounds', hue='Sentiment', data=df) 

    #save grouped bar chart
    plot.savefig("grouped_bar_chart.jpg")
    plot.show()

    
def hex_to_RGB(hex_str):
    """ 
    Convert color hex value to a list of RGB values.

    Arguments:
    - hex_str: String representing the hex value of a specific color

    Returns:
    - rgb_values: List representing the red, green and blue values of the color
    """
    #Add base parameter 16 to the int() function to change to base 16
    rgb_values = [int(hex_str[i:i+2], 16) for i in range(1,6,2)]
    return rgb_values

def get_color_gradient(c1, c2, n):
    """
    Given two colors in hex value, returns a list of n colors to form a gradient.

    Arguments:
    - c1: String representing the hex value of a color
    - c2: String representing the hex value of another color
    - n: Integer representing the number of colors needed to form a gradient

    Returns:
    - gradient_list: List representing hex values of n colors needed to form a gradient
    """
    #get rgb values for both start and end colors
    c1_rgb = np.array(hex_to_RGB(c1))/255
    c2_rgb = np.array(hex_to_RGB(c2))/255

    #interpolate between c1(mix = 0) and c2(mix = 1)
    #generate mix values for all colors in gradient from c1 to c2
    mix_pcts = [x/(n-1) for x in range(n)]

    #generate all rgb values for each color in gradient
    rgb_colors = [((1-mix)*c1_rgb + (mix*c2_rgb)) for mix in mix_pcts]

    #convert rgb values to hex values for colors in gradient
    gradient_list = ["#" + "".join([format(int(round(val*255)), "02x") for val in item]) for item in rgb_colors]

    return gradient_list


if __name__ == "__main__":
    p = PreProcess()
    #print(type(p.reviews))
    #generate_pie_chart()
    generate_extra_chart(p, 15)
    pass

