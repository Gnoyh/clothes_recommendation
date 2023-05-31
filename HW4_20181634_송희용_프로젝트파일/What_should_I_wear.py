import tkinter as tk
from tkinter import ttk

import sqlite3
from sqlite3 import Error

import datetime

import random


def connetion():
    try:
        connection = sqlite3.connect("Clothes.db", isolation_level = "")
        return connection
    except Error:
        print(Error)


def readData():
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM clothes_list")

    data = cursor.fetchall()
    list = []

    for i in data:
        list.append(i)

    return list


def insertData(data):
    cursor = connection.cursor()

    cursor.execute("INSERT INTO clothes_list (id, name, type, detailtype, color, latestdate) VALUES (?, ?, ?, ?, ?, ?)", data)

    connection.commit()

    tree.insert("", "end", text="-", values=(data[0], data[1], data[5]))
    tree.yview_moveto(1.0)

    text.insert(tk.END, "\n옷 추가 서비스를 완료했습니다!\n")
    text.see(tk.END)


def deleteData(id):
    cursor = connection.cursor()

    cursor.execute("DELETE FROM clothes_list WHERE id = '%s'" %id)

    connection.commit()

    text.insert(tk.END, "\n============================================================\n"
                        "\n옷 삭제 서비스를 완료했습니다!\n")
    text.see(tk.END)


def updateData(latestdate, id):
    cursor = connection.cursor()

    cursor.execute("UPDATE clothes_list SET latestdate = '%s' WHERE id = '%s'" %(latestdate, id))

    connection.commit()

    tree.delete(*tree.get_children())
    tree.yview_moveto(1.0)

    showTree()


def showTree():
    list = readData()

    for i in range(len(list)):
        tree.insert("", "end", text="-", values=(list[i][0], list[i][1], list[i][5]))

    tree.yview_moveto(1.0)

def recommendClothes():
    clothesTempList = [
        [(-100, 5), (-10, 5), (10, 20), (10, 20), (5, 15), (5, 15), (10, 20), (10, 20), (10, 20), (10, 20)],
        [(-10, 25), (-15, 25), (-100, 25), (-15, 25), (-100, 25), (-100, 25)],
        [(25, 100), (25, 100), (25, 30), (25, 100), (25, 100), (30, 100)],
        [(-100, 100), (-100, 100), (-100, 100), (-100, 100), (21, 100)]]

    colorMatchList = [[1, 1, 1, 1, 1, 1, 1, 1],
                      [1, 1, 1, 1, 1, 1, 0, 1],
                      [1, 1, 1, 1, 1, 1, 1, 0],
                      [1, 1, 1, 1, 1, 1, 1, 1],
                      [1, 1, 1, 1, 1, 1, 1, 0],
                      [1, 1, 1, 1, 1, 1, 1, 0],
                      [1, 0, 1, 1, 1, 1, 0, 0],
                      [1, 1, 0, 1, 0, 0, 0, 0]]

    randomCheckList = []
    randomClothesList = []

    def recommendClothesStart():
        text.insert(tk.END, "\n============================================================\n"
                            "\n옷 추천 서비스를 시작합니다!\n")
        text.see(tk.END)

        inputTemp()


    def inputTemp():
        clearButtons()

        text.insert(tk.END, "\n오늘의 기온을 입력해주세요!\n")
        text.see(tk.END)

        tempEntry = tk.Entry(window)
        tempEntry.grid(row=3, column=1, columnspan=2)

        deleteButtonList.append(tempEntry)

        def clickButton():
            temp = tempEntry.get()

            text.insert(tk.END, "\n>> 오늘의 기온은 %s°C 입니다!\n"
                                "\n추천할 옷을 선택중입니다...\n" % temp)
            text.see(tk.END)

            clearButtons()

            if int(temp) <= 20:
                findOuter(temp)
            else:
                findTops(temp)

        enterButton = tk.Button(window, text="입력", command=clickButton)
        enterButton.grid(row=3, column=4)

        deleteButtonList.append(enterButton)


    def findOuter(temp):
        list = readData()

        randomClothesList.clear()
        randomCheckList.clear()

        for i in range(len(list)):
            if list[i][2] == 0:
                if list[i][5] != "-":
                    strptime = datetime.datetime.strptime(list[i][5], "%Y-%m-%d")
                    date = strptime.date()

                    delta = datetime.date.today() - date

                    if int(delta.days) >= 14 and clothesTempList[list[i][2]][list[i][3]][0] <= \
                            int(temp) <= clothesTempList[list[i][2]][list[i][3]][1]:
                        randomCheckList.append((list[i][1], list[i][4], list[i][0]))
                else:
                    if clothesTempList[list[i][2]][list[i][3]][0] <= \
                            int(temp) <= clothesTempList[list[i][2]][list[i][3]][1]:
                        randomCheckList.append((list[i][1], list[i][4], list[i][0]))

        if len(randomCheckList) != 0:
            randomClothes = random.choice(randomCheckList)

            randomClothesList.append((randomClothes[0], randomClothes[2]))

            findTops(temp, randomClothes[1])
        else:
            text.insert(tk.END, "\n추천할 수 있는 외투가 없습니다!\n")
            text.see(tk.END)


    def findTops(temp, color=None):
        list = readData()

        if color is None:
            randomClothesList.clear()
            randomCheckList.clear()

            for i in range(len(list)):
                if list[i][2] == 1 or list[i][2] == 2:
                    if list[i][5] != "-":
                        strptime = datetime.datetime.strptime(list[i][5], "%Y-%m-%d")
                        date = strptime.date()

                        delta = datetime.date.today() - date

                        if int(delta.days) >= 14 and clothesTempList[list[i][2]][list[i][3]][0] <= \
                                int(temp) <= clothesTempList[list[i][2]][list[i][3]][1]:
                            randomCheckList.append((list[i][1], list[i][4], list[i][0]))
                    else:
                        if clothesTempList[list[i][2]][list[i][3]][0] <= \
                                int(temp) <= clothesTempList[list[i][2]][list[i][3]][1]:
                            randomCheckList.append((list[i][1], list[i][4], list[i][0]))

            if len(randomCheckList) != 0:
                randomClothes = random.choice(randomCheckList)

                randomClothesList.append((randomClothes[0], randomClothes[2]))

                findBottoms(temp, randomClothes[1])
            else:
                text.insert(tk.END, "\n추천할 수 있는 상의가 없습니다!\n")
                text.see(tk.END)
        else:
            randomCheckList.clear()

            for i in range(len(list)):
                if list[i][2] == 1:
                    if list[i][5] != "-":
                        strptime = datetime.datetime.strptime(list[i][5], "%Y-%m-%d")
                        date = strptime.date()

                        delta = datetime.date.today() - date

                        if int(delta.days) >= 14 and clothesTempList[list[i][2]][list[i][3]][0] <= \
                                int(temp) <= clothesTempList[list[i][2]][list[i][3]][1] and \
                                colorMatchList[color][list[i][4]] == 1:
                            randomCheckList.append((list[i][1], list[i][4], list[i][0]))
                    else:
                        if clothesTempList[list[i][2]][list[i][3]][0] <= \
                                int(temp) <= clothesTempList[list[i][2]][list[i][3]][1] and \
                                colorMatchList[color][list[i][4]] == 1:
                            randomCheckList.append((list[i][1], list[i][4], list[i][0]))

            if len(randomCheckList) != 0:
                randomClothes = random.choice(randomCheckList)

                randomClothesList.append((randomClothes[0], randomClothes[2]))

                findBottoms(temp, color, randomClothes[1])
            else:
                text.insert(tk.END, "\n추천할 수 있는 상의가 없습니다!\n")
                text.see(tk.END)


    def findBottoms(temp, color1, color2=None):
        list = readData()

        if color2 is None:
            randomCheckList.clear()

            for i in range(len(list)):
                if list[i][2] == 3:
                    if list[i][5] != "-":
                        strptime = datetime.datetime.strptime(list[i][5], "%Y-%m-%d")
                        date = strptime.date()

                        delta = datetime.date.today() - date

                        if int(delta.days) >= 14 and clothesTempList[list[i][2]][list[i][3]][0] <= \
                                int(temp) <= clothesTempList[list[i][2]][list[i][3]][1] and \
                                colorMatchList[color1][list[i][4]] == 1:
                            randomCheckList.append((list[i][1], list[i][4], list[i][0]))
                    else:
                        if clothesTempList[list[i][2]][list[i][3]][0] <= \
                                int(temp) <= clothesTempList[list[i][2]][list[i][3]][1] and \
                                colorMatchList[color1][list[i][4]] == 1:
                            randomCheckList.append((list[i][1], list[i][4], list[i][0]))
        else:
            randomCheckList.clear()

            for i in range(len(list)):
                if list[i][2] == 3:
                    if list[i][5] != "-":
                        strptime = datetime.datetime.strptime(list[i][5], "%Y-%m-%d")
                        date = strptime.date()

                        delta = datetime.date.today() - date

                        if int(delta.days) >= 14 and clothesTempList[list[i][2]][list[i][3]][0] <= \
                                int(temp) <= clothesTempList[list[i][2]][list[i][3]][1] and \
                                colorMatchList[color1][list[i][4]] == 1 and \
                                colorMatchList[color2][list[i][4]] == 1:
                            randomCheckList.append((list[i][1], list[i][4], list[i][0]))
                    else:
                        if clothesTempList[list[i][2]][list[i][3]][0] <= \
                                int(temp) <= clothesTempList[list[i][2]][list[i][3]][1] and \
                                colorMatchList[color1][list[i][4]] == 1 and \
                                colorMatchList[color2][list[i][4]] == 1:
                            randomCheckList.append((list[i][1], list[i][4], list[i][0]))

        if len(randomCheckList) != 0:
            randomClothes = random.choice(randomCheckList)

            randomClothesList.append((randomClothes[0], randomClothes[2]))

            selectClothes(temp)
        else:
            text.insert(tk.END, "\n추천할 수 있는 바지가 없습니다!\n")
            text.see(tk.END)


    def selectClothes(temp):
        text.insert(tk.END, "\n>> ")

        for i in range(len(randomClothesList) - 1):
            text.insert(tk.END, "%s, " % randomClothesList[i][0])

        text.insert(tk.END, "%s\n\n이 옷으로 선택하겠습니까?\n" % randomClothesList[-1][0])
        text.see(tk.END)

        yesButton = tk.Button(window, text="네", command=recommendClothesEnd)
        yesButton.grid(row=3, column=1)

        deleteButtonList.append(yesButton)

        if int(temp) <= 20:
            noButton = tk.Button(window, text="아니오", command=lambda temp=temp: findOuter(temp))
            noButton.grid(row=3, column=3)
        else:
            noButton = tk.Button(window, text="아니오", command=lambda temp=temp: findTops(temp))
            noButton.grid(row=3, column=3)

        deleteButtonList.append(noButton)


    def recommendClothesEnd():
        clearButtons()

        text.insert(tk.END, "\n>> 오늘 입을 옷을 결정했습니다!\n"
                            "\n옷 추천 서비스를 완료했습니다!\n")
        text.see(tk.END)

        for clothes in randomClothesList:
            updateData(datetime.date.today(), clothes[1])


    recommendClothesStart()


def inputClothes():
    clothesTypeList = {"외투": 0, "긴소매": 1, "반소매 / 민소매": 2, "바지": 3}

    clothesDetailTypeList = [{"패딩": 0, "겨울 코트": 1, "환절기 코트": 2, "블레이저": 3, "후드집업": 4,
                              "가죽": 5, "재킷": 6, "바람막이": 7, "조끼": 8, "가디건": 9},
                             {"긴소매 셔츠": 0, "긴소매 티셔츠": 1, "긴소매 니트": 2, "긴소매 카라": 3, "긴소매 맨투맨": 4, "긴소매 후드": 5},
                             {"반소매 셔츠": 0, "반소매 티셔츠": 1, "반소매 니트": 2, "반소매 카라": 3, "반소매 기능성": 4, "민소매": 5},
                             {"데님 바지": 0, "코튼 바지": 1, "슬랙스 바지": 2, "트레이닝 바지": 3, "반바지": 4}]

    clothesColorList = {"흰색": 0, "회색": 1, "검정색": 2, "네이비": 3, "올리브": 4,
                        "브라운 / 베이지": 5, "웜톤 원색": 6, "쿨톤 원색": 7}

    dataList = [0, "", 0, 0, 0, ""]

    def inputClothesStart():
        text.insert(tk.END, "\n============================================================\n"
                            "\n옷 추가 서비스를 시작합니다!\n")
        text.see(tk.END)

        selectClothesType()


    def selectClothesType():
        r = 3
        c = 0

        clearButtons()

        text.insert(tk.END, "\n추가할 옷의 종류를 선택해주세요!\n")
        text.see(tk.END)

        for key in clothesTypeList:
            clothesTypeButton = tk.Button(window, text=key, command=lambda key=key: selectClothesDetailType(key))

            clothesTypeButton.grid(row=r, column=c)
            c += 1

            deleteButtonList.append(clothesTypeButton)


    def selectClothesDetailType(key):
        r = 3
        c = 0

        clearButtons()

        text.insert(tk.END, "\n>> %s을(를) 선택했습니다!\n"
                            "\n추가할 옷의 세부 종류를 선택해주세요!\n" % key)
        text.see(tk.END)

        dataList[2] = clothesTypeList[key]

        for key in clothesDetailTypeList[clothesTypeList[key]]:
            clothesDetailTypeButton = tk.Button(window, text=key, command=lambda key=key: selectClothesColor(key))

            if c < 5:
                clothesDetailTypeButton.grid(row=r, column=c)
                c += 1
            else:
                r += 1
                c = 0

                clothesDetailTypeButton.grid(row=r, column=c)
                c += 1

            deleteButtonList.append(clothesDetailTypeButton)


    def selectClothesColor(key):
        r = 3
        c = 0

        clearButtons()

        text.insert(tk.END, "\n>> %s을(를) 선택했습니다!\n"
                            "\n추가할 옷의 색상을 선택해주세요!\n" % key)
        text.see(tk.END)

        dataList[3] = clothesDetailTypeList[dataList[2]][key]

        for key in clothesColorList:
            clothesColorButton = tk.Button(window, text=key, command=lambda key=key: inputClothesEnd(key))

            if c < 5:
                clothesColorButton.grid(row=r, column=c)
                c += 1
            else:
                r += 1
                c = 0

                clothesColorButton.grid(row=r, column=c)
                c += 1

            deleteButtonList.append(clothesColorButton)


    def inputClothesEnd(key):
        clearButtons()

        text.insert(tk.END, "\n>> %s을(를) 선택했습니다!\n" % key)
        text.see(tk.END)

        dataList[4] = clothesColorList[key]

        newId = dataList[2] * 100 + dataList[3] * 10 + dataList[4]
        newName = "%s %s" % (
        findKey(clothesColorList, dataList[4]), findKey(clothesDetailTypeList[dataList[2]], dataList[3]))

        insertData((newId, newName, dataList[2], dataList[3], dataList[4], "-"))


    inputClothesStart()


def deleteClothes():
    focusedItem = tree.focus()

    if focusedItem:
        id = tree.item(focusedItem)["values"][0]

        deleteData(id)
    else:
        text.insert(tk.END, "\n삭제할 옷을 선택해주세요!\n")
        text.see(tk.END)

    tree.delete(*tree.get_children())
    tree.yview_moveto(1.0)

    showTree()


def clearButtons():
    for button in deleteButtonList:
        button.destroy()

    deleteButtonList.clear()


def findKey(dic, value):
    for key, val in dic.items():
        if val == value:
            return key

    return None


connection = connetion()
window = tk.Tk()

deleteButtonList = []


tree = ttk.Treeview(window, columns=("ID", "Name", "LatestDate"))
tree.grid(row=0, column=0, columnspan=5)

tree.column("ID", width=0, stretch=tk.NO)
tree.heading("ID", text="")

tree.column("Name", anchor="center")
tree.heading("Name", text="Name", anchor="center")

tree.column("LatestDate", anchor="center")
tree.heading("LatestDate", text="LatestDate", anchor="center")


recommendButton = tk.Button(window, text="옷 추천", command=recommendClothes)
recommendButton.grid(row=1, column=1)

inputButton = tk.Button(window, text="옷 추가", command=inputClothes)
inputButton.grid(row=1, column=2)

deleteButton = tk.Button(window, text="옷 삭제", command=deleteClothes)
deleteButton.grid(row=1, column=3)


text = tk.Text(window)
text.insert(tk.END, "안녕하세요!\n")
text.grid(row=2, column=0, columnspan=5)


showTree()

window.mainloop()