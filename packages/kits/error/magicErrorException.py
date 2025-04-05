class MagicErrorException(Exception):

    def __init__(self):
        print('---------------------------------')
        print('Encountered Catastrophic Error, Terminating Application')
        print('---------------------------------')


