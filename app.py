import time
import OsrsStats
import customtkinter as cTk
from PIL import Image, ImageTk
import urllib
import io

# Functions
def get_user_stats():
    player_exist.configure(text="Checking...", text_color="goldenrod1") # Change status text
    player_exist.update() # Update the text
    player = OsrsStats.OsrsPlayer(player_name.get()) # Create OsrsPlayer object

    try:
        for child in skill_frame.winfo_children():
            child.destroy()
        for child in other_scroll_frame.winfo_children():
            child.destroy()
    except:
        pass

    #--- Check if player exists ---
    if player.player_exists == True:
        player_name_button.configure(text="✓", text_color="spring green") # Change Button Style

        # Generating Skill Window
        player_exist.configure(text="Loading Skills...", text_color="goldenrod1")
        player_exist.update()
        skill_per_row = 2 # Set Static Skill Page Variables
        player_skills = player.skills(raw=True) # Update Player Skills

        # ------- Highest xp left panel ---------
        highest_xp_icon_request = urllib.request.urlopen(player_skills[player.highest_xp[0]][3]).read()
        highest_xp_icon_image = Image.open(io.BytesIO(highest_xp_icon_request))
        highest_xp_icon_image = cTk.CTkImage(highest_xp_icon_image)

        highest_xp_icon.configure(image=highest_xp_icon_image)
        highest_xp_rank.configure(text=player_skills[player.highest_xp[0]][0])
        highest_xp_level.configure(text=player_skills[player.highest_xp[0]][1])
        highest_xp_xp.configure(text=player_skills[player.highest_xp[0]][2])

        # ------- Lowest xp left panel ---------
        lowest_xp_icon_request = urllib.request.urlopen(player_skills[player.lowest_xp[0]][3]).read()
        lowest_xp_icon_image = Image.open(io.BytesIO(lowest_xp_icon_request))
        lowest_xp_icon_image = cTk.CTkImage(lowest_xp_icon_image)

        lowest_xp_icon.configure(image=lowest_xp_icon_image)
        lowest_xp_rank.configure(text=player_skills[player.lowest_xp[0]][0])
        lowest_xp_level.configure(text=player_skills[player.lowest_xp[0]][1])
        lowest_xp_xp.configure(text=player_skills[player.lowest_xp[0]][2])

        # Creating Headers
        for i in range(skill_per_row):
            # Rank
            rank_header = cTk.CTkLabel(skill_frame, text="Rank", text_color="spring green")
            rank_header.grid(row=0, column=i*4+1)
            # Level
            level_header = cTk.CTkLabel(skill_frame, text="Level", text_color="spring green")
            level_header.grid(row=0, column=i*4+2)
            # XP
            xp_header = cTk.CTkLabel(skill_frame, text="XP", text_color="spring green")
            xp_header.grid(row=0, column=i*4+3)

        # Generating stat display
        column_counter = 0
        row_counter = 1

        skill_ypadding = 1

        for i in player_skills: # Loop over all elements in skill dictionary
            if player_skills[i][0] == "Unknown": # If player has no overall rank
                continue # Skip to next element in loop
            
            # Request icon from highscore page
            skill_icon_request = urllib.request.urlopen(player_skills[i][3]).read()
            skill_icon_image = Image.open(io.BytesIO(skill_icon_request))
            skill_icon_image = cTk.CTkImage(skill_icon_image)

            # Display Icon
            skill_icon = cTk.CTkLabel(skill_frame, image=skill_icon_image, text=" ")
            skill_icon.grid(row=row_counter, column=column_counter, padx=(frame_padding*6, frame_padding), pady=skill_ypadding)

            # Display Rank
            skill_rank = cTk.CTkLabel(skill_frame, text=f"{player_skills[i][0]:,d}")
            skill_rank.grid(row=row_counter, column=column_counter+1, padx=frame_padding, pady=skill_ypadding)

            # Display Level
            skill_level = cTk.CTkLabel(skill_frame, text=f"{player_skills[i][1]:,d}")
            skill_level.grid(row=row_counter, column=column_counter+2, padx=frame_padding, pady=skill_ypadding) 

            # Display XP
            skill_xp = cTk.CTkLabel(skill_frame, text=f"{player_skills[i][2]:,d}")
            skill_xp.grid(row=row_counter, column=column_counter+3, padx=frame_padding, pady=skill_ypadding) 

            # Evere skill uses 4 columns, when this reaches the skills per row
            # Increment the row by 1
            column_counter += 4
            if column_counter == skill_per_row*4:
                row_counter += 1
                column_counter = 0

        # Update Other Page
        player_exist.configure(text="Loading Other...", text_color="goldenrod1")
        player_exist.update()
        player_clues = player.clues(raw=True) # Get clues
        player_other = player.other(raw=True) # Get other

        # Set Static Variables
        other_per_row = 3

        # Creating Headers
        for i in range(other_per_row):
            # Rank
            rank_header = cTk.CTkLabel(other_scroll_frame, text="Rank", text_color="spring green")
            rank_header.grid(row=0, column=i*3+1)
            # Score
            score_header = cTk.CTkLabel(other_scroll_frame, text="Score", text_color="spring green")
            score_header.grid(row=0, column=i*3+2)

        # Generating stat display
        column_counter = 0
        row_counter = 1
        for i in player_clues: # Loop over all elements in skill dictionary
            
            # Request icon from highscore page
            clue_icon_request = urllib.request.urlopen(player_clues[i][2]).read()
            clue_icon_image = Image.open(io.BytesIO(clue_icon_request))
            clue_icon_image = cTk.CTkImage(clue_icon_image)

            # Display Icon
            clue_icon = cTk.CTkLabel(other_scroll_frame, image=clue_icon_image, text=" ")
            clue_icon.grid(row=row_counter, column=column_counter, padx=(frame_padding*6, frame_padding), pady=skill_ypadding)

            # Display Rank
            clue_rank = cTk.CTkLabel(other_scroll_frame, text=f"{player_clues[i][0]:,d}")
            clue_rank.grid(row=row_counter, column=column_counter+1, padx=frame_padding, pady=skill_ypadding)

            # Display Score
            clue_score = cTk.CTkLabel(other_scroll_frame, text=f"{player_clues[i][1]:,d}")
            clue_score.grid(row=row_counter, column=column_counter+2, padx=frame_padding, pady=skill_ypadding) 

            # Evere skill uses 4 columns, when this reaches the per row
            # Increment the row by 1
            column_counter += 3
            if column_counter == other_per_row*3:
                row_counter += 1
                column_counter = 0
        
        for i in player_other: # Loop over all elements in skill dictionary
            # Request icon from highscore page
            other_icon_request = urllib.request.urlopen(player_other[i][2]).read()
            other_icon_image = Image.open(io.BytesIO(other_icon_request))
            other_icon_image = cTk.CTkImage(other_icon_image)

            # Display Icon
            other_icon = cTk.CTkLabel(other_scroll_frame, image=other_icon_image, text=" ")
            other_icon.grid(row=row_counter, column=column_counter, padx=(frame_padding*6, frame_padding), pady=skill_ypadding)

            # Display Rank
            other_rank = cTk.CTkLabel(other_scroll_frame, text=f"{player_other[i][0]:,d}")
            other_rank.grid(row=row_counter, column=column_counter+1, padx=frame_padding, pady=skill_ypadding)

            # Display Score
            other_level = cTk.CTkLabel(other_scroll_frame, text=f"{player_other[i][1]:,d}")
            other_level.grid(row=row_counter, column=column_counter+2, padx=frame_padding, pady=skill_ypadding) 

            # Evere skill uses 4 columns, when this reaches the per row
            # Increment the row by 1
            column_counter += 3
            if column_counter == other_per_row*3:
                row_counter += 1
                column_counter = 0

        player_exist.configure(text=f"{player.username} Loaded!", text_color="spring green") # Display success message 
        root.geometry(f"{str(window_width)}x{str(window_height)}") # Expand window to show statistics
    # If player does not exist.
    else:
        player_name_button.configure(text="✗", text_color="Red")
        player_exist.configure(text=f"{player.username} Not Found!", text_color="Red")


# ------------------------- Application Setup ---------------------------------------
#------ Application Variables ----------
window_height = 440
window_width = 800
frame_padding = 4
cTk.set_default_color_theme("green")

root = cTk.CTk()
root.geometry(f"300x70")
#root.geometry(f"{window_width}x{window_height}")
root.resizable(width=False, height=False)
root.title("OSRS Tracker")


#------------------------ Settings Frame (Left Frame) -------------------------------
settingsframe = cTk.CTkFrame(root, border_color="gray10",border_width=2, width=300-frame_padding, height=window_height-frame_padding)
settingsframe.grid_propagate(False)
settingsframe.pack_propagate(False)
settingsframe.grid(row=0, column=0, padx=frame_padding / 2, pady=frame_padding / 2)

# Entry for username
player_name = cTk.CTkEntry(settingsframe, width=200, placeholder_text="Username")
player_name.grid(row=0, column=0, pady=(10,3), padx=(30,5))

# Button to submit username
player_name_button = cTk.CTkButton(settingsframe, text=">", width=30, fg_color="gray13", hover_color="gray10", command=get_user_stats)
player_name_button.grid(row=0, column=1, pady=(10,3))

# Text below entry field displaying status messages.
player_exist = cTk.CTkLabel(settingsframe, text=" ")
player_exist.grid(row=1,column=0, columnspan=4, padx=(20,0))

# ---------- Highest XP stat left frame ------------
highest_xp_frame = cTk.CTkFrame(settingsframe, height=60)
highest_xp_frame.grid(row=2, column=0, columnspan=2, pady=(10,20), padx=(20,0))

highest_xp = cTk.CTkLabel(highest_xp_frame,width=50, text="Highest XP", text_color="goldenrod1").grid(row=0, column=0, columnspan=4) # Header

highest_xp_icon = cTk.CTkLabel(highest_xp_frame, text=" ")
highest_xp_icon.grid(row=1, column=0, padx=frame_padding*3) # Icon

highest_xp_rank = cTk.CTkLabel(highest_xp_frame, text="rank")
highest_xp_rank.grid(row=1, column=1, padx=frame_padding*3) # Rank

highest_xp_level = cTk.CTkLabel(highest_xp_frame, text="level")
highest_xp_level.grid(row=1, column=2, padx=frame_padding*3) # Level

highest_xp_xp = cTk.CTkLabel(highest_xp_frame, text="xp")
highest_xp_xp.grid(row=1, column=3, padx=frame_padding*3) # XP

# --------- Lowest XP stat left frame -------------
lowest_xp_frame = cTk.CTkFrame(settingsframe, height=60)
lowest_xp_frame.grid(row=3, column=0, columnspan=2, pady=(0,20), padx=(20,0))

lowest_xp = cTk.CTkLabel(lowest_xp_frame, text="Lowest XP", text_color="goldenrod1").grid(row=0, column=0, columnspan=4) # Header
lowest_xp_icon = cTk.CTkLabel(lowest_xp_frame, text=" ")
lowest_xp_icon.grid(row=1, column=0, padx=frame_padding*3) # Icon

lowest_xp_rank = cTk.CTkLabel(lowest_xp_frame, text="rank")
lowest_xp_rank.grid(row=1, column=1, padx=frame_padding*3) # Rank

lowest_xp_level = cTk.CTkLabel(lowest_xp_frame, text="level")
lowest_xp_level.grid(row=1, column=2, padx=frame_padding*3) # Level

lowest_xp_xp = cTk.CTkLabel(lowest_xp_frame, text="xp")
lowest_xp_xp.grid(row=1, column=3, padx=frame_padding*3) # XP


# --------- Average level left frame -------------
average_level_frame = cTk.CTkFrame(settingsframe, height=60)
average_level_frame.grid(row=4, column=0, columnspan=2, pady=(0,20), padx=(20,0))

average_level = cTk.CTkLabel(average_level_frame, text="Average Level", text_color="goldenrod1").grid(row=0, column=0, columnspan=1) # Header
average_level_icon = cTk.CTkLabel(average_level_frame, text=" ")
average_level_icon.grid(row=1, column=0, padx=frame_padding*3) # Icon

average_level_level = cTk.CTkLabel(average_level_frame, text="level")
average_level_level.grid(row=1, column=1, padx=frame_padding*3) # Rank






# ---------------------- Content Page (Right Frame) -----------------------
contentframe = cTk.CTkFrame(root, border_color="gray10",border_width=2, width=window_width - (300+frame_padding), height=window_height - frame_padding)
contentframe.grid_propagate(False)
contentframe.pack_propagate(False)
contentframe.grid(row=0, column=1, padx=frame_padding / 2, pady=frame_padding / 2)

#-------- Adding tabs to content window ----------
tabcontrol = cTk.CTkTabview(contentframe, width=window_width-(300+(frame_padding*4)), height=window_height-(frame_padding*3), fg_color="transparent")
tabcontrol.pack_propagate(False)
tabcontrol.pack()

tabcontrol.add("Skills")
skill_frame = cTk.CTkFrame(tabcontrol.tab("Skills"), width=window_width-(300+(frame_padding*4)), height=window_height-(frame_padding*3))
skill_frame.pack()

tabcontrol.add("Other")
other_scroll_frame = cTk.CTkScrollableFrame(tabcontrol.tab("Other"), width=window_width-(300+(frame_padding)), height=window_height-(frame_padding*3))
other_scroll_frame.pack()

tabcontrol.add("Monitoring")


root.mainloop()