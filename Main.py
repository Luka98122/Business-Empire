import pygame
import random
import time
import datetime
import json


window = pygame.display.set_mode((513, 975))
pygame.display.set_caption("Business Empire")


class Globals:
    balance = 0
    businessList = []


def doIncomes():
    for shop in Globals.businessList:
        shop.update()


class Auto:
    def __init__(self, ime, cena, zarada, kilaza) -> None:
        self.ime = ime
        self.cena = cena
        self.zarada = zarada
        self.kilaza = kilaza


class TaxiCompany:
    def __init__(self, ime, mesta) -> None:
        self.ime = ime
        self.mesta = mesta
        self.pocetnoVreme = int(time.time())
        self.listaAutomobila = []

    def update(self):
        if (int(time.time()) - self.pocetnoVreme) % 2 == 0:
            for auto in self.listaAutomobila:
                Globals.balance += auto.zarada

    def addAuto(self, auto):
        self.listaAutomobila.append(auto)


class InvisButton:
    def __init__(self, rect):
        self.rect = rect

    def update(self, tuple):
        x = tuple[0]
        y = tuple[1]

        if (
            x > self.rect.x
            and x < self.rect.x + self.rect.width
            and y > self.rect.y
            and y < self.rect.y + self.rect.height
        ):
            return True
        return False


class Shop:
    img = pygame.image.load("Textures\\BlankShop.jpg")
    img = pygame.transform.scale(img, (440, 133))

    def __init__(self, name, stage) -> None:
        self.lastPayment = int(time.time())
        if stage == 1:
            self.base = 1000
        if stage == 2:
            self.base = 2000
        if stage == 3:
            self.base = 3000
        self.name = name
        self.initTime = int(time.time())
        self.level = 0
        self.flag = 1

    def update(self):
        if (int(time.time()) - self.lastPayment) // 15 > 1:
            Globals.balance += (
                (self.base * (1 + self.level * 0.05) / 240)
                * (int(time.time()) - self.lastPayment)
                // 15
            )
            self.lastPayment = int(time.time())
        if (int(time.time()) - self.lastPayment) % 15 == 0:
            if self.flag == 0:
                Globals.balance += self.base * (1 + self.level * 0.05) / 240
                self.flag = 1
                self.lastPayment = int(time.time())
        else:
            self.flag = 0

    def draw(self, pos, window):
        window.blit(
            self.img,
            pygame.Rect(pos.x, pos.y, self.img.get_width(), self.img.get_height()),
        )
        font = pygame.font.Font(None, 33)
        incomeText = "${:.2f}".format(self.base * (1 + self.level * 0.05))
        text = font.render(incomeText, True, pygame.Color("Black"))
        text_rect = pygame.Rect(pos.x + 13, pos.y + 90, 300, 75)
        nameText = font.render(self.name, True, pygame.Color("Black"))
        name_rect = pygame.Rect(pos.x + 80, pos.y + 20, 300, 75)
        window.blit(nameText, name_rect)
        window.blit(text, text_rect)


class Factory:
    img = pygame.image.load("Textures\\BlankFactory.jpg")
    img = pygame.transform.scale(img, (440, 133))

    def __init__(self, name, stage) -> None:
        self.lastPayment = int(time.time())
        if stage == 1:
            self.base = 5000
        if stage == 2:
            self.base = 10000
        if stage == 3:
            self.base = 15000
        self.name = name
        self.initTime = int(time.time())
        self.level = 0
        self.flag = 1

    def update(self):
        if (int(time.time()) - self.lastPayment) // 15 > 1:
            Globals.balance += (
                (self.base * (1 + self.level * 0.05) / 240)
                * (int(time.time()) - self.lastPayment)
                // 15
            )
            self.lastPayment = int(time.time())
        if (int(time.time()) - self.lastPayment) % 15 == 0:
            if self.flag == 0:
                Globals.balance += self.base * (1 + self.level * 0.05) / 240
                self.flag = 1
                self.lastPayment = int(time.time())
        else:
            self.flag = 0

    def draw(self, pos, window):
        window.blit(
            self.img,
            pygame.Rect(pos.x, pos.y, self.img.get_width(), self.img.get_height()),
        )
        font = pygame.font.Font(None, 33)
        incomeText = "${:.2f}".format(self.base * (1 + self.level * 0.05))
        text = font.render(incomeText, True, pygame.Color("Black"))
        text_rect = pygame.Rect(pos.x + 13, pos.y + 90, 300, 75)
        nameText = font.render(self.name, True, pygame.Color("Black"))
        name_rect = pygame.Rect(pos.x + 80, pos.y + 20, 300, 75)
        window.blit(nameText, name_rect)
        window.blit(text, text_rect)


pygame.font.init()


def businessScreen(window):
    businessScreenImg = pygame.image.load("Textures\\BusinessScreen.jpg")
    clickerPageButton = InvisButton(pygame.Rect(210, 846, 94, 73))
    while True:
        doIncomes()
        window.blit(businessScreenImg, pygame.Rect(0, 0, 389, 799))
        totalIncome = 0
        for shop in Globals.businessList:
            totalIncome += shop.base * (1 + shop.level * 0.05)
        font = pygame.font.Font(None, 63)
        TotalIncomeText = "${:.2f}".format(float(totalIncome))
        text = font.render(TotalIncomeText, True, pygame.Color("Black"))
        window.blit(text, pygame.Rect(30, 147, 400, 90))
        events = pygame.event.get()
        if pygame.mouse.get_pressed()[0] == True:
            if clickerPageButton.update(pygame.mouse.get_pos()) == True:
                mainScreen(window)
        currentY = 324
        for shop in Globals.businessList:
            shop.draw(pygame.Vector2(40, currentY), window)
            currentY += 150
        pygame.display.flip()


def convertBusinessToDict(obj: Shop):
    resDict = {
        "name": obj.name,
        "level": obj.level,
        "base": obj.base,
        "lastPayment": obj.lastPayment,
        "type": str(type(obj)),
    }
    return resDict


def convertDictToObj(dict):
    type = dict["type"]
    if type == "<class '__main__.Factory'>":
        fact = Factory(dict["name"], None)
        fact.base = dict["base"]
        fact.lastPayment = dict["lastPayment"]
        return fact
    if type == "<class '__main__.Shop'>":
        shop = Shop(dict["name"], None)
        shop.base = dict["base"]
        shop.lastPayment = dict["lastPayment"]
        return shop


def mainScreen(window):
    clickerButton = InvisButton(pygame.Rect(0, 340, 512, 500))
    businessTabButton = InvisButton(pygame.Rect(111, 846, 89, 68))
    mainScreenImg = pygame.image.load("Textures\\Main.jpg")
    lastState = False
    while True:
        doIncomes()
        balance = Globals.balance
        window.blit(mainScreenImg, pygame.Rect(0, 0, 389, 799))
        events = pygame.event.get()

        for event in events:
            if event.type == pygame.QUIT:
                f = open("SaveData.json", "w")
                dictList = []
                for shop in Globals.businessList:
                    dictList.append(convertBusinessToDict(shop))
                myDict = {
                    "Balance": Globals.balance,
                    "BusinessList": dictList,
                }
                json_obj = json.dumps(myDict)
                f.write(json_obj)
                f.close()
                exit()
        if pygame.mouse.get_pressed()[0] == True:
            if (
                clickerButton.update(pygame.mouse.get_pos()) == True
                and lastState == False
            ):
                Globals.balance += 10
            if businessTabButton.update(pygame.mouse.get_pos()) == True:
                businessScreen(window)

        font = pygame.font.Font(None, 55)
        myStr = "${:.2f}".format(round(float(balance), 2))
        text = font.render(myStr, True, pygame.Color("White"))
        text_rect = pygame.Rect(40, 140, 300, 75)
        window.blit(text, text_rect)
        pygame.display.flip()
        lastState = pygame.mouse.get_pressed()[0]


try:
    f = open("SaveData.json", "r")
    print("read")
    contents = f.read()
    Globals.balance = json.loads(contents)
    Globals.balance = Globals.balance["Balance"]
    Globals.businessList = []
    for item in json.loads(contents)["BusinessList"]:
        Globals.businessList.append(convertDictToObj(item))
except Exception as e:
    print(f"Error {e}")
    pass
""""
myShop = Shop("Aroma", 2)
myShop2 = Shop("Maxi", 2)
myFactory = Factory("Pepsi", 2)
Globals.businessList.append(myShop2)
Globals.businessList.append(myShop)
Globals.businessList.append(myFactory)
"""

mojaKomp = TaxiCompany("Ceviz", 5)
print(mojaKomp.ime)
mercedes = Auto("Mercedes", 0, 50000, 504429)
mojaKomp.addAuto(mercedes)
Globals.businessList.append(mojaKomp)

mainScreen(window)
