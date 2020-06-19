from models import *
from dbapp import db


def en(usr):
    usr.u_lang = "en"
    db.session.commit()
    return """MENU
|--INFO
|   |--How it works
|   |--How to follow
|   |--Notifications
|   |--Contact
|
|--FOLLOWING
|   |--instructions
|   |--followed countries id's
|   |--countries id's
|   |--chng/time/off
|   |
|   |--BUTTONS:
|       |--Followed country1
|       |--Followed country2
|       |--Followed country3
|       | .
|       | .
|       | .
|       |--Followed country12
|
|--COUNTRIES
|   |--top 40 chorzy
|   |--top 40 zmarli
|   |--top 40 recovered
|   |--top 40 infected tdy
|   |--Data of all countries
|	
|--LANGUAGE"""

def pl(usr):
    usr.u_lang = "pl"
    db.session.commit()
    return """MENU
|--INFO
|   |--Jak to dziala
|   |--Jak obserwowac
|   |--Powiadomienia
|   |--Kontakt
|
|--OBSERWOWANIE
|   |--instrukcje
|   |--id krajow obserwowanych
|   |--id krajow
|   |--zmiana/czas/wyl
|   |
|   |--PRZYCISKI:
|       |--Obserwowany kraj1
|       |--Obserwowany kraj2
|       |--Obserwowany kraj3
|       | .
|       | .
|       | .
|       |--Obserwowany kraj12
|
|--KRAJE
|   |--top 40 chorzy
|   |--top 40 zmarli
|   |--top 40 wyzdrowiali
|   |--top 40 zarazeni dzis
|   |--Dane wszystkich krajow
|	
|--JEZYK"""


"""Return message c_name, c_id"""
def followed_id(usr):
    if usr.u_lang=="pl":
        ret = ""
        for c in usr.u_followed:
            ret += "%s, %d\n" %(c.c_name_pl, c.c_id)
        return "Brak" if ret == "" else ret
    else:
        ret = ""
        for c in usr.u_followed:
            ret += "%s, %d\n" %(c.c_name, c.c_id)
        return "None" if ret == "" else ret

"""Returns message all c_name, c_id"""
def c_list_id(usr):
    if usr.u_lang=="pl":    
        ret = ""
        for c in Country.query.order_by(Country.c_name_pl).all():
            ret += "%s, %d\n" %(c.c_name_pl, c.c_id)
        return ret
    else:
        ret = ""
        for c in Country.query.order_by(Country.c_name).all():
            ret += "%s, %d\n" %(c.c_name, c.c_id)
        return ret

"""Return actual type"""
def notif_chng(usr):
    mode = usr.u_foll_type
    if mode == "off":
        usr.u_foll_type = "chng"
    elif mode == "chng":
        usr.u_foll_type = "time"
    elif mode == "time":
        usr.u_foll_type = "off"
    db.session.commit()
    return info_txt["Now_"+usr.u_lang] + usr.u_foll_type

def by_inf_now(usr):
    t_40 = Country.query.order_by(Country.c_curr_cases).all()[-40:]
    ret = ""
    if usr.u_lang=="pl":
        for c in t_40:
            ret += "%d. %s, Chorzy: %d\n" %(c.c_pos, c.c_name_pl, c.c_curr_cases)
        return ret
    else:
        for c in t_40:
            ret += "%d. %s, ill: %d\n" %(c.c_pos, c.c_name, c.c_curr_cases)
        return ret


"Return message all c_name, c_ill_sum"
def by_ill(usr):
    t_40 = Country.query.order_by(Country.c_ill_sum).all()[-40:]
    ret = ""
    if usr.u_lang=="pl":
        for c in t_40:
            ret += "%d. %s, Zachororwan: %d\n" %(c.c_pos, c.c_name_pl, c.c_ill_sum)
        return ret
    else:
        for c in t_40:
            ret += "%d. %s, all cases: %d\n" %(c.c_pos, c.c_name, c.c_ill_sum)
        return ret

def by_inf(usr):
    t_40 = Country.query.order_by(Country.c_inf_tdy).all()[-40:]
    ret = ""
    if usr.u_lang=="pl":
        for c in t_40:
            ret += "%d. %s, Zarazeni dzis: %d\n" %(c.c_pos, c.c_name_pl, c.c_inf_tdy)
        return ret        
    else:
        for c in t_40:
            ret += "%d. %s, infected tdy: %d\n" %(c.c_pos, c.c_name, c.c_inf_tdy)
        return ret


"Return message all c_name, c_dead"
def by_dead(usr):
    t_40 = Country.query.order_by(Country.c_dead).all()[-40:]
    ret = ""
    if usr.u_lang=="pl":
        for c in t_40:
            ret += "%s, zmarli: %d\n" %(c.c_name_pl, c.c_dead)
        return ret
    else:
        for c in t_40:
            ret += "%s, dead: %d\n" %(c.c_name, c.c_dead)
        return ret


def by_dead_tdy(usr):
    t_40 = Country.query.order_by(Country.c_deaths_tdy).all()[-40:]
    ret = ""
    if usr.u_lang=="pl":
        for c in t_40:
            ret += "%s, zmarli dzis: %d\n" %(c.c_name_pl, c.c_deaths_tdy)
        return ret
    else:
        for c in t_40:
            ret += "%s, deaths tdy: %d\n" %(c.c_name, c.c_deaths_tdy)
        return ret

"Return message all c_name, c_recov"
def by_recov(usr):
    t_40 = Country.query.order_by(Country.c_recover).all()[-40:]
    ret = ""
    if usr.u_lang=="pl":
        for c in t_40:
            ret += "%s, wyzdrowiali: %d\n" %(c.c_name_pl, c.c_recover)
        return ret
    else:
        for c in t_40:
            ret += "%s, recov: %d\n" %(c.c_name, c.c_recover)
        return ret



def fast(usr):
    typ = "WROC" if usr.u_lang=="pl" else "BACK"
    rtn = [{
    "content_type":"text",
    "title": typ,
    "payload":"Follow_un"
    }]
    
    priv_fast_btn = {
    "content_type":"text",
    "title":"",
    "payload":""
    }
    count = 0
    followed = usr.u_followed.all()
    if usr.u_lang == "pl":
        for cntry in followed:
            if count <12:    
                btn = priv_fast_btn.copy()
                btn["title"] = cntry.c_name_pl
                btn["payload"]="Fast."+cntry.c_name
                rtn.append(btn) 
            else:
                break
            count += 1

    else:
        for cntry in followed:
            if count <12:    
                btn = priv_fast_btn.copy()
                btn["title"] = cntry.c_name
                btn["payload"]="Fast."+cntry.c_name
                rtn.append(btn) 
            else:
                break
            count += 1
    return rtn

def all_fast_stat(usr):
    ls_foll_c_ill = Country.query.order_by(Country.c_ill_sum).all()    
    ret=""

    if usr.u_lang=="pl":
        for c in ls_foll_c_ill:
            data = c.info_ls()
            ret += "%s, %d, %d, %d, %d, %d\n" %(data[1], data[8],
                    data[4], data[5], data[6], data[7])
        ret += "_, chorzy teraz, chrz.dzis, zm., zm.dzis, wyzdro."
        return ret
    else:
        for c in ls_foll_c_ill:
            data = c.info_ls()
            ret += "%s, %d, %d, %d, %d, %d\n" %(data[0], data[8],
                    data[4], data[5], data[6], data[7])
        ret += "_,curr. ill, infected tdy., dead, dead tdy, recvrd"
        return ret

### ZMIENIA TEKST NA FCJE
funcje = {"en":en, "pl":pl, "followed_id":followed_id, "c_list_id":c_list_id,
        "notif_chng":notif_chng, "by_ill":by_ill, "by_dead":by_dead,
        "by_recov":by_recov, "by_inf_now":by_inf_now, "by_dead_tdy":by_dead_tdy,
        "Fast":fast, "by_inf":by_inf, "all_fast_stat":all_fast_stat}


how_to_follow_en =  """In order to follow country send:
.foll X,X..,X
Where X is an name or id
przyklady:
.foll poland,usa,Canada
.foll 30,2
.foll 1
.foll Ukraine
.foll RUSSIA,14,Cypr

REMEMBER TO TURN ON NOTIFICATIONS
see MENU/INFO/Notifications"""

how_to_follow_pl =  """Aby obserwowac Kraj wyslij:
.foll X,X..,X
Gdzie X to nazwa albo id
przyklady:
.foll polska,usa,kanada
.foll 30,2
.foll 1
.foll Czechy
.foll ROSJA,14,Cypr

PAMIETAJ O WLACZENIU POWIADOMIEN
zobacz MENU/INFO/Powiadomienia"""

how_to_set_notif_en = """When One allready follows chosen countries
One can set notifications to get messages
in one of three modes:
1.CHNG
Every time followed countries data changes
One gets a message with its current data.
2.TIME
Every two hours One gets "update" on followed
countries which data has changed in these two hours.
3.OFF

In order to change between three modes:
<off/chng/time>
press button
MENU/FOLLOWING/"off/chng/time"
"""

how_to_set_notif_pl = """Kiedy juz zaczniesz obserwowac wybrane kraje
mozesz ustawic sobie powiadomienia aby dostawac
wiadomosc w jednym z dwoch trybow:
1.CHNG
Za kazdym razem kiedy zmieniaja sie dane
obserwowanego przez ciebie kraju, dostajesz wiadomosc z jego danymi.
2.TIME
Co dwie godziny dostajesz wiadomosc z "aktualizacja" czyli
obsrwowane kraje ktorych dane ulegly zmianie w tym czasie.
3.WYLACZONE

Aby przelaczac miedzy trzema trybami:
<off/chng/time>
naciskaj przycisk
MENU/OBSERWOWANIE/"wyl/zmiana/czas" """

how_it_works_en = """In case of problems:
-See help videos.
https://www.facebook.com/Covid-Info-Bot-100109041628520/

Every two minutes I download data from:
www.worldometers.info/coronavirus,
but on the site data for single countries
changes much less often.

One can follow Countries in order to get
up to date notifications and to have
quick access buttons for these countries.
(MENU/FOLLOWING/FOLLOWED BUTTONS) up to 12 btns.
Notifications are sent in two modes:
1. Every change in data of followed countries
for a single country it is not often.
2. Less often, every two hours
And One can allways turn them OFF.

!!!FB has a 'anti spam feature' that unables me to send messages
after 24 since your last sent message.
To keep notifications running press any button every 24 hours,
if you forget nothing except updates is lost :) !!!


One can view information about every country typing in its name or id.
One can view all countries with data, sorted by ill, dead, recovered and infected tdy.
They are in MENU/COUNTRIES"""

how_it_works_pl = """W przypadku problemow:
-Zobacz strone aby zapoznac sie z filmami pomocniczymi.
https://www.facebook.com/Covid-Info-Bot-100109041628520/

Co dwie minuty pobieram informacje z
www.worldometers.info/coronavirus,
ale na stronie zmieniaja sie rzadziej
dla pojedynczych krajow.

Mozesz obserwowac kraje aby dostawac
na biezaco powiadomienia oraz zeby
miec przyciski szybkiego dostepu do tych krajow.
(MENU/OBSERWOWANIE/OBSERWOWANE PRZYCISKI) do 12 przyciskow.

Powiadomienia wysylane sa w dwoch trybach:
1. Przy kazdej zmianie danych obserwowanych krajow
dla pojedynczego kraju to jest dosc rzadko
2. Rzadziej, bo co dwie godziny pod warunkiem ze dane ulegly zmianie.
oraz zawsze mozna je WYLACZYC.

!!!FB ma taka 'funkcje anty spamowa' ktora uniemozliwia wysylanie
po 24 od ostaniej twojej wyslanej wiadomosci.
Aby utrzymac powiadomienia wlaczone wcisnij bylejaki guzik kazde 24 godziny,
jezeli zapomnisz oprocz powiadomien nic nie przepada :) !!!

Mozesz wyswietlac informacje wszystkich krajow wpisujac nazwe albo id.
Mozesz wyswietlac listy z danymi krajow,
sortowanymi po chorych, zmarlych, wyzdrowialych i zarazonych dzis.
W zakladce KRAJE sa listy wszystkich krajow."""

contact_en = """Contact:
covidpoland@gmail.com"""

contact_pl = """Kontakt:
covidpoland@gmail.com"""

instructions_en = """How to follow?
1. One needs to type .foll X,X..,X
Where X is countries name or id,
2. Ready!

In ORDER TO TURN ON NOTIFICAIONS:
Switch between notification modes
off/change/time
by pressing button
Modes descriptions are in MENU/INFO/Notifications

How to unfollow?
1. type in .unfl X,X..,X
Where X is name or id of country,
2. Ready! """

instructions_pl = """Jak obserwowac?
1. trzeba wpisac .foll X,X..,X
Gdzie X to jest nazwa albo id kraju,
2. Gotowe!

ABY WLACZYC POWIADOMIENIA:
przelaczaj miedzy trybami powiadomien
wylaczone/zmiana/czas
klikajac przycisk
Opisy trybow sa w MENU/INFO/Powiadomienia

Jak anulowac obserwowanie?
1. trzeba wpisac .unfl X,X..,X
Gdzie X to nazwa albo id kraju,
2. Gotowe! """

### errs, dynamic and templates

Cmd_wrong_art_en = "cmd wrong atributes"
Cmd_wrong_art_pl = "komenda zle atrybuty"

Succ_folw_c_en = "Success! You are now following new countries!"
Succ_folw_c_pl = "Powodzenie! Udalo ci sie obserwowac nowe kraje!"

Succ_unfw_c_en = "Great! You have unfollowed succesfull!"
Succ_unfw_c_pl = "Dobrze! Poprawnie usunieto z obserwowanych!"

Succ_foll_type_chng_en = "Notifications type changed"
Succ_foll_type_chng_pl = "Tryb powiadomien zmieniony"

Wrong_cmd_en = "Wrong command! .foll or .unfl"
Wrong_cmd_pl = "Komenda zle wpisana .foll albo .unfl"

Country_name_err_en = """No accents!
None Country with that name or id is in database,
Some might be tricky to find as their names are shortend.
Check MENU/FOLLOWING/Countries id's, in order to see all Countries with their names."""
Country_name_err_pl  = """Nie uzywaj polskich znakow!!!
NIE znaleziono kraju z podana nazwa albo id,
niektore kraje moga byc ciezkie do znalezienia poniewaz ich nazwy sa skrocone.
Obejrzyj MENU/OBSERWOWANIE/Kraje z id, aby zobaczyc wszystkie kraje z nazwami."""


# Bierze 12 z info_ls + c_id
#name, id, pos, sum_ill, inf_tdy, dead, dead_tdy, recovered,
# #curr inf, critical, cas/1m, dead/1m
#%(ls[0], ls[12], ls[2], ls[3], ls[4], ls[5], ls[6], ls[7], ls[8], ls[9], ls[10], ls[11])
# %s, %d, %d, %d, %d, %d, %d, %d, %d, %d, %f, %f
Country_info_en = """Country: %s
id: %d
Position: %d
All infected: %d
Infected today: +%d
Dead: %d
Deaths Today: +%d
Recovered: %d
Currently infected: %d
Critical cases: %d
Cases per 1M: %f
Deaths per 1M: %f"""


Country_info_pl = """Kraj: %s
id: %d
Pozycja: %d
Ilosc przypadkow: %d
Zarazeni dzis: +%d
Zmarli: %d
Zmarli dzis: +%d
Wyzdrowiali: %d
Przypadkow aktualnych: %d
Krytyczne przypadki: %d
Przypadki na 1M: %f
Smierci na 1M: %f"""



### errs info and templates

info_txt = {"how_to_follow_en":how_to_follow_en, "how_to_follow_pl":how_to_follow_pl,
            "how_to_set_notif_en":how_to_set_notif_en, "how_to_set_notif_pl":how_to_set_notif_pl,
            "how_it_works_en":how_it_works_en, "how_it_works_pl":how_it_works_pl,
            "contact_en":contact_en, "contact_pl":contact_pl,
            "instructions_en":instructions_en, "instructions_pl":instructions_pl,
            "Country_name_err_en":Country_name_err_en, "Country_name_err_pl":Country_name_err_pl,
            "Cmd_wrong_atr_en":Cmd_wrong_art_en, "Cmd_wrong_atr_pl":Cmd_wrong_art_pl,
            "Succ_folw_c_en":Succ_folw_c_en, "Succ_folw_c_pl":Succ_folw_c_pl,
            "Succ_unfw_c_en":Succ_unfw_c_en, "Succ_unfw_c_pl":Succ_unfw_c_pl,
            "Succ_foll_type_chng_en":Succ_foll_type_chng_en, "Succ_foll_type_chng_pl":Succ_foll_type_chng_pl,
            "Wrong_cmd_en":Wrong_cmd_en, "Wrong_cmd_pl":Wrong_cmd_pl,
            "Country_info_en":Country_info_en, "Country_info_pl":Country_info_pl,
            "Now_en":"This is new mode: ", "Now_pl":"To jest nowy tryb: "}


### commands
command_ls = ["foll", "unfl"]