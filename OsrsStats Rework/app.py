
import stat_processor
import customtkinter as cTk
from PIL import Image, ImageTk
import urllib
import io
import datetime

def cancel_refresh():
    refresh_changes_timer.delete(0,cTk.END)
    refresh_changes_timer.configure(textvariable="")
    refresh_changes.configure(text="Refresh", text_color="white")

def refresh_stats():
    changes, skill_stats, clue_stats, other_stats, original_skill_stats, original_clue_stats, original_other_stat = player.compare()

    if refresh_changes_timer.get() != "":
        refresh_changes.configure(text="Refreshing", text_color="goldenrod2")
        refresh_time = int(refresh_changes_timer.get()) * 1000 # Get ms from seconds
        refresh_timestamp = f"{datetime.datetime.now().strftime('%H')}:{datetime.datetime.now().strftime('%M')}:{datetime.datetime.now().strftime('%S')}"
        refresh_last_refresh.configure(text=refresh_timestamp)
        root.after(refresh_time, refresh_stats)

    if len(changes) != 0:
        for change in changes:
            change_frame = cTk.CTkFrame(monitoring_scroll_frame, fg_color="gray10", width=450, height=30) # Create frame for change
            change_frame.grid_propagate(False) # Keep shape
            change_frame.grid(row=player.__changes_counter, column=0, columnspan=4)

            # Timestamp for change
            change_time = cTk.CTkLabel(change_frame, text=f"{datetime.datetime.now().strftime('%H')}:{datetime.datetime.now().strftime('%M')} : ", text_color="gray30")
            change_time.grid(row=0, column=0, padx=(5,5))

            # Find icon depending on if it is a level, xp, clue or other change
            if changes[change][0] == "level" or changes[change][0] == "xp":
                change_icon_image = cTk.CTkImage(Image.open(io.BytesIO(urllib.request.urlopen(skill_stats[change][3]).read())))
            elif changes[change][0] == "clue":
                change_icon_image = cTk.CTkImage(Image.open(io.BytesIO(urllib.request.urlopen(clue_stats[change][2]).read())))
            else:
                change_icon_image = cTk.CTkImage(Image.open(io.BytesIO(urllib.request.urlopen(other_stats[change][2]).read())))
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
                    old_new = cTk.CTkLabel(change_frame, text=f"{original_skill_stats[change][1]} ➜ {original_skill_stats[change][1] + changes[change][1]}")
                    player_skills[change][1] += changes[change][1]
                else:
                    new_xp = original_skill_stats[change][2] + changes[change][1]
                    old_new = cTk.CTkLabel(change_frame, text=f"{original_skill_stats[change][2]:,d} ➜ {new_xp:,d}")
                    player_skills[change][2] += changes[change][1]

            elif changes[change][0] == "clue":
                old_new = cTk.CTkLabel(change_frame, text=f"{original_clue_stats[change][1]} ➜ {original_clue_stats[change][1] + changes[change][1]}")
                player_clues[change][1] += changes[change][1]

            else:
                old_new = cTk.CTkLabel(change_frame, text=f"{original_other_stat[change][1]} ➜ {original_other_stat[change][1] + changes[change][1]}")
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
    player = stat_processor.OsrsPlayer(player_name.get()) # Create OsrsPlayer object
    player.__changes_counter = 0
    try:
        for child in skill_frame.winfo_children():
            child.destroy()
        for child in other_scroll_frame.winfo_children():
            child.destroy()
        for child in monitoring_scroll_frame.winfo_children():
            child.destroy()
        cancel_refresh()
    except:
        pass

    #--- Check if player exists ---
    if player.player_exists == True:

        # Display Icons or have placeholder text (increase loading time for testing)
        displayico = True
        if displayico == False:
            placeholder_icon = cTk.CTkImage(Image.open(io.BytesIO(urllib.request.urlopen("https://www.runescape.com/img/rsp777/title2/launcher.png").read())))

        player_name_button.configure(text="✓", text_color="spring green") # Change Button Style

        # Generating Skill Window
        skill_per_row = 2 # Set Static Skill Page Variables

        global player_skills
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

        skill_ypadding = 1

        skill_counter = 0
        skill_count = len(player_skills)

        for i in player_skills: # Loop over all elements in skill dictionary

            # Update loading text to show skill count
            skill_counter += 1
            player_exist.configure(text=f"Loading Skills... ({skill_counter}/{skill_count})", text_color="goldenrod1")
            player_exist.update()

            if player_skills[i][0] == "Unknown": # If player has no overall rank
                continue # Skip to next element in loop
            
            # Display Icon
            if displayico == True:
                skill_icon_image = cTk.CTkImage(Image.open(io.BytesIO(urllib.request.urlopen(player_skills[i][3]).read())))
                skill_icon = cTk.CTkLabel(skill_frame, image=skill_icon_image, text=" ")
            else:
                skill_icon = cTk.CTkLabel(skill_frame, image=placeholder_icon, text=" ", text_color="gray9")
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

        clue_count = len(player_clues)
        clue_counter = 0
        other_count = len(player_other)
        other_counter = 0
        

        for i in player_clues: # Loop over all elements in skill dictionary

        # Update loading text to show skill count
            clue_counter += 1
            player_exist.configure(text=f"Loading Clues... ({clue_counter}/{clue_count})", text_color="goldenrod1")
            player_exist.update()
            
            # Display Icon
            if displayico == True:
                clue_icon_image = cTk.CTkImage(Image.open(io.BytesIO(urllib.request.urlopen(player_clues[i][2]).read())))
                clue_icon = cTk.CTkLabel(other_scroll_frame, image=clue_icon_image, text=" ")
            else:
                clue_icon = cTk.CTkLabel(other_scroll_frame, image=placeholder_icon, text=" ", text_color="gray9")
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
            other_counter += 1
            player_exist.configure(text=f"Loading Other... ({other_counter}/{other_count})", text_color="goldenrod1")
            player_exist.update()

            # Display Icon
            if displayico == True:
                other_icon_image = cTk.CTkImage(Image.open(io.BytesIO(urllib.request.urlopen(player_other[i][2]).read())))
                other_icon = cTk.CTkLabel(other_scroll_frame, image=other_icon_image, text=" ")
            else:
                other_icon = cTk.CTkLabel(other_scroll_frame, image=placeholder_icon, text=" ", text_color="gray9")
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


    # ------- Highest xp left panel ---------
    highest_xp_icon_image = cTk.CTkImage(Image.open(io.BytesIO(urllib.request.urlopen(player_skills[player.highest_xp[0]][3]).read())))
    highest_xp_icon.configure(image=highest_xp_icon_image)
    highest_xp_level.configure(text=player_skills[player.highest_xp[0]][1])
    highest_xp_xp.configure(text=f"{player_skills[player.highest_xp[0]][2]:,d}")

    # ------- Lowest xp left panel ---------
    lowest_xp_icon_image = cTk.CTkImage(Image.open(io.BytesIO(urllib.request.urlopen(player_skills[player.lowest_xp[0]][3]).read())))
    lowest_xp_icon.configure(image=lowest_xp_icon_image)
    lowest_xp_level.configure(text=player_skills[player.lowest_xp[0]][1])
    lowest_xp_xp.configure(text=f"{player_skills[player.lowest_xp[0]][2]:,d}")

    # -------- Average Level left panel -------
    average_level.configure(text=player._average_level)
    average_xp.configure(text=f"{player._average_xp:,d}")

    return player # Return player object


# ------------------------- Application Setup ---------------------------------------
#------ Application Variables ----------
window_height = 440
window_width = 800
frame_padding = 4
cTk.set_default_color_theme("green")

root = cTk.CTk()
#root.geometry(f"300x70")
root.geometry(f"800x450")
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
player_exist.grid(row=1,column=0, columnspan=3, padx=(20,0), pady=(0,15))

# -------------- Key Stats Frame --------------------------
key_stats_frame = cTk.CTkFrame(settingsframe, fg_color="gray15", width=260, height=345)
key_stats_frame.grid_propagate(False)
key_stats_frame.grid(row=2, column=0, columnspan=5, padx=(15,0))

# ---------- Highest XP stat left frame ------------
highest_xp_frame = cTk.CTkFrame(key_stats_frame, width=230, height=60, fg_color="gray13")
highest_xp_frame.grid_propagate(False)
highest_xp_frame.grid(row=0, column=0, columnspan=3, padx=13, pady=15)

highest_xp = cTk.CTkLabel(highest_xp_frame, text="Highest XP", text_color="goldenrod1", width=230)
highest_xp.grid(row=0, column=0, columnspan=4) # Header

highest_xp_icon_placeholder = cTk.CTkImage(Image.open(io.BytesIO(urllib.request.urlopen("https://www.runescape.com/img/rsp777/title2/globe.gif").read())))
highest_xp_icon = cTk.CTkLabel(highest_xp_frame, text=" ", image=highest_xp_icon_placeholder)
highest_xp_icon.grid(row=1, column=0, padx=frame_padding*3) # Icon

highest_xp_level = cTk.CTkLabel(highest_xp_frame, text="level")
highest_xp_level.grid(row=1, column=1, padx=frame_padding*3) # Level

highest_xp_xp = cTk.CTkLabel(highest_xp_frame, text="xp")
highest_xp_xp.grid(row=1, column=2, padx=frame_padding*3) # XP

# --------- Lowest XP stat left frame -------------
lowest_xp_frame = cTk.CTkFrame(key_stats_frame, width=230, height=60, fg_color="gray13")
lowest_xp_frame.grid_propagate(False)
lowest_xp_frame.grid(row=1, column=0, columnspan=3, padx=13, pady=15)

lowest_xp = cTk.CTkLabel(lowest_xp_frame, text="Lowest XP", text_color="goldenrod1", width=230)
lowest_xp.grid(row=0, column=0, columnspan=4) # Header

lowest_xp_icon_placeholder = cTk.CTkImage(Image.open(io.BytesIO(urllib.request.urlopen("https://www.runescape.com/img/rsp777/title2/globe.gif").read())))
lowest_xp_icon = cTk.CTkLabel(lowest_xp_frame, text=" ", image=lowest_xp_icon_placeholder)
lowest_xp_icon.grid(row=1, column=0, padx=frame_padding*2) # Icon

lowest_xp_level = cTk.CTkLabel(lowest_xp_frame, text="level")
lowest_xp_level.grid(row=1, column=1, padx=frame_padding*2) # Level

lowest_xp_xp = cTk.CTkLabel(lowest_xp_frame, text="xp")
lowest_xp_xp.grid(row=1, column=2, padx=frame_padding*2) # XP


# --------- Average level left frame -------------

average_frame = cTk.CTkFrame(key_stats_frame, width=230, height=60, fg_color="gray13")
average_frame.grid_propagate(False)
average_frame.grid(row=2, column=0, columnspan=3, padx=13, pady=15)

average_level_header = cTk.CTkLabel(average_frame, text="Average:", text_color="goldenrod1", width=230)
average_level_header.grid(row=0, column=0, columnspan=4)

average_level_icon_image = cTk.CTkImage(Image.open(io.BytesIO(urllib.request.urlopen("https://www.runescape.com/img/rsp777/title2/globe.gif").read())))
average_level_icon = cTk.CTkLabel(average_frame, text=" ", image=average_level_icon_image)
average_level_icon.grid(row=1, column=0, padx=frame_padding*3) # Icon

average_level = cTk.CTkLabel(average_frame, text="level")
average_level.grid(row=1, column=1, padx=frame_padding*2) # Level

average_xp = cTk.CTkLabel(average_frame, text="xp")
average_xp.grid(row=1, column=2, padx=frame_padding*2) # xp



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
skill_frame = cTk.CTkFrame(tabcontrol.tab("Skills"), width=470, height=window_height-(frame_padding*10), fg_color="gray15")
skill_frame.pack()

tabcontrol.add("Other")
other_scroll_frame = cTk.CTkScrollableFrame(tabcontrol.tab("Other"), width=450, height=window_height-(frame_padding*10), fg_color="gray15")
other_scroll_frame.pack()


# ---------------- Monitoring tab ---------------
tabcontrol.add("Monitoring")
monitoring_scroll_frame = cTk.CTkScrollableFrame(tabcontrol.tab("Monitoring"), fg_color="gray12", width=450, height=315)
monitoring_scroll_frame.grid(row=1, column=0, columnspan=4, pady=(20, 0))

refresh_changes = cTk.CTkButton(tabcontrol.tab("Monitoring"), text="Refresh", fg_color="gray12", hover_color="gray10", command=refresh_stats)
refresh_changes.grid(row=0, column=0, columnspan=1, pady=(10,0))

refresh_changes_timer = cTk.CTkEntry(tabcontrol.tab("Monitoring"), placeholder_text="Refresh Interval   (s)")
refresh_changes_timer.grid(row=0, column=1, pady=(10,0))

refresh_loop_cancel = cTk.CTkButton(tabcontrol.tab("Monitoring"), text="✗", text_color="Red", width=30, fg_color="gray13", hover_color="gray10", command=cancel_refresh)
refresh_loop_cancel.grid(row=0, column=2, pady=(10,0))

refresh_last_refresh = cTk.CTkLabel(tabcontrol.tab("Monitoring"), width=50, text="", text_color="gray30")
refresh_last_refresh.grid(row=0, column=3, pady=(10,0))

root.mainloop()