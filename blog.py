# -*- coding: UTF-8 -*-

import datatime

import os.path
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web

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
        (r'/resetpassword', ResetpasswordHandler),
        (r'/user', UserHandler),
        (r'/commit', CommitHandler),
        ]
        settings = dict(
            template_path=os.path.join(os.path.dirname(__file__), ""),
            static_path=os.path.join(os.path.dirname(__file__), "static"),
            debug=True,        
     ) 
     

        conn = Connection()
        self.blog = conn ["blog"]
        self.user = conn ["user"]
        self.commit=conn['commit']
        tornado.web.Application.__init__(self,handlers,**settings)


def init_logging(console=0):
    if console:
        fh = logging.StreamHandler()
    else:
        fh = logging.handlers.RotatingFileHandler('%s%s' % (setting.LOG_PATH, setting.LOG_FILENAME),
                maxBytes=500*1024*1024,
                backupCount=3)
        formatter = logging.Formatter('%(levelname)-8s %(asctime)s %(module)s:%(lineno)d:%(funcName)s %(message)s')
        fh.setFormatter(formatter)

    root_logger = logging.getLogger()
    root_logger.addHandler(fh)
    root_logger.setLevel(setting.LOG_LEVEL)
        
    
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
                 article_doc = {'title':title, 'author':author 'time':time}
                 coll.insert(article_doc)
                 #del article_doc["_id"]    
        self.render('home.html',article_doc=article_doc)            
                

class EditpostHandler(tornado.web.RequestHandler):
    def get(self):
        coll = self.application.db.blog
        article_doc = coll.find_one({"title":"title"})
        article = self.get_argument('article','')
        title = self.get_argument('title','')
        atime = datatime.datatime.now()
        self.render('editpost.html',title=title,article=article,time=atime)
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
                article_doc = {'commit':commit_doc}
                 coll.insert(article_doc)
                 coll1.insert(commit_doc)
                 self.render('commit.html', title=noun1, article=blog1,commit=commit_doc)
    #def get(self):
    #noun1 = self.get_argument('','')
    #blog1 = self.get_argument('blog1','')
    #commit = self.get_argument('commit','')
    # self.render('commit.html', title=noun1, article=blog1, commit=commit)

 class LoginHandler(BaseHandler):
    def get(self):
        self.render("login.html")

    def post(self):
        account = self.get_argument('account',default=None)
        password = self.get_argument('password',default=None)
        next_url = self.get_argument('next',default=home_url)

        if not account or not password:
            self.message='帐号或密码不能为空'
            return self.render("login.html")
        
        try:
            m = db_user.find_one({'account':account})
            if not m:
                raise
            wd = self.hash_password(unicode(m['_id']),password)
            member = db_user.find_one({'account':account,'password':wd})
            if not member:
                raise
        except:
            self.message='帐号或密码错误'
            return self.render("login.html")

        
        if not member['active']:
            self.message='帐号不可用'
            return self.render("login.html")
        
        self.session.mid = member['_id']
        self.session.uid = member['_id']
        self.session.nickname = member['name']
        self.session.email = member['account']
        self.redirect(next_url)

class LogoutHandler(BaseHandler):

    @tornado.web.authenticated
    def get(self):

        self.session.clean()
        self.redirect("/login")


class ResetPasswordHandler(BaseHandler):

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

class MemberCreateHandler(BaseHandler):

    template_name = "register.html"

    @tornado.web.authenticated
    def get(self):
        self.render(self.template_name)

    @tornado.web.authenticated
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
            return self.render(login.html)

        tmp={}
       
        tmp['account'] = account
        tmp['password'] = password
        tmp['name'] = name
        tmp['gender'] = gender
        tmp['number'] = number
        tmp['phone'] = phone
        tmp['qq'] = QQ
        tmp['email'] = email
        tmp['active'] = True
        tmp['atime'] = datetime.datetime.now()
 
        uid = db_user.save(tmp)
        
        wd = self.hash_password(unicode(uid),password)
        db_user.update({'_id':uid},{'$set':{'password':wd}})

        self.redirect(home_url)  

        def main():
            print ('systerm started ...')
            tornado.options.parse_command_line()
            http_server = tornado.httpserver.HTTPServer(Application())
            http_server.listen(options.port)
            tornado.ioloop.IOLoop.instance().start()

             

if __name__ == '__main__':
    try:
        console = sys.argv[-1]
        if console != '1':
            console =0
    except:
        console = 0 
    init_logging(console)
    main()
    
