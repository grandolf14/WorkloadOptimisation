from PyQt5.QtWidgets import  QPushButton

#region Klassen
class dom():
    """domain objects, defined by start end end point [int], provides different analyse and math operations for domains

    """


    def consecutive(self, other):
        """checks if two domains are consecutiv to eachother

        :param other: domain object
        :return: ->bool
        """
        if self.a==other.b or other.a==self.b:
            return True
        else:
            return False

    def __eq__(self,other):
        """calculates the intersection of two domains, if there is any

        :param other: domain object
        :return: -> domain object | False
        """
        if dom.a(self)<dom.b(other) and dom.a(other)<dom.b(self):
            Newdomain=sorted([dom.a(self),dom.a(other),dom.b(self),dom.b(other)])
            return dom(Newdomain[1],Newdomain[2])
        else:
            return False
        
    def __ne__(self,other):
        """ checks the domains for similarity

        :param other: domain object
        :return: -> bool
        """
        if self.a==other.a and self.b==other.b:
            return False
        else:
            return True 
   
    def __add__(self,other):
        """returns both domains if they are neither consecutive nor intersect or the new domain if they do

        :param other: domain object
        :return: ->list [domain object]
        """
        if self == other or dom.consecutive(self,other):
            if self.a < other.a:
                a1 = self.a
            else:
                a1 = other.a

            if self.b>other.b:
                b1 = self.b
            else:
                b1=other.b
            return [dom(a1,b1)]
        else:
            
            return [self, other]
            
    def __sub__(self,other):
        """deducts the other domain from self

        :param other: domain object
        :return: ->domain object
        """
        if self==other:
            if self.a<other.a and self.b>other.b:
                 return ([dom(self.a,other.a),dom(other.b,self.b)])
            elif self.a<other.a and self.b<=other.b:
                return ([dom(self.a,other.a)])
            elif self.a>=other.a and self.b>other.b:
                return ([dom(other.b,self.b)])
            elif self.a>other.a and self.b<other.b:
                return[]
        else:
            return [self]
    


    #Instanzmethoden
 
    def __init__(self,a,b):
        """initializes a new domain, the bigger value of the two being b and the smaller being a

        :param a: int
        :param b: int
        """
        if a>b:
            self.a=b
            self.b=a
        else:           
            self.a=a
            self.b=b
            
    def a(self):
        """ returns the start value of the domain

        :return: ->int
        """
        return self.a
    
    def b(self):
        """ returns the end value of the domain

        :return: ->int
        """
        return self.b
    
    def len(self):
        """ returns the length of the domain

        :return: ->int
        """
        if self is None:
            return 0
        else:
            return self.b-self.a

    def __repr__(self):
        """defines the console depiction for a domain object

        :return: ->str
        """
        return "(%d to %d)" %(self.a,self.b)


class Proj ():
    """manages the proj data

    :var lst: list
        contains all current project instances
    """
    lst=[] 

    @classmethod
    def Rlst(cls):
        """returns the list of all current projects"""
        return Proj.lst
        
    def __lt__(self,other):
        """checks if the other project was initialized after self

        :param other: domain object
        :return: bool
        """
        if self.internalname<other.internalname:
            return True
        else:
            return False

    def __init__(self, name, start=0,dauer=0,workload=0):
        """ initializes a new Proj and adds it to the list of all projects

        :param name: int
            internal name of project
        :param start: int
            relative startdate
        :param dauer:  int
            duration in days
        :param workload: int
            workload in hours
        """

        self.internalname=name
        self.DOM= dom(start, start+dauer)       #Ursprungsdomain    
        self.WL=workload                        #Ursprungsworkload 
        self.negwl= 0                           #verbrauchte workload
        self.dom= [self.DOM]                    #Arbeitsdomain 
        self.dom2=[]                            #finale bereiche
        self.domwl=[]                           #finale wl/bereich
        self.intersect=[]
        self.marker=True
        Proj.lst.append(self)                   #fügt bei Projektinitialisierung das Projekt der klassenliste hinzu 

    def DOM(self):
        """returns the initalized domain

        :return: domain object
        """
        return self.DOM
    
    def WL(self):
        """returns the initalized workload

        :return: ->int
        """
        return self.WL
    
    def len(self):
        """returns the total length of the current workload configuration

        :return: ->int
        """
        added=[]
        if len(self.dom2)!=0:
            for i in flatten(self.dom2):
                added.append(i.len())
        else:
            for i in flatten(self.dom):
                added.append(i.len())    
        return sum(added)
    
    def dailywl(self):
        """returns the current average workload or False if there is no current domain left for project

        :return: -> int
        """
        if self.len() >0:
            return self.WL/self.len()
        else:
            return False
    
    def __repr__(self):
        """returns the console appearance if Proj is printed

        :return: ->str
        """
        return "Proj"+str(self.internalname)
        return "\nName: Proj"+str(self.internalname)+"\nDaten:"+str(self.DOM)+"\nneue Daten:" +str(self.dom2)+"\nTagesworkload:"+ str([round(x,1) for x in self.domwl])+"\ndifferenz: "+str(self.WL)+" "+str(self.WL==self.negwl)+"\n"


class superbereich():
    """manages the parent sectors for each sector

    :var lst: list
        contains all current parent sectors

    :var name: int, private
        the name counter

    """
    lst=[]
    name=0

    def __init__(self,domain=0,projekte=0,children=0):
        """initializes the parent sector and if no childrens assigned creates a child for every object in domain

        :param domain: the domains inside the parent sector
        :param projekte: list of projects in the parent sector
        :param children: list of all children of the parent sector
        """

        self.internalname="superbereich "+str(superbereich.name)
        if children==0:
            self.children=[bereich(domain[x],projekte,self)for x in range(len(domain))]
        else:
            self.children=[children]

        superbereich.name+=1
        superbereich.lst.append(self)

  
    def mediumwl(self):
        """returns the average workload for parent sector"""
        if len(self.proj())==0 or len(self.DOM())==0:
            return 0
        else:                                 
            return sum(flatten([x.WL for x in self.PROJ()] ))/sum(flatten([x.len() for x in self.DOM()]))
        
    def DOM(self):
        """returns all startdomains of the children"""
        return flatten(listjoin([x.DOM() for x in self.children]))

    def dom(self):
        """returns all current domains of the children"""
        return flatten(listjoin([x.dom() for x in self.children]))
    
    def proj(self):
        """returns all unfinished children projects"""
        return list(set(flatten([x.proj() for x in self.children])))
    
    def PROJ(self):
        """returns all children projects"""
        return list(set(flatten([x.PROJ() for x in self.children])))

    def __repr__(self):
        """defines console apearance string"""
        return "\nBereiche:"+str(self.dom())+"mediumwl: "+str(self.mediumwl())+"\nprojekte"+str([x.internalname for x in self.proj()])#+  sort  "bereiche:"+str(self.bereiche) #+"mediumwl:"+str(self.mediumwl())

    @classmethod
    def initialise(cls,bereiche,bereichsprojekte):
        """initializes superbereich objects from each index of bereiche and bereichsprojekte

        :param bereiche: list of domain-lists for each superbereich
        :param bereichsprojekte: list of project-lists for each superbereich
        :return: ->None
        """
        new2=[]
        for i in range(len(bereichsprojekte)):
            new2.append([])
            new=flatten([[x.DOM.a , x.DOM.b] for x in bereichsprojekte[i]])
            for j in range(len(bereiche[i])):
                new2[i].append([])
                for k in new:
                    if k>=bereiche[i][j].a and k<=bereiche[i][j].b:
                        new2[i][j].append(k)
                        new2[i][j].extend([[x.a,x.b]for x in [bereiche[i][j]]])
                        new2[i][j]=sorted(list(set(flatten(new2[i][j]))))
        new3=[]
        for i in range(len(new2)):
            new3.append([])
            for j in range(len(new2[i])):
                new3[i].append([dom(new2[i][j][x],new2[i][j][x+1])for x in range(len(new2[i][j])-1)])

        [superbereich(flatten(new3[x]),bereichsprojekte[x]) for x in range(len(new3))]


class bereich():
    """provides functions to work with sectors, manages the initialization of bereich2 objects

    :var lst: list, list of all initialized sectors
    :var name: int, private
        provides unique names for all sectors
    """
    lst=[]
    name=0
    
    
    
        
    #Instanzmethoden
    
    def __init__(self,domain=[],projekte=[],parent=[],children=False):
        """

        :param domain: list of domains
        :param projekte: list of projects active in this sector
        :param parent: list with the parentsector
        :param children: list of all children|False of the sector
        """
        self.internalname="bereich "+str(bereich.name)
        self.parent=parent
        if children:
            self.children=children
        else:
            self.children=[bereich2(domain,projekte,self)]

        bereich.name+=1
        bereich.lst.append(self)

    def active(self):
        """if any of the children is still active (to be calculated) return True, else False"""

        return flatten([[x.active for x in self.children if x],False])[0]

    def DOM(self):
        """returns the domains of the children"""
        return listjoin([x.dom for x in self.children])

    def dom(self):
        """returns the domains of the sectors children if they do not exceed the mediumwl"""
        return listjoin([x.dom for x in self.children if x.wl<self.parent.mediumwl()-0.001])

    def proj(self):
        """returns the active projects of this sector, which are not finished"""
        return [x for x in list(set(flatten([x.proj for x in self.children]))) if x.WL-x.negwl>0]
    
    def PROJ(self):
        """returns all projects of the sector"""
        return sorted(list(set(flatten([x.proj for x in self.children]))))
    
    def len(self):
        """returns the current sector length"""

        return sum([x.len() for x in self.dom()])
       
    def __repr__(self):
        """defines the console representation of class bereich"""
        return str(self.internalname)
        return "\n"+str(self.dom())+"  "+str(["  Proj"+str(x.internalname) for x in self.proj()])+str(self.children)+str(self.parent)


    @classmethod
    def Rlst(cls):
        """readonly bereich.lst"""
        return bereich.lst

    @classmethod
    def update(cls):
        """searches the current bereich.lst for bereiche with identical projectspread and creates a new bereich
            object joining the old and corresponding superbereich if necessary

        :return: ->None
        """
        #for each bereich searches for index of bereiche with same projects
        newlist=[]
        for i in range(len(bereich.lst)):
            newlist.append([])
            for j in range(len(bereich.lst)-i):
                if len(bereich.lst[i].proj())== len(bereich.lst[j+i].proj()):
                    value=i+j
                    if len(bereich.lst[j+i].proj())>0:
                        for k in range(len(bereich.lst[i].proj())):
                            if bereich.lst[i].proj()[k]!=bereich.lst[i+j].proj()[k]:
                                value=-1
                    else:
                        if not bereich.lst[i].parent is bereich.lst[i+j].parent:
                                value=-1 
                    if value!=-1:
                        newlist[i].append(i+j)
                                                        

        # creates the merged list of all bereiche with completly identical projects
        for z in range(len(newlist)):           #TODO remove z loop, never used
            for i in range(len(newlist)):
                for j in range(len(newlist[i])):
                    newlist[i].extend(flatten(newlist[newlist[i][j]]))
                    newlist[i]=list(set(newlist[i]))

        #for each bereich alle bereiche with identical projectspread
        newlist2=[]
        for i in range(len(newlist)):
            newlist2.append([])
            if len(newlist[i])==0 or newlist[i][0]!="x":
                newlist2[i].extend([bereich.lst[i]])
            else:
                continue
            for j in range(len(newlist[i])):
                if newlist[i][j]=="x":
                    continue
                if newlist[i][j]!=i:
                    newlist2[i].extend([bereich.lst[newlist[i][j]]])
                    newlist2[i]=flatten(newlist2[i])
                    newlist[newlist[i][j]]=["x"]

        #newlist = newlist2 without empty lists
        newlist=[]
        for i in newlist2:
            if len(i)>0:
                newlist.append(i)

        #selects all children for the sector
        newlistchildren=[]
        for i in range(len(newlist)):
            newlistchildren.append([])
            for j in range(len(newlist[i])):
                for k in newlist[i][j].children:
                    newlistchildren[i].append(k)
        
        #creates the new bereich objects with corresponding children and parent
        finallist=[]
        for i in range(len(newlist)):
            finallist.append(bereich(parent=newlist[i][0].parent,children=flatten(newlistchildren[i])))


        # updates childrens of superbereich to new bereich
        for i in superbereich.lst:                                              #fehler?
            i.children=flatten([x for x in finallist if x.parent is i and len(x.proj())>0])

        # removes all appearance of bereich in any superbereichs children, if the bereichs average workload exceeds the
        # parents workload, in that case construct a new superbereich as parent for the bereich object
        for i in finallist: 
            if len(i.proj())>0 and (sum([x.WL for x in i.PROJ()])/sum([x.len() for x in i.DOM()]))<i.parent.mediumwl():     #fehler? #wenn der eigene max Mediumwl kleiner als der parentmediumwl
                for j in superbereich.lst:
                    if i in j.children:
                            j.children.remove(i)

                for j in finallist:
                    if not j is i:
                        for k in i.proj():
                            for l in j.children:
                                if k in l.proj:
                                    l.proj.remove(k)
                i.parent=superbereich(children=i)
            

        #Progaufgabe:  update superbereich einfügen?

        # updates the old bereich.lst with new bereiche
        bereich.lst=finallist


class bereich2():
    """subsectors are the smallest unit of sectors with equal projectspread

    :var lst: list of all initialized bereich2 objects
    :var name: int, private
        provides internal name data
    """
    lst=[]
    name=0

    def __init__(self,domain,projekte,parent):
        """

        :param domain:the domains of the subsector
        :param projekte:projects of the subsector
        :param parent: the parent
        """
        self.internalname="bereich2 "+str(bereich2.name)
        self.parent=parent
        self.dom=domain
        self.proj=[x for x in projekte if x.DOM==self.dom]
        self.wl=0
        self.active=True

        bereich2.name+=1
        bereich2.lst.append(self)


    def __repr__(self):
        """defines the console appearance

        :return: ->str
        """
        return str(self.dom)+ str(self.wl)

#endregion

#initialisierungsmethoden
def defIn(data_):
    """for each dataset initializes a project with given data

    :param data_:list
    :return: ->None
    """

    add=len(Proj.lst)
    for i in range(len(data_)):
        Proj(i+add, data_[i][0], data_[i][1], data_[i][2])
    
def sortprojforsuperbereiche(Liste,marker=0):       #     #input: [[proj1,proj2,proj3]]
    """ sorts the projects in parentsectors to enable calculation

    selects the project with highest average workload, if it is higher than the total average workload it is treated as
    single project for further calculation and its domain is deducted from every over projects domain. Recursive calls
    itself as long as any project in the parentsector has an higher workload than the average wl of the parentsector.

    :param Liste: list, contains the list of parentsector lists [list of projects] to calculate
    :param marker:
    :return: ->list
    """
    Newlist=[]
    for i in Liste:
        Bereiche=flatten([listjoin([x.dom for x in flatten(i)])])   #creates the sum of all listed domains
        mediumwl=(sum([x.WL for x in i])/sum([x.len() for x in (flatten(listjoin([x.dom for x in i])))]))  #calculates mediumWL for joined sectors
        Liste2=sortprojlistdailywl(i)
        worklist=[]
        marker2=True


        while Liste2[-1].dailywl()>mediumwl or len(sortprojlistdailywl(flatten(Newlist)))>0 and sortprojlistdailywl(flatten(Newlist))[-1].dailywl()>=mediumwl:

            # first iteration: choses the total highest wl proj in worklist, other iteration: choses the highest
            # workload project in newlist
            if marker2:
                worklist.append(Liste2[-1])
                marker2=False
            else:
                worklist.append(sortprojlistdailywl(flatten(Newlist))[-1])
                worklist=flatten([worklist])
                
                for k in range(len(worklist)-1):
                    for j in range(len(worklist[k].dom)):
                        for l in range(len(worklist[-1].dom)):
                            if worklist[k].dom[j]==worklist[-1].DOM:
                                worklist[-1].dom[l]=worklist[-1].dom[l]+(worklist[k].dom[j]==worklist[-1].DOM)
                            worklist[-1].dom=flatten(worklist[-1].dom)
                        worklist=flatten(worklist)
            

            mediumwl=(sum([x.WL for x in worklist])/sum([x.len() for x in flatten(listjoin([x.dom for x in worklist]))]))


            # deducts the domain of the highest average workload project >toatal average workload from the superdomain
            Trimbereiche=flatten(listjoin(flatten([x.dom for x in worklist])))

            for j in range(len(Bereiche)):
                Bereiche[j]=[Bereiche[j]-Trimbereiche[0]]
            Bereiche=flatten([Bereiche])

            # appends all projects intersecting with worklist project to deduct the worklist project from
            Newlist = []
            for j in range(len(Bereiche)):
                Newlist.append([])
                for k in i:
                    if k.DOM==Bereiche[j]:      #TODO maybe fix the issue with for loop+ if i.e. intersection found with any, break, else (for the loop) substract
                        Newlist[j].append(k)

            # deducts the worklist project domain from all intersecting projects
            for j in range(len(Newlist)):
                for k in range(len(Newlist[j])):
                    for l in range(len(Newlist[j][k].dom)):
                        if Newlist[j][k].dom[l]!=Trimbereiche[0]:
                            Newlist[j][k].dom[l]=Newlist[j][k].dom[l]-Trimbereiche[0]          
                        Newlist[j][k].dom=flatten(Newlist[j][k].dom)

        
        if len(worklist)==0:
            Newlist=Liste
        else:
            Newlist.extend([worklist])

        # newlist contains the domains of all changed projects after deduction, each project having an own list,
        # extracting the deductee in an own list for it is now treated as single project
        # calculates the new mediumwl for each project
        mediumwl=[]
        for j in Newlist:
            if len(j)>1:
                mediumwl.append(sum([x.WL for x in j])/sum([x.len()for x in flatten(listjoin([x.dom for x in j]))]))
            else:
                mediumwl.append(j[0].dailywl())

        # if there is any project with higher mediumWL than the average wl of the current list, recursive calls
        # itself until every project with higher workload than the superbereich average Wl is extracted as own project
        for j in range(len(Newlist)):
            Liste3=sortprojlistdailywl(Newlist[j])
            if Liste3[-1].dailywl()>mediumwl[j] and marker!=len(Liste3): #TODO delete marker
                Newlist[j]=sortprojforsuperbereiche([Liste3],len(Liste3))        
        

    return Newlist

#werkzeugmethoden
def listjoin(a1):
    """returns the sum of all listed domains

    checks for interection with the last item of a2, if there is none creates new entry, if there is any adds the two
    domains
    :param a1: list of domain objects
    :return: list of domain objects, intersections added to one
    """
    a1=flatten(a1)
    if len(a1)>1:
        a1=sortDomlst(a1)
        a2=[a1.pop(0)]
        for i in a1:
            try:
                if len(a2[-1])>=1:
                    pass
            except:
                pass
            else:
                a2=flatten(a2)

            if i==a2[-1]:
                a2[-1]=i+a2[-1]
            else:
                a2.append(i)
        return flatten(a2)
    else:
        return a1

def sortDomlst(a):
    """sorts a list of domains ascending by startdate and duration

    :param a: list, containing domain objects
    :return: ->list
    """
    a1=[a.pop(0)]
    for j in range(len(a)):
        for i in range(len(a1)+1):
            if i>=len(a1):
                break
            if a[j].a>a1[i].a:
                continue
            elif a[j].a==a1[i].a and a[j].b>a1[i].b:
                continue
            else:
                break
        a1.insert(i,a[j])
    return a1
    
def sortprojlistdailywl(a):
    """sorts a list of projects by its average daily workload in ascending order

    :param a: list of projects
    :return:
    """
    a1=[]
    for j in range(len(a)):
        for i in range(len(a1)+1):
            if i>=len(a1):
                break
            if a[j].dailywl()>a1[i].dailywl():
                continue
            else:
                break
        a1.insert(i,a[j])
    return a1

#TODO annotations
def sortprojlistmaxdailywl(a):             # a= bereichliste
    a1=[]
    for j in range(len(a)):
        for i in range(len(a1)+1):
            if i>=len(a1):
                break    
            if len(a[j].proj())==0:
                i=len(a1)+1
                break
            if len(a[j].proj())>len(a1[i].proj()):
                continue
            elif len(a[j].proj())==len(a1[i].proj()) and (a[j].proj()[0].WL/a[j].len())>(a1[i].proj()[0].WL/a1[i].len()): 
                continue
            else:
                break
        a1.insert(i,a[j])
    return a1

#listmanagement       
def flatten(input):
    """reduces a mulit-dimensional list into one single list

    :param input: list, multidimensional
    :return: ->list
    """

    newlst=[input]
    if type(input)==list:
        newlst=[]
        for k in input:
            if type(k)==list:
                append=flatten(k)
                newlst.extend(append)
            else:            
                newlst.append(k)
    return newlst

def shiftpath(input):
    """reduces a multi-nested-list to only contain the last sublist of each list

    :param input: multi-nested-list
    :return: ->list
    """
    Newlist=[[]]
    k=0
    i=0

    # the function recursive calls itself until type(dataObject)!= list and returns this datum
    while i <=len(Newlist):
        while k<len(input):
            if type(input[k])==list:
                extend=shiftpath(input[k])
                Newlist.extend(extend)
                k+=1
                i+=1
                break
            else:
                Newlist[i].append(input[k])
                k+=1

        if k+1>len(input):
            break
        else:
            Newlist.append([])

        i+=1 
        
    for i in Newlist:
        if type(i)==list and len(i)==0:
            Newlist.remove(i)

    return Newlist

def math():
    """calculates the optimal workload distribution and inserts the optimal distribution into the projects

    :return: ->None
    """

    new=shiftpath(sortprojforsuperbereiche([Proj.Rlst()])) # contains the lists of parentsectors [list of projects]


    # creates domain lists for each parentsector
    superbereiche=[]
    for i in new:
        superbereiche.append(flatten(listjoin(flatten([x.dom for x in i]))))

    # checks if there is any intersection between any subdomains of the parentsectors
    Superbereichejoin=[]
    for i in range(len(superbereiche)):
        Superbereichejoin.append([])
        for j in range(len(superbereiche)-(i)): #+1
            Value=-1
            for k in superbereiche[i+j]:        #+1
                for l in superbereiche[i]:
                    if l==k:
                        Value=(i+j)             #+1
            if Value!=-1:
                Superbereichejoin[i].append(Value)

    # inserts all intersections of the indexed parentsector into the corresponding sector list
    for z in range(len(Superbereichejoin)):  #TODO remove z, not referenced? Maybe it enables the join of all intersecting parentsecors
        for i in range(len(Superbereichejoin)):
            for j in range(len(Superbereichejoin[i])):
                Superbereichejoin[i].extend(flatten(Superbereichejoin[Superbereichejoin[i][j]]))
                Superbereichejoin[i]=list(set(Superbereichejoin[i]))

    # adds all indexes unequal to i in superbereiche2 [i]
    superbereiche2=[]
    for i in range(len(Superbereichejoin)):
        superbereiche2.append([])
        if len(Superbereichejoin[i])==0 or Superbereichejoin[i][0]!="x":        #TODO invert continue statement as gatekeeper
            superbereiche2[i].extend(superbereiche[i])
        else:
            continue
        for j in range(len(Superbereichejoin[i])):
            if Superbereichejoin[i][j]=="x":
                continue
            if Superbereichejoin[i][j]!=i:
                superbereiche2[i].extend(superbereiche[Superbereichejoin[i][j]])
                Superbereichejoin[Superbereichejoin[i][j]]=["x"]

    for i in range(len(superbereiche2)):
        superbereiche2[i]=flatten(listjoin(superbereiche2[i]))

    # converts back to superbereiche
    superbereiche=[]
    for i in superbereiche2:
        if len(i)>0:
            superbereiche.append(i)

    # selects all Projects for each superbereiche into new list
    superbereicheProj=[]
    for j in range(len(superbereiche)):
        superbereicheProj.append([])
        for i in Proj.Rlst():
            value=False
            for k in superbereiche[j]:
                for l in i.dom:
                    if k==l:
                        value=True
            if value:
                superbereicheProj[j].append(i)

    superbereich.initialise(superbereiche,superbereicheProj)  #initialisisert die superbereiche

    # calculates the final wl distribution, if there is any project with just one domain fist solves this, else solves
    # a domain with just one project. By marking the projects and domains as solved these are excluded for the next round
    # after anything is solved alway removes solved projects from all other domains and updates the sector list
    for a in range(30):

        if not len(flatten([x.proj for x in bereich.lst])):
            break

        bereich.update()

        do=True
        ProjATM=0
        # projekt.intersection mit allen bereichen füllen, in denen das Projekt activ ist
        for i in Proj.Rlst():
            i.intersect=[x for x in bereich.lst if i in x.proj() and x.active()]

        # checks for projects with just one sector and solves it
        for i in Proj.Rlst():
            if len(i.intersect)==1 and i.marker:

                mediumwl=99999999999999999999999999999

                #calculates mediumworkload #TODO necessary? isnt it always mediumwl
                while 1:
                    oldmediumwl=mediumwl
                    mediumwl=((i.WL-i.negwl)+sum([(x.wl*x.dom.len()) for x in i.intersect[0].children if x.wl<mediumwl]))/sum([x.dom.len() for x in i.intersect[0].children if x.wl<mediumwl])

                    if mediumwl==oldmediumwl:
                        break
                #creates the final domain and wl for the project if project workload does not exceed bereich wl
                for j in [x for x in i.intersect[0].children if x.wl<mediumwl]:
                    i.dom2.append(j.dom)
                    i.domwl.append(mediumwl-j.wl)
                    j.wl+=(mediumwl-j.wl)

                i.negwl=i.WL
                i.dom2=flatten(i.dom2)
                do=False
                i.marker=False

                ProjATM=i

                

                break




        if do:  #TODO anstatt "do" mit "else" an die for i in Proj.Rlst schleife hängen

            # for every sector with just one project: adds the sectors children domain to the projects final domains
            # and the sectors average wl to final wl list of the project, if other projects already have a workload in
            # the sector, deduct this wl
            for i in sortprojlistmaxdailywl(bereich.Rlst()):

                if len(i.proj())==1 and i.proj()[0].marker and i.active():
                    ProjATM=flatten(i.proj()[0])[0]
                    for j in i.children:
                        j.active=False

                    if sum([x.wl for x in i.children])==0:
                        #writes all children wl and dom into proj final wl and dom
                        for j in range(len(i.children)):
                            ProjATM.dom2.append([i.children[j].dom])

                            if i.parent.mediumwl()*i.len()>=ProjATM.WL-ProjATM.negwl:
                                ProjATM.domwl.append((ProjATM.WL-ProjATM.negwl)/i.len())
                            else:
                                ProjATM.domwl.append(i.parent.mediumwl())

                            if i.parent.mediumwl()*i.len()>=ProjATM.WL-ProjATM.negwl:           #TODO move into first if statement for same condition
                                ProjATM.negwl=ProjATM.WL
                            else:
                                ProjATM.negwl+=i.parent.mediumwl()*i.len()

                    else:
                        mediumwl=min(i.parent.mediumwl(),sum([x.WL for x in i.PROJ()])/i.len())                            #summe aller wl der in diesem Bereich aktiven Projekte
                        ProjATM.dom2.append(i.dom())
                        for j in i.children:
                            ProjATM.domwl.append(mediumwl-j.wl)
                            ProjATM.negwl+=((mediumwl-j.wl)*j.dom.len())
                            j.wl+=(mediumwl-j.wl)

                    ProjATM.dom2=flatten(ProjATM.dom2)

                    break


                
        if ProjATM==0:
            break

        # removes the project from all sectors where it is not finally inserted if there is no workload left
        if ProjATM.WL-ProjATM.negwl<=0:
            for i in [x for x in Proj.Rlst() if not x==ProjATM]: #TODO remove outer loop: no impact

                for j in bereich.lst:
                    value=False
                    for k in j.dom():
                        for l in ProjATM.dom2:
                            if k==l:
                                value=True
                    if not value:
                        for k in j.children:
                            if ProjATM in k.proj:
                                k.proj.remove(ProjATM)

def reset():
    """resets all class-lists for new calculation

    :return: ->None
    """
    Proj.lst=[]
    superbereich.lst=[]
    bereich.lst=[]
    bereich2.lst=[]

def main(data=[]):
    """initializes new projects and the workload optimization

    :param data: list
    :return:
    """
    reset()

    if len(data)==0:
        #data=[[5,105,300],[0,100,150],[20,10,80],[15,20,160],[80,80,200]]                                               #sowohl parallele als auch individuelle Lasten
        #data=[[0,60,300], [20,100,800], [80,30,500], [70,80,400], [25,10,100]]                                         #nur indiviudelle Lasten
        data=[[0,30,400],[5,20,600],[35,15,300],[20,40,300],[50,15,10000],[55,25,500],[70,85,1701],[60,25,500]]        #nur indiviudelle Lasten, 2 Bereiche

    defIn(data)
    math()
    return Proj.Rlst()



