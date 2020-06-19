from routes2 import Country_info, post_msg, search
from rts_qckmsg import qck_dict
from models import *
from dbapp import app, db
from functions import *
from mess import logger

def info_fc_chng(ls):
    for c_id in ls:
        country = search(c_id)
        for usr in country.followers.all():
            if usr.u_foll_type=="chng":
                logger.debug("sent CHNG class update to: %s, country: %s" %(usr.u_mess_id, country.c_name))
                post_msg(usr.u_mess_id, Country_info(country.info_ls(), usr.u_lang), fast(usr))

def info_fc_time():
    data = open("/var/www/kwasny.yao.cl/public_html/mess2/mess2/app/file.pckl", "rb")
    try:
        ls = load(data)
    except:
        ls = []
    data.close()
    data = open("/var/www/kwasny.yao.cl/public_html/mess2/mess2/app/file.pckl", "wb")
    dump([], data)
    data.close()
    logger.info("Since last time changed: "+str(ls))
    for c_id in ls:
        country = search(c_id)
        for usr in country.followers.all():
            if usr.u_foll_type=="time":
                logger.debug("sent TIME class update to: %s, country: %s" %(usr.u_mess_id, country.c_name))
                post_msg(usr.u_mess_id, Country_info(country.info_ls(), usr.u_lang), fast(usr))


if __name__ == "__main__":
    from pickle import load, dump
    from models import *
    from functions import funcje, info_txt
    info_fc_time()