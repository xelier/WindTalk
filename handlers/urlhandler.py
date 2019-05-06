from application.comment.handler import commentHandler
from application.user.handler import userHandler
from application.article.handler import articleHandler

url_handlers = [
    (r"/", userHandler.WelcomeHandler),
    (r"/rmt/register", userHandler.RegisterHandler),
    (r"/rmt/login", userHandler.LoginHandler),
    (r"/rmt/modifyUser", userHandler.ModifyUserHandler),
    (r"/rmt/modifyPwd", userHandler.ModifyPwdHandler),
    (r"/rmt/getUserInfo", userHandler.GetUserInfoHandler),
    (r"/rmt/logout", userHandler.UserExitHandler),

    (r"/rmt/addArticle", articleHandler.AddArticleHandler),
    (r"/rmt/deleteArticle", articleHandler.DeleteArticleHandler),
    (r"/rmt/modifyArticle", articleHandler.ModifyArticleHandler),
    (r"/rmt/queryArticleList", articleHandler.QueryArticleListHandler),
    (r"/rmt/queryArticleInfo", articleHandler.QueryArticleInfoHandler),

    (r"/rmt/addComment", commentHandler.AddCommentHandler),
    (r"/rmt/deleteComment", commentHandler.DeleteCommentHandler),
    (r"/rmt/queryCommentList", commentHandler.QueryCommentListHandler)
]
