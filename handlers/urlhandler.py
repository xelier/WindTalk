from application.comment.handler import commentHandler
from application.user.handler import userHandler
from application.article.handler import articleHandler

url_handlers = [
    (r"/", userHandler.WelcomeHandler),
    (r"/register", userHandler.RegisterHandler),
    (r"/login", userHandler.LoginHandler),
    (r"/modifyUser", userHandler.ModifyUserHandler),
    (r"/modifyPwd", userHandler.ModifyPwdHandler),
    (r"/getUserInfo", userHandler.GetUserInfoHandler),
    (r"/logout", userHandler.UserExitHandler),

    (r"/addArticle", articleHandler.AddArticleHandler),
    (r"/deleteArticle", articleHandler.DeleteArticleHandler),
    (r"/modifyArticle", articleHandler.ModifyArticleHandler),
    (r"/queryArticleList", articleHandler.QueryArticleListHandler),
    (r"/queryArticleInfo", articleHandler.QueryArticleInfoHandler),

    (r"/addComment", commentHandler.AddCommentHandler),
    (r"/deleteComment", commentHandler.DeleteCommentHandler),
    (r"/queryCommentList", commentHandler.QueryCommentListHandler)
]
