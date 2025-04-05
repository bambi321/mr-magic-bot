from packages.apiManagers.magicConfigAPI import magicGetShowLogMessages

class MagicLoggerManager:

    def __init__(self):
        self.__showLogMessages = magicGetShowLogMessages()

        if not self.__showLogMessages:
            print("You have turned off logged messages.  Please don't break me :)")

    def log(self, message):
        if self.__showLogMessages:
            print(message)