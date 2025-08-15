import tkinter as tk
from tkinter import filedialog, messagebox, PhotoImage
import configparser

# Funkcie
def browse(entry): # Explorer
    folder = filedialog.askdirectory()
    if folder:
        entry.delete(0, tk.END)
        entry.insert(0, folder)

def delete_category(row_widgets): # Vymazať riadok
    if len(category_entries) <= 1:
        messagebox.showwarning("Warning", "At least one category must remain!")
        return
    for widget in row_widgets:
        widget.destroy()
    category_entries.remove(row_widgets)
    refresh_rows()

def refresh_rows(): # Refresh riadky
    for idx, row_widgets in enumerate(category_entries, start=1):
        for col, widget in enumerate(row_widgets):
            widget.grid(row=idx, column=col, padx=5, pady=5)

def add_category(): # Pridaj riadok
    row = len(category_entries) + 1

    section_name_entry = tk.Entry(frame, width=20, font=("Comic Sans MS", 30)) # pole pre nazov sekcie
    section_name_entry.grid(row=row, column=0, padx=5, pady=5)


    source_entry = tk.Entry(frame, width=30, font=("Comic Sans MS", 12)) # Pole pre zdrojovy priečinok
    source_entry.grid(row=row, column=1, padx=5, pady=5)

    browse_source_btn = tk.Button(frame, text="Browse", command=lambda e=source_entry: browse(e), bg="#FFD700", fg="#000000", relief="raised", bd=4) # Tlačidlo exploreru pre zdroj
    browse_source_btn.grid(row=row, column=2, padx=5)


    dest_entry = tk.Entry(frame, width=30, font=("Comic Sans MS", 12)) # Pole pre cieľový priečinok
    dest_entry.grid(row=row, column=3, padx=5, pady=5)

    browse_dest_btn = tk.Button(frame, text="Browse", command=lambda e=dest_entry: browse(e), bg="#FFD700", fg="#000000", relief="raised", bd=4) #Tlačidlo exploreru pre destinaciu
    browse_dest_btn.grid(row=row, column=4, padx=5)


    delete_btn = tk.Button(frame, text="Delete", bg="#FF4500", fg="white", font=("Comic Sans MS", 10, "bold"), relief="raised", bd=4) # Tlačidlo pre vymazanie riadku
    delete_btn.grid(row=row, column=5, padx=5)
    delete_btn.configure(command=lambda rw=[section_name_entry, source_entry, browse_source_btn, dest_entry, browse_dest_btn, delete_btn]: delete_category(rw)) # Logika odstranenia riadku


    category_entries.append([section_name_entry, source_entry, browse_source_btn, dest_entry, browse_dest_btn, delete_btn]) # Vytvoriť riadok dalsí

def save_config(): # Uložiť konfiguráciu
    config = configparser.ConfigParser()
    for row_widgets in category_entries:
        section_name = row_widgets[0].get().strip()
        source = row_widgets[1].get().strip()
        dest = row_widgets[3].get().strip()
        if section_name and source and dest:
            config[section_name] = {'source': source, 'destination': dest}

    if not config.sections(): # Ak nenisu žiadne sekcie, VARUJ!!!!!!!!
        messagebox.showwarning("Warning", "No valid sections to save!")
        return

    with open('config.ini', 'w') as configfile: # Vpíš do config.ini konfiguráciu
        config.write(configfile)

    messagebox.showinfo("Success", "config.ini has been created successfully!")

# Hlavne gui
root = tk.Tk()
root.title("PeachBak - Config Generator")
root.geometry("1100x650")
root.configure(bg="#FFEFD5")  # broskynova farba pozadia !!!

# Ikonkra
try:
    root.iconbitmap("icon.ico")
except:
    pass

# Logo vľavo hore
try:
    logo = PhotoImage(file="logo.png")
    logo_label = tk.Label(root, image=logo, bg="#FFEFD5")
    logo_label.image = logo
    logo_label.place(x=15, y=10) #Umiestnenie
except:
    pass

# Nadpis
title_label = tk.Label(root, text="PeachBak - Config Generator", font=("Comic Sans MS", 22, "bold"), bg="#FFDAB9", fg="#FF4500", relief="ridge", bd=4)
title_label.pack(pady=20, ipadx=10, ipady=10)

# Oramovať šecko!!!!
frame = tk.Frame(root, bg="#FFDEAD", bd=5, relief="groove")
frame.pack(pady=10, padx=10, fill="x")

# Vrch tabuľky
headers = ["Section Name", "Source Folder", "", "Destination Folder", "", "Actions"]
for col, text in enumerate(headers):
    lbl = tk.Label(frame, text=text, font=("Comic Sans MS", 12, "bold"), bg="#FFDAB9", fg="#8B0000", relief="ridge", bd=3, padx=3, pady=3)
    lbl.grid(row=0, column=col, padx=3, pady=3)

category_entries = []
add_category()  # pridať začiatočný zakladny riadok

# rám tlačidiel
button_frame = tk.Frame(root, bg="#FFEFD5")
button_frame.pack(pady=15)

tk.Button(button_frame, text="Add Category", command=add_category, bg="#32CD32", fg="white", font=("Comic Sans MS", 12, "bold"), relief="raised", bd=4).grid(row=0, column=0, padx=10) # Tlačidlo pridania kategorie
tk.Button(button_frame, text="Create Config", command=save_config, bg="#FF4500", fg="white", font=("Comic Sans MS", 12, "bold"), relief="raised", bd=4).grid(row=0, column=1, padx=10) # Tlačidko uloženia configu

root.mainloop() #Spusti toto šecko please please 🥺
