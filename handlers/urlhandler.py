from application.user.handler import userHandler

urlhandlers = [
    (r"/", userHandler.WelcomeHandler),
    (r"/register", userHandler.RegisterHandler),
    (r"/login", userHandler.LoginHandler),
    (r"/modifyUser", userHandler.ModifyUserHandler),
    (r"/modifyPwd", userHandler.ModifyPwdHandler),
    (r"/getUserInfo", userHandler.GetUserInfoHandler),
    (r"/logout", userHandler.UserExitHandler)
]
