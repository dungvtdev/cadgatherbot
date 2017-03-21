class ResourceGatherBot(object):

    def __init__(self, name, caller, callback):
        self.name = name
        self.caller = caller
        self.callback = callback

    def work(self):
        result = self.caller()
        callback(result)


class BotsDispatch(object):

    def __init__(self):
        super(BotsDispatch, self).__init__()

        self.bots = []
        self.interval = 1000

    def register_bot(self, bot):
        is_contain = next(
            (True for inbot in self.bots if inbot.name == bot.name), False)
        if(not is_contain):
            self.bots.append(bot)

    def unregister_bot(self, bot_name):
        index = next((i for i, inbot in enumerate(
            self.bots) if inbot.name == bot_name), -1)
        if(index >= 0):
            self.bots.pop(index)

    def options(self, **kargv):
        if("interval" in kargv):
            self.interval = kargv["interval"]

    def run(self):
        pass
