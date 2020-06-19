from bs4 import BeautifulSoup
from requests import get
from models import Country, follow_c
from dbapp import db
from mess import logger
from pickle import load, dump
from routes2 import search

def get_update():
    """download raw data, parse it, return list with every countries data NOT ready"""
    stat = 0
    pow = 0
    while pow<5 and str(stat) !="200":
        try:
            r = get('https://www.worldometers.info/coronavirus')
            stat=r.status_code
        except:
            pass
        pow+=1

    if pow>=5:
        exit()
    content = r.content
    soup = BeautifulSoup(content, 'lxml')
    tbody = soup.find_all("tbody")
    kraje = tbody[0].find_all("tr")
    total = tbody[1].find_all("tr")[0]
    kraje.append(total)
    return kraje

def index_stats(content):
    """Clean out stats of a single country and place them in a list
    as world has no number at beggining it gets 0 as its place"""
    ret = []
    for stats in content.find_all("td"):
        z = stats.text.strip().strip(" ").replace(",", "").replace("+", "").replace(":", "")
        if z=="" or z==" " or z=="N/A":
            z = "0"

        # Teraz wzsystko jest albo str albo str(int) albo str(float)
        # Jezeli to sa same cyfry to zrob int(z)
        if z.isdigit():
            z = int(z)

        # W przeciwnym wypadku moze to jest float? wiec: float(z)
        else:
            try:
                z = float(z)
            except:
                pass
        ret.append(z)
    return ret

def stats_ls():
    """Returns double nested list of countries stats"""
    rtn = []
    for country in get_update():
        rtn.append( index_stats(country) )
    return rtn

def db_update(all_sts_ls):
    """Update databse, as input take double nested list of stats"""
    rtn_change_id = []
    logger.debug(str(len(all_sts_ls)))
    for country in all_sts_ls:
        ctry = search(country[1])
        if ctry == None:
            logger.info("NEW COUNTRY:" + country[1])
            ctry = Country(c_pos=country[0], c_name = country[1], c_name_pl=country[1], c_ill_sum = country[2], c_inf_tdy = country[3],
                            c_dead = country[4], c_deaths_tdy = country[5], c_recover = country[6], c_curr_cases = country[7],
                            c_crit_cases = country[8], c_case_1m = country[9], c_dead_1m = country[10])
            db.session.add(ctry)
        else:
            logger.debug("%d, %s" %(ctry.c_id, ctry.c_name))
            chng = ctry.update(country[0], country[2], country[3], country[4], country[5], country[6], country[8], country[9], country[10], country[11])
            if chng:
                rtn_change_id.append(ctry.c_id)
    db.session.commit()
    return rtn_change_id

if __name__ == "__main__":
    chng = db_update(stats_ls())
    logger.info("chng: " + str(chng))
    if chng!=[]:
        from subs import info_fc_chng
        info_fc_chng(chng)
    chng_file = open("/var/www/kwasny.yao.cl/public_html/mess2/mess2/app/file.pckl", "rb")
    try:
        file_ls = load(chng_file)
    except:
        file_ls = []
    chng_file.close()
    
    if not file_ls==chng:
        for c_id in chng:
            if not c_id in file_ls:
                file_ls.append(c_id)
        logger.info("chng file_ls after sum: " + str(file_ls))
        chng_file = open("/var/www/kwasny.yao.cl/public_html/mess2/mess2/app/file.pckl", "wb")
        dump(file_ls, chng_file)
        chng_file.close()

    # zeby nie powtarzalo sie chng i chng_ls
    # jakas funcja
    #non_repetetive = fcja
    #ls = non_repetetive