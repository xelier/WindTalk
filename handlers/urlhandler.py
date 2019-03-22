from application.user.handler import userhandler

urlhandlers = [
    (r"/", userhandler.WelcomeHandler),
    (r"/register", userhandler.RegisterHandler),
    (r"/login", userhandler.LoginHandler),
    (r"/modifyUser", userhandler.ModifyUser),
    (r"/modifyPwd", userhandler.ModifyPwd),
    (r"/getUserInfo", userhandler.GetUserInfo),
    (r"/logout", userhandler.UserExit)
]
