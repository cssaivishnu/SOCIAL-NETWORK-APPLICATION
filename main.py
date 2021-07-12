from tkinter import *
from tkinter import ttk
from PIL import ImageTk, Image 
from tkinter import filedialog

user_contacts = {}
group_contacts = {}
users_set = set()
groups_set = set()


def Update_details():
    start_user=False
    start_group=False
    file = open("social_network.txt","r")
    for each in file:
        if(each=='#users\n'):
            start_user=True
            continue
        if(each=='#groups\n'):
            start_group=True
            continue
        line=each[1:]
        id=line.split(':')[0]
        linked_contacts=line.split(':')[1].split(',')
        linked_contacts[0]=linked_contacts[0][1:]
        linked_contacts[len(linked_contacts)-1]=linked_contacts[len(linked_contacts)-1].split('>')[0]
        if(start_user and not start_group):
            user_contacts[id]=linked_contacts
        if(users_started and groups_started):
            group_contacts[id]=linked_contacts
    for user_id,linked_ids in user_contacts.items():
        users.add(user_id)
        for linked_id in linked_ids:
            users.add(linked_id)
    for group_id in group_contacts:
        groups.add(group_id)
    file.close()

def display_contacts(user_id):
    top=Toplevel()
    top.title("Display Contacts of a User")
    top.geometry("500x500")
    Button(top,text="Exit Window",command=top.destroy).pack()
    Label(top,text="Display Contacts").pack()
    frame_1 = Frame(top)
    frame_1.pack(fill=BOTH,expand=1)
    canvas_=Canvas(frame_1)
    canvas_.pack(side=LEFT,fill=BOTH,expand=1)
    scroll_bar=ttk.Scrollbar(frame_1,orient=VERTICAL,command=canvas_.yview)
    scroll_bar.pack(side=RIGHT,fill=Y)
    canvas_.configure(yscrollcommand=scroll_bar.set)
    canvas_.bind('<Configure>' , lambda e : canvas_.configure(scrollregion=canvas_.bbox("all")))
    frame_2 = Frame(canvas_)
    canvas_.create_window((0,0), window=frame_2, anchor="nw")
    if str(user_id) in user_contacts :
        for contact in user_contacts[str(user_id)]:
            Label(frame_2,text="User : "+contact_id).pack()
    else:
        Label(frame_2,text="The user "+str(user_id)+" has 0 contacts.").pack()

def get_groups(user_id):
    top=Toplevel()
    top.title("Displaying Groups of a User")
    top.geometry("500x500")
    Button(top,text="Close the Window",command=top.destroy).pack()
    Label(top,text="Display the groups joined").pack()
    frame_1=Frame(top)
    frame_2.pack(fill=BOTH,expand=1)
    canvas_=Canvas(frame_1)
    canvas_.pack(side=LEFT,fill=BOTH,expand=1)
    scroll_bar = ttk.Scrollbar(frame_1,orient=VERTICAL,command=canvas_.yview)
    scroll_bar.pack(side=RIGHT,fill=Y)
    canvas_.configure(yscrollcommand=scroll_bar.set)
    canvas_.bind('<Configure>' , lambda e : canvas_.configure(scrollregion=canvas_.bbox("all")))
    frame_2 = Frame(canvas_)
    canvas_.create_window((0,0), window=frame_2, anchor="nw")
    for group_id,members_list in group_contacts.items():
        if str(user_id) in members_list :
            Label(frame_2,text="Group : "+group_id).pack()

def compose_post(user_id):
    top=Toplevel()
    top.title("Post Message as a User")
    top.geometry("700x700")
    recipents=[]
    if str(user_id) in user_contacts :
        for contact_id in user_contacts[str(user_id)]:
            recipents.append("User : "+str(contact_id))
    for group_id,members_list in GROUP_CONTACTS.items():
        if str(user_id) in members_list :
            recipents.append("Group : "+str(group_id))
    if len(recipents) == 0 :
        Label(top,text="There is neither user nor group to which the user :"+str(user_id)+" can send a message.").pack()
    else:
        path_image=Label(top,text=" no path ")
        recipent=StringVar()
        recipent.set(recipents[0])
        Label(top,text="Whom do you want to message?").pack()
        option_menu=OptionMenu(top,recipent,*recipents)
        option_menu.pack()
        text_box = Text(top,width=40,height=10)
        text_box.pack(pady=20)
        Button(top,text="Send the Message",command=lambda:send_message(top,text_box.get(1.0,END),image_path.cget("text"),recipent.get(),user_id)).pack()
        frame_=Frame(top)
        get_image_button=Button(top,text="Click this button for selecting an image.",command=lambda :get_image(my_frame,path_image))
        get_image_button.pack(pady=10)

def send_message(master,message,img_path,recipent,sender_id):
    master.destroy()
    receivers_list=[]
    sender="From #User : "+str(sender_id)
    if recipent.split(':')[0].rstrip() == "User":
        receivers_list.append(recipent.split(':')[1].lstrip())
    else:
        sender=sender+" via #Group : "+str(recipent.split(':')[1].lstrip())
        for contact_id in group_contacts[str(recipent.split(':')[1].lstrip())]:
            receivers_list.append(contact_id)
    file=open("messages.txt","a")
    for receiver_id in receivers_list:
        file.write("#User:"+str(receiver_id)+"\n")
        file.write(sender+"\n")
        file.write("#Image_path:"+image_path+"\n")
        file.write(message.strip()+"\n")
    file.close()

def get_image(master,path_label):
    for widget in master.winfo_children():
        widget.destroy()
    master.filename=filedialog.askopenfilename(initialdir=".",title="Select an Image",filetypes=(("png files","*.png"),("jpg files","*.jpg"),("all files","*")))
    image_path = master.filename
    path_label.config(text=image_path)
    imag = Image.open(image_path)
    imag = imag.resize((250, 250), Image.ANTIALIAS)
    imag = ImageTk.PhotoImage(imag)
    panel = Label(master, image = imag) 
    panel.image = imag
    panel.pack()
    master.pack()

def display_messages(user_id):
    top=Toplevel()
    top.title("Display the Messages Received by an User")
    top.geometry("500x500")
    Button(top,text="Close the Window",command=top.destroy).pack()
    Label(top,text="Display Messages").pack()
    frame_1 = Frame(top).pack(fill=BOTH,expand=1)
    canvas_=Canvas(frame_1).pack(side=LEFT,fill=BOTH,expand=1)
    scroll_bar = ttk.Scrollbar(frame_1,orient=VERTICAL,command=canvas_.yview).pack(side=RIGHT,fill=Y)
    canvas_.configure(yscrollcommand=scroll_bar.set)
    canvas_.bind('<Configure>' , lambda e : canvas_.configure(scrollregion=canvas_.bbox("all")))
    frame_2 = Frame(canvas_)
    canvas.create_window((0,0), window=frame_2, anchor="nw")
    file_name=open("messages.txt","r")
    lines=[]
    for each in file:
        lines.append(each)
    length=len(lines)
    j=0
    while j<length:
        if lines[j]=="#User:"+str(user_id)+"\n" :
            message_frame=Frame(frame_2)
            Label(message_frame,text=lines[j+1].rstrip()).pack()
            if lines[j+2].split(':')[1].rstrip() != " no path ":
                imag = Image.open(lines[j+2].split(':')[1].rstrip()) 
                imag = imag.resize((250, 250), Image.ANTIALIAS) 
                imag = ImageTk.PhotoImage(imag)
                panel = Label(message_frame, image = imag)
                panel.image = imag
                panel.pack()
            else:
                Label(message_frame,text="<No image was attached>").pack()
            messag=""
            k=j+3
            while k<length and lines[k][:5]!="#User":
                messag=messag+lines[k]
                k = k+1
            messag=messag[:len(messag)-1]
            j=k-1
            Label(message_frame,text=messag).pack()
            message_frame.pack(pady=10)
        j = j+1
    file_name.close()

def _menu_():
    root = Tk()
    root.title("||SOCIAL NETWORK||")
    root.geometry("500x500")
    Button(root,text="QUIT",command=root.destroy).pack()
    _id_=StringVar()
    Label(root,text="_USERS LIST OF USERS_").pack(pady=10)
    for user_id in users:
        Radiobutton(root,text="USER : "+str(user_id),variable=_id_,value=str(user_id)).pack()
    Button(root,text="Display Incoming Messages of the user",command=lambda:display_messages(_id_.get())).pack(pady=(10,0))
    Button(root,text="Display Existing Contacts of the user",command=lambda:display_contacts(_id_.get())).pack()
    Button(root,text="Display Groups of the user",command=lambda:get_groups(selected_id.get())).pack()
    Button(root,text="Compose and Post messages as a user",command=lambda:compose_post(selected_id.get())).pack()
    root.mainloop()


Update_details()
_menu_()