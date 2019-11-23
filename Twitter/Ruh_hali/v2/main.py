from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from pyvirtualdisplay import Display
import matplotlib.pyplot as plt
import time

def emojileri_cek(twitter_username,copd): # copd = count of page downs
    display = Display(visible=0, size=(800,600))
    display.start() #Selenium'u gizle
    
    url = "https://www.twitter.com/"+twitter_username
    driver = webdriver.Chrome()
    driver.get(url) 
    time.sleep(1)
    
    
    elem = driver.find_element_by_tag_name("body") #Sadece body kismina odaklan
    no_of_pagedowns = 100 #Sayfayi asagi kaydirma sayisi
    #Sayfa yuklenemeyecegi icin muhtemelen 100 kere indiremeyecek.
    
    while no_of_pagedowns: 
        elem.send_keys(Keys.PAGE_DOWN)
        time.sleep(0.3) #Sayfalarin tam bir sekilde yuklenebilmesi icin sure uzatilabilir.
        no_of_pagedowns-=1
    
    twitter_elm = driver.find_elements_by_class_name("tweet") #Tweetlere odaklan
    temojis = [] #Emojilerin yuklenecegi liste
    
    for post in twitter_elm:
        username = post.find_element_by_class_name("username") 
        if(username.text.lower() == "@" +twitter_username.lower()): 
            img = post.find_elements_by_css_selector('img') #Emojiler img taginin altinda
            for i in img:
                if(i.get_attribute("aria-label")):
                    temojis.append(i.get_attribute("alt")) #Emojiler alt=... seklinde saklaniyor
    driver.quit()
    display.stop()
    durum(temojis)
    
def durum(arr):
    pos_sayisi, neg_sayisi, notr_sayisi = 0,0,0
    posEmoji = "😀😃😄😁😆😅😂🤣☺😊😇🙂🙃😉😌😍😘😗😙😚😋😛😝😜🤪💞🤩😏😭🤗💕❤️💙🧡💚💯👑❣️💖💫⭐🌟✨⚡🔥"
    negEmoji = "😞😔😟😕🙁☹😣😖😫😩😢😓😪😭😤😠😡🤬🤯🤢🤮😷❌❗🤒🤕👹👺👻💀👽😾🖕🏿👎🏻👎🧟‍♂🧟‍♀"
    for emoji in arr:
        if(emoji in posEmoji):
            pos_sayisi += 1
        elif(emoji in negEmoji):
            neg_sayisi += 1
        else:
            notr_sayisi += 1
    analiz(pos_sayisi,neg_sayisi,notr_sayisi)
    

def analiz(pos,neg,notr): #Emojilerin oranini cikti ile gosteriyoruz
    basliklar = "Pozitif Emojiler", "Negatif Emojiler", "Notr Emojiler"
    veriler = [pos,neg,notr]
    fig1, ax1 = plt.subplots()
    ax1.pie(veriler, labels = basliklar, autopct="%1.1f%%", shadow=True, startangle=90)
    ax1.axis("equal")
    plt.title("Twitter Emoji Analizi")
    plt.savefig("sonuc.png")
    plt.show()

    
def menu():
    target = input("Kullanici adini giriniz:")
    copd = int(input("Sayfayi asagi cekme deneme sayisi:"))
    emojileri_cek(target, copd)
    
menu()
