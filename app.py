import time
import OsrsStats
import customtkinter as cTk

# Functions
def get_user_stats():
    player = OsrsStats.OsrsPlayer(player_name.get())
    if player.player_exists == True:
        player_name_button.configure(text="✓", text_color="spring green")
        player_exist.configure(text=f"{player.username} Loaded!", text_color="spring green")
    else:
        player_name_button.configure(text="✗", text_color="Red")
        player_exist.configure(text=f"{player.username} Not Found!", text_color="Red")

# Application Variables
window_height = 400
window_width = 800
frame_padding = 4

# Application
root = cTk.CTk()
root.geometry(f"{str(window_width)}x{str(window_height)}")
root.resizable(width=False, height=False)
root.title("OSRS Tracker")

# Settings Frame (Left Frame)
settingsframe = cTk.CTkFrame(root, border_color="gray10",border_width=2, width=300-frame_padding, height=window_height-frame_padding)
settingsframe.grid_propagate(False)
settingsframe.grid(row=0, column=0, padx=frame_padding / 2, pady=frame_padding / 2)

player_name = cTk.CTkEntry(settingsframe, width=200, placeholder_text="Username")
player_name.grid(row=0, column=0, pady=(10,3), padx=(40,5))

player_name_button = cTk.CTkButton(settingsframe, text=">", width=30, fg_color="gray13", hover_color="gray10", command=get_user_stats)
player_name_button.grid(row=0, column=1, pady=(10,3))

player_exist = cTk.CTkLabel(settingsframe, text=" ")
player_exist.grid(row=1,column=0,columnspan=2)

# Content Page (Right Frame)
contentframe = cTk.CTkFrame(root, border_color="gray10",border_width=2,width=window_width - (300+frame_padding), height=window_height - frame_padding)
contentframe.grid_propagate(False)
contentframe.grid(row=0, column=1, padx=frame_padding / 2, pady=frame_padding / 2)

tabcontrol = cTk.CTkTabview(contentframe)

tabcontrol.add("Skills")
tabcontrol.add("Other")
tabcontrol.add("Monitoring")

root.mainloop()