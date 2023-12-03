import time
import OsrsStats
import customtkinter as cTk
from PIL import Image, ImageTk
import urllib
import io
import datetime

# TEST ADDS
def add_level():
    try:
        player._add_skill_level(add_level_input.get(), 1)
    except:
        pass

def add_xp():
    try:
        player._add_skill_xp(add_xp_input.get(),1000)
    except:
        pass

def add_clue():
    try:
        player._add_clue_count(add_clue_input.get(),1)
    except:
        pass    

def add_other():
    try:
        player._add_other_count(add_other_input.get(),1)
    except:
        pass

def refresh_stats():
    changes = player.compare()
    if len(changes) != 0:
        for change in changes:
            change_frame = cTk.CTkFrame(monitoring_scroll_frame, fg_color="gray10", width=450, height=30) # Create frame for change
            change_frame.grid_propagate(False) # Keep shape
            change_frame.grid(row=player.__changes_counter, column=0, columnspan=4)

            # Timestamp for change
            change_time = cTk.CTkLabel(change_frame, text=f"{datetime.datetime.now().hour}:{datetime.datetime.now().strftime('%M')} : ", text_color="gray30")
            change_time.grid(row=0, column=0, padx=(5,5))

            # Find icon depending on if it is a level, xp, clue or other change
            if changes[change][0] == "level" or changes[change][0] == "xp":
                change_icon_image = cTk.CTkImage(Image.open(io.BytesIO(urllib.request.urlopen(player_skills[change][3]).read())))
            elif changes[change][0] == "clue":
                change_icon_image = cTk.CTkImage(Image.open(io.BytesIO(urllib.request.urlopen(player_clues[change][2]).read())))
            else:
                change_icon_image = cTk.CTkImage(Image.open(io.BytesIO(urllib.request.urlopen(player_other[change][2]).read())))
            change_icon = cTk.CTkLabel(change_frame, text=" ", image=change_icon_image, bg_color="transparent")
            change_icon.grid(row=0, column=1, padx=3)

            # Name of activity
            activity_text = cTk.CTkLabel(change_frame, text=change.capitalize(), text_color="spring green")
            activity_text.grid(row=0, column=2, padx=5)

            # Increased by text
            change_text = cTk.CTkLabel(change_frame, text=" increased ")
            change_text.grid(row=0, column=3, padx=3)

            # Check what suffix of change, level/levels, clue/clues etc.
            if changes[change][0] == "level":
                level_or_levels ="levels" if changes[change][1] > 1 else "level"
                change_amount = cTk.CTkLabel(change_frame, text=f"{changes[change][1]} {level_or_levels}", text_color="spring green")
            elif changes[change][0] == "xp":
                change_amount = cTk.CTkLabel(change_frame, text=f"{changes[change][1]:,d} xp", text_color="spring green")
            elif changes[change][0] == "clue":
                clue_or_clues ="clues" if changes[change][1] > 1 else "clue"
                change_amount = cTk.CTkLabel(change_frame, text=f"{changes[change][1]} {clue_or_clues}", text_color="spring green")
            else:
                change_amount = cTk.CTkLabel(change_frame, text=f"{changes[change][1]} score", text_color="spring green")

            # pack change + suffix   
            change_amount.grid(row=0, column=4, padx=4)

            # Get level, xp, clue or other before and after with arrow between
            if changes[change][0] == "level" or changes[change][0] == "xp":
                if changes[change][0] == "level":
                    old_new = cTk.CTkLabel(change_frame, text=f"{player_skills[change][1]} ➜ {player_skills[change][1] + changes[change][1]}")
                    player_skills[change][1] += changes[change][1]
                else:
                    new_xp = player_skills[change][2] + changes[change][1]
                    old_new = cTk.CTkLabel(change_frame, text=f"{player_skills[change][2]:,d} ➜ {new_xp:,d}")
                    player_skills[change][2] += changes[change][1]

            elif changes[change][0] == "clue":
                old_new = cTk.CTkLabel(change_frame, text=f"{player_clues[change][1]} ➜ {player_clues[change][1] + changes[change][1]}")
                player_clues[change][1] += changes[change][1]

            else:
                old_new = cTk.CTkLabel(change_frame, text=f"{player_other[change][1]} ➜ {player_other[change][1] + changes[change][1]}")
                player_other[change][1] += changes[change][1]
            
            # Pack old -> new label
            old_new.grid(row=0, column=5, padx=5)

            # Increase row counter so next frame will be on the next row.
            player.__changes_counter += 1


# Functions
def get_user_stats():
    player_exist.configure(text="Checking...", text_color="goldenrod1") # Change status text
    player_exist.update() # Update the text
    global player
    player = OsrsStats.OsrsPlayer(player_name.get()) # Create OsrsPlayer object
    player.__changes_counter = 0
    try:
        for child in skill_frame.winfo_children():
            child.destroy()
        for child in other_scroll_frame.winfo_children():
            child.destroy()
    except:
        pass

    #--- Check if player exists ---
    if player.player_exists == True:

        # Display Icons or have placeholder text (increase loading time for testing)
        displayico = True

        player_name_button.configure(text="✓", text_color="spring green") # Change Button Style

        # Generating Skill Window
        player_exist.configure(text="Loading Skills...", text_color="goldenrod1")
        player_exist.update()
        skill_per_row = 2 # Set Static Skill Page Variables

        global player_skills
        player_skills = player.skills(raw=True) # Update Player Skills

        # ------- Highest xp left panel ---------
        highest_xp_icon_image = cTk.CTkImage(Image.open(io.BytesIO(urllib.request.urlopen(player_skills[player.highest_xp[0]][3]).read())))
        highest_xp_icon.configure(image=highest_xp_icon_image)
        highest_xp_rank.configure(text=f"{player_skills[player.highest_xp[0]][0]:,d}")
        highest_xp_level.configure(text=player_skills[player.highest_xp[0]][1])
        highest_xp_xp.configure(text=f"{player_skills[player.highest_xp[0]][2]:,d}")

        # ------- Lowest xp left panel ---------
        lowest_xp_icon_image = cTk.CTkImage(Image.open(io.BytesIO(urllib.request.urlopen(player_skills[player.lowest_xp[0]][3]).read())))
        lowest_xp_icon.configure(image=lowest_xp_icon_image)
        lowest_xp_rank.configure(text=f"{player_skills[player.lowest_xp[0]][0]:,d}")
        lowest_xp_level.configure(text=player_skills[player.lowest_xp[0]][1])
        lowest_xp_xp.configure(text=f"{player_skills[player.lowest_xp[0]][2]:,d}")

        # -------- Average Level left panel -------
        average_level.configure(text=player._average_level)

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
            
            # Display Icon
            if displayico == True:
                skill_icon_image = cTk.CTkImage(Image.open(io.BytesIO(urllib.request.urlopen(player_skills[i][3]).read())))
                skill_icon = cTk.CTkLabel(skill_frame, image=skill_icon_image, text=" ")
            else:
                skill_icon = cTk.CTkLabel(skill_frame, text="ico", text_color="gray9")
            skill_icon.grid(row=row_counter, column=column_counter, padx=(frame_padding*6, frame_padding), pady=skill_ypadding)

            # Display Rank
            skill_rank = cTk.CTkLabel(skill_frame, text=f"{player_skills[i][0]:,d}")
            skill_rank.grid(row=row_counter, column=column_counter+1, padx=frame_padding, pady=skill_ypadding)

            # Display Level (green if 99)
            if player_skills[i][1] == 99 or player_skills[i][1] == 2277:
                if player_skills[i][2] == 200000000:
                    skill_level = cTk.CTkLabel(skill_frame, text=f"{player_skills[i][1]:,d}", text_color="goldenrod1")
                else:
                    skill_level = cTk.CTkLabel(skill_frame, text=f"{player_skills[i][1]:,d}", text_color="spring green")
            else:
                skill_level = cTk.CTkLabel(skill_frame, text=f"{player_skills[i][1]:,d}")
            skill_level.grid(row=row_counter, column=column_counter+2, padx=frame_padding, pady=skill_ypadding) 

            # Display XP
            if player_skills[i][2] == 200000000:
                skill_xp = cTk.CTkLabel(skill_frame, text=f"{player_skills[i][2]:,d}", text_color="goldenrod1")
            else:
                skill_xp = cTk.CTkLabel(skill_frame, text=f"{player_skills[i][2]:,d}")
            skill_xp.grid(row=row_counter, column=column_counter+3, padx=(frame_padding, frame_padding*5), pady=skill_ypadding) 

            # Evere skill uses 4 columns, when this reaches the skills per row
            # Increment the row by 1
            column_counter += 4
            if column_counter == skill_per_row*4:
                row_counter += 1
                column_counter = 0

        # Update Other Page
        player_exist.configure(text="Loading Other...", text_color="goldenrod1")
        player_exist.update()
        global player_clues
        global player_other
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
            
            # Display Icon
            if displayico == True:
                clue_icon_image = cTk.CTkImage(Image.open(io.BytesIO(urllib.request.urlopen(player_clues[i][2]).read())))
                clue_icon = cTk.CTkLabel(other_scroll_frame, image=clue_icon_image, text=" ")
            else:
                clue_icon = cTk.CTkLabel(other_scroll_frame, text="ico", text_color="gray9")
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

            # Display Icon
            if displayico == True:
                other_icon_image = cTk.CTkImage(Image.open(io.BytesIO(urllib.request.urlopen(player_other[i][2]).read())))
                other_icon = cTk.CTkLabel(other_scroll_frame, image=other_icon_image, text=" ")
            else:
                other_icon = cTk.CTkLabel(other_scroll_frame, text="ico", text_color="gray9")
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

        # Add borders to frames
        settingsframe.configure(border_color="gray10",border_width=2)
        contentframe.configure(border_color="gray10",border_width=2)

        player_exist.configure(text=f"{player.username} Loaded!", text_color="spring green") # Display success message 
        root.geometry(f"{str(window_width)}x{str(window_height)}") # Expand window to show statistics
    # If player does not exist.
    else:
        player_name_button.configure(text="✗", text_color="Red")
        player_exist.configure(text=f"{player.username} Not Found!", text_color="Red")

    return player # Return player object


# ------------------------- Application Setup ---------------------------------------
#------ Application Variables ----------
window_height = 440
window_width = 800
frame_padding = 4
cTk.set_default_color_theme("green")

root = cTk.CTk()
root.geometry(f"300x70")
root.resizable(width=False, height=False)
root.title("OSRS Tracker")


#------------------------ Settings Frame (Left Frame) -------------------------------
settingsframe = cTk.CTkFrame(root, width=300-frame_padding, height=window_height-frame_padding)
settingsframe.grid_propagate(False)
settingsframe.grid(row=0, column=0, padx=frame_padding / 2, pady=frame_padding / 2)

# Entry for username
player_name = cTk.CTkEntry(settingsframe, width=200, placeholder_text="Username")
player_name.grid(row=0, column=0, columnspan=3 , pady=(10,3), padx=(30,5))

# Button to submit username
player_name_button = cTk.CTkButton(settingsframe, text=">", width=30, fg_color="gray13", hover_color="gray10", command=get_user_stats)
player_name_button.grid(row=0, column=3, pady=(10,3))

# Text below entry field displaying status messages.
player_exist = cTk.CTkLabel(settingsframe, text="Waiting for username..", text_color="gray5")
player_exist.grid(row=1,column=0, columnspan=4, padx=(20,0), pady=(0,15))


# -------------- Key Stats Frame --------------------------
key_stats_frame = cTk.CTkFrame(settingsframe, fg_color="gray15")
key_stats_frame.grid(row=2, column=0, columnspan=5, padx=frame_padding*1.5)

# ---------- Highest XP stat left frame ------------
highest_xp = cTk.CTkLabel(key_stats_frame, text="Highest XP", text_color="goldenrod1")
highest_xp.grid(row=0, column=0, columnspan=4) # Header

highest_xp_icon = cTk.CTkLabel(key_stats_frame, text=" ")
highest_xp_icon.grid(row=1, column=0, padx=frame_padding*3) # Icon

highest_xp_rank = cTk.CTkLabel(key_stats_frame, text="rank")
highest_xp_rank.grid(row=1, column=1, padx=frame_padding*3) # Rank

highest_xp_level = cTk.CTkLabel(key_stats_frame, text="level")
highest_xp_level.grid(row=1, column=2, padx=frame_padding*3) # Level

highest_xp_xp = cTk.CTkLabel(key_stats_frame, text="xp")
highest_xp_xp.grid(row=1, column=3, padx=frame_padding*3) # XP

# --------- Lowest XP stat left frame -------------
lowest_xp = cTk.CTkLabel(key_stats_frame, text="Lowest XP", text_color="goldenrod1")
lowest_xp.grid(row=2, column=0, columnspan=4, pady=(15,0)) # Header

lowest_xp_icon = cTk.CTkLabel(key_stats_frame, text=" ")
lowest_xp_icon.grid(row=3, column=0, padx=frame_padding*3) # Icon

lowest_xp_rank = cTk.CTkLabel(key_stats_frame, text="rank")
lowest_xp_rank.grid(row=3, column=1, padx=frame_padding*3) # Rank

lowest_xp_level = cTk.CTkLabel(key_stats_frame, text="level")
lowest_xp_level.grid(row=3, column=2, padx=frame_padding*3) # Level

lowest_xp_xp = cTk.CTkLabel(key_stats_frame, text="xp")
lowest_xp_xp.grid(row=3, column=3, padx=frame_padding*3) # XP


# --------- Average level left frame -------------
average_level_icon_image = cTk.CTkImage(Image.open(io.BytesIO(urllib.request.urlopen("https://www.runescape.com/img/rsp777/title2/globe.gif").read())))
average_level_icon = cTk.CTkLabel(key_stats_frame, text=" ", image=average_level_icon_image)
average_level_icon.grid(row=4, column=0, padx=frame_padding*3, pady=(30,0)) # Icon

average_level_header = cTk.CTkLabel(key_stats_frame, text="Average Level:", text_color="goldenrod1")
average_level_header.grid(row=4, column=1, columnspan=2, pady=(30,0))

average_level = cTk.CTkLabel(key_stats_frame, text="level")
average_level.grid(row=4, column=3, columnspan=1, padx=frame_padding*3, pady=(30,0)) # Rank




# ---------------------- Content Page (Right Frame) -----------------------
contentframe = cTk.CTkFrame(root, width=window_width - (300+frame_padding), height=window_height - frame_padding)
contentframe.grid_propagate(False)
contentframe.pack_propagate(False)
contentframe.grid(row=0, column=1, padx=frame_padding / 2, pady=frame_padding / 2)

#-------- Adding tabs to content window ----------
tabcontrol = cTk.CTkTabview(contentframe, width=window_width-(300+(frame_padding*4)), height=window_height-(frame_padding*3), fg_color="transparent")
tabcontrol.pack_propagate(False)
tabcontrol.pack()

tabcontrol.add("Skills")
skill_frame = cTk.CTkFrame(tabcontrol.tab("Skills"), width=460, height=window_height-(frame_padding*3), fg_color="gray15")
skill_frame.pack()

tabcontrol.add("Other")
other_scroll_frame = cTk.CTkScrollableFrame(tabcontrol.tab("Other"), width=450, height=window_height-(frame_padding*5), fg_color="gray15")
other_scroll_frame.pack()

tabcontrol.add("Monitoring")
monitoring_scroll_frame = cTk.CTkScrollableFrame(tabcontrol.tab("Monitoring"), fg_color="gray12", width=450)
monitoring_scroll_frame.grid(row=5, column=0, columnspan=4)

add_level_button = cTk.CTkButton(tabcontrol.tab("Monitoring"), text="Add Level", command=add_level)
add_level_button.grid(row=0, column=0)
add_level_input = cTk.CTkEntry(tabcontrol.tab("Monitoring"), placeholder_text="Skill")
add_level_input.grid(row=0, column=1)

add_xp_button = cTk.CTkButton(tabcontrol.tab("Monitoring"), text="Add XP", command=add_xp)
add_xp_button.grid(row=1, column=0)
add_xp_input = cTk.CTkEntry(tabcontrol.tab("Monitoring"), placeholder_text="Skill")
add_xp_input.grid(row=1, column=1)

add_clue_button = cTk.CTkButton(tabcontrol.tab("Monitoring"), text="Add Clue", command=add_clue)
add_clue_button.grid(row=2, column=0)
add_clue_input = cTk.CTkEntry(tabcontrol.tab("Monitoring"), placeholder_text="Clue")
add_clue_input.grid(row=2, column=1)

add_other_button = cTk.CTkButton(tabcontrol.tab("Monitoring"), text="Add Other", command=add_other)
add_other_button.grid(row=3, column=0)
add_other_input = cTk.CTkEntry(tabcontrol.tab("Monitoring"), placeholder_text="Other")
add_other_input.grid(row=3, column=1)

refresh_skills = cTk.CTkButton(tabcontrol.tab("Monitoring"), text="Refresh", command=refresh_stats)
refresh_skills.grid(row=4, column=0)

root.mainloop()