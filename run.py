from normalization import Normalizer
import  nltk
from nltk import bigrams
#================= Loading dataset and normalize it  ===========================
Normalizer = Normalizer()

def loading_dataSet():
    file = open("res/dataset.txt", "r")
    data = file.read()
    file.close()
    docs = data.split("\n")
    types = []
    train = []
    for d in docs:
        d = d.split()
        if len(d)!=0:
            types.append(d[0])
    print('dataset Count = '+str(len(types)))
    normalized_corpus = Normalizer.normalize_corpus(docs)
    normalized_corpus.remove('')
    counter = 0
    for x in normalized_corpus :
        train.append((x,types[counter]))
        counter = counter +1
    return train

normalized_dataset = loading_dataSet()
#===============================================================================
#========================= Starting Trainning dataset ==========================
selected_features = None
def add_lexical_features(fdist, feature_vector, text):
    feature_vector["len"] = len(text)
    text_nl = nltk.Text(text)
    for word, freq in fdist.items():
        fname = "UNI_" + word
        if selected_features == None or fname in selected_features:
            feature_vector[fname] = 1

def features(review_words):
    feature_vector = {}
    uni_dist = nltk.FreqDist(review_words)
    my_bigrams = list(bigrams(review_words))
    bi_dist = nltk.FreqDist(my_bigrams)
    add_lexical_features(uni_dist,feature_vector, review_words)
    return feature_vector

featuresets = [(features(words), label) for (words, label) in normalized_dataset ]
classifier = nltk.NaiveBayesClassifier.train(featuresets)


#==========================================================================================
#========================================== GUI funcs  ===================================

def classify_btn_clicked():
    def setClassification(type):
        if type == '1':
            classi_out.setPlainText('culture')
        elif type == '2':
            classi_out.setPlainText('sport')
        elif type == '3':
            classi_out.setPlainText('economy')
        elif type == '4':
            classi_out.setPlainText('international')
        elif type == '5':
            classi_out.setPlainText('local')
        elif type == '6':
            classi_out.setPlainText('religion')
    tester_doc = file_.toPlainText().strip()
    normalized_tester_doc = Normalizer.normalize_corpus([tester_doc])
    featuresets_test = [features(words) for words in normalized_tester_doc ]
    predicted_label = classifier.classify_many(featuresets_test)
    setClassification(predicted_label[0])

current_cb = 'Sports'
def combobox_changed ():
    global current_cb
    current_cb = cb.currentText()

def append_btn_clicked():
     filee = open('res/dataset.txt','a')
     text = file_2.toPlainText().strip()
     if text!= '' :
         if current_cb == 'Sports':
             filee.write('2 '+text+'\n')
         elif current_cb == 'culture':
             filee.write('1 '+text+'\n')
         elif current_cb == 'economy':
               filee.write('3 '+text+'\n')
         elif current_cb == 'international':
             filee.write('4 '+file_2.toPlainText().strip()+'\n')
         elif current_cb == 'local':
             filee.write('5 '+file_2.toPlainText().strip()+'\n')
         elif current_cb == 'religion':
             filee.write('6 '+file_2.toPlainText().strip()+'\n')
     else :
         showMessageBox('warning','please type your Document')

     file_2.setPlainText('')
     filee.close()
#================================= Design ================================================
#------------------------------------------------------------------------------------------
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import sys
from PyQt5.QtWidgets import *
app= QApplication(sys.argv)
window = QWidget()
window.resize(700,700)
window.setWindowTitle("Documents Classification")
pixmap = QPixmap('res/bk.jpg').scaled(700,700)
lab = QLabel(window)
lab.setPixmap(pixmap)

Label = QLabel(window,text='<h2>Input Your Document To be Classified :</h2>')
Label.resize(440,30)
Label.move(150,100)


file_ = QTextEdit(window)
file_.resize(450,150)
file_.move(140,150)



bu1 = QPushButton('classify',window)
bu1.resize(80,50)
bu1.move(600,190)
bu1.clicked.connect(classify_btn_clicked)

classi_out = QTextEdit(window)
classi_out.move(250,310)
classi_out.resize(200 ,40)

Label2 = QLabel(window,text='<h2>Append Trainning file with new dataset :</h2>')
Label2.resize(440,30)
Label2.move(150,400)

file_2 = QTextEdit(window)
file_2.resize(450,150)
file_2.move(140,440)

cb = QComboBox(window)
cb.addItem("Sports")
cb.addItem("culture")
cb.addItem("economy")
cb.addItem("international")
cb.addItem("religion")
cb.addItem("local")
cb.resize(80,50)
cb.move(600,450)
cb.currentTextChanged.connect(combobox_changed)

bu2 = QPushButton('Append',window)
bu2.resize(80,50)
bu2.move(250,600)
bu2.clicked.connect(append_btn_clicked)

def showMessageBox(title,message):
        msgBox = QMessageBox()
        msgBox.setIcon(QMessageBox.Warning)
        msgBox.setWindowTitle(title)
        msgBox.setText(message)
        msgBox.setStandardButtons(QMessageBox.Ok)
        msgBox.exec_()
window.show()
app.exec_()
