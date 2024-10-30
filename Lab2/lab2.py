#!/usr/bin/env python3
alphabeth = 'abcdefghijklmnopqrstuvwxyz, '

def createList (x):
    if x > 0:
        return list(range(0,x+1))
    elif x < 0:
        return list(range(x,0+1))
    else:
        return [0]

print (createList(-10))

def moveLetter(letter,key):
    letterIndex = alphabeth.find(letter)
    newLetterIndex = (letterIndex+key) % len(alphabeth)
    return alphabeth[newLetterIndex]

def encryptMessage(message, key):
    encryptedMessage = ""
    for i in message:
        encryptedMessage+=moveLetter(i,key)
    return encryptedMessage

message = input('What is the message?\n')
key = input("enter your key\n")
encryptedMes = encryptMessage(message,int(key))
print(encryptedMes)
print("")



# ----
# hackerman part

def decrypt(message):
    for i in range(len(alphabeth)):
        print(encryptMessage(message,i))

decrypt(encryptedMes)

# -- vigenere
#
def encryptMessageVigenere(message, keyList):
    encryptedMessage = ""
    position = 0
    for i in message:
        encryptedMessage+=moveLetter(i,keyList[position])
        position = position % len(keyList)
    return encryptedMessage


def getListFromWord(word):
    listOfIndexes = []
    for i in word:
        listOfIndexes.append(alphabeth.find(i))
    return listOfIndexes


mess1 = input("message:\n")
key = input("key:\n")

response = encryptMessageVigenere(mess1,getListFromWord(key))
print(response)

def decryptVigenere(cypher, keyList):
    decryptedMessage = ""
    position = 0
    for i in cypher:
        decryptedMessage+=moveLetter(i,-keyList[position])
        position = position % len(keyList)
    return decryptedMessage

print(decryptVigenere(response,getListFromWord(key)))
