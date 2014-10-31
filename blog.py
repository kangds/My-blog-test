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

    

if __name__ == '__main__':
    print ('systerm started ...')
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
