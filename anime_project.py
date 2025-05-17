import random
import pickle
from jikanpy import Jikan
import tkinter
from PIL import ImageTk
from urllib.request import urlopen
def create():
    f=open('anime.dat','wb')
    
    list=['Dragon Ball']
    pickle.dump(list,f)
    f.close()


def include1(x):
    f=open('anime.dat','rb')
  
    list1=pickle.load(f)
    f.close()
    f=open('anime.dat','wb')

    list1.append(x)
    pickle.dump(list1,f)
    f.close()

def suggest_genre(genre):
    jikan=Jikan()
    num=random.randrange(50)
    anime=jikan.top(type='anime',page=num)
    anime1=anime['data']
    for i in anime1:
        l=i.keys()
        k=i['genres']
        
        for j in k:
            name=j['name']
        
            if name==genre:
                item=i['title']
                lis=[]
                lis.append(item)
    
    return lis            

def top():
    jikan=Jikan()  
    anime=jikan.top('anime',page=1)
    l=len(anime)
    c=anime['data']
    
    lis=len(c)
    anime_list=[]
    for i in range(lis):
        x=c[i]['title']
        
        anime_list.append(x)
    return anime_list
def current_airing():
    jikan=Jikan()
    anime=jikan.seasons(extension='now')
    anime1=random.choice(anime['data'])
    anime2=anime1['titles'][0]['title']
    return anime2
def randomize(x):
    anime=random.choice(x)
    return anime

def read():
    f=open('anime.dat','rb')
    list=pickle.load(f)
    return list

def search(name):
    jikan=Jikan()
    anime=jikan.search('anime',name)
    data=anime['data'][0]
    return data,name
def gui(data,name):
    root=tkinter.Tk()
    root.geometry('1000x650')
    
    #scroll_bar = tkinter.Scrollbar(root) 
  
    #scroll_bar.pack( side = 'bottom', fill = 'x' )
    #scroll_bar.pack(side='right',fill='y')
    url=data['images']['jpg']['image_url']
    genre=[]
    for i in data['genres']:
        genre.append(i['name'])
    gen=''
    for i in genre:
        gen =gen+i+';'
    genre=gen
    score=data['score']
    synopsis=data['synopsis']
    synop=''
    try:
        for i in range(150):
            synop +=synopsis[i]
    except:
        synop='None'
    synopsis=synop+'...'
    rank=data['rank']
    dat=urlopen(url)
    img=ImageTk.PhotoImage(data=dat.read())
    tkinter.Label(root,image=img).pack()
    root.title(name)
    lbl=tkinter.Label(root,text=f'NAME:{name}',font=('ariel',14,'bold'))
    lbl1=tkinter.Label(root,text=f'RANK:{rank}',font=('ariel',12,'bold'))
    lbl2=tkinter.Label(root,text=f'GENRE:{genre}',font=('ariel',12,'bold'),)
    lbl3=tkinter.Label(root,text=f'SCORE:{score}',font=('ariel',12,'bold'))
    lbl4=tkinter.Label(root,text=f'SYNOPSIS:{synopsis}',font=('ariel',10),justify='center')
    lbl.pack()
    lbl1.pack()
    lbl2.pack()
    lbl3.pack()
    lbl4.pack()
    root.mainloop()

def read_file():
    f=open('anime.dat','rb')
    data=pickle.load(f)
    for i in data:
        print(i)
    print('*********************************************')

try:   
    finished=read()
except:
    create()
    finished=read()
def main():
    print('What would you like to do?')
    print('**********************************************')
    print('1.Recommend anime based on genre')
    print('2.Recommend a top anime')
    print('3.Recommend currently airing anime')
    print('4.watched anime')
    print('5.Exit')
    print('**********************************************')
    c=int(input('Enter the respective number:'))
    print('**********************************************')
    if c==1:
        genre=input("Input Genre(ex:Romance,Action...):")
        genre=genre.title()
        rec=suggest_genre(genre)
        show=randomize(rec)
        while show in finished:
            rec=suggest_genre(genre)
            show=randomize(rec)
        print(f'watch "{show}" bro!!!')
        dat,name=search(show)
        gui(dat,name)
        watched=input('Have you watched this anime(y/n):')
        if watched.lower()=='y':
            include1(show)
            main()
        elif watched.lower()=='n':
            print('Have a great time watching!!')
            main()
        else:
            print('incorrect input!!!')

    elif c==2:
        top_anime=top()
        anime=randomize(top_anime)
        while anime in finished:
            top_anime=top()
            anime=randomize(top_anime)
        dat,name=search(anime)
        gui(dat,name)
        watched=input('Have you watched this anime(y/n):')
        if watched.lower()=='y':
            include1(anime)
            main()
        elif watched.lower()=='n':
            print('Have a great time watching!!')
            main()
        else:
            print('incorrect input!!!')
    elif c==3:
        current=current_airing()
        while current in finished:
            current=current_airing()
        dat,name=search(current)
        gui(dat,name)
        watched=input('Have you watched this anime(y/n):')
        if watched.lower()=='y':
            include1(current)
            main()
        elif watched.lower()=='n':
            print('Have a great time watching!!')
            main()
        else:
            print('incorrect input!!!')
    elif c==4:
        read_file()
        main()
    elif c==5:
        print('Exitted Successfully!!!!')
    else:
        print("incorrect input!!!")


main()