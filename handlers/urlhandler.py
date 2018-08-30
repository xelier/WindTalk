from handlers import userhandler

urlhandlers = [
    (r"/", userhandler.IndexHandler)
]