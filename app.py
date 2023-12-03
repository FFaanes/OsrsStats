import time
import OsrsStats
import customtkinter as cTk
from PIL import Image, ImageTk
import urllib
import io

# Functions
def get_user_stats():
    player_exist.configure(text="Checking...", text_color="goldenrod1")
    root.update()
    player = OsrsStats.OsrsPlayer(player_name.get()) # Create OsrsPlayer object

    skill_scroll_frame= cTk.CTkFrame(tabcontrol.tab("Skills"), width=window_width-(300+(frame_padding*4)), height=window_height-(frame_padding*3))
    skill_scroll_frame.pack()

    # If player exists
    if player.player_exists == True:
        player_name_button.configure(text="✓", text_color="spring green") # Change Button Style

        # Generating Skill Window
        player_exist.configure(text="Loading Skills...", text_color="goldenrod1")
        root.update()
        skill_per_row = 2 # Set Static Skill Page Variables
        player_skills = player.skills(raw=True) # Update Player Skills

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

        skill_rows = len(player_skills) / skill_per_row
        skill_ypadding = abs(((tabcontrol.tab("Skills")._current_height) - (skill_rows * rank_header._current_height * 1.2)) / (skill_rows * 2))

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
        root.update()
        player_clues = player.clues(raw=True) # Get clues
        player_other = player.other(raw=True) # Get other

        # Set Static Variables
        other_per_row = 3
        other_ypadding = 1.5

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
            clue_icon.grid(row=row_counter, column=column_counter, padx=(frame_padding*6, frame_padding), pady=other_ypadding)

            # Display Rank
            clue_rank = cTk.CTkLabel(other_scroll_frame, text=f"{player_clues[i][0]:,d}")
            clue_rank.grid(row=row_counter, column=column_counter+1, padx=frame_padding, pady=other_ypadding)

            # Display Score
            clue_score = cTk.CTkLabel(other_scroll_frame, text=f"{player_clues[i][1]:,d}")
            clue_score.grid(row=row_counter, column=column_counter+2, padx=frame_padding, pady=other_ypadding) 

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
            other_icon.grid(row=row_counter, column=column_counter, padx=(frame_padding*6, frame_padding), pady=other_ypadding)

            # Display Rank
            other_rank = cTk.CTkLabel(other_scroll_frame, text=f"{player_other[i][0]:,d}")
            other_rank.grid(row=row_counter, column=column_counter+1, padx=frame_padding, pady=other_ypadding)

            # Display Score
            other_level = cTk.CTkLabel(other_scroll_frame, text=f"{player_other[i][1]:,d}")
            other_level.grid(row=row_counter, column=column_counter+2, padx=frame_padding, pady=other_ypadding) 

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

# Application Variables
window_height = 440
window_width = 800
frame_padding = 4
cTk.set_default_color_theme("green")

# Application
root = cTk.CTk()
root.geometry(f"300x70")
#root.geometry(f"{window_width}x{window_height}")
root.resizable(width=False, height=False)
root.title("OSRS Tracker")

# Settings Frame (Left Frame)
settingsframe = cTk.CTkFrame(root, border_color="gray10",border_width=2, width=300-frame_padding, height=window_height-frame_padding)
settingsframe.grid_propagate(False)
settingsframe.pack_propagate(False)
settingsframe.grid(row=0, column=0, padx=frame_padding / 2, pady=frame_padding / 2)

player_name = cTk.CTkEntry(settingsframe, width=200, placeholder_text="Username")
player_name.grid(row=0, column=0, pady=(10,3), padx=(30,5))

player_name_button = cTk.CTkButton(settingsframe, text=">", width=30, fg_color="gray13", hover_color="gray10", command=get_user_stats)
player_name_button.grid(row=0, column=1, pady=(10,3))

player_exist = cTk.CTkLabel(settingsframe, text=" ")
player_exist.grid(row=1,column=0, columnspan=4, padx=(20,0))

# Highest XP stat left frame
highest_xp_frame = cTk.CTkFrame(settingsframe, height=60)
highest_xp_frame.grid(row=2, column=0, columnspan=5, pady=(10,20), padx=(20,0))

highest_xp = cTk.CTkLabel(highest_xp_frame, text="Highest XP", text_color="goldenrod1").grid(row=0, column=0, columnspan=4) # Header
highest_xp_icon = cTk.CTkLabel(highest_xp_frame, text="icon").grid(row=1, column=0, padx=frame_padding*5) # Icon
highest_xp_rank = cTk.CTkLabel(highest_xp_frame, text="rank").grid(row=1, column=1, padx=frame_padding*5) # Rank
highest_xp_level = cTk.CTkLabel(highest_xp_frame, text="level").grid(row=1, column=2, padx=frame_padding*5) # Level
highest_xp_xp = cTk.CTkLabel(highest_xp_frame, text="xp").grid(row=1, column=3, padx=frame_padding*5) # XP

# Lowest XP stat left frame
lowest_xp_frame = cTk.CTkFrame(settingsframe, height=60)
lowest_xp_frame.grid(row=3, column=0, columnspan=5, pady=(0,20), padx=(20,0))

lowest_xp = cTk.CTkLabel(lowest_xp_frame, text="Lowest XP", text_color="goldenrod1").grid(row=0, column=0, columnspan=4) # Header
lowest_xp_icon = cTk.CTkLabel(lowest_xp_frame, text="icon").grid(row=1, column=0, padx=frame_padding*5) # Icon
lowest_xp_rank = cTk.CTkLabel(lowest_xp_frame, text="rank").grid(row=1, column=1, padx=frame_padding*5) # Rank
lowest_xp_level = cTk.CTkLabel(lowest_xp_frame, text="level").grid(row=1, column=2, padx=frame_padding*5) # Level
lowest_xp_xp = cTk.CTkLabel(lowest_xp_frame, text="xp").grid(row=1, column=3, padx=frame_padding*5) # XP

# Content Page (Right Frame)
contentframe = cTk.CTkFrame(root, border_color="gray10",border_width=2, width=window_width - (300+frame_padding), height=window_height - frame_padding)
contentframe.grid_propagate(False)
contentframe.pack_propagate(False)
contentframe.grid(row=0, column=1, padx=frame_padding / 2, pady=frame_padding / 2)

# Adding tabs to content window
tabcontrol = cTk.CTkTabview(contentframe, width=window_width-(300+(frame_padding*4)), height=window_height-(frame_padding*3), fg_color="transparent")
tabcontrol.pack_propagate(False)
tabcontrol.pack()

tabcontrol.add("Skills")
skill_frame= cTk.CTkFrame(tabcontrol.tab("Skills"), width=window_width-(300+(frame_padding*4)), height=window_height-(frame_padding*3))
skill_frame.pack()

tabcontrol.add("Other")
other_scroll_frame = cTk.CTkScrollableFrame(tabcontrol.tab("Other"), width=window_width-(300+(frame_padding)), height=window_height-(frame_padding*3))
other_scroll_frame.pack()

tabcontrol.add("Monitoring")


root.mainloop()