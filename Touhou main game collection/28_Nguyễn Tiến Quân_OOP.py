from tkinter import *
from tkinter import messagebox
from tkinter import PhotoImage
from tkinter import ttk
from tkinter import filedialog
from tkcalendar import DateEntry
import json
import os

class TouhouGameCollectionApp:
    def __init__(self, root):
        self.window = root
        self.window.title("Touhou Main Game Collection")
        self.window.geometry("500x500")

        self.game_list = []
        self.load_games()

        self.create_widgets()

    def create_widgets(self):
        # Button frame
        self.button_frame = Frame(self.window, bg='grey', bd=5)
        self.button_frame.pack(side=RIGHT, fill=Y)

        # Search frame
        self.search_frame = Frame(self.window)
        self.search_frame.pack(side=TOP, fill=X)
        self.search_entry = Entry(self.search_frame, width=40)
        self.search_entry.pack(side=LEFT, padx=10, pady=10)

        # Listbox
        self.listbox = Listbox(self.window, width=50, height=20)
        self.listbox.pack(side=LEFT, fill=BOTH, expand=True)

        for game in self.game_list:
            self.listbox.insert(END, game)

        # Buttons
        buttons = [
            ("Add", self.add_game),
            ("Edit", self.edit_game),
            ("Delete", self.delete_game),
            ("Load", self.load_game),
            ("Path", self.path_game),
            ("Category", self.game_category),
            ("Info", self.info),
            ("Refresh", self.refresh, "pink"),
            ("Search", self.search_item, None, self.search_frame, LEFT)
        ]

        for btn in buttons:
            self.create_button(*btn)

    def create_button(self, text, command, bg=None, frame=None, side=TOP):
        if frame is None:
            frame = self.button_frame
        button = Button(frame, text=text, command=command, padx=10, width=10, height=2)
        if bg:
            button.config(bg=bg, activebackground="red", relief="raised")
        button.pack(side=side, padx=10, pady=5)

    def load_games(self):
        try:
            with open("games_info_database.txt", "r") as game_file:
                for line in game_file:
                    game_info = json.loads(line)
                    game_name = f"Touhou {game_info['Part']}: {game_info['Name']}"
                    self.game_list.append(game_name)
        except FileNotFoundError:
            pass

    def add_game(self):
        GameEntryWindow(self, "Add Game", self.save_game)

    def save_game(self, game_info, path):
        game_info["Path"] = path
        with open("games_info_database.txt", "a") as game_file:
            json.dump(game_info, game_file)
            game_file.write("\n")
        self.refresh()

    def edit_game(self):
        selected_index = self.listbox.curselection()
        if selected_index:
            game_name = self.listbox.get(selected_index[0])
            game_info = self.get_game_info(game_name)
            if game_info:
                GameEntryWindow(self, "Edit Game", self.save_edited_game, game_info)
        else:
            messagebox.showwarning("Warning", "Please select a game to edit.")

    def save_edited_game(self, updated_game_info, path):
        updated_game_info["Path"] = path
        updated_lines = []
        with open("games_info_database.txt", "r") as game_file:
            for line in game_file:
                game_info = json.loads(line)
                if updated_game_info["Name"] == game_info["Name"] and updated_game_info["Part"] == game_info["Part"]:
                    updated_lines.append(json.dumps(updated_game_info) + "\n")
                else:
                    updated_lines.append(line)
        with open("games_info_database.txt", "w") as game_file:
            game_file.writelines(updated_lines)
        self.refresh()

    def delete_game(self):
        selected_index = self.listbox.curselection()
        if selected_index:
            confirm = messagebox.askyesno("Delete Game", "Are you sure you want to delete this game?")
            if confirm:
                game_name = self.listbox.get(selected_index[0])
                updated_lines = []
                with open("games_info_database.txt", "r") as game_file:
                    for line in game_file:
                        game_info = json.loads(line)
                        if game_name != f"Touhou {game_info['Part']}: {game_info['Name']}":
                            updated_lines.append(line)
                with open("games_info_database.txt", "w") as game_file:
                    game_file.writelines(updated_lines)
                self.refresh()
        else:
            messagebox.showwarning("Warning", "Please select a game to delete.")

    def load_game(self):
        selected_index = self.listbox.curselection()
        if selected_index:
            game_name = self.listbox.get(selected_index[0])
            game_info = self.get_game_info(game_name)
            if game_info:
                os.startfile(game_info['Path'])
            self.listbox.selection_clear(0, END)

    def path_game(self):
        selected_index = self.listbox.curselection()
        if selected_index:
            game_name = self.listbox.get(selected_index[0])
            game_info = self.get_game_info(game_name)
            if game_info:
                os.startfile(os.path.dirname(game_info['Path']))

    def game_category(self):
        CategoryWindow(self)

    def info(self):
        selected_index = self.listbox.curselection()
        if selected_index:
            game_name = self.listbox.get(selected_index[0])
            game_info = self.get_game_info(game_name)
            if game_info:
                InfoWindow(self, game_info)
        else:
            InfoWindow(self)

    def refresh(self):
        self.listbox.delete(0, END)
        self.game_list.clear()
        self.load_games()
        for game in self.game_list:
            self.listbox.insert(END, game)

    def search_item(self):
        search_term = self.search_entry.get().lower()
        self.listbox.delete(0, END)
        for item in self.game_list:
            if search_term in item.lower():
                self.listbox.insert(END, item)

    def get_game_info(self, game_name):
        try:
            with open("games_info_database.txt", "r") as game_file:
                for line in game_file:
                    game_info = json.loads(line)
                    if game_name == f"Touhou {game_info['Part']}: {game_info['Name']}":
                        return game_info
        except FileNotFoundError:
            pass
        return None

class GameEntryWindow:
    def __init__(self, parent, title, save_callback, game_info=None):
        self.parent = parent
        self.save_callback = save_callback
        self.game_info = game_info

        self.window = Toplevel(parent.window)
        self.window.title(title)

        # Create labels and entries
        Label(self.window, text="Generation:").grid(row=0, column=0, padx=10, pady=5, sticky="e")
        self.generation_entry = ttk.Combobox(self.window, values=["Retro Era", "1st Windows Generation", "2nd Windows Generation", "3rd Windows Generation"])
        self.generation_entry.grid(row=0, column=1, padx=10, pady=5)
        if game_info:
            self.generation_entry.set(game_info["Generation"])

        Label(self.window, text="Part:").grid(row=1, column=0, padx=10, pady=5, sticky="e")
        self.part_entry = Entry(self.window, width=23)
        self.part_entry.grid(row=1, column=1, padx=10, pady=5)
        if game_info:
            self.part_entry.insert(0, game_info["Part"])

        Label(self.window, text="Name:").grid(row=2, column=0, padx=10, pady=5, sticky="e")
        self.name_entry = Entry(self.window, width=23)
        self.name_entry.grid(row=2, column=1, padx=10, pady=5)
        if game_info:
            self.name_entry.insert(0, game_info["Name"])

        Label(self.window, text="Type:").grid(row=3, column=0, padx=10, pady=5, sticky="e")
        self.type_entry = ttk.Combobox(self.window, values=["Classic Bullet Hell", "Versus Bullet Hell", "Bullet Hell Photography", "Bullet Hell Freezing", "Bullet Hell Boss Attack", "Side-Scroller", "Fighting", "Breakout"])
        self.type_entry.grid(row=3, column=1, padx=10, pady=5)
        if game_info:
            self.type_entry.set(game_info["Type"])

        Label(self.window, text="Release(Date):").grid(row=4, column=0, padx=10, pady=5, sticky="e")
        self.release_date_entry = DateEntry(self.window, width=20, background='red', foreground='white', borderwidth=2)
        self.release_date_entry.grid(row=4, column=1, padx=10, pady=5)
        if game_info:
            self.release_date_entry.set_date(game_info["Release(Date)"])

        Label(self.window, text="Developer:").grid(row=5, column=0, padx=10, pady=5, sticky="e")
        self.developer_entry = Entry(self.window, width=23)
        self.developer_entry.grid(row=5, column=1, padx=10, pady=5)
        if game_info:
            self.developer_entry.insert(0, game_info["Developer"])

        Label(self.window, text="Publisher:").grid(row=6, column=0, padx=10, pady=5, sticky="e")
        self.publisher_entry = Entry(self.window, width=23)
        self.publisher_entry.grid(row=6, column=1, padx=10, pady=5)
        if game_info:
            self.publisher_entry.insert(0, game_info["Publisher"])

        Label(self.window, text="Path:").grid(row=7, column=0, padx=10, pady=5, sticky="e")
        self.path_entry = Entry(self.window, width=23)
        self.path_entry.grid(row=7, column=1, padx=10, pady=5)
        if game_info:
            self.path_entry.insert(0, game_info["Path"])

        # Browse button for path
        Button(self.window, text="Browse", command=self.browse_path).grid(row=7, column=2, padx=5, pady=5)

        # Save button
        Button(self.window, text="Save", command=self.save_game).grid(row=8, column=0, columnspan=3, pady=10)

    def browse_path(self):
        path = filedialog.askopenfilename()
        if path:
            self.path_entry.delete(0, END)
            self.path_entry.insert(0, path)

    def save_game(self):
        game_info = {
            "Generation": self.generation_entry.get(),
            "Part": self.part_entry.get(),
            "Name": self.name_entry.get(),
            "Type": self.type_entry.get(),
            "Release(Date)": self.release_date_entry.get(),
            "Developer": self.developer_entry.get(),
            "Publisher": self.publisher_entry.get()
        }
        path = self.path_entry.get()
        self.save_callback(game_info, path)
        self.window.destroy()

class CategoryWindow:
    def __init__(self, parent):
        self.window = Toplevel(parent.window)
        self.window.title("Game Category")
        self.window.geometry("300x300")

        categories = [
            "Retro Era",
            "1st Windows Generation",
            "2nd Windows Generation",
            "3rd Windows Generation",
            "Classic Bullet Hell",
            "Versus Bullet Hell",
            "Bullet Hell Photography",
            "Bullet Hell Freezing",
            "Bullet Hell Boss Attack",
            "Side-Scroller",
            "Fighting",
            "Breakout"
        ]

        Label(self.window, text="Categories:", font=("Helvetica", 16)).pack(pady=10)
        for category in categories:
            Label(self.window, text=category).pack(anchor="w")

class InfoWindow:
    def __init__(self, parent, game_info=None):
        self.window = Toplevel(parent.window)
        self.window.title("Info")
        self.window.geometry("400x200")

        if game_info:
            info_text = (
                f"Name: {game_info['Name']}\n"
                f"Part: {game_info['Part']}\n"
                f"Generation: {game_info['Generation']}\n"
                f"Type: {game_info['Type']}\n"
                f"Release(Date): {game_info['Release(Date)']}\n"
                f"Developer: {game_info['Developer']}\n"
                f"Publisher: {game_info['Publisher']}\n"
                f"Path: {game_info['Path']}\n"
            )
            Label(self.window, text=info_text, justify=LEFT).pack(pady=10)
        else:
            info_text = (
                "Touhou Main Game Collection\n"
                "Created by: Satoshi Watanabe\n"
                "This app helps you manage and launch Touhou games easily.\n"
                "Use the buttons to add, edit, or delete game entries."
            )
            Label(self.window, text=info_text, justify=LEFT).pack(pady=10)

if __name__ == "__main__":
    root = Tk()
    app = TouhouGameCollectionApp(root)
    root.mainloop()
