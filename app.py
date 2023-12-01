import OsrsStats
import customtkinter as cTk


# Application
root = cTk.CTk()
root.geometry("800x400")
root.resizable(width=False, height=False)
root.title("OSRS Player Lookup")

settingsframe = cTk.CTkFrame(root, border_color="red",border_width=2, width=300, height=200)
settingsframe.grid_propagate(False)
settingsframe.grid(row=0, column=0)

player_name = cTk.CTkEntry(settingsframe, width=200, placeholder_text="Username")
player_name.grid(row=0, column=0, pady=10, padx=(40,5))

player_name_button = cTk.CTkButton(settingsframe, text=">", width=30)
player_name_button.grid(row=0, column=1)

player_exist = cTk.CTkLabel(settingsframe,text="Please Enter Username")
player_exist.grid(row=1,column=0)

# Display Content
contentframe = cTk.CTkFrame(root, border_color="green",border_width=2,width=500, height=200)
contentframe.grid_propagate(False)
contentframe.grid(row=0, column=1)

root.mainloop()