import requests
from bs4 import BeautifulSoup as bs
import emoji


def menu():
    hedef = input("Hedef kisinin kullanici adini girin :")
    tweetleri_cek(hedef)

def tweetleri_cek(hedef):
    url = "https://twitter.com/"+hedef
    istek = requests.get(url)
    
    if(istek.status_code!=200):
        print("Bir sorun olustu lutfen tekrar deneyin!")
    
    else:
        result = []
        corba = bs(istek.text,"lxml")
        for p in corba.find_all('p',{'class':'TweetTextSize TweetTextSize--normal js-tweet-text tweet-text'}):    
            emoji = p.select('img.Emoji')
        
            if emoji:
                for em in emoji:
                    index = p.contents.index(em)
                p.contents[index].replace_with(em['alt'])
            result.append(p.getText())
        for i in result:
            if(extract_emojis(i)):
                print(extract_emojis(i))
            else:
                pass

def extract_emojis(string):
    return ''.join(c for c in string if c in emoji.UNICODE_EMOJI)

menu()
