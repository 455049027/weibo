import  tornado.web
import  tornado.ioloop
from tornado.options import parse_command_line

import views

route = [
    (r'/',views.HomepageHandler),
    (r'/user/login', views.LoginHandler),
    (r'/user/info', views.UserinfoHanler),
    (r'/user/show', views.ShowHandler),
    (r'/user/post',views.Post_wbHandler),
    (r'/user/register',views.RegisterHandler),
    (r'/comment/commit',views.CommentCommitHandler),
    (r'/comment/reply',views.ReplyCommentHandler)
]

web_app = tornado.web.Application(
    route,
    template_path='./template',
    static_path='./statics'
)

web_app.listen(9001,'0.0.0.0')
tornado.ioloop.IOLoop.current().start()