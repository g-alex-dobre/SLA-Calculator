from tkinter import *
import json
from tkinter import messagebox
from tkinter import filedialog

#main categories to be used and displayed in the categories selectbox
CATEGORIES = ["Housing/Hosting", "Internal Connectivity", "VCI Connect"]

#create the window
screen = Tk()

#set the title of the window
screen.title("SLA Calculator")

#create main label/title
label = Label(text="Select a category and then an offering \n to view SLA and description")
label.grid(row=2, column=2, padx=50, pady=50)

#label for create a new offering
add_offer_label = Label(text="Select a category from above \n then enter details below to add a new offering")
add_offer_label.grid(row=5, column=2, padx=50, pady=50)

#add_category = Label(text="New category name:")
#add_category.grid(row=4, column=1)

#create left side labels
add_offering = Label(text="New offering name:")
add_offering.grid(row=6, column=1)

add_description = Label(text="Description:")
add_description.grid(row=7, column=1)

add_slatime = Label(text="E2E delivery time:")
add_slatime.grid(row=8, column=1)

category_label = Label(text="Select category")
category_label.grid(row=3, column=1)

offering_label = Label(text="Select offer")
offering_label.grid(row=4, column=1)

#add_category_entry = Entry()
#add_category_entry.grid(row=4, column=2)

#create entries for when adding a new item

add_offering_entry = Entry(width=45)
add_offering_entry.grid(row=6, column=2, sticky="W")

add_slatime_entry = Entry()
add_slatime_entry.grid(row=8, column=2, sticky="W")

add_description_entry = Text(height=7, width=45)
add_description_entry.grid(row=7, column=2, sticky="W")


#create right side labels - these are used to display data from the database/json file
present_description = Label(text="", padx=50, pady=50)
present_description.grid(row=3, column=3, sticky="E")

present_slatime = Label(text="")
present_slatime.grid(row=4, column=3)


#SAve Buttons to add new items in the Json file - below the funtion called when button pressed
def save():

    category = listbox.get(ANCHOR)
    offering = add_offering_entry.get()
    description = add_description_entry.get("1.0",END)
    slatime = add_slatime_entry.get()

    new_data = {
        offering: {
            "category": category,
            "offering_description": description,
            "slatime": int(slatime)

        }
    }

    if len(category) == 0 or len(offering) == 0 or len(description) == 0 or len(slatime) == 0:
        messagebox.showinfo(title="Oops", message="Make sure you complete all the fields!")
    else:
        try:
            with open("data.json", "r") as data_file:
                data = json.load(data_file)
                data.update(new_data)
        except FileNotFoundError:
            with open("data.json", "w") as data_file:
                json.dump(new_data, data_file, indent=4)
        else:
            with open("data.json", "w") as data_file:
                json.dump(data, data_file, indent=4)
        finally:
            #add_category_entry.delete(0, END)
            add_offering_entry.delete(0, END)
            add_description_entry.delete("1.0", END)
            add_slatime_entry.delete(0, END)
            messagebox.showinfo(title="Offering added", message="Successfully added new offering to database")


#Create the actual button : calls action() when pressed
button = Button(text="Submit new offering", command=save)
button.grid(row=9, column=2, pady=10)

#Listbox for category selection - this is the function called when you click on an item in the categories select box
def listbox_used(event):
    # Gets current selection from listbox
    categ_selected = listbox.get(ANCHOR)
    try:
        with open("data.json", "r") as data_file:
            data = json.load(data_file)
            listofitems = [item[0] for item in data.items() if item[1]["category"] == categ_selected]
    except FileNotFoundError:
        listofitems=[]
    create_offering_listbox(listofitems)

#create the actual listbox to show main categories
listbox = Listbox(height=3, width=45)

#adding items in the listbox, from categories contstant defined at top
for item in CATEGORIES:
    listbox.insert(CATEGORIES.index(item), item)

#binding the above function to the listbox, to run when a selection is made
listbox.bind("<<ListboxSelect>>", listbox_used)

#add the listbox to the GUI window
listbox.grid(row=3, column=2)

#create listbox for group offerings inside main categories
offerings_listbox = Listbox(height=5, width=45)

#create the function that will run when an item is selected in the offerings listbox
def listbox_offerings_used(event):


    selected_offering = offerings_listbox.get(ANCHOR)
    if len(selected_offering) != 0:
        try:
            with open("data.json", "r") as data_file:
                data = json.load(data_file)
                new_text = data[selected_offering]["offering_description"]
                new_sla = data[selected_offering]["slatime"]
        except FileNotFoundError or KeyError:
            pass
        present_description.config(text=f"Description of selected offering: {new_text}")
        present_slatime.config(text=f"SLA Time: {new_sla} Days")

#create a function that will be called every time another item in the categories listbox is selected
# this will update the items in the offerings listbox based on selected category

def create_offering_listbox(listofitems):

    #offerings_listbox = Listbox(height=len(listofitems))
    offerings_listbox.delete(0,END)
    for item1 in listofitems:
        offerings_listbox.insert(listofitems.index(item1), item1)

offerings_listbox.bind("<<ListboxSelect>>", listbox_offerings_used)
offerings_listbox.grid(row=4, column=2)


screen.config(width=600, height=600)
screen.mainloop()

