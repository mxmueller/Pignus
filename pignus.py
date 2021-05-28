import random
import string
import eel
import eel.browsers

eel.init('web')

@eel.expose
def connection(param):
    print('Response:', True, param)
    return 'Response', True, param

@eel.expose
class Password:
    def __init__(self):
        self.length = None
        self.Caps = None

    @eel.expose
    def getPassword(self):
        result = self.setPasswordFromChoice()
        return result

    @eel.expose
    def setPasswordFromChoice(self):
        if self.Caps:
            letters = string.ascii_letters
        else:
            letters = string.ascii_lowercase

        return ''.join(random.choice(letters) for i in range(self.length))

@eel.expose
class Salting:
    def __init__(self):
        self.input = None
        self.specialCharsLength = None  # int
        self.enforceMaxLength = None  # bool

    def getSaltedPassword(self):
        if self.enforceMaxLength:
            return self._setSaltingToStringEnforced()
        else:
            return self._setSaltingToString()

    def _setSaltingToStringEnforced(self):
        c = 0
        l = list(self.input)
        while c < round((len(self.input) / 100) * self.specialCharsLength):
            r = self.getRandomPositions()
            for i in range(len(self.input)):
                if i == r:
                    l[i] = self.getSalt()
                    sl = "".join(l)
                    self.input = sl
            c += 1
        return self.input

    def _setSaltingToString(self):
        s = self.input
        c = 0
        while c < round((len(self.input) / 100) * self.specialCharsLength):
            i = self.getRandomPositions()
            a = s[:i] + self.getSalt() + s[i:]
            s = a
            self.input = s
            c += 1
        return self.input

    def getRandomPositions(self):
        return (random.randint(0, len(self.input))) - 1

    def getSalt(self):
        return random.choice(string.punctuation)

@eel.expose
def saltPasswordButtonPress(jsPasswordString, jsRange, jsEnforceLength):
    userSaltingPreferences = Salting()
    userSaltingPreferences.input = jsPasswordString
    userSaltingPreferences.specialCharsLength = int(jsRange)
    userSaltingPreferences.enforceMaxLength = jsEnforceLength
    return userSaltingPreferences.getSaltedPassword()

@eel.expose
def passwordButtonPress(jsLength, jsCaps):
    userPasswordPreferences = Password()
    userPasswordPreferences.length = int(jsLength)
    userPasswordPreferences.Caps = jsCaps
    return userPasswordPreferences.getPassword()

   # if checkbuttonAutoSaltWidgetVar.get():
     #   saltPasswordButtonPress()

eel.start('index.html', mode='chrome' , size=(900, 800), port=8000  ,host='localhost',disable_cache=True, close_callback='close_callback', )