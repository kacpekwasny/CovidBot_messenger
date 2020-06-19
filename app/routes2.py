from flask import Flask, request
import json
import requests
import os
import re

from config import Config
from mess import app, db
from mess import logger
from models import User, Country, follow_c
from rts_qckmsg import qck_dict
from functions import funcje, info_txt, command_ls

@app.route("/", methods=["GET"])
def index():
    return "Test"

@app.route('/webhook', methods=['GET'])
def verify():
    # webhook verification
    if request.args.get('hub.mode') == 'subscribe' and request.args.get('hub.challenge'):
        if not request.args.get('hub.verify_token') == Config.VERIFY_TOKEN:
            logger.error("Verification missmatch") ### ERROR ###
            return 'Verification token missmatch', 403
        logger.info("correct hub challenge") ### info ###
        return request.args['hub.challenge'], 200
    return 'verification token', 200


@app.route('/webhook', methods=['POST'])
def msg_action():
    msg_data = request.get_data()
    for sender, message, payload in get_msg_data(msg_data):
        ln = len(message)
        if ln>400:
            userr = User.query.filter_by(u_mess_id=sender).first()
            if userr.u_lang=="pl":
                post_msg(sender, "Nie rob", qck_dict["Menu_pl"])
            else:
                post_msg(sender, "Just dont", qck_dict["Menu_en"])
            logger.error("ATTACK: %s, len of msg: %d" %(sender, ln))
            return "ok", 200

        else:
            logger.info("for loop Incoming from %s: %s - and payload: %s" %(sender, message, payload)) ### DEBUG ###
            messg, qck = handle_data(sender, message, payload) ### handle data musi zwracac rozne ###
            logger.debug("return: msg: %s, qck[0][title]: %s" %(messg, qck[0]["title"]))
            
            if messg==None or qck==None:
                logger.error("some fc has err check prev logs to find it, it returns None!!")
                messg = "NULL"
            

            #####   HANDLING LONG MESSAGES   #####
            if len(messg)>=320:
                messages = messg.split("\n")
                msg = ""
                bck = ""
                err_stop = len(messages)
                count = 0
                for message_ in messages:
                    if count-3<err_stop:
                        count += 1
                        msg += message_+"\n"
                        if len(msg)>=320:
                            post_msg(sender, bck, qck)
                            msg = message_+"\n"
                            bck = msg
                        else:
                            if len(msg)>300:
                                post_msg(sender, msg, qck)
                                bck = ""
                                msg = ""
                            else:
                                bck = msg
                    else:
                        logger.error("Message over 320, split not working properly")
                        logger.error("str(messages): "+str(messages))
                        post_msg(sender, "ERROR", qck)
                        return  "ok", 200
                post_msg(sender, msg, qck)
                ### END      HANDLING LONG MESSAGES      END ###

            else:
                post_msg(sender, messg, qck)
        return "ok", 200


def get_msg_data(payload):
    data = json.loads(payload)
    events = data["entry"][0]["messaging"]
    for event in events:
        if "message" in event and "text" in event["message"] and "quick_reply" in event["message"] and "payload" in event["message"]["quick_reply"]:
            yield event["sender"]["id"], event["message"]["text"].encode('unicode_escape'), event["message"]["quick_reply"]["payload"].encode('unicode_escape')

        elif "message" in event and "text" in event["message"]:
            yield event["sender"]["id"], event["message"]["text"].encode('unicode_escape'), "None"

        else:
            yield event["sender"]["id"], "None", "None"


"""Sends to everyone message in their language of choice"""
def broadcast(msg_en, msg_pl):
    users = User.query.all()
    for user in users:
        if user.u_lang == "pl":
            post_msg(user.u_mess_id, msg_pl, qck_dict["Menu_pl"])
        else:
            post_msg(user.u_mess_id, msg_en, qck_dict["Menu_en"])


"""Returns msg, qck_reply"""
def handle_data(sender, message, payload):
    if user_new(sender) == False:
        usr = User(u_mess_id=sender)
        #logger.info("!!! NEW USER mess_id: %s" %(sender)) ### info ###
        db.session.add(usr)
        db.session.commit()
        return "Welcome,\nChose language.", qck_dict["Language_en"]
    else:
        usr = User.query.filter_by(u_mess_id=sender).first()
        return user_possib(usr, message, payload)

"""Returns True/Flase"""
def user_new(sender):
    usr = User.query.filter_by(u_mess_id=sender).first()
    return usr if usr != None else False


"""user_possib(usr, message, payload), fcja bedzie rozkladac data
    i przywolywac odpowiednie fcje"""
#  return msg, qck_reply
def user_possib(usr, message, payload):
    lng = usr.u_lang
    if payload != "None":
        if "." in payload:
            events = payload.split(".")
            events0 = events[0]
            events1 = events[1]
            logger.debug("rtn: %s, funcja: %s" %(events[0], events[1])) ### DEBUG ###
            if events0+"_en" in qck_dict:
                if events1 in funcje:
                    ret_txt = funcje[events1](usr)
                    qck_rep = qck_dict[events0+ "_" +usr.u_lang]
                    logger.debug("ret_txt: %s, qck_rply[0][title]: %s" %(ret_txt, qck_rep[0]["title"]))
                    return ret_txt, qck_rep

                elif events1+"_en" in info_txt:
                    return info_txt[events[1]+"_"+usr.u_lang], qck_dict[events0+"_"+usr.u_lang]

                else:
                    logger.error("ERROR konfiguracji %s, %s" %(events0, events1))
            else:   ### ELSE JEST ZROBIONE DLA DYNAMICZNEGO qck_rts  ktore jest w funcjach
                cntry = search(events1)
                return Country_info(cntry.info_ls(), usr.u_lang), funcje[events0](usr)
        
        
        else:
            if payload+"_en" in qck_dict:
                return message, qck_dict[payload+"_"+lng]
            elif payload in funcje:   ### ELSE JEST DLA dynamicznego qck_rts ktore jest w funcjach zalezy od usr
                return message, funcje[payload](usr)
            else:
                return message, qck_dict["Menu_"+usr.u_lang]

    elif "." in message:
        cmd = message.strip(".")
        return command(cmd, usr)

    else:
        return country_data(message, usr)

            



# return info, Menu
"""command(text, usr)"""
def command(text, usr):
    cmd = text[0:4].lower()
    if " " in text:
        atr = text[5:]
    else:
        atr = text[4:]
    lng = usr.u_lang
    if cmd in command_ls:
        if cmd == "foll":
            ctry_to_flw = re.split(",", atr)
            for j in ctry_to_flw:
                cntry = search(j)
                if cntry==None:
                    return info_txt["Cmd_wrong_atr_"+lng], qck_dict["Info_"+lng]
                logger.info("%s following %s" %(usr.u_mess_id, cntry.c_name)) ### DEBUG ###
                logger.debug("cmd==unfl:"+cntry.c_name)
                usr.follow_c(cntry)
            db.session.commit()
            return info_txt["Succ_folw_c_"+lng], qck_dict["Follow_un_"+lng]

        elif cmd == "unfl":
            ctry_to_unfw_str = re.split(",", atr)
            logger.debug("unfl: "+str(ctry_to_unfw_str))
            for j in ctry_to_unfw_str:
                cntry = search(j)
                if cntry==None:
                    return info_txt["Cmd_wrong_atr_"+lng], qck_dict["Info_"+lng]

                logger.info("%s unfollowing %s" %(usr.u_mess_id, cntry.c_name))
                logger.debug("cmd==unfl:"+cntry.c_name)
                usr.unfollow_c(cntry)
            db.session.commit()
            return info_txt["Succ_unfw_c_"+lng], qck_dict["Follow_un_"+lng]


        # oraz dodac do functions.command_ls
        #elif cmd=="nowa_comenda":
        #   to costam 

    else:
        return info_txt["Wrong_cmd_"+lng], qck_dict["Menu_"+lng]

"""Takes text and returns Country object or None"""
def search(text):
    if type(text)==str:
        text = text.strip()
    country = None
    # SZUKANIE PO id
    if type(text)==int or text.isdigit():
        try:
            country = Country.query.filter_by(c_id=int(text)).first()
        except:
            pass
    #SZUKANIE Kraj Z Duzej
    if country == None:
        country = Country.query.filter_by(c_name = text.title()).first()
    if country == None:
        country = Country.query.filter_by(c_name_pl = text.title()).first()
    #SZUKANIE taK JAk ktoS WPIsAL
    if country == None:
        country = Country.query.filter_by(c_name = text).first()
    if country == None:
        country = Country.query.filter_by(c_name_pl = text).first()
    #SZUKANIE DUZYMI LITERAMI
    if country == None:
        country = Country.query.filter_by(c_name = text.upper()).first()
    if country == None:
        country = Country.query.filter_by(c_name_pl = text.upper()).first()
    return country

"""Returns Country stats as msg, and country_"lng" as qck_rply"""
def country_data(text, usr):
    lng = usr.u_lang
    cnt = search(text)
    if cnt==None:
        return info_txt["Country_name_err_"+lng], qck_dict["Menu_"+lng]
    else:
        return Country_info(cnt.info_ls(), lng), qck_dict["Menu_"+lng]

"""Returns message with Country info in proper lng"""
def Country_info(ls, lng):
    template = info_txt["Country_info_"+lng]
    if lng=="pl":
        return template %(ls[1], ls[12], ls[2], ls[3], ls[4], ls[5], ls[6], ls[7], ls[8], ls[9], ls[10], ls[11])
    else:
        return template %(ls[0], ls[12], ls[2], ls[3], ls[4], ls[5], ls[6], ls[7], ls[8], ls[9], ls[10], ls[11])

"""Sends message does not return anything"""
def post_msg(recipient, payload, quick):
    logger.debug(recipient + ", " + payload+"THAT WAS SENT!!! post_msg()")
    requests.post("https://graph.facebook.com/v2.6/me/messages",
    params={"access_token": Config.AT},
    data = json.dumps({
        "recipient": {"id": recipient},
        "message": {"text": payload,
                    "quick_replies": quick}
    }),
    headers={"Content-type": "application/json"})