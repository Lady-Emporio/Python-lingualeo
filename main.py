from PyQt5 import Qt
import sys
import sqlite3
import random
def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

#var n== next# use in range 4 linear. not global
COUNT_WORDS=4 #use 4 words

conn=sqlite3.connect("lingualeo.db")
conn.row_factory = dict_factory
cursor=conn.cursor()


# #Если ? то не нужны ковычки иначе кавычки (ENG='bend')
# eng_input=[input("eng word=:"),]
# order="SELECT ru,image,audio FROM MainTable WHERE ENG=?"
# cursor.execute(order,eng_input)
# print(cursor.fetchall())


# #выбираем слова которые начинаются с b
# order="SELECT * FROM MainTable WHERE ENG LIKE 'b%'"
# cursor.execute(order)
# print(cursor.fetchall())

# eng_input="0"
# while eng_input!="999":
#     eng_input=[input("999==exit,id word=:"),]
#     order="SELECT ru,image,audio FROM MainTable WHERE id=?"
#     cursor.execute(order,eng_input)
#     print(cursor.fetchall())



order="SELECT MAX(ID) FROM MainTable"
cursor.execute(order)
max_id=cursor.fetchone()["MAX(ID)"]
if max_id==None or max_id <=COUNT_WORDS:
    print(max_id,"max_id very small")
    raise ValueError
select_ids=[]
list_block_ids=[]
n=[*range(1,max_id+1)] #id start 1. Not 0. range start 0.
while len(select_ids)!=COUNT_WORDS:
    choice_id=random.choice(n)
    if choice_id not in list_block_ids:
        list_block_ids.append(choice_id)
        select_ids.append(choice_id)


select_words=[]
for i in select_ids:
    i=str(i)
    order="SELECT eng,ru,audio,image FROM MainTable WHERE id=?"
    cursor.execute(order,(i,))
    n1=cursor.fetchone()
    n2={
      "eng":n1["eng"],
      "ru":n1["ru"],
      "audio":n1["audio"],
      "image":n1["image"],
        }
    select_words.append(n2)
conn.close()
###Работа с базой на этом этапе закончена.
print(select_words)

###########eng to ru #######################
translate=random.choice(select_words)
eng_to_translate=translate["eng"]
ru_to_translate=translate["ru"]




class Button(Qt.QPushButton):
    def __init__(self,text,nomber):
        super().__init__()
        self.setText(str(text))
        self.nomber=nomber
        self.audio=None
        if self.nomber!="NoClick":
            self.clicked.connect(self.vasa)

        self.col = Qt.QColor(123, 123, 123)
        self.col.setRed(254)
        self.setStyleSheet("Button{ background-color: %s }" %
            self.col.name())
    def image(self,img):
        p = Qt.QPixmap(img)
        self.setIcon(Qt.QIcon(p))
        self.setIconSize(Qt.QSize(150, 100))



    def vasa(self):
        sender = self.sender()
        if self.audio!=None:
            player.setMedia(Qt.QMediaContent(Qt.QUrl.fromLocalFile(self.audio)))
            player.play()

        if sender.text()==ru_to_translate:
            self.setStyleSheet("*{ background-color: green }")
        else:
            self.setStyleSheet("*{ background-color: red }")

class Example(Qt.QWidget):
    def __init__(self):
        super().__init__()
        self.run()
    def run(self):
        self.setWindowTitle("Lingualeo and Python(PyQt5)")
        self.resize(480,600)
        vbox = Qt.QGridLayout()
        list_buttom=[Button("",i) for i in range(3*4)]

        vbox.addWidget(Button(eng_to_translate,"NoClick"), 0, 0,1,4)
        row=1
        col=0
        for i in list_buttom:
            vbox.addWidget(i,row,col)
            col = col if row != 3 else col + 1
            row=row+1 if row!=3 else 1


        row_3=[0,3,6,9]
        #p=Qt.QPixmap(select_words[0]["image"])
        #list_buttom[0].setIcon(Qt.QIcon(p))

        #list_buttom[0].setText(select_words[0]["image"])
        list_buttom[0].image(select_words[0]["image"])
        list_buttom[1].setText("run audio")
        list_buttom[1].audio=select_words[0]["audio"]
        list_buttom[2].setText(select_words[0]["ru"])

        #list_buttom[3].setText(select_words[1]["image"])
        list_buttom[3].image(select_words[1]["image"])
        list_buttom[4].setText("run audio")
        list_buttom[4].audio = select_words[1]["audio"]
        list_buttom[5].setText(select_words[1]["ru"])

        #list_buttom[6].setText(select_words[2]["image"])
        list_buttom[6].image(select_words[2]["image"])
        list_buttom[7].setText("run audio")
        list_buttom[7].audio = select_words[2]["audio"]
        list_buttom[8].setText(select_words[2]["ru"])

        #list_buttom[9].setText(select_words[3]["image"])
        list_buttom[9].image(select_words[3]["image"])
        list_buttom[10].setText("run audio")
        list_buttom[10].audio = select_words[3]["audio"]
        list_buttom[11].setText(select_words[3]["ru"])

        self.setLayout(vbox)
        self.show()


app = Qt.QApplication(sys.argv)
player = Qt.QMediaPlayer()
ex = Example()
sys.exit(app.exec_())


