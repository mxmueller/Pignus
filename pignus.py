@@ -0,0 +1,147 @@
import random
import string
import tkinter

# User UI
from tkinter import LEFT, END
from ttkthemes import themed_tk as tk


class Password:
    def __init__(self):
        self.length = None
        self.Caps = None

    def getPassword(self):
        result = self.setPasswordFromChoice()
        return result

    def setPasswordFromChoice(self):
        if self.Caps:
            letters = string.ascii_letters
        else:
            letters = string.ascii_lowercase

        return ''.join(random.choice(letters) for i in range(self.length))


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


# gui
pignusGui = tk.ThemedTk()
pignusGui.get_themes()
pignusGui.set_theme("blue")
pignusGui.title("Pignus - Advanced password generator")
pignusGui.geometry("400x500")

scaleLengthLabel = tkinter.Label(pignusGui, text='Set password length:')
scaleLengthLabel.pack(padx=15, pady=4, fill='both')

scaleLengthWidget = tkinter.Scale(pignusGui, from_=0, to=50, orient=tkinter.HORIZONTAL)
scaleLengthWidget.set(10)
scaleLengthWidget.pack(padx=15, pady=4, fill='both')

scaleSaltLengthLabel = tkinter.Label(pignusGui, text='Percentage of letters to be salted:')
scaleSaltLengthLabel.pack(padx=15, pady=4, fill='both')

scaleSaltLengthWidget = tkinter.Scale(pignusGui, from_=0, to=100, orient=tkinter.HORIZONTAL)
scaleSaltLengthWidget.set(35)
scaleSaltLengthWidget.pack(padx=15, pady=4, fill='both')


def saltPasswordButtonPress():
    userSaltingPreferences = Salting()
    userSaltingPreferences.input = passwordEntry.get()
    userSaltingPreferences.specialCharsLength = scaleSaltLengthWidget.get()
    userSaltingPreferences.enforceMaxLength = checkbuttonEnforceLengthWidgetVar.get()
    saltEntry.delete(0, END)
    saltEntry.insert(0, userSaltingPreferences.getSaltedPassword())


def passwordButtonPress():
    userPasswordPreferences = Password()
    userPasswordPreferences.length = scaleLengthWidget.get()
    userPasswordPreferences.Caps = checkbuttonCapsWidgetVar.get()
    passwordEntry.delete(0, END)
    passwordEntry.insert(0, userPasswordPreferences.getPassword())

    if checkbuttonAutoSaltWidgetVar.get():
        saltPasswordButtonPress()


checkbuttonCapsWidgetVar = tkinter.IntVar()
checkbuttonCapsWidget = tkinter.Checkbutton(pignusGui, variable=checkbuttonCapsWidgetVar,
                                            text="Use upper and lower case letters")
checkbuttonCapsWidget.select()
checkbuttonCapsWidget.pack(padx=15, pady=4, fill='both')

checkbuttonAutoSaltWidgetVar = tkinter.IntVar()
checkbuttonAutoSaltWidget = tkinter.Checkbutton(pignusGui, variable=checkbuttonAutoSaltWidgetVar,
                                                text="Automatically salt generated text password")
checkbuttonAutoSaltWidget.select()
checkbuttonAutoSaltWidget.pack(padx=15, pady=4, fill='both')

checkbuttonEnforceLengthWidgetVar = tkinter.IntVar()
checkbuttonEnforceLengthWidget = tkinter.Checkbutton(pignusGui, variable=checkbuttonEnforceLengthWidgetVar,
                                                text="Keep password length when salting")
checkbuttonEnforceLengthWidget.select()
checkbuttonEnforceLengthWidget.pack(padx=15, pady=4, fill='both')

passwordEntry = tkinter.Entry(pignusGui)
passwordButton = tkinter.Button(pignusGui, text="Start entire process", command=passwordButtonPress)

saltEntry = tkinter.Entry(pignusGui)
saltButton = tkinter.Button(pignusGui, text="Just Salt", command=saltPasswordButtonPress)

passwordLabel = tkinter.Label(pignusGui, text='Text password:')
saltLabel = tkinter.Label(pignusGui, text='Salted password:')

passwordLabel.pack(padx=15, pady=4, fill='both')
passwordEntry.pack(padx=15, pady=4, fill='both')
saltLabel.pack(padx=15, pady=4, fill='both')
saltEntry.pack(padx=15, pady=4, fill='both')
passwordButton.pack(padx=15, pady=3, fill='both')
saltButton.pack(padx=15, pady=6, fill='both')

pignusGui.mainloop()
