from application.user.handler import userhandler

urlhandlers = [
    (r"/", userhandler.IndexHandler)
]