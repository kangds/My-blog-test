# -*- coding: UTF-8 -*-
#encoding=utf-8

import datetime
import setting

import os.path
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web

from tornado.options import define, options
define("port", default=8000, help="run on the given port", type=int)


class Application(tornado.web.Application):

    def __init__(self):
        handlers = [
        (r'/', HomeHandler),
        (r'/editpost', EditpostHandler),
        (r'/edituser', EdituserHandler),
        (r'/login', LoginHandler),
        (r'/logout',LogoutHandler),
        (r'/register', RegisterHandler),
        (r'/resetpassword', ResetpasswordHandler),
        (r'/user', UserHandler),
        (r'/photo', PhotoHandler),
        (r'/commit', CommitHandler),
        ]

        settings = dict(
            blog_title = "Our blog",
            template_path=os.path.join(os.path.dirname(__file__), ""),
            static_path = os.path.join(os.path.dirname(__file__), "static"),
            #static_path = os.path.join(os.path.dirname(__file__), "images"),
            #ui_modules = {"Entry": EntryModule},
            xsrf_cookies = True,
            cookie_secret = "__TODO:_GENERATE_YOUR_OWN_RANDOM_VALUE_HERE__",
            login_url = "/login",
            home_url =  "/",
            debug=setting .DEBUG,
            ) 
        tornado.web.Application.__init__(self,handlers,**settings)


class HomeHandler(tornado.web.RequestHandler):   
    def get(self):
        self.render('home.html')

    def post(self):
        self.render('home.html')            
                
class PhotoHandler(tornado.web.RequestHandler):   
    def get(self):
        self.render('photo.html')

    def post(self):
        self.render('photo.html')            

class EditpostHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('editpost.html')
    def post(self):
        self.render('editpost.html')


class DeleteHandler(tornado.web.RequestHandler):
    def get(self):
        key = self.get_argument("key")
        try:
            article = Article.get(key)
        except db.BadKeyError:
            raise tornado.web.HTTPError(404)
        self.render("delete.html", article=article)

    def post(self):
        key = self.get_argument("key")
        try:
            article = Article.get(key)
        except db.BadKeyError:
            raise tornado.web.HTTPError(404)
        article.delete()
        self.redirect("/")



class CommitHandler(tornado.web.RequestHandler):

    #def get(self):
     #   id = self.get_argument("id",'')
     #   entry = None
     #   if id:
     #       entry = self.db.get("SELECT * FROM entries WHERE id = %s",int(id))
     #       self.render("commit.html")
     def post(self):
        aid = self.get_argument('_id','')
        commit = self.get_argument('commit','')
        title = self.get_argument('title','')
        time = self.get_argument('time','')
        author = session.user.name
        cid = self.get_argument('_id','')
        ccommit = self.get_argument('ccommit','')
        ctime = datatime.datatime.now()
        cauthor = session.user.name
        if aid:
            sql = """INSERT INTO article(commit)
            VALUES ('commit')"""
            cursor.execute(sql)

            sql = """ INSERT INTO commit(ccommit, ctime, cauthor)
            VALUES ('commit', 'ctime', 'cauthor')"""
            try:
                cursor.execute(sql)
                db.commit()
            except:
                db.rollback()
        else:
                 raise tornado.web.HTTPError(404)
        self.render("commit.html")
    

class EdituserHandler(tornado.web.RequestHandler):

    """docstring for EdituserHandler"""
    def  post(self):
        email = self.session.user.email
        name = self.session.user.name
        sno = self.session.user.sno
        gender = self.session.user.gender
        self.render('edituser.html')
    def  get(self):
        email = self.session.user.email
        name = self.session.user.name
        sno = self.session.user.sno
        gender = self.session.user.gender
        self.render('edituser.html')

        
class UserHandler(tornado.web.RequestHandler):

    """docstring for UserHandler"""
    def  get(self):
        email = self.get_argument('email','')
        name  = self.get_argument('name','')
        sno = self.get_argument('sno','')
        phone = self.get_argument('phone','')
        location = self.get_argument('location','')
        age = self.get_argument('age','')
        gender = self.get_argument('gender','')
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
        self.session.user.name = user['name']
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

            uid = self.session.uid
            wd = self.hash_password(unicode(uid),oldpass)
            sql ="SELECT email FROM user WHERE oldpass=='wd' and uid=='_id' "
            sql ="SELECT email FROM user WHERE email=='wd' and uid=='_id' "
            if not sql:
                self.message = '旧的密码不正确'
                raise

            if newpass != confirm:
                self.message = '两次新密码不一致'
                raise
        except:
            return self.render('resetpasswd.html',success=False)

        newwd = self.hash_password(unicode(uid),newpass)
        sql = "UPDATE user SET uid='_id', newwd='password'"
        cursor.execute(sql)
        db.commit()

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
        gender = self.get_argument('gender',default=None)
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

            if not gender or not name:
                self.message = '性别或姓名不能为空'
                raise

                raise
        except:
            return self.render(register.html)

        tem = {}
       
        tem['email'] = email
        tem['password'] = password
        tem['name'] = name
        tem['gender'] = gender
        tem['sno'] = sno
        tem['phone'] = phone
        tem['qq'] = QQ
        tem['city'] = city
        tem['location'] = location
        tem['hobby'] = hobby
        tem['age'] = age
 
        #uid = db_user华中农业大学理学院信息与计算科学2011级1班班级博客共享平台.save(tmp)
        sql = " INSERT INTO user ('uid','tem')"
        cursor.execute(sql)
        db.commit()
        
        wd = self.hash_password(unicode(uid),password)
        sql = "UPDATE user SET uid='_id',wd='password'"
        cursor.execute(sql)
        db.commit()

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
            sql = "SELECT uid and wd FROM user WHERE uid=='_id' and wd=='password' "
            #if not db_user.find_one({'_id':uid,'password':wd}):
            if not sql: 
                self.message = '旧的密码不正确'
                raise

            if newpass != confirm:
                self.message = '两次新密码不一致'
                raise
        except:
            return self.render('resetpasswd.html',success=False)

        newwd = self.hash_password(unicode(uid),newpass)
        #db_user.update({'_id':uid},{'$set':{'password':newwd}})
        sql = " UPDATE user SET uid='_id',newwd='password')"
        cursor.execute(sql)
        db.commit()

        self.session.uid = None
        self.session.clean()
        return self.render('resetpasswd.html',success=True)


if __name__ == '__main__':
            print ('systerm started ...')
            tornado.options.parse_command_line()
            http_server = tornado.httpserver.HTTPServer(Application())
            http_server.listen(options.port)
            #tornado.httpserver.HTTPServer(Application()).listen(options.port)
            tornado.ioloop.IOLoop.instance().start()
