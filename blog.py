# -*- coding: UTF-8 -*-

import datetime
import setting

import os.path
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import MySQLdb

from pymongo import Connection

from tornado.options import define, options

define("port", default=8000, help="run on the given port", type=int)
define("mysql_host", default="127.0.0.1:3306", help="blog database host")
define("mysql_database", default="blog", help="blog database name")
define("mysql_user", default="blog", help="blog database user")
define("mysql_password", default="blog", help="blog database password")


class Application(tornado.web.Application):

    def __init__(self):
        handlers = [
        (r'/', HomeHandler),
        (r'/editpost', EditpostHandler),
        (r'/edituser', EdituserHandler),
        (r'/login', LoginHandler),
        (r'/register', RegisterHandler),
        (r'/resetpassword', ResetpasswordHandler),
        (r'/user', UserHandler),
        (r'/commit', CommitHandler),
        ]

        settings = dict(
            blog_title = "Our blog",
            template_path=os.path.join(os.path.dirname(__file__), ""),
            static_path=os.path.join(os.path.dirname(__file__), "static"),
            #ui_modules = {"Entry": EntryModule},
            xsrf_cookies = True,
            cookie_secret = "__TODO:_GENERATE_YOUR_OWN_RANDOM_VALUE_HERE__",
            login_url = "/login",
            home_url = "/",
            debug=setting .DEBUG,        
     ) 
        tornado.web.Application.__init__(self,handlers,**settings)
        self.db = MySQLdb.connect(
            host = 'options.mysql_host', database = 'options.mysql_database',
            user = 'options.mysql_user', password = 'options.mysql_password' ) 


class BaseHandler(tornado.web.RequestHandler):
    @property
    def db(self):
        return self.application.db

    def get_current_user(self):
        user_id = self.get_secure_cookie("blogdemo_user")
        if not user_id: return None
        return self.db.get("SELECT * FROM authors WHERE id = %s", int(user_id))

    
class HomeHandler(BaseHandler):   

    def get(self):
        entrise = self.db.query("SELECT * FROM entries ORDER BY published "
                                "DESC LIMIT 5")
        self.render('home.html', entries=entries)

    def post(self):
        id = self.get_argument('_id','')
        title = self.get_argument('title','')
        time = datatime.datatime.now()
        author = session.user.name
        if id:
                 entry = self.db.get("SELECT * FROM entries WHERE id = %s",int(id))
                 if not entry: raise tornado.web.HTTPError(404)
                 self.db.execute(
                    "UPDATE entries SET title = %s, author = %s, time = %s "
                    "WHERE id = %s", title, time, author, int(id))
                
        else:
              id = self.get_argument('_id','')
              title = self.get_argument('title','')
              time = datatime.datatime.now()
              author = session.user.name

              self.render('home.html',)            
                

class EditpostHandler(tornado.web.RequestHandler):
    def post(self):
        self.render('editpost.html')


class DeleteHandler(BaseHandler):
    def get(self):
        key = self.get_argument("key")
        try:
            entry = Entry.get(key)
        except db.BadKeyError:
            raise tornado.web.HTTPError(404)
        self.render("delete.html", entry=entry)

    def post(self):
        key = self.get_argument("key")
        try:
            entry = Entry.get(key)
        except db.BadKeyError:
            raise tornado.web.HTTPError(404)
        entry.delete()
        self.redirect("/")



class CommitHandler(tornado.web.RequestHandler):

    #def get(self):
     #   id = self.get_argument("id",'')
     #   entry = None
     #   if id:
     #       entry = self.db.get("SELECT * FROM entries WHERE id = %s",int(id))
     #       self.render("commit.html")

    def post(self):
        id = self.get_argument('_id','')
        commit = self.get_argument('commit','')
        title = self.get_argument('title','')
        time = self.get_argument('time','')
        author = self.get_argument('author','')
        ccommit = self.get_argument('ccommit','')
        ctime = datatime.datatime.now()
        cauthor = session.user.name
        cursor = db.cursor()
        if id:
            sql = """ INSERT INTO article(commit)
            VALUES ('commit')"""
            sql = """ INSERT INTO commit(ccommit, ctime, cauthor)
            VALUES ('commit', 'ctime', 'cauthor')"""
            try:
                cursor.execute(sql)
                db.commit()
            except:
                db.rollback()
        else:
                 raise tornado.web.HTTPError(404)
    

class EdituserHandler(tornado.web.RequestHandler):

    """docstring for EdituserHandler"""
    def  post(self):
        email = self.session.useremail
        name = self.session.username
        sno = self.session.usersno
        sex = self.session.usersex
        self.render('edituser.html')

        
class UserHandler(tornado.web.RequestHandler):

    """docstring for UserHandler"""
    def  post(self):
        email = self.get_argument('email','')
        name  = self.get_argument('name','')
        sno = self.get_argument('sno','')
        phone = self.get_argument('phone','')
        location = self.get_argument('location','')
        age = self.get_argument('age','')
        sex = self.get_argument('sex','')
        city = self.get_argument('city','')
        hobby = self.get_argument('hobby','')
        self.render('user.html')
    
        

class LoginHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("login.html")

    def post(self):
        email = self.get_argument('email',default=None)
        password = self.get_argument('password',default=None)
        next_url = self.get_argument('next',default=home_url)

        if not email or not password:
            self.message='帐号或密码不能为空'
            return self.render("login.html")
        
        try:
            email = ({'email':email})
            if not email:
                raise
            wd = self.hash_password(unicode(m['_id']),password)
            user = ({'email':email,'password':wd})
            if not user:
                raise
        except:
            self.message='帐号或密码错误'
            return self.render("login.html")

        
        if not user['active']:
            self.message='帐号不可用'
            return self.render("login.html")
        
        self.session.uid = user['email']
        self.session.username = user['name']
        self.redirect(next_url)

class LogoutHandler(tornado.web.RequestHandler):

    @tornado.web.authenticated
    def get(self):

        self.session.clean()
        self.redirect("/login")


class ResetpasswordHandler(tornado.web.RequestHandler):

    @tornado.web.authenticated
    def get(self):
        self.render('resetpasswd.html',success=False)

    @tornado.web.authenticated
    def post(self):

        oldpass = self.get_argument('oldpass',default=None)
        newpass = self.get_argument('newpass',default=None)
        confirm = self.get_argument('confirm',default=None)

        try:
            if not oldpass or not newpass or not confirm:
                self.message = '密码不能为空'
                raise

            id = self.session.aid
            wd = self.hash_password(unicode(uid),oldpass)
            sql ="SELECT email from user WHERE email=="wd" and uid=="_id" "
            if not sql:
                self.message = '旧的密码不正确'
                raise

            if newpass != confirm:
                self.message = '两次新密码不一致'
                raise
        except:
            return self.render('resetpasswd.html',success=False)

        newwd = self.hash_password(unicode(uid),newpass)
        "UPDATE user SET uid='_id', newwd='password'"
        #db_user.update({'_id':uid},{'$set':{'password':newwd}})

        self.session.uid = None
        self.session.name = None
        self.session.clean()
        return self.render('resetpassword.html',success=True)

class RegisterHandler(tornado.web.RequestHandler):

    template_name = "register.html"

    def get(self):
        self.render(self.template_name)

    def post(self):
        email = self.get_argument('email',default=None)
        password = self.get_argument('password',default=None)
        name = self.get_argument('name',default=None)
        sno = self.get_argument('sno','')
        location = self.get_argument('location','')
        city = self.get_argument('city','')
        sex = self.get_argument('sex',default=None)
        phone = self.get_argument('phone',default=None)
        QQ = self.get_argument('qq',default=None)
        hobby = self.get_argument('hobby','')
        age = self.get_argument('age','')
        
        try:
            if not email or not password:
                self.message = '帐号或密码不能为空'
                raise

            if "SELECT email FROM user WHERE email==email":
                self.message = '帐号已经存在'
                raise

            if not sex or not name:
                self.message = '性别或姓名不能为空'
                raise

                raise
        except:
            return self.render(register.html)

        tmp={}
       
        tmp['email'] = email
        tmp['password'] = password
        tmp['name'] = name
        tmp['sex'] = sex
        tmp['sno'] = sno
        tmp['phone'] = phone
        tmp['qq'] = QQ
        tmp['city'] = city
        tmp['location'] = location
        tmp['hobby'] = hobby
        tem['age'] = age
        tmp['atime'] = datetime.datetime.now()
 
        #uid = db_user.save(tmp)
        " INSERT INTO user ("uid","tem")"
        
        wd = self.hash_password(unicode(uid),password)
        "UPDATE user SET uid='_id',wd='password'"

        self.redirect(home_url)  


class ResetPasswordHandler(tornado.web.RequestHandler):

    def get(self):
        self.render('resetpasswd.html',success=False)

    def post(self):

        oldpass = self.get_argument('oldpass',default=None)
        newpass = self.get_argument('newpass',default=None)
        confirm = self.get_argument('confirm',default=None)

        try:
            if not oldpass or not newpass or not confirm:
                self.message = '密码不能为空'
                raise

            uid = self.session.uid
            wd = self.hash_password(unicode(uid),oldpass)
            "sql = SELECT uid and wd FROM user WHERE uid=='_id' and wd=='password' "
            #if not db_user.find_one({'_id':uid,'password':wd}):
            if not sql 
                self.message = '旧的密码不正确'
                raise

            if newpass != confirm:
                self.message = '两次新密码不一致'
                raise
        except:
            return self.render('resetpasswd.html',success=False)

        newwd = self.hash_password(unicode(uid),newpass)
        #db_user.update({'_id':uid},{'$set':{'password':newwd}})
        " UPDATE user SET uid='_id',newwd='password')"

        self.session.uid = None
        self.session.uid = None
        self.session.clean()
        return self.render('resetpasswd.html',success=True)


if __name__ == '__main__':
            print ('systerm started ...')
            tornado.options.parse_command_line()
            http_server = tornado.httpserver.HTTPServer(Application())
            http_server.listen(options.port)
            tornado.ioloop.IOLoop.instance().start()
