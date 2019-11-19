import requests
from bs4 import BeautifulSoup as bs
import emoji


def menu():
    #hedef = input("Hedef kisinin kullanici adini girin :")
    tweetleri_cek("EceSeckinCom")

def tweetleri_cek(hedef):
    url = "https://twitter.com/"+hedef
    istek = requests.get(url)
    
    if(istek.status_code!=200):
        print("Bir sorun olustu lutfen tekrar deneyin!")
    
    else:
        result = []
        emojiler = []
        corba = bs(istek.text,"lxml")
        for p in corba.find_all('img',{'class':'Emoji Emoji--forText'}):    
            emoji = str(p)
            result.append(emoji[10])
        # Result emojileri direkt olarak kendi hallerinde tutuyor
        for i in result:
            emojiler.append(extract_emojis(i)) #Emojiler adli liste ise demojize edilmis halleri tutuyor. Karsilastirma icin bize bu liste lazim
        oranla(emojiler)
        print(result,emojiler,sep = "\n")
        del result

def extract_emojis(string):
    emojis = ''.join(c for c in string if c in emoji.UNICODE_EMOJI)
    return emoji.demojize(emojis)


def oranla(arr):
    
    mutlu,mutsuz,notr = 0,0,0
    
    positive = [':bowtie:', ':face_with_tears_of_joy:', ':simple_smile:', ':blush:', ':relaxed:', ':heart_eyes:', ':heart_eyes:', ':kissing_closed_eyes:', ':relieved:', 
                ':grin:', ':stuck_out_tongue_winking_eye:', ':grinning:', ':kissing_smiling_eyes:', ':sweat_smile:', ':joy:', ':smile:', ':smile:', 
                ':laughing:', ':smiley:', ':smirk:', ':kissing_heart:', ':satisfied:', ':wink:', ':stuck_out_tongue_closed_eyes:', ':stuck_out_tongue:', 
                ':grimacing:', ':smiling_face_with_3_hearts:', ':revolving_hearts:', ':smiling_imp:', ':beaming_face_with_smiling_eyes:', ':smiling_face_with_3_hearts:', ':innocent:', ':dancer:', ':dancers:', ':couple_with_heart:', ':couplekiss:', ':trollface:', ':yum:', ':neutral_face:']

    
    negative = [':frowning:', ':drooling_face:', ':open_mouth:', ':confused:', ':expressionless:', ':disappointed_relieved:', ':pensive:', ':confounded:', ':cold_sweat:', 
                ':cry:', ':scream:', ':tired_face:', ':rage:', ':sleepy:', ':dizzy_face:', ':dizzy_face:', ':anguished:', ':hushed:', ':unamused:', 
                ':weary:', ':sweat:', ':weary:', ':disappointed:', ':fearful:', ':persevere:', ':sob:', ':angry:', ':triumph:']

    
    for i in arr:
        for j in positive:
            if(i==j):
                mutlu+=1
            else:pass
        for k in negative:
            if(i==k):
                mutsuz+=1
            else:pass
    
    boyut = len(arr)
    if(boyut==0):
        print("Bu kisi hakkinda bilgi edinemedik!")
    else:
        notr = int( ((boyut-(mutlu+mutsuz))/boyut)*100    )
        mutlu = int((mutlu/boyut)*100)
        mutsuz = int((mutsuz/boyut)*100)
        print("Bu kisi %{} mutlu, %{} mutsuz, %{} ise notr!".format(mutlu,mutsuz,notr))
    
   
menu()
