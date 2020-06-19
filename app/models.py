from dbapp import db

follow_c = db.Table('follow_c',
           db.Column('u_id', db.Integer, db.ForeignKey('user.u_id')),
           db.Column('c_id', db.Integer, db.ForeignKey('country.c_id'))
)


class User(db.Model):
    u_id = db.Column(db.Integer, primary_key = True)
    u_mess_id = db.Column(db.String(20), unique=True)
    u_lang = db.Column(db.String(2), default="en")
    u_foll_type = db.Column(db.String(4), default="off") ### time / chng
    u_time_update = db.Column(db.String())
    u_followed = db.relationship('Country', secondary=follow_c, backref=db.backref('followers', lazy='dynamic'), lazy='dynamic')

    def chng_lang(self, lng):
        if lng != self.u_lang:
            self.u_lang = lng

    def follow_c(self, country):
        if not self.is_following(country.c_name):
            country.followers.append(self)

    def unfollow_c(self, country):
        if self.is_following(country.c_name):
            country.followers.remove(self)

    def is_following(self, c_name):
        rtn = self.u_followed.filter_by(c_name=str(c_name)).count()
        if rtn>0:
            return True
        else:
            return False

    def change_foll_type(self, type_): # NOT USED
        if self.u_foll_type == type_:
            return True
        elif type_ == "time":
            self.u_foll_type = "time"
            return True
        elif type_ == "chng":
            self.u_foll_type = "chng"
            return True
        else:
            return False

class Country(db.Model):
    c_id = db.Column(db.Integer, primary_key=True)
    c_pos = db.Column(db.Integer)
    c_name = db.Column(db.String(30))
    c_name_pl = db.Column(db.String(30))
    c_ill_sum = db.Column(db.Integer)
    c_inf_tdy = db.Column(db.Integer)
    c_dead = db.Column(db.Integer)
    c_deaths_tdy = db.Column(db.Integer)
    c_recover = db.Column(db.Integer)
    c_curr_cases = db.Column(db.Integer)
    c_crit_cases = db.Column(db.Integer)
    c_case_1m = db.Column(db.Float)
    c_dead_1m = db.Column(db.Float)

    """update takes stats updates them and if change has occured returns True"""
    def update(self, c_pos, c_ill_sum, c_inf_tdy, c_dead, c_deaths_tdy, c_recover, c_curr_cases, c_crit_cases, c_case_1m, c_dead_1m):
        change_hpnd = False

        if self.c_ill_sum != c_ill_sum:
            self.c_ill_sum = c_ill_sum
            change_hpnd = True

        if self.c_dead != c_dead:
            self.c_dead = c_dead
            change_hpnd = True

        if self.c_recover != c_recover:
            self.c_recover = c_recover
            change_hpnd = True

        self.c_inf_tdy = c_inf_tdy
        self.c_deaths_tdy = c_deaths_tdy
        self.c_curr_cases = c_curr_cases
        self.c_crit_cases = c_crit_cases
        self.c_pos = c_pos
        self.c_case_1m = c_case_1m
        self.c_dead_1m = c_dead_1m

        return change_hpnd 

    def info_ls(self):  # returns 13, name, name_pl pos, ill, inf_tdy, dead, dead_tdy,
                            #recov, current, crit, cases/1M, dead/1M, id
        return [self.c_name, self.c_name_pl, self.c_pos, self.c_ill_sum, self.c_inf_tdy,
        self.c_dead, self.c_deaths_tdy, self.c_recover, self.c_curr_cases, self.c_crit_cases,
        self.c_case_1m, self.c_dead_1m, self.c_id]