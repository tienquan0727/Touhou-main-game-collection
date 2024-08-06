from tkinter import *
from tkinter import messagebox
from tkinter import PhotoImage
from tkinter import ttk
from tkinter import filedialog
from tkcalendar import DateEntry
import json
import os
#cửa sổ chính
window = Tk()
window.iconbitmap(r"icon.ico")
window.title ("Touhou main game collection")
window.geometry("500x500")

#các hàm cho button
#_______________________________________________________Add_______________________________________________________
def add_game():
    if hasattr(save_game, 'save_window'):
        save_game.save_window.destroy()
    if not hasattr(add_game, 'add_window') or not add_game.add_window.winfo_exists():
        add_game.add_window = Toplevel(window)
        add_game.add_window.title("Add Game")

        # Tạo các label và entry cho các trường thông tin
        Label(add_game.add_window, text="Generation:").grid(row=0, column=0, padx=10, pady=5, sticky="e")
        generation_entry = ttk.Combobox(add_game.add_window, values=["Retro Era", "1st Windows Generation", "2nd Windows Generation", "3rd Windows Generation"])
        generation_entry.grid(row=0, column=1, padx=10, pady=5)
        generation_entry.current(3)

        Label(add_game.add_window, text="Part:").grid(row=1, column=0, padx=10, pady=5, sticky="e")
        part_entry = Entry(add_game.add_window, width=23)
        part_entry.grid(row=1, column=1, padx=10, pady=5)

        Label(add_game.add_window, text="Name:").grid(row=2, column=0, padx=10, pady=5, sticky="e")
        name_entry = Entry(add_game.add_window, width=23)
        name_entry.grid(row=2, column=1, padx=10, pady=5)

        Label(add_game.add_window, text="Type:").grid(row=3, column=0, padx=10, pady=5, sticky="e")
        type_entry = ttk.Combobox(add_game.add_window, values=["Classic Bullet Hell", "Versus Bullet Hell", "Bullet Hell Photography", "Bullet Hell Freezing", "Bullet Hell Boss Attack", "Side-Scroller", "Fighting", "Breakout"])
        type_entry.grid(row=3, column=1, padx=10, pady=5)
        type_entry.current(0)

        Label(add_game.add_window, text="Release(Date):").grid(row=4, column=0, padx=10, pady=5, sticky="e")
        release_date_entry = DateEntry(add_game.add_window, width=20, background='red', foreground='black', borderwidth=2)
        release_date_entry.grid(row=4, column=1, padx=10, pady=5)

        Label(add_game.add_window, text="Release(Place):").grid(row=5, column=0, padx=10, pady=5, sticky="e")
        release_place_entry = Entry(add_game.add_window, width=23)
        release_place_entry.grid(row=5, column=1, padx=10, pady=5)

        # next button
        Next_button = Button(add_game.add_window, text="Next", command=lambda: Next(generation_entry.get(), part_entry.get(),name_entry.get(), type_entry.get(), release_date_entry.get(), release_place_entry.get()))
        Next_button.grid(row=6, columnspan=2, padx=10, pady=5)

def Next(generation, part, name, type, release_date, release_place):
    add_game.add_window.destroy()
    if not hasattr(save_game, 'save_window') or not save_game.save_window.winfo_exists():
        save_game.save_window = Toplevel(window)
        save_game.save_window.title("Path")

        # Tạo Listbox để hiển thị đường dẫn thư mục
        pathbox = Listbox(save_game.save_window, width=50, height=1)
        pathbox.grid(row=0, column=0, padx=10, pady=10)

        # Nút để chọn thư mục
        location_button = Button(save_game.save_window, text="Location", command=lambda: Location(pathbox))
        location_button.grid(row=0, column=1, padx=10, pady=5)

        # Nút để lưu thông tin và đóng cửa sổ
        save_button = Button(save_game.save_window, text="Save", command=lambda: save_game(generation, part, name, type, release_date, release_place, pathbox.get(END)))
        save_button.grid(row=1, column=0, columnspan=2, padx=10, pady=5)

def Location(pathbox):
    selected_directory = filedialog.askopenfilename(title="Game Location")
    if selected_directory:
        pathbox.delete(0, END)
        pathbox.insert(END, selected_directory)

def save_game(generation, part, name, type, release_date, release_place, path):
    # Tạo một dictionary để lưu thông tin của trò chơi
    game_info = {
        "Generation": generation,
        "Part": part,
        "Name": name,
        "Type": type,
        "Release Date": release_date,
        "Release Place": release_place,
        "Path": path
    }
    game_file = open("games_info_database.txt", "a")
    json.dump(game_info, game_file)
    game_file.write("\n")
    game_file.close()
    save_game.save_window.destroy()
    messagebox.showinfo("Save Game", "Mục đã được thêm! (Vui lòng Refresh)")

#_______________________________________________________Edit_______________________________________________________

def edit_game():
    selected_index = listbox.curselection()
    if selected_index:
        game_file = open("games_info_database.txt", "r")
        selected_game = listbox.get(selected_index[0])
        for line in game_file:
            game_info = json.loads(line)
            game_name = f"Touhou {game_info['Part']}: {game_info['Name']}"
            if selected_game == game_name:
                game_generation = game_info['Generation']
                game_part = game_info['Part']
                game_name = game_info['Name']
                game_type = game_info['Type']
                game_release_date = game_info['Release Date']
                game_release_place = game_info['Release Place']
                path = game_info['Path']
                break
        game_file.close()

        if hasattr(save_game_e, 'save_window_e'):
            save_game_e.save_window_e.destroy()
        if not hasattr(edit_game, 'edit_window') or not edit_game.edit_window.winfo_exists():
            edit_game.edit_window = Toplevel(window)
            edit_game.edit_window.title("Edit Game")

            # Tạo các label và entry cho các trường thông tin
            Label(edit_game.edit_window, text="Generation:").grid(row=0, column=0, padx=10, pady=5, sticky="e")
            generation_entry = ttk.Combobox(edit_game.edit_window, values=["Retro Era", "1st Windows Generation", "2nd Windows Generation", "3rd Windows Generation"])
            generation_entry.grid(row=0, column=1, padx=10, pady=5)
            generation_entry.current(generation_entry["values"].index(game_generation))

            Label(edit_game.edit_window, text="Part:").grid(row=1, column=0, padx=10, pady=5, sticky="e")
            part_entry = Entry(edit_game.edit_window, width=23)
            part_entry.grid(row=1, column=1, padx=10, pady=5)
            part_entry.insert(0, game_part)

            Label(edit_game.edit_window, text="Name:").grid(row=2, column=0, padx=10, pady=5, sticky="e")
            name_entry = Entry(edit_game.edit_window, width=23)
            name_entry.grid(row=2, column=1, padx=10, pady=5)
            name_entry.insert(0, game_name)

            Label(edit_game.edit_window, text="Type:").grid(row=3, column=0, padx=10, pady=5, sticky="e")
            type_entry = ttk.Combobox(edit_game.edit_window, values=["Classic Bullet Hell", "Versus Bullet Hell", "Bullet Hell Photography", "Bullet Hell Freezing", "Bullet Hell Boss Attack", "Side-Scroller", "Fighting", "Breakout"])
            type_entry.grid(row=3, column=1, padx=10, pady=5)
            type_entry.current(type_entry["values"].index(game_type))

            Label(edit_game.edit_window, text="Release(Date):").grid(row=4, column=0, padx=10, pady=5, sticky="e")
            release_date_entry = DateEntry(edit_game.edit_window, width=20, background='red', foreground='white', borderwidth=2)
            release_date_entry.grid(row=4, column=1, padx=10, pady=5)
            release_date_entry.set_date(game_release_date)

            Label(edit_game.edit_window, text="Release(Place):").grid(row=5, column=0, padx=10, pady=5, sticky="e")
            release_place_entry = Entry(edit_game.edit_window, width=23)
            release_place_entry.grid(row=5, column=1, padx=10, pady=5)
            release_place_entry.insert(0, game_release_place)

            # next button
            Next_button = Button(edit_game.edit_window, text="Next", command=lambda: Next_e(selected_game, generation_entry.get(), part_entry.get(), name_entry.get(), type_entry.get(), release_date_entry.get(), release_place_entry.get(), path))
            Next_button.grid(row=6, columnspan=2, padx=10, pady=5)
    else:
        messagebox.showwarning("Warning", "Xin hãy chọn 1 mục!")



def Next_e(selected_game, generation, part, name, type, release_date, release_place, path):
    edit_game.edit_window.destroy()
    if not hasattr(save_game_e, 'save_window_e') or not save_game_e.save_window_e.winfo_exists():
        save_game_e.save_window_e = Toplevel(window)
        save_game_e.save_window_e.title("Change Path")

        # Tạo Listbox để hiển thị đường dẫn thư mục
        pathbox_e = Listbox(save_game_e.save_window_e, width=50, height=1)
        pathbox_e.grid(row=0, column=0, padx=10, pady=10)
        pathbox_e.insert(END, path)

        # Nút để chọn thư mục
        location_button_e = Button(save_game_e.save_window_e, text="Location", command=lambda: Location_e(pathbox_e))
        location_button_e.grid(row=0, column=1, padx=10, pady=5)

        # Nút để lưu thông tin và đóng cửa sổ
        save_button_e = Button(save_game_e.save_window_e, text="Save", command=lambda: save_game_e(selected_game, generation, part, name, type, release_date, release_place, pathbox_e.get(END)))
        save_button_e.grid(row=1, column=0, columnspan=2, padx=10, pady=5)

def Location_e(pathbox_e):
    selected_directory = filedialog.askopenfilename(title="Game Location")
    if selected_directory:
        pathbox_e.delete(0, END)
        pathbox_e.insert(END, selected_directory)

def save_game_e(selected_game, generation, part, name, type, release_date, release_place, path):
    # Tạo một dictionary để lưu thông tin của trò chơi
    game_info_dictionary = {
        "Generation": generation,
        "Part": part,
        "Name": name,
        "Type": type,
        "Release Date": release_date,
        "Release Place": release_place,
        "Path": path
    }
    updated_lines = []
    game_file = open("games_info_database.txt", "r")
    for line in game_file:
        game_info = json.loads(line)
        game_name = f"Touhou {game_info['Part']}: {game_info['Name']}"
        if selected_game == game_name:
            updated_lines.append(json.dumps(game_info_dictionary) + "\n")
        else:
            updated_lines.append(line)
    game_file.close()
    new_game_file = open("games_info_database.txt", "w")
    new_game_file.writelines(updated_lines)
    new_game_file.close()
    save_game_e.save_window_e.destroy()
    messagebox.showinfo("Edit Game", "Mục đã được chỉnh sửa! (Vui lòng Refresh)")

#_______________________________________________________Delete_______________________________________________________

def delete_game():
    updated_lines = []
    selected_index = listbox.curselection()
    if selected_index:
        xac_nhan = messagebox.askyesno("Delete Game", "Bạn có thật sự muốn xóa mục này không?")
        if xac_nhan:
            game_file = open("games_info_database.txt", "r")
            selected_game = listbox.get(selected_index[0])
            for line in game_file:
                game_info = json.loads(line)
                game_name = f"Touhou {game_info['Part']}: {game_info['Name']}"
                if selected_game == game_name:
                    continue
                else:
                    updated_lines.append(line)
            new_game_file = open("games_info_database.txt", "w")
            new_game_file.writelines(updated_lines)
            new_game_file.close()
            listbox.selection_clear(0, END)
            messagebox.showinfo("Delete Game", "Mục đã được xóa! (Vui lòng Refresh)")
        else:
            listbox.selection_clear(0, END)
    else:
        messagebox.showwarning("Warning", "Xin hãy chọn 1 mục!")


#_______________________________________________________Load_______________________________________________________

def load_game():
    selected_index = listbox.curselection()
    if selected_index:
        game_file = open("games_info_database.txt", "r")
        selected_game = listbox.get(selected_index[0])  # Lấy tên game từ index được chọn trong listbox
        for line in game_file:
            game_info = json.loads(line)
            game_name = f"Touhou {game_info['Part']}: {game_info['Name']}"
            if selected_game == game_name:
                game_path = game_info['Path']
                os.startfile(game_path)
                break
    else:
        messagebox.showwarning("Warning", "Xin hãy chọn 1 mục!")
    listbox.selection_clear(0, END)

#_______________________________________________________Path_______________________________________________________

def path_game():
    selected_index = listbox.curselection()
    if selected_index:
        game_file = open("games_info_database.txt", "r")
        selected_game = listbox.get(selected_index[0])  # Lấy tên game từ index được chọn trong listbox
        for line in game_file:
            game_info = json.loads(line)
            game_name = f"Touhou {game_info['Part']}: {game_info['Name']}"
            if selected_game == game_name:
                game_path = game_info['Path']
                parent_path = os.path.dirname(game_path)
                os.startfile(parent_path)
                break
        game_file.close()
    else:
        messagebox.showwarning("Warning", "Xin hãy chọn 1 mục!")

#____________________________________________________Category______________________________________________________

def game_category():
    if not hasattr(game_category, 'category_window') or not game_category.category_window.winfo_exists():
        game_category.category_window = Toplevel(window)
        game_category.category_window.title("Category")

        Label(game_category.category_window, text="Generation:").grid(row=0, column=0, padx=10, pady=5, sticky="e")
        generation_entry = ttk.Combobox(game_category.category_window, values=["All", "Retro Era", "1st Windows Generation", "2nd Windows Generation", "3rd Windows Generation"])
        generation_entry.grid(row=0, column=1, padx=10, pady=5)
        generation_entry.current(0)

        Label(game_category.category_window, text="Type:").grid(row=1, column=0, padx=10, pady=5, sticky="e")
        type_entry = ttk.Combobox(game_category.category_window, values=["All", "Classic Bullet Hell", "Versus Bullet Hell", "Bullet Hell Photography", "Bullet Hell Freezing", "Bullet Hell Boss Attack", "Side-Scroller", "Fighting", "Breakout"])
        type_entry.grid(row=1, column=1, padx=10, pady=5)
        type_entry.current(0)

        submit_button = Button(game_category.category_window, text="Submit", command=lambda: submit(generation_entry.get(), type_entry.get()))
        submit_button.grid(row=2, columnspan=2, padx=10, pady=5)

def submit(generation, type):
    game_category.category_window.destroy()
    game_file = open("games_info_database.txt", "r")
    game_list = []
    gen_name = generation
    type_name = type
    for line in game_file:
        game_info = json.loads(line)
        game_name = f"Touhou {game_info['Part']}: {game_info['Name']}"
        txts_generation = f"{game_info['Generation']}"
        txts_list = f"{game_info['Type']}"
        if gen_name == txts_generation and type_name == txts_list:
            listbox.delete(0, END)
            game_list.append(game_name)
        elif gen_name == "All" and type_name == txts_list:
            if type_name == txts_list:
                listbox.delete(0, END)
                game_list.append(game_name)
        elif gen_name == txts_generation and type_name == "All":
            if gen_name == txts_generation:
                listbox.delete(0, END)
                game_list.append(game_name)
    game_file.close()
    for game in game_list:
        listbox.insert(END, game)

#_____________________________________________________info______________________________________________________

def info():
    selected_index = listbox.curselection()
    if selected_index:
        if not hasattr(info, 'info_window') or not info.info_window.winfo_exists():
            info.info_window = Toplevel(window)
            info.info_window.title("Game Info")
        game_file = open("games_info_database.txt", "r")
        selected_game = listbox.get(selected_index[0])
        for line in game_file:
            game_info = json.loads(line)
            game_name = f"Touhou {game_info['Part']}: {game_info['Name']}"
            if selected_game == game_name:
                game_generation = game_info['Generation']
                game_part = game_info['Part']
                game_name = game_info['Name']
                game_type = game_info['Type']
                game_release = f"{game_info['Release Place']}, {game_info['Release Date']}"
                break
        game_file.close()

        Label(info.info_window, text="Generation:").grid(row=0, column=0, padx=10, pady=5, sticky="e")
        genbox = Listbox(info.info_window, width=23, height=1)
        genbox.grid(row=0, column=1, padx=10, pady=10)
        genbox.insert(END, game_generation)

        Label(info.info_window, text="Part:").grid(row=1, column=0, padx=10, pady=5, sticky="e")
        partbox = Listbox(info.info_window, width=23, height=1)
        partbox.grid(row=1, column=1, padx=10, pady=10)
        partbox.insert(END, game_part)

        Label(info.info_window, text="Name:").grid(row=2, column=0, padx=10, pady=5, sticky="e")
        namebox = Listbox(info.info_window, width=23, height=1)
        namebox.grid(row=2, column=1, padx=10, pady=10)
        namebox.insert(END, game_name)

        Label(info.info_window, text="Type:").grid(row=3, column=0, padx=10, pady=5, sticky="e")
        typebox = Listbox(info.info_window, width=23, height=1)
        typebox.grid(row=3, column=1, padx=10, pady=10)
        typebox.insert(END, game_type)

        Label(info.info_window, text="Release:").grid(row=4, column=0, padx=10, pady=5, sticky="e")
        releasebox = Listbox(info.info_window, width=23, height=1)
        releasebox.grid(row=4, column=1, padx=10, pady=10)
        releasebox.insert(END, game_release)

        listbox.selection_clear(0, END)
    else:
        thong_bao = messagebox.askokcancel("Thông báo", "Nếu như bạn không chọn 1 mục trước khi ấn nút thì bây giờ sẽ đi tới cửa sổ thông tin nhà phát triển!\n------------------------------------------------------------------------------\n                                      ( TIẾP TỤC? )\n------------------------------------------------------------------------------")
        if thong_bao:
            if not hasattr(info, 'info_window') or not info.info_window.winfo_exists():
                info.info_window = Toplevel(window)
                info.info_window.title("Thông Tin Sinh Viên")
                info.info_window.geometry("280x130")

            Label(info.info_window, text="Tên:").grid(row=0, column=0, padx=10, pady=5, sticky="e")
            tensv = Listbox(info.info_window, width=23, height=1)
            tensv.grid(row=0, column=1, padx=10, pady=10)
            tensv.insert(END, "Nguyễn Tiến Quân")

            Label(info.info_window, text="MSV:").grid(row=1, column=0, padx=10, pady=5, sticky="e")
            MSV = Listbox(info.info_window, width=23, height=1)
            MSV.grid(row=1, column=1, padx=10, pady=10)
            MSV.insert(END, "21115054120180")

            Label(info.info_window, text="Lớp SH:").grid(row=2, column=0, padx=10, pady=5, sticky="e")
            lopSH = Listbox(info.info_window, width=23, height=1)
            lopSH.grid(row=2, column=1, padx=10, pady=10)
            lopSH.insert(END, "21DT1")

#_____________________________________________________Refresh______________________________________________________
def refresh():
    listbox.delete(0, END)
    game_list = []
    game_file = open("games_info_database.txt", "r")
    for line in game_file:
        game_info = json.loads(line)
        game_name = f"Touhou {game_info['Part']}: {game_info['Name']}"
        game_list.append(game_name)
    for game in game_list:
        listbox.insert(END, game)
#______________________________________________________Search______________________________________________________
def search_item(): #thanh tìm kiếm
    search_term = search_entry.get().lower() #lấy từ thanh tìm kiếm
    listbox.delete(0, END)
    for item in game_list:
        if search_term in item.lower():
            listbox.insert(END, item)

# frame cho buttons bên phải và backgroud
button_frame = Frame(window, bg='grey', bd=5)
button_frame.pack(side=RIGHT, fill=Y)
background_image = PhotoImage(file="frame.png")
resized_image = background_image.subsample(6)
background_label = Label(button_frame, image=resized_image)
background_label.place(x=4.5, y=340)

#frame cho thanh tìm kiếm
search_frame = Frame(window)
search_frame.pack(side=TOP, fill=X)
search_entry = Entry(search_frame, width=40)
search_entry.pack(side=LEFT, padx=10, pady=10)

#frame cho nút refresh

# Listbox hiển thị danh sách game
listbox = Listbox(window, width=50, height=20)
listbox.pack(side=LEFT, fill=BOTH, expand=True)

#list các game được lấy từ file txt
game_list = []
game_file = open("games_info_database.txt", "r")
for line in game_file:
    game_info = json.loads(line)
    game_name = f"Touhou {game_info['Part']}: {game_info['Name']}"
    game_list.append(game_name)
for game in game_list:
    listbox.insert(END, game)
game_file.close()

#Button
b1 = Button(button_frame, text="Add", command=add_game, padx=10, width=10, height=2)
b2 = Button(button_frame, text="Edit", command=edit_game, padx=10, width=10, height=2)
b3 = Button(button_frame, text="Delete", command=delete_game, padx=10, width=10, height=2)
b4 = Button(button_frame, text="Load", command=load_game, padx=10, width=10, height=2)
b5 = Button(button_frame, text="Path", command=path_game, padx=10, width=10, height=2)
b6 = Button(button_frame, text="Category", command=game_category, padx=10, width=10, height=2)
b7 = Button(button_frame, text="Info", command=info, padx=10, width=10, height=2)
b8 = Button(button_frame, text="Refresh", command=refresh, bg="pink", activebackground="red",relief="raised", padx=10, width=10, height=2)
b9 = Button(search_frame, text="Search", command=search_item)
b1.pack()
b2.pack()
b3.pack()
b4.pack()
b5.pack()
b6.pack()
b7.pack()
b8.pack(side=BOTTOM)
b9.pack(side=LEFT, padx=10)
window.mainloop()