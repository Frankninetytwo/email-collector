'''
This will be left incomplete for now as the entire project
just served the purpose to warm up with python and
web interaction.
'''


class Output:
    def __init__(self, urls, emails):
        self.fPath = 'output.txt'
        self.urls = urls
        self.emails = emails


    def writeToFile(self):
        fWriter = open(self.fPath)
        #
        # ...
        #

    def writeToTerminal(self):
        print('''........''')
