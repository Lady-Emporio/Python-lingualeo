from PyQt5 import Qt
import sys
import sqlite3
import random
def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

def getMaxId(cursor):
    order = "SELECT MAX(ID) FROM MainTable"
    cursor.execute(order)
    max_id = cursor.fetchone()["MAX(ID)"]
    if max_id == None or max_id <= COUNT_WORDS:
        print(max_id, "max_id very small")
        raise ValueError
    return max_id



COUNT_WORDS=4 #use 4 words

def getCountWords():
    conn=sqlite3.connect("lingualeo.db")
    conn.row_factory = dict_factory
    cursor=conn.cursor()

    MAX_ID=getMaxId(cursor)

    select_ids=[]
    list_block_ids=[]
    n=[*range(1,MAX_ID+1)] #id start 1. Not 0. range start 0.
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
    return select_words


###########eng to ru #######################
class Button(Qt.QPushButton):
    def __init__(self,text,nomber):
        super().__init__()
        self.setText(str(text))
        self.nomber=nomber
        self.audio=self.ru_to_translate=None
        if self.nomber=="refresh":
            self.clicked.connect(self.refresh)
        elif self.nomber!="NoClick":
            self.clicked.connect(self.vasa)
        self.col = Qt.QColor(123, 123, 123)
        self.col.setRed(254)
        self.setStyleSheet("Button{ background-color: %s }" % self.col.name())
    def image(self,img):
        p = Qt.QPixmap(img)
        self.setIcon(Qt.QIcon(p))
        self.setIconSize(Qt.QSize(150, 100))
    def vasa(self):
        sender = self.sender()
        if self.audio!=None:
            player.setMedia(Qt.QMediaContent(Qt.QUrl.fromLocalFile(self.audio)))
            player.play()
        if sender.text()==self.ru_to_translate:
            self.setStyleSheet("*{ background-color: green }")
        else:
            self.setStyleSheet("*{ background-color: red }")
    def refresh(self):
        #pass
        global ex
        n=getCountWords()
        #print(ex,n)
        ex.run(n)



class Example(Qt.QWidget):
    def __init__(self):
        super().__init__()
        self.vbox=Qt.QGridLayout()


    def run(self,select_words):
        translate = random.choice(select_words)
        eng_to_translate = translate["eng"]
        ru_to_translate = translate["ru"]
        self.setWindowTitle("Lingualeo and Python(PyQt5)")
        #self.resize(480,600)
        #print(self.vbox.count())
        for i in reversed(range(self.vbox.count())):
            self.vbox.itemAt(i).widget().setParent(None)


        list_buttom=[Button("",i) for i in range(3*4)]
        self.vbox.addWidget(Button(eng_to_translate,"NoClick"), 0, 0,1,4)
        refresh_but=Button("refresh", "refresh")
        self.vbox.addWidget(refresh_but, 0, 5)

        row=1
        col=0
        for i in list_buttom:
            i.ru_to_translate=ru_to_translate
            self.vbox.addWidget(i,row,col)
            col = col if row != 3 else col + 1
            row=row+1 if row!=3 else 1


        list_buttom[0].image(select_words[0]["image"])
        list_buttom[1].setText("run audio")
        list_buttom[1].audio=select_words[0]["audio"]
        list_buttom[2].setText(select_words[0]["ru"])

        list_buttom[3].image(select_words[1]["image"])
        list_buttom[4].setText("run audio")
        list_buttom[4].audio = select_words[1]["audio"]
        list_buttom[5].setText(select_words[1]["ru"])

        list_buttom[6].image(select_words[2]["image"])
        list_buttom[7].setText("run audio")
        list_buttom[7].audio = select_words[2]["audio"]
        list_buttom[8].setText(select_words[2]["ru"])

        list_buttom[9].image(select_words[3]["image"])
        list_buttom[10].setText("run audio")
        list_buttom[10].audio = select_words[3]["audio"]
        list_buttom[11].setText(select_words[3]["ru"])

        self.setLayout(self.vbox)
        self.show()


app = Qt.QApplication(sys.argv)
player = Qt.QMediaPlayer()
ex = Example()
ex.run(getCountWords())
sys.exit(app.exec_())


