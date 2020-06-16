from urllib import request
from urllib.error import HTTPError
from urllib.error import URLError
import re
import socket
import time
from output import Output

'''
TODO
- output class
- calling the output class from EmailCollector
- enable usage from terminal/cmd
- implement depth parameter to prevent infinite redirecting
- parameter that defines if the program is allowed to leave the start website
  (for now it does that by default)
- allow more than one thread to work on the collection of emails
''' 

class EmailCollector:
    def __init__(self, startUrl, countEmailsNeeded):
        # all urls that were investigated
        self.urls = []
        self.urls.append(startUrl.lower())
        # all emails that were found in the above urls
        self.emails = set()
        self.countEmailsNeeded = countEmailsNeeded


    # returns an empty string in case of failure
    def getHtmlTextFromUrl(self, url):
        htmlText = ""
        try:
            htmlText = request.urlopen(url, timeout = 3).read()
        except HTTPError as error:
            if error.code == 451:
                # can't read it due to legal reasons
                return ""
            elif error.code == 404:
                # page not found
                return ""
            elif error.code == 308:
                # permanent redirect
                return ""
            else:
                #raise

                # got tired of all the various http errors that may occur...
                return ""
        except URLError:
            # url not valid
            return ""
        except socket.timeout:
            return ""

        return htmlText


    def extractEmailsFromHtmlText(self, htmlText):
        foundEmails = re.findall(
            # might want to add to regex at the beginning of the string:
            # (?!\S*\.(?:jpg|png|gif|bmp)(?:[\s\n\r]|$))
            re.compile(br'[A-Z0-9._%+-]+@[A-Z0-9.-]{3,65}\.[A-Z]{2,4}', re.IGNORECASE), htmlText)
        for i in range(0, foundEmails.__len__()):
            # convert from byte to char
            foundEmails[i] = foundEmails[i].decode('utf-8')
            # make all emails be lowercase
            foundEmails[i] = foundEmails[i].lower()
        return foundEmails


    def extractUrlsFromHtmlText(self, htmlText):
        # alternative regex:
        #(?i)\b((?:https?:(?:/{1,3}|[a-z0-9%])|[a-z0-9.\-]+[.](?:com|net|org|edu|gov|mil|aero|asia|biz|cat|coop|info|int|jobs|mobi|museum|name|post|pro|tel|travel|xxx|ac|ad|ae|af|ag|ai|al|am|an|ao|aq|ar|as|at|au|aw|ax|az|ba|bb|bd|be|bf|bg|bh|bi|bj|bm|bn|bo|br|bs|bt|bv|bw|by|bz|ca|cc|cd|cf|cg|ch|ci|ck|cl|cm|cn|co|cr|cs|cu|cv|cx|cy|cz|dd|de|dj|dk|dm|do|dz|ec|ee|eg|eh|er|es|et|eu|fi|fj|fk|fm|fo|fr|ga|gb|gd|ge|gf|gg|gh|gi|gl|gm|gn|gp|gq|gr|gs|gt|gu|gw|gy|hk|hm|hn|hr|ht|hu|id|ie|il|im|in|io|iq|ir|is|it|je|jm|jo|jp|ke|kg|kh|ki|km|kn|kp|kr|kw|ky|kz|la|lb|lc|li|lk|lr|ls|lt|lu|lv|ly|ma|mc|md|me|mg|mh|mk|ml|mm|mn|mo|mp|mq|mr|ms|mt|mu|mv|mw|mx|my|mz|na|nc|ne|nf|ng|ni|nl|no|np|nr|nu|nz|om|pa|pe|pf|pg|ph|pk|pl|pm|pn|pr|ps|pt|pw|py|qa|re|ro|rs|ru|rw|sa|sb|sc|sd|se|sg|sh|si|sj|Ja|sk|sl|sm|sn|so|sr|ss|st|su|sv|sx|sy|sz|tc|td|tf|tg|th|tj|tk|tl|tm|tn|to|tp|tr|tt|tv|tw|tz|ua|ug|uk|us|uy|uz|va|vc|ve|vg|vi|vn|vu|wf|ws|ye|yt|yu|za|zm|zw)/)(?:[^\s()<>{}\[\]]+|\([^\s()]*?\([^\s()]+\)[^\s()]*?\)|\([^\s]+?\))+(?:\([^\s()]*?\([^\s()]+\)[^\s()]*?\)|\([^\s]+?\)|[^\s`!()\[\]{};:'".,<>?«»“”‘’])|(?:(?<!@)[a-z0-9]+(?:[.\-][a-z0-9]+)*[.](?:com|net|org|edu|gov|mil|aero|asia|biz|cat|coop|info|int|jobs|mobi|museum|name|post|pro|tel|travel|xxx|ac|ad|ae|af|ag|ai|al|am|an|ao|aq|ar|as|at|au|aw|ax|az|ba|bb|bd|be|bf|bg|bh|bi|bj|bm|bn|bo|br|bs|bt|bv|bw|by|bz|ca|cc|cd|cf|cg|ch|ci|ck|cl|cm|cn|co|cr|cs|cu|cv|cx|cy|cz|dd|de|dj|dk|dm|do|dz|ec|ee|eg|eh|er|es|et|eu|fi|fj|fk|fm|fo|fr|ga|gb|gd|ge|gf|gg|gh|gi|gl|gm|gn|gp|gq|gr|gs|gt|gu|gw|gy|hk|hm|hn|hr|ht|hu|id|ie|il|im|in|io|iq|ir|is|it|je|jm|jo|jp|ke|kg|kh|ki|km|kn|kp|kr|kw|ky|kz|la|lb|lc|li|lk|lr|ls|lt|lu|lv|ly|ma|mc|md|me|mg|mh|mk|ml|mm|mn|mo|mp|mq|mr|ms|mt|mu|mv|mw|mx|my|mz|na|nc|ne|nf|ng|ni|nl|no|np|nr|nu|nz|om|pa|pe|pf|pg|ph|pk|pl|pm|pn|pr|ps|pt|pw|py|qa|re|ro|rs|ru|rw|sa|sb|sc|sd|se|sg|sh|si|sj|Ja|sk|sl|sm|sn|so|sr|ss|st|su|sv|sx|sy|sz|tc|td|tf|tg|th|tj|tk|tl|tm|tn|to|tp|tr|tt|tv|tw|tz|ua|ug|uk|us|uy|uz|va|vc|ve|vg|vi|vn|vu|wf|ws|ye|yt|yu|za|zm|zw)\b/?(?!@)))
        foundUrls = re.findall(br'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', htmlText)
        for i in range(0, foundUrls.__len__()):
            foundUrls[i] = foundUrls[i].decode('utf-8')
        return foundUrls


    def log(self):
        output = Output(self.urls, self.emails)
        output.writeToTerminal()
        output.writeToFile()


    # returns the time spent collecting in seconds
    def collect(self):
        startTime = time.time()
        i = 0
        while i < self.urls.__len__():
            htmlText = self.getHtmlTextFromUrl(self.urls[i])

            if htmlText == "":
                i += 1
                continue

            self.emails.update(self.extractEmailsFromHtmlText(htmlText))

            if(self.emails.__len__() >= self.countEmailsNeeded):
                return time.time() - startTime

            '''
            TODO
            There's still a max depth parameter missing here as
            some website might cause an infinite loop!
            '''
            foundUrls = set(self.extractUrlsFromHtmlText(htmlText))

            for val in foundUrls:
                if val not in self.urls:
                    self.urls.append(val)
            
            i += 1

        return time.time() - startTime


    # call .collect() first
    def getEmails(self):
        return self.emails


    # call .collect() first
    def getUrls(self):
        return self.urls


#
# parameters that need to be set first:
#
countEmailsNeeded = 3
startUrl = 'https://stackoverflow.com'

emailCollector = EmailCollector(startUrl, countEmailsNeeded)
secondsSpentCollecting = emailCollector.collect()
emails = emailCollector.getEmails()
print("following emails ({}) were found:".format(emails.__len__()))
for email in emails:
    print(email)
print("\ncollected within {} seconds from {} distinct urls".format(
    round(secondsSpentCollecting, 2),
    emailCollector.getUrls().__len__())
)
