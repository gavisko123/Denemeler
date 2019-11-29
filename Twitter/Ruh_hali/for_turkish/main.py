import pandas as pd
import numpy as np
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from pyvirtualdisplay import Display
import time
from textblob import TextBlob
import re
import matplotlib.pyplot as plt
import turkishnlp
from turkishnlp import detector

def getTweets(twitter_username, sayi):
    display = Display(visible=0, size=(800,600))
    display.start()
    
    driver = webdriver.Chrome()
    url = "https://twitter.com/"+twitter_username
    driver.get(url)
    time.sleep(2)
    
    tweets = []
    elem = driver.find_element_by_tag_name("body")
    
    while sayi:
        elem.send_keys(Keys.PAGE_DOWN)
        time.sleep(0.3)
        sayi-=1
    
    twitter_elm = elem.find_elements_by_class_name('tweet')
    for post in twitter_elm:
        tweets.append(post.find_element_by_css_selector(".TweetTextSize.TweetTextSize--normal").text)
    
    driver.quit()
    display.stop()
    return tweets

def clean_tweets(tweet):
    return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)"," ",tweet).split())


def turkce_mi(tweet):
    temizle = clean_tweets(tweet)
    global nesne
    if(len(temizle) == 0 ):
        return 0
    elif(nesne.is_turkish(tweet) == True):
        return tweet
    else:
        return 0
    

def analyze_sentiment(tweet):
    if(turkce_mi(tweet)!=0):
        analysis = TextBlob(turkce_mi(tweet))
        print(analysis)
        if(analysis.sentiment.polarity > 0):
            return 1
        elif(analysis.sentiment.polarity ==0):
            return 0
        else:
            return -1
    
    
    
def tweets_to_df(tweets):
    df = pd.DataFrame(data=[tweet for tweet in tweets], columns=['Tweets'])
    df['len'] = np.array([len(tweet) for tweet in tweets])
    return df

def dialog(pos,neg,notr):
    basliklar = "POSITIVE", "NEGATIVE", "NOTR"
    veriler = [pos,neg,notr]
    fig1, ax1 = plt.subplots()
    ax1.pie(veriler, labels = basliklar, autopct="%1.1f%%", shadow=True, startangle=90)
    ax1.axis("equal")
    plt.title("Twitter Sentiment Analysis")
    plt.savefig("sonuc.png")
    psikolojik_analiz(pos,neg,notr)
    plt.show()
    

def psikolojik_analiz(pos,neg,notr):
    if(pos > neg):
        print("This person usually happy!")
    elif(pos < neg):
        print("This person usually unhappy!")
    else:
        print("This person completely neutral!")
    
def menu():
    print("""
      
    
                  TWITTER SENTIMENT ANALYSIS
    
    
    Coded by FFH
    """)
    target = input("Enter target name:")
    asagi_cek = int(input("Number of page downs:"))
    liste = getTweets(target, asagi_cek)    
    df = tweets_to_df(liste)    
    df['sentiment'] = np.array([analyze_sentiment(tweet) for tweet in df['Tweets']])
    pos,neg,notr = 0,0,0
    for i in df['sentiment']:
        if(i==1):
            pos+=1
        elif(i==0):
            notr+=1
        else:
            neg+=1
    
    dialog(pos, neg, notr)
nesne = detector.TurkishNLP()
nesne.download()
nesne.create_word_set()
menu()
