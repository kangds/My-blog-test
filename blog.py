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


class Application(tornado.web.Application):

    def __init__(self):
        handlers = [
        (r'/', HomeHandler),
        (r'/editpost', EditpostHandler),
        (r'/edituser', EdituserHandler),
        (r'/login', LoginHandler),
        (r'/register', RegisterHandler),
        (r'/resetpassword', ResetPasswordHandler),
        (r'/user', UserHandler),
        (r'/commit', CommitHandler),
        ]

        settings = dict(
            template_path=os.path.join(os.path.dirname(__file__), ""),
            static_path=os.path.join(os.path.dirname(__file__), "static"),
            debug=setting .DEBUG,        
     ) 
     

        conn = Connection()
        self.blog = conn ["blog"]
        self.user = conn ["user"]
        self.commit=conn['commit']
        tornado.web.Application.__init__(self,handlers,**settings)

    
class HomeHandler(tornado.web.RequestHandler):   

    def get(self):
        coll = self.application.db.blog
        article_doc = coll.find()
        self.render('home.html',article_doc=article_doc)

    def post(self):
        aid = self.get_argument('_id','')
        title = self.get_argument('title','')
        #article = self.get_argument("article",'')
        #commit = self.get_argument('commit','')
        time = self,get_argument('time','')
        author = self.get_argument('author','') 
        coll = self.application.db.blog
        article_doc = coll.find_one({"aid":aid})
        if article_doc:
                 article_doc['title'] = title
                 #article_doc['article'] = article
                 #article_doc['commit'] = commit
                 article_doc['time'] = time
                 article_doc['author'] = author
                 coll.save(article_doc)
        else:
                 #article_doc = {'title':title,'article':article,'commit':commit,'time':time}
                 article_doc = {'title':title, 'author':author, 'time':time}
                 coll.insert(article_doc)
                 #del article_doc["_id"]    
        self.render('home.html',article_doc=article_doc)            
                

class EditpostHandler(tornado.web.RequestHandler):

    def post(self):
        coll = self.application.db.blog
        article_doc = coll.find_one({"aid":"_id"})
        article = self.get_argument('article','')
        title = self.get_argument('title','')
        atime = datatime.datatime.now()
        self.render('editpost.html',title=title,article=article,time=atime)


class CommitHandler(tornado.web.RequestHandler):

    def post(self):
        commit = self.get_argument('commit','')
        coll = self.application.blog.blog
        coll1 = self.application.commit.commit
        commit_doc = coll.find_one({"_id":'id'})
        if article_doc:
                 article_doc ['commit'] = commit
                 coll.save(article_doc)
                 commit_doc['text'] = commit
                 commit_doc['time'] = datatime.datatime.now()
                 #评论作者 
                 self.redirect('/commit')
        else:
                 commit_doc = {'text':commit,'time':datatime.datatime.now()}
                 article_doc = {'commit':commit}
                 coll.insert(article_doc)
                 coll1.insert(commit_doc)
                 self.render('commit.html', title=noun1, article=blog1,commit=commit)
    

class EdituserHandler(tornado.web.RequestHandler):

    """docstring for EdituserHandler"""
    def  post(self):
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
            m = db_user.find_one({'email':email})
            if not m:
                raise
            wd = self.hash_password(unicode(m['_id']),password)
            user = db_user.find_one({'email':email,'password':wd})
            if not user:
                raise
        except:
            self.message='帐号或密码错误'
            return self.render("login.html")

        
        if not user['active']:
            self.message='帐号不可用'
            return self.render("login.html")
        
        self.session.mid = user['_id']
        self.session.uid = user['_id']
        self.session.nickname = user['name']
        self.session.email = user['email']
        self.redirect(next_url)

class LogoutHandler(tornado.web.RequestHandler):

    @tornado.web.authenticated
    def get(self):

        self.session.clean()
        self.redirect("/login")


class ResetPasswordHandler(tornado.web.RequestHandler):

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

            mid = self.session.mid
            wd = self.hash_password(unicode(mid),oldpass)
            if not db_user.find_one({'_id':mid,'password':wd}):
                self.message = '旧的密码不正确'
                raise

            if newpass != confirm:
                self.message = '两次新密码不一致'
                raise
        except:
            return self.render('resetpasswd.html',success=False)

        newwd = self.hash_password(unicode(mid),newpass)
        db_user.update({'_id':mid},{'$set':{'password':newwd}})

        self.session.mid = None
        self.session.uid = None
        self.session.clean()
        return self.render('resetpasswd.html',success=True)

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
        number = self.get_argument('number',default=None)
        phone = self.get_argument('phone',default=None)
        QQ = self.get_argument('qq',default=None)
        email = self.get_argument('email',default=None)
        
        try:
            if not email or not password:
                self.message = '帐号或密码不能为空'
                raise
            if not email.endswith('@androidesk.com'):
                self.message = '帐号不是公司邮箱'
                raise

            if db_user.find_one({'email':email}):
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
 
        uid = db_user.save(tmp)
        
        wd = self.hash_password(unicode(uid),password)
        db_user.update({'_id':uid},{'$set':{'password':wd}})

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

            mid = self.session.mid
            wd = self.hash_password(unicode(mid),oldpass)
            if not db_user.find_one({'_id':mid,'password':wd}):
                self.message = '旧的密码不正确'
                raise

            if newpass != confirm:
                self.message = '两次新密码不一致'
                raise
        except:
            return self.render('resetpasswd.html',success=False)

        newwd = self.hash_password(unicode(mid),newpass)
        db_user.update({'_id':mid},{'$set':{'password':newwd}})

        self.session.mid = None
        self.session.uid = None
        self.session.clean()
        return self.render('resetpasswd.html',success=True)


if __name__ == '__main__':
            print ('systerm started ...')
            tornado.options.parse_command_line()
            http_server = tornado.httpserver.HTTPServer(Application())
            http_server.listen(options.port)
            tornado.ioloop.IOLoop.instance().start()
