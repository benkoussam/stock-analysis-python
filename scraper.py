# Sentiment Analysis of Twitter Data - Web Scraper
# Author: Mimi Benkoussa

documented_code.rb linguist-documentation=true

# Import/libraries used
from __future__ import division
from bs4 import BeautifulSoup
import csv

# Welcome message upon launch
print " "
print "Sentiment Analysis of Twitter Data - Web Scraper"
print "Author: Mimi Benkoussa"
print " "
nb = raw_input('Welcome to this sentiment analysis program of Twitter stocks.\nPlease input the stock you wish to analyze below as a .html file.\nOr, you can simply enter "demo" to run a sentiment analysis of #NYSE:BAC (Bank of America) from Nov. 1 2017 - Dec. 11 2017. \n')

# Creating a new file, OUTPUT.csv, that will hold the scraped, cleaned tweets
new = csv.writer(open("OUTPUT", "w"))
new.writerow(["Tweets: "])
new.writerow([ ])		# allows for space between Tweets

# User input - either "demo" or another .html file obtained from Twitter search
try:
    if nb.split('.')[1] == "html":
        demo = nb
    else:
        demo = "bacc.html"
except IndexError:
    demo = "bacc.html"

# Using BeautifulSoup to parse the html file
data = open(demo).read()
soup = BeautifulSoup(data, "html.parser")

# Parsing by HTML tweet class
tweets = soup.find_all('div', class_="js-tweet-text-container")

# Writing the tweets to OUTPUT.csv
def writetweets():
	new.writerow(tweets)

# Splitting the tweets, getting rid of any unneccessary tags and text
def splitter():
    list1 = []
    read = csv.reader(open("OUTPUT", "r"))
    for li in read:
        for l in li:
            first = l.split('<p class="TweetTextSize js-tweet-text tweet-text" data-aria-label-part="0" lang="en">')
            for i in first:
                if i[0] != "<":
                    list1.append(i)
    return list1

# Further tweet cleanup
def cleanup():
    list1 = splitter()
    list2 = []
    for i in list1:
        first = i.split('<a')
        list2.append(first[0])
    return list2

# Definition of positive and negative sentiments
def sentiments():
    mydic = {'positive': 0, 'negative': 0}
    # Positive and negative wordbanks. Please see attached resources sheet
    # Plurals were included, just in case
    punc = [',', '.', ';', '?', '!']
    positive = ['holdings', 'profit', 'profits', 'sold', 'sells', 'increases', 'increase', 'invests', 'invest', 'growth', 'grow', 'soaring', 'bullish', 'raises', 'acquires', 'acquire']
    negative = ['sells', 'trimmed', 'ban', 'bans', 'decreases', 'decrease', 'drop', 'drops', 'tragic', 'loss', 'losses', 'negative', 'dip', 'dips', 'plumment', 'plumets', 'fail', 'fails']
    l = cleanup()
    for i in l:
        sp = i.split(" ")
        for j in sp:
            if j == "EPS":
                index = sp.index(j)
                before = sp[index-1]
                if before.split('$')[0] == '-' or before.split('$')[1] < 0:
                    mydic['negative'] +=1
                    break
                elif before.split('$')[1] > 0:
                    mydic['positive'] +=1
                    break
            elif len(j) > 0 and j[-1] in punc:
                if j[:-1].lower() in positive:
                    mydic['positive'] += 1
                    break
                elif j[:-1].lower() in negative:
                    mydic['negative'] += 1
                    break
            elif j.lower() in positive:
                mydic['positive'] += 1
                break
            elif j.lower() in negative:
                mydic['negative'] += 1
                break
    possum = mydic['positive']
    negsum = mydic['negative']
    total = negsum + possum
    print (negsum/total) * 100,"% negative"
    print (possum/total) * 100,"% positive"
    if (possum/total) * 100 > (negsum/total) * 100:
        print "Sentiment analysis has determined a positive change in this stock!"
    else:
        print "Sentiment analysis has determined a negative change in this stock!"


def demo():
    writetweets()
    splitter()
    cleanup()
    # If you would like to view all of the cleaned tweets in console, uncomment the portion below.
    """
    for i in cleanup():
        print i
        print '\n'
    """
    sentiments()

if __name__ == '__main__':
    demo()
