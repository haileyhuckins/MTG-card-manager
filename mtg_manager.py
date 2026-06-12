import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox

# MTG Card Collection Manager
# CISP 71 / 71L Final - Hailey Huckins

# Create database and cards table
def connect_db():
    conn = sqlite3.connect("mtg_cards.db")
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS cards (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
                card_name TEXT,
                mana_cost TEXT,
                color TEXT,
                card_type TEXT,
                foil_status TEXT
        )
    """)

    conn.commit()
    conn.close()

# Add a new card record to the database
def add_record():
    # Validate user input before adding record
    if card_name_var.get() == "" or mana_cost_var.get() == "":
        messagebox.showwarning("Warning", "Card name and mana cost fields cannot be empty.")
        return
    
    if color_var.get() == "Select Color":
        messagebox.showwarning("Warning", "Please select a color.")
        return
    
    if card_type_var.get() == "Select Type":
        messagebox.showwarning("Warning", "Please select a card type.")
        return
    
    conn = sqlite3.connect("mtg_cards.db")
    cursor = conn.cursor()

    # Insert new record into database
    cursor.execute("""
        INSERT INTO cards (card_name, mana_cost, color, card_type, foil_status)
        VALUES (?, ?, ?, ?, ?)
    """, (
        card_name_var.get(),
        mana_cost_var.get(),
        color_var.get(),
        card_type_var.get(),
        foil_var.get()))

    conn.commit()
    conn.close()

    load_records()
    clear_fields()
    messagebox.showinfo("Success", "Card record added successfully.")

# Load all records from database into treeview
def load_records():
    # Clear old records from tree
    for row in tree.get_children():
        tree.delete(row)

    conn = sqlite3.connect("mtg_cards.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM cards")
    rows = cursor.fetchall()

    for row in rows:
        tree.insert("", tk.END, values=row)

    conn.close()

# Clear all input fields
def clear_fields():
    card_name_var.set("")
    mana_cost_var.set("")
    color_var.set("Select Color")
    card_type_var.set("Select Type")
    foil_var.set("Non-Foil")

# Clear button command
def clear_button():
    clear_fields()

# Display selected record in the input fields
def select_record(event):
    selected = tree.focus()
    values = tree.item(selected, "values")

    if values:
        card_name_var.set(values[1])
        mana_cost_var.set(values[2])
        color_var.set(values[3])
        card_type_var.set(values[4])
        foil_var.set(values[5])

# Update selected card record
def update_record():
    selected = tree.focus()
    values = tree.item(selected, "values")

    if not values:
        messagebox.showwarning("Warning", "Please select a record to update.")
        return
    
    conn = sqlite3.connect("mtg_cards.db")
    cursor = conn.cursor()

    # Update selected database record
    cursor.execute("""
            UPDATE cards
            SET card_name=?, mana_cost=?, color=?, card_type=?, foil_status=?
            WHERE id=?
        """,(
            card_name_var.get(),
            mana_cost_var.get(),
            color_var.get(),
            card_type_var.get(),
            foil_var.get(),
            values[0]))
    
    conn.commit()
    conn.close()

    load_records()
    clear_fields()
    messagebox.showinfo("Success", "Card record updated successfully.")

# Delete selected card record
def delete_record():
    selected = tree.focus()
    values = tree.item(selected, "values")

    if not values:
        messagebox.showwarning("Warning", "Please select a record to delete.")
        return
    
    conn = sqlite3.connect("mtg_cards.db")
    cursor = conn.cursor()

    # Delete selected record from database
    cursor.execute("DELETE FROM cards WHERE id=?", (values[0],))

    conn.commit()
    conn.close()

    load_records()
    clear_fields()
    messagebox.showinfo("Success", "Card record deleted successfully.")

# ---------------- MAIN WINDOW ----------------
root = tk.Tk()
root.title("MTG Card Collection Manager")
root.geometry("800x700")
# Title
tk.Label(root, text="🐉 MTG Card Collection Manager 🐉",
    font=("Calibri", 14, "bold")).grid(row=0, column=0, columnspan=3, pady=10)

connect_db()

# ---------------- VARIABLES ----------------
card_name_var = tk.StringVar()
mana_cost_var = tk.StringVar()
color_var = tk.StringVar(value="Select Color")
card_type_var = tk.StringVar(value="Select Type")
foil_var = tk.StringVar(value="Non-Foil")

# ---------------- FORM ----------------
# Card Name
tk.Label(root, text="Card Name").grid(row=1, column=0, padx=10, pady=10)
tk.Entry(root, textvariable=card_name_var, width=30).grid(row=1, column=1, padx=10, pady=10)
# Mana Cost
tk.Label(root, text="Mana Cost").grid(row=2, column=0, padx=10, pady=10)
tk.Entry(root, textvariable=mana_cost_var, width=8).grid(row=2, column=1, padx=10, pady=10)
# Color (OptionMenu)
tk.Label(root, text="Color").grid(row=3, column=0, padx=10, pady=10)
color_menu = tk.OptionMenu(root, color_var, "White", "Blue", "Black", "Red", "Green", "Colorless", "Multicolor")
color_menu.config(width=18)
color_menu.grid(row=3, column=1, padx=10, pady=10)
# Card Type (OptionMenu)
tk.Label(root, text="Card Type").grid(row=4, column=0, padx=10, pady=10)
type_menu = tk.OptionMenu(root, card_type_var, "Creature", "Instant", "Sorcery", "Artifact", "Enchantment", "Planeswalker", "Land")
type_menu.config(width=18)
type_menu.grid(row=4, column=1, padx=10, pady=10)
# Foil Status (RadioButtons)
tk.Label(root, text="Foil Status").grid(row=5, column=0, padx=10, pady=10)

tk.Radiobutton(root,text="Foil", variable=foil_var, value="Foil").grid(row=5, column=1, sticky="w")
tk.Radiobutton(root,text="Non-Foil", variable=foil_var, value="Non-Foil").grid(row=5, column=2, sticky="e")

# ---------------- BUTTONS ----------------
button_frame = tk.Frame(root)
button_frame.grid(row=6, column=0, columnspan=4, pady=15)

tk.Button(button_frame, text="Add Record", width=15, command=add_record).grid(row=0, column=0, padx=10)
tk.Button(button_frame, text="Update Record", width=15, command=update_record).grid(row=0, column=1, padx=10)
tk.Button(button_frame,text="Delete Record", width=15, command=delete_record).grid(row=0, column=2, padx=10)
tk.Button(button_frame, text="Clear Fields", width=15, command=clear_button).grid(row=0, column= 3, padx=10)

# ---------------- TREEVIEW ----------------
tree = ttk.Treeview(
    root,
    columns=("ID", "Card Name", "Mana Cost", "Color", "Card Type", "Foil Status"),
    show="headings")

tree.heading("ID", text="ID")
tree.heading("Card Name", text="Card Name")
tree.heading("Mana Cost", text="Mana Cost")
tree.heading("Color", text="Color")
tree.heading("Card Type", text="Card Type")
tree.heading("Foil Status", text="Foil Status")

tree.column("ID", width=40)
tree.column("Card Name", width=200)
tree.column("Mana Cost", width=90)
tree.column("Color", width=100)
tree.column("Card Type", width=120)
tree.column("Foil Status", width=100)

tree.grid(row=7, column=0, columnspan=4, padx=10, pady=20)

# Add vertical scrollbar to treeview
scrollbar = ttk.Scrollbar(root, orient="vertical", command=tree.yview)
tree.configure(yscrollcommand=scrollbar.set)
scrollbar.grid(row=7, column=4, sticky="ns", pady=20)

# Display selected treeview record in form fields
tree.bind("<<TreeviewSelect>>", select_record)

# Automatically load records when program starts
load_records()

root.mainloop()