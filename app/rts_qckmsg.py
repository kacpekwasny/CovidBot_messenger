### LANGUAGE ### "English", "polski", "menu"

Lng = [{
    "content_type":"text",
    "title":"ENGLISH",
    "payload":"Menu.en"     ### .en
},{
    "content_type":"text",
    "title":"POLSKI",
    "payload":"Menu.pl"     ### .pl
}]

### MENU ### "info", "settings", "follow", "countries"
Menu_en = [{
    "content_type":"text",
    "title":"INFO",
    "payload":"Info"
},{
    "content_type":"text",
    "title":"FOLLOWING",
    "payload":"Follow_un"
},{
    "content_type":"text",
    "title":"COUNTRIES",
    "payload":"Countries"
},{
    "content_type":"text",
    "title":"LANGUAGE",
    "payload":"Language"
}]

Menu_pl = [{
    "content_type":"text",
    "title":"INFO",
    "payload":"Info"
},{
    "content_type":"text",
    "title":"OBSERWOWANIE",
    "payload":"Follow_un"
},{
    "content_type":"text",
    "title":"KRAJE",
    "payload":"Countries"
},{
    "content_type":"text",
    "title":"JEZYK",
    "payload":"Language"
}]

### FOLLOW ### "info", "UNFOLLOW", "FOLLOW", "menu"

Follow_en = [{
    "content_type":"text",
    "title":"MENU",
    "payload":"Menu"
},{
    "content_type":"text",
    "title":"Instructions",
    "payload":"Follow_un.instructions" ### .instructions
},{
    "content_type":"text",
    "title":"Followed",
    "payload":"Follow_un.followed_id"     ### .followed
},{
    "content_type":"text",
    "title":"off/chng/time",
    "payload":"Follow_un.notif_chng"     ### .notif_chng ####
},{
    "content_type":"text",
    "title":"Countries id's",
    "payload":"Follow_un.c_list_id"    ### .c_list_id
},{
    "content_type":"text",
    "title":"FOLLOWED BUTTONS",
    "payload":"Fast"
}]

Follow_pl = [{
    "content_type":"text",
    "title":"MENU",
    "payload":"Menu"
},{
    "content_type":"text",
    "title":"Instrukcje",
    "payload":"Follow_un.instructions" ### .instructions
},{
    "content_type":"text",
    "title":"Obserwowane",
    "payload":"Follow_un.followed_id"     ### .followed
},{
    "content_type":"text",
    "title":"wyl/zmiana/czas",
    "payload":"Follow_un.notif_chng"     ### .notif_chng ####
},{
    "content_type":"text",
    "title":"Kraje z id",
    "payload":"Follow_un.c_list_id"    ### .c_list_id
},{
    "content_type":"text",
    "title":"OBSERWOWANE PRZYCISKI",
    "payload":"Fast"
}]



Countries_en = [{
    "content_type":"text",
    "title":"MENU",
    "payload":"Menu"
},{
    "content_type":"text",
    "title":"Top 40 by Ill",
    "payload":"Countries.by_inf_now"            ### .by_inf_now
},{
    "content_type":"text",
    "title":"Top 40 by infected tdy",
    "payload":"Countries.by_inf"    ### .by_inf
},{
    "content_type":"text",
    "title":"Top 40 by Dead",
    "payload":"Countries.by_dead"           ### .by_dead
},{
    "content_type":"text",
    "title":"Top 40 by Dead tdy",
    "payload":"Countries.by_dead_tdy"           ### .by_dead_tdy
},{
    "content_type":"text",
    "title":"Top 40 by recovered",
    "payload":"Countries.by_recov"          ### .by_recov
},{
    "content_type":"text",
    "title":"Top 40 by all cases",
    "payload":"Countries.by_ill"            ### .by_ill ZACHOROWAN, All cases
},{
    "content_type":"text",
    "title":"All Countr. data",
    "payload":"Countries.all_fast_stat"     ### .all_fast_stat
}]

Countries_pl = [{
    "content_type":"text",
    "title":"MENU",
    "payload":"Menu"
},{
    "content_type":"text",
    "title":"Top 40 po chorych",
    "payload":"Countries.by_inf_now"            ### .by_inf_now
},{
    "content_type":"text",
    "title":"Top 40 zarazeni dzis",
    "payload":"Countries.by_inf"    ### .by_inf
},{
    "content_type":"text",
    "title":"Top 40 po zmarlych",
    "payload":"Countries.by_dead"           ### .by_dead
},{
    "content_type":"text",
    "title":"Top 40 po zm. dzis",
    "payload":"Countries.by_dead_tdy"           ### .by_dead_tdy
},{
    "content_type":"text",
    "title":"Top 40 po wyzdrowialych",
    "payload":"Countries.by_recov"          ### .by_recov
},{
    "content_type":"text",
    "title":"Top 40 po zachorwan",
    "payload":"Countries.by_ill"            ### .by_ill
},{
    "content_type":"text",
    "title":"Wszystkie kraje dane",
    "payload":"Countries.all_fast_stat"     ### .all_fast_stat
}]

Info_en =[{
    "content_type":"text",
    "title":"MENU",
    "payload":"Menu"
},{
    "content_type":"text",
    "title":"How it works",
    "payload":"Info.how_it_works"       ### .how_it_works
},{
    "content_type":"text",
    "title":"How to follow",
    "payload":"Info.how_to_follow"      ### .how_to_follow
},{
    "content_type":"text",
    "title":"Notifications-help",
    "payload":"Info.how_to_set_notif"   ### .how_to_set_notif
},{
    "content_type":"text",
    "title":"Contact",                  ### TRZBA SOBIE NOWY MAIL ZALOZYC
    "payload":"Info.contact"            ### .contact
}]

Info_pl =[{
    "content_type":"text",
    "title":"MENU",
    "payload":"Menu"
},{
    "content_type":"text",
    "title":"Jak to dziala",
    "payload":"Info.how_it_works"       ### .how_it_works
},{
    "content_type":"text",
    "title":"Jak obserwowac",
    "payload":"Info.how_to_follow"      ### .how_to_follow
},{
    "content_type":"text",
    "title":"Powiadomienia pomoc",
    "payload":"Info.how_to_set_notif"   ### .how_to_set_notif
},{
    "content_type":"text",
    "title":"Kontakt",                  ### TRZBA SOBIE NOWY MAIL ZALOZYC
    "payload":"Info.contact"            ### .contact
}]

"""
{
    "content_type":"text",
    "title":"",
    "payload":""
}

priv_fast_btn = {
    "content_type":"text",
    "title":"",
    "payload":""
}
"""

## MOZNA BY DAC TO DO dict i przywolywac po quick_stats[*payload*]
qck_dict = {"Language_en":Lng, "Language_pl":Lng, "Menu_en":Menu_en,
            "Menu_pl":Menu_pl, "Follow_un_en":Follow_en, "Follow_un_pl":Follow_pl,
            "Countries_en":Countries_en,"Countries_pl":Countries_pl,
            "Info_en":Info_en, "Info_pl":Info_pl}


# STARE
"""{
    "content_type":"text",
    "title":"Countr. foll. stats",
    "payload":"Countries.foll_fast_stat"    ### .foll_fast_stat
}




"""