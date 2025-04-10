import sys
import Kalender

from PyQt5 import  QtWidgets
from PyQt5.QtCore import QSize
from PyQt5.QtWidgets import QMainWindow, QLabel, QWidget, QPushButton, QGridLayout, QLineEdit,QMessageBox, QStackedWidget, QTabWidget
from datetime import  datetime, timedelta

#TODO Domains der bereiche zurück in Daten verwandeln, Tabelle erstellen
#TODO Today: schon getätigte Workloads hinzufügen
#TODO projekte Speichern/Laden können
#TODO button "addworktime to projekt" hinzufügen (zum verwalten der schon getätigten worktime)

class MyWindow(QMainWindow):
    """ Holds the main Window oft the application

    """

    def __init__(self):
        """initializes the core Widgets and layouts

        """
        super().__init__()

        self.setMinimumSize(QSize(350,300))
        self.setWindowTitle("Kalenderoptimierung")
        
        self.Tabs=QTabWidget()
        self.setCentralWidget(self.Tabs)

        #DailyTab definiton
        self.Today=QWidget()
        self.TabTodaygrid=QGridLayout()

        self.Today.setLayout(self.TabTodaygrid)
        self.DayStacked=QStackedWidget()
        self.TabTodaygrid.addWidget(self.DayStacked)

        #TimelineTab definition
        self.Timeline=QWidget()
        self.TabTimelinegrid=QGridLayout()

        self.Timeline.setLayout(self.TabTimelinegrid)
        self.TimeStacked=QStackedWidget()
        self.TabTimelinegrid.addWidget(self.TimeStacked)


        #ProjectManagerTab definition
        self.ProjectManager=QWidget()
        self.TabProjgrid=QGridLayout()

        self.ProjectManager.setLayout(self.TabProjgrid)
        self.ProjStacked=QStackedWidget()
        self.TabProjgrid.addWidget(self.ProjStacked)

        #AddTabs to TabWidget
        self.Tabs.addTab(self.Today,"Today")
        self.Tabs.addTab(self.Timeline, "Timeline")
        self.Tabs.addTab(self.ProjectManager,"Project Manager")
        
        

        self.update=False
        self.TimeWin()
        self.TodayWin()
        self.ProjectsWin(0)
        
    def TimeWin(self):
        """manages the layout of the episodes in the timewin window

        :return: -> None
        """
        # removes all widgets from TabTimelinegrid
        for i in reversed(range(self.TabTimelinegrid.count())): 
            self.TabTimelinegrid.itemAt(i).widget().setParent(None)


        label=QLabel("")
        self.TabTimelinegrid.addWidget(label,0,0)
        
        for i,item in enumerate(bereich.lst):
            
            text="%s \nbis \n%s" %(item.start().strftime("%d.%m.%Y"),item.end().strftime("%d.%m.%Y"))
            label=QLabel(text)
            self.TabTimelinegrid.addWidget(label,1,i)

            label=QLabel("")
            self.TabTimelinegrid.addWidget(label,2,i)
            
            for j in range(len(item.proj)):
                text="Projekt%d:\n %.2fh" %(item.proj[j].internalname,item.workloads[j])
                label=QLabel(text)
                self.TabTimelinegrid.addWidget(label,3+j,i)

    def EditWin(self,index,projIndex):
        """manages the layout and content of the project editing window

        :param index: int
            the index of current stacked widget
        :param projIndex: int
        :return: ->None
        """

        self.projIndex=projIndex

        Edit=QWidget()
        self.ProjStacked.insertWidget(index,Edit) 

        Editgrid=QGridLayout()
        Edit.setLayout(Editgrid)

        Label=QLabel("Edit Projekt")
        Editgrid.addWidget(Label,0,0)
      
        label=QLabel("\nAlter Beginn: %s\nNeues Startdatum" %store.liste[projIndex][0].strftime("%d.%m.%Y"))
        Editgrid.addWidget(label)

        self.TBStart = QLineEdit(self)
        self.TBStart.insert(str(store.liste[projIndex][0].strftime("%d.%m.%Y")))
        Editgrid.addWidget(self.TBStart)


        label=QLabel("\nAltes Ende: %s \nNeues Enddatum:" %store.liste[projIndex][1].strftime("%d.%m.%Y"))
        Editgrid.addWidget(label)

        self.TBEnd = QLineEdit(self)
        self.TBEnd.insert(str(store.liste[projIndex][1].strftime("%d.%m.%Y")))
        Editgrid.addWidget(self.TBEnd)


        label=QLabel("\nAltes Workload: %d\nNeues Workload:" %store.liste[projIndex][2])
        Editgrid.addWidget(label)

        self.TBWorkload = QLineEdit(self)
        self.TBWorkload.insert(str(store.liste[projIndex][2]))
        Editgrid.addWidget(self.TBWorkload)
            

        button=QPushButton("Apply to Project")
        button.clicked.connect(self.btn_apply_clicked)
        Editgrid.addWidget(button)

        button=QPushButton("Cancel")
        button.clicked.connect(self.btn_return_clicked)
        Editgrid.addWidget(button)  

    def NewWin(self):
        """ manages the window for new creation of projects

        :return: ->None
        """
        New=QWidget()
        self.ProjStacked.addWidget(New) 

        Newgrid=QGridLayout()
        New.setLayout(Newgrid)

        Label=QLabel("New")
        Newgrid.addWidget(Label,0,0)

        self.new=[]
      
        label=QLabel("start")
        Newgrid.addWidget(label)

        self.TBStart = QLineEdit(self)
        Newgrid.addWidget(self.TBStart)


        label=QLabel("ende")
        Newgrid.addWidget(label)

        self.TBEnd = QLineEdit(self)
        Newgrid.addWidget(self.TBEnd)


        label=QLabel("Workload")
        Newgrid.addWidget(label)

        self.TBWorkload = QLineEdit(self)
        Newgrid.addWidget(self.TBWorkload)
            

        button=QPushButton("Create new Project")
        button.clicked.connect(self.btn_create_clicked)
        Newgrid.addWidget(button)

        button=QPushButton("Cancel")
        button.clicked.connect(self.btn_return_clicked)
        Newgrid.addWidget(button)  

    def ProjectsWin(self, index):
        """manages the content of the project list depiction

        :param index: int
            index of current widget in stacked Widget
        :return: -> None
        """
        Projects=QWidget()
        self.ProjStacked.insertWidget(index,Projects)

        Projectsgrid=QGridLayout()
        Projects.setLayout(Projectsgrid)
        
        collumn=0
        for i in range(len(store.liste)):
                
            label=QLabel("Start: %s \nEnde: %s \nWorkload:%d" %(store.liste[i][0].strftime("%d.%m.%Y"),store.liste[i][1].strftime("%d.%m.%Y"),store.liste[i][2]))
            Projectsgrid.addWidget(label,1,collumn)
            button=QPushButton("löschen")
            button.page=i
            button.clicked.connect(self.btn_delete_clicked)
            Projectsgrid.addWidget(button,2,collumn)
            button=QPushButton("bearbeiten")
            button.page=i
            button.clicked.connect(self.btn_edit_clicked)
            Projectsgrid.addWidget(button,3,collumn)
            collumn+=1
        
        
        button=QPushButton("New Project")
        button.clicked.connect(self.btn_new_clicked)
        
        Projectsgrid.addWidget(button,1,collumn)


        if self.update:
            button=QPushButton("Update")
            button.setStyleSheet("background-color: red")
            button.clicked.connect(self.btn_update_clicked)

            Projectsgrid.addWidget(button,2,collumn)


    def TodayWin(self):
        """manages the content of the today-tab

        :return: ->None
        """

        # remove all current widget
        for i in reversed(range(self.TabTodaygrid.count())): 
            self.TabTodaygrid.itemAt(i).widget().setParent(None)
        
        today=datetime.today()

        text="heute: %s" %today.strftime("%d.%m.%Y")
        label=QLabel(text)
        self.TabTodaygrid.addWidget(label,0,0)

        
        if today<bereich.firstdate or today>bereich.lst[-1].end():
            text="nichts zu tun"
        else:
            for i in range(len(bereich.lst)):
                if today>bereich.lst[i].start() and today<bereich.lst[i].end():
                    break
            
            

        for j in range(len(bereich.lst[i].proj)):
            text=str(bereich.lst[i].proj[j])+"\nTodays Workload: %.2f" %bereich.lst[i].workloads[j]
            label=QLabel(text)
            self.TabTodaygrid.addWidget(label,1,j)


    def btn_update_clicked(self):
        """updates all windows on_click

        :return:
        """
        self.update=False
        store.update()
        self.TimeWin()
        self.TodayWin()
        self.btn_return_clicked()

    def btn_create_clicked(self):
        """checks new project for invalid input and updates data_store

        :return: ->None
        """
        
        if self.TBStart.text().strip()=="":
            QMessageBox.about(self,"Fehler","Geben Sie ihren Projektstart ein.\nFormat:TT.MM.JJJJ")
            return
        elif self.TBEnd.text().strip()=="":
            QMessageBox.about(self,"Fehler","Geben Sie ihr Projektende ein.\nFormat:TT.MM.JJJJ")
            return
        elif self.TBWorkload.text().strip()=="":
            QMessageBox.about(self,"Fehler","Geben Sie ihren Projektworkload in Stunden ein.")
            return
        
        elif float(self.TBWorkload.text())<1:
            QMessageBox.about(self,"Fehler","Workload muss mindestens eine Stunde betragen")
            return
        
        try:
            datetime.strptime(self.TBStart.text(),"%d.%m.%Y")
        except ValueError:
            QMessageBox.about(self,"Fehler","Bitte geben Sie ein reales Datum als Startdatum ein.\nFormat: TT.MM.JJJ")
            return

        try:
            datetime.strptime(self.TBEnd.text(),"%d.%m.%Y")
        except ValueError:
            QMessageBox.about(self,"Fehler","Bitte geben Sie ein reales Datum als Enddatum ein.\nFormat: TT.MM.JJJ")
            return
        
        if datetime.strptime(self.TBStart.text(),"%d.%m.%Y")>datetime.strptime(self.TBEnd.text(),"%d.%m.%Y"):
            QMessageBox.about(self,"Fehler","Projektende muss nach dem Projektstart liegen")
            return
        
        store.liste.append([datetime.strptime(self.TBStart.text(),"%d.%m.%Y"),datetime.strptime(self.TBEnd.text(),"%d.%m.%Y"),float(self.TBWorkload.text())])
        self.update=True
        
        self.btn_return_clicked()
        
    def btn_apply_clicked(self):
        """ checks input for invalid data and updates store.liste with new projectdata

        :return: ->None
        """
        if self.TBStart.text().strip()=="":
            QMessageBox.about(self,"Fehler","Geben Sie ihren Projektstart ein.\nFormat: TT.MM.JJJJ")
            return
        elif self.TBEnd.text().strip()=="":
            QMessageBox.about(self,"Fehler","Geben Sie ihr Projektende ein.\nFormat: TT.MM.JJJJ")
            return
        elif self.TBWorkload.text().strip()=="":
            QMessageBox.about(self,"Fehler","Geben Sie ihren Projektworkload in Stunden ein.")
            return
        
        elif float(self.TBWorkload.text())<1:
            QMessageBox.about(self,"Fehler","Workload muss mindestens eine Stunde betragen")
            return
        
        try:
            datetime.strptime(self.TBStart.text(),"%d.%m.%Y")
        except ValueError:
            QMessageBox.about(self,"Fehler","Bitte geben Sie ein reales Datum als Startdatum ein.\nFormat: TT.MM.JJJ")
            return
        
        try:
            datetime.strptime(self.TBEnd.text(),"%d.%m.%Y")
        except ValueError:
            QMessageBox.about(self,"Fehler","Bitte geben Sie ein reales Datum als Enddatum ein.\nFormat: TT.MM.JJJ")
            return
        
        if datetime.strptime(self.TBStart.text(),"%d.%m.%Y")>datetime.strptime(self.TBEnd.text(),"%d.%m.%Y"):
            QMessageBox.about(self,"Fehler","Projektende muss nach dem Projektstart liegen")
            return
        store.liste[self.projIndex]=[datetime.strptime(self.TBStart.text(),"%d.%m.%Y"),datetime.strptime(self.TBEnd.text(),"%d.%m.%Y"),float(self.TBWorkload.text())]

        self.update=True
        self.btn_return_clicked()

    def btn_return_clicked(self):
        """ standard exit function for all edits

        :return: ->None
        """
        self.ProjectsWin(0)
        self.ProjStacked.setCurrentIndex(0)

    def btn_delete_clicked(self):
        """deletes project if messagebox is confirmed

        :return: ->None
        """
        msg=QMessageBox()
        msg.setText("Wollen sie das Projekt wirklich löschen?")
        msg.setWindowTitle("Löschen")
        msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        returnValue = msg.exec()
        if returnValue == QMessageBox.Ok:
            
            button = self.sender()
            store.liste.remove(store.liste[button.page])
            self.update=True
            index=self.ProjStacked.currentIndex()
            self.ProjectsWin(index+1)
            self.ProjStacked.setCurrentIndex(index+1)

    def btn_edit_clicked(self):
        """ opens the editing window for selected project

        :return: ->None
        """
        button = self.sender()
        self.EditWin(0,button.page)
        self.ProjStacked.setCurrentIndex(0)
        
    def btn_new_clicked(self):
        """ opens the window for a new project

        :return: ->None
        """
        self.NewWin()
        self.ProjStacked.setCurrentIndex(self.ProjStacked.count()-1)

def listRework(liste):
    """converts the datetime objects to project datasets each containing the start, the duration and the total workload

    :param liste: nested list
    :return: ->list, [relative start, duration in days, total workload in hours]
    """
    Newlist=[]
    firstDate=[x[0] for x in liste]
    firstDate=sorted(firstDate)[0]
    for i in range(len(liste)):
        Newlist.append([])
        Newlist[i]=[(liste[i][0]-firstDate).days,(liste[i][1]-liste[i][0]).days,liste[i][2]]

    bereich.firstdate=firstDate
    return Newlist

class store():
    """ manages the core Prohect data
    :var liste: list
        contains the core-project-data [start, end, workload] for each project

    :var updated: list
        contains all optimized sector workloads
    """

    liste=[]
    updated=[]
    

    def __init__(self):
        """reads the data.txt file, loads it into store.liste and initializes the optimisation calculation

        """

        #reads the data.txt file if existing
        try:
            fr=open('data.txt', 'r')
            raw = fr.read()
            list2=raw.split(";")
            list2=[x.split(",") for x in list2]
            liste=[]
            
            
            for i in range(len(list2)):
                liste.append([])
                for j in range(len(list2[i])):
                    if j==2:
                        liste[i].append(int(list2[i][j]))
                    else:
                        liste[i].append(datetime.strptime(list2[i][j],"%d.%m.%Y")) 
        except:
            liste=[]


        store.liste=liste

        # initializes domain calculation based on store.liste
        store.update()

    @classmethod
    def update(store):
        store.updated= Kalender.main(listRework(store.liste))
        bereich.initialisation()

class bereich():
    """provides operations on each sectors data

    :var lst: list of all initialized sectors
    :var firstdate: contains the first date of all projectmanagement
    """
    lst=[]
    firstdate=0

    def __init__(self,domain,proj,wl):
        """initializes sectors

        :param domain: domain object
        :param proj: list of projects
        :param wl: list of int
        """
        self.dom=domain
        self.proj=[proj]
        self.workloads=[wl]

        bereich.lst.append(self)



    def end(self):
        """returns the enddate of the sector"""
        add=timedelta(days=self.dom.b)
        enddate=bereich.firstdate+add
        return enddate

    def start(self):
        """returns the startdate of the sector"""
        add=timedelta(days=self.dom.a)
        enddate=bereich.firstdate+add
        return enddate

    def __repr__(self):
        """defines console representation"""
        text=""
        for j in range(len(self.proj)):
            str2=("\nProjekt"+str(self.proj[j].internalname)+ ":\n%.2fh\n"%self.workloads[j])
            text+=str2
        return text

    @classmethod
    def initialisation(cls):
        """ converts the project information to sector information and initializes new sectors

        :return: ->None
        """
        # appends project and corresponding workload to sector or creates a new sector if the sector misses in bereich.lst
        bereich.lst = []
        for project in store.updated:
            for j in range(len(project.dom2)):
                for k in bereich.lst:
                    if not project.dom2[j] != k.dom: #TODO invert to gatekeeper
                        k.proj.append(project)
                        k.workloads.append(project.domwl[j])
                        break
                    else:
                        continue
                else:
                    bereich(project.dom2[j], project, project.domwl[j])

        #sorts the bereich.lst by startdate and secondly enddate
        a = bereich.lst
        a1 = [a.pop(0)]
        for j in range(len(a)):
            for i in range(len(a1) + 1):
                if i >= len(a1):
                    break
                if a[j].dom.a > a1[i].dom.a:
                    continue
                elif a[j].dom.a == a1[i].dom.a and a[j].dom.b > a1[i].dom.b:
                    continue
                else:
                    break
            a1.insert(i, a[j])
        bereich.lst = a1


#Main Programm

liste=store()

App = QtWidgets.QApplication(sys.argv)
win = MyWindow()
win.show()
App.exec_()

#saves the changed project data
fw=open("data.txt","w")
str=""
for i in range(len(store.liste)):
    for j in store.liste[i]:
        if type(j)==datetime:
            str+=j.strftime("%d.%m.%Y")+","
        else:
            str+="%d"%j
    if i!=len(store.liste)-1:
        str+=";"


fw.write(str)
fw.close()
sys.exit()