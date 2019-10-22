import datetime
from math import ceil
from hashlib import sha256

import tornado.web
from sqlalchemy.orm.exc import NoResultFound
from model import User,Weibo,Comment,Session

class RegisterHandler(tornado.web.RequestHandler):
    @staticmethod
    def gen_password(password):
        bytes_code = password.encode('utf8')
        hash_code = sha256(bytes_code)
        return hash_code.hexdigest()

    def get(self):
        self.render('register.html')

    def post(self):
        nickname = self.get_argument('nickname')
        password = self.get_argument('password')
        gender =  self.get_argument('gender')
        city = self.get_argument('city')
        bio = self.get_argument('bio')

        safe_password = self.gen_password(password)

        session = Session()

        user = User(nickname=nickname,password=safe_password,gender=gender,city=city,bio=bio)

        session.add(user)
        session.commit()

        self.redirect('/user/login')
class LoginHandler(tornado.web.RequestHandler):

    def get(self):
        self.render('login.html',warning='')

    def post(self):
        nickname = self.get_argument('nickname')
        password = self.get_argument('password')

        safe_password = RegisterHandler.gen_password(password)

        session = Session()
        q_user = session.query(User)
        try:
            user = q_user.filter_by(nickname=nickname).one()
        except NoResultFound:
            self.render('login.html',warning='用户名输入错误！')

        if user.password == safe_password:
            self.set_cookie('user_id',str(user.id))
            self.redirect('/user/info')
        else:
            self.render('login.html',warning='密码输入错误！')

class UserinfoHanler(tornado.web.RequestHandler):
    def get(self):
        try:
            user_id = int(self.get_cookie('user_id'))
        except TypeError:
            self.redirect('/user/login')

        session = Session()
        q_user = session.query(User)
        user = q_user.filter_by(id=user_id).one()
        self.render('info.html',user=user)

class Post_wbHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('post_wb.html')

    def post(self):

        user_id = int(self.get_cookie('user_id'))

        content = self.get_argument('content')

        session = Session()
        weibo = Weibo(user_id=user_id,content=content,created=datetime.datetime.now())
        session.add(weibo)
        session.commit()

        self.redirect('/user/show?weibo_id=%s' %weibo.id)

class ShowHandler(tornado.web.RequestHandler):
    def get(self):
        weibo_id = int(self.get_cookie('user_id'))

        session = Session()
        weibo = session.query(Weibo).get(weibo_id)
        author = session.query(User).get(weibo.user_id)

        all_comments = session.query(Comment).filter_by(wb_id=weibo.id).order_by(Comment.created.desc())

        comment_auther_id_list = {cmt.user_id for cmt in all_comments}
        comment_auther_list = session.query(User).filter(User.id.in_(comment_auther_id_list))
        comment_authors = {u.id:u for u in comment_auther_list}

        self.render('show.html',weibo=weibo,user=author,all_comments=all_comments,comment_authors=comment_authors)

class HomepageHandler(tornado.web.RequestHandler):
    def get(self):
            page = int(self.get_argument('page',1))
            per_page_size = 10

            session = Session()
            q_weibo = session.query(Weibo)
            all_pages =  ceil(q_weibo.count() / per_page_size)

            wb_list = q_weibo.filter().order_by(Weibo.created.desc()).limit(per_page_size).offset((page-1) * per_page_size)

            q_user = session.query(User)
            user_id_list = (wb.user_id for wb in wb_list)
            users = {u.id:u for u in q_user.filter(User.id.in_(user_id_list))}

            self.render('home.html',wb_list=wb_list,users=users,all_pages=all_pages,cur_page=page)


class CommentCommitHandler(tornado.web.RequestHandler):
    def post(self):
        content = self.get_argument('content')
        wb_id = self.get_argument('wb_id')
        user_id = self.get_cookie('user_id')

        session = Session()
        comment = Comment(user_id=user_id,wb_id=wb_id,content=content,created=datetime.datetime.now())

        session.add(comment)
        session.commit()

        self.redirect('/user/show?weibo_id=%s' %wb_id)

class ReplyCommentHandler(tornado.web.RequestHandler):

    def get(self):
        cmt_id = int(self.get_argument('cmt_id'))

        session = Session()
        comment = session.query(Comment).get(cmt_id)
        user = session.query(User).get(comment.user_id)

        self.render('reply_comment.html',comment=comment,user=user)

    def post(self):
        user_id = self.get_cookie('user_id')
        wb_id = int(self.get_argument('wb_id'))
        cmt_id = int(self.get_argument('cmt_id'))
        content = self.get_argument('content')
        created = datetime.datetime.now()

        session = Session()
        comment = Comment(user_id=user_id,wb_id=wb_id,cmt_id=cmt_id,content=content,created=created,)
        session.add(comment)
        session.commit()

        self.redirect('/user/show?weibo_id=%s' %wb_id)
