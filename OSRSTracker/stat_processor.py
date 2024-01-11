import requests
import pandas as pd
from bs4 import BeautifulSoup

import copy
import pickle


class OsrsPlayer:
    def __init__(self, username):
        # Gather parameters using class functions
        self.username = self._fix_username(username) # Prepare username for request
        self.lowest_skill = ["",99]
        self.lowest_xp = ["",200000000]
        self.highest_xp = ["",0]
        self.lvl99 = [] # List of 99's
        self.player_exists = False

        # Html Get request
        self.__html = BeautifulSoup( requests.get(f"https://secure.runescape.com/m=hiscore_oldschool/hiscorepersonal?user1={self.username}").text, 'html.parser')

        # Check if player exists.
        try:
            if "No player" in self.__html.find("div", {"align":"center"}).find("div", {"align":"center"}).text:
                self.player_exists = False
                print("Player Not Found!")
                return
        except:
            # Run functions to overwrite default values
            self.player_exists = True
            self._skill_stats = self._collect_skills()
            self._clue_stats = self._collect_clues()
            self._other_stats = self._collect_other()
            print("Player Stats Loaded!")
       
    # Used in __init__ to replace spaces with % to work in link request
    def _fix_username(self, username):
        try:
            username.replace(" ","%20")
        except:
            pass
        return username
    
    def _collect_skills(self):
        self._skill_stats = {}
        self.__html = BeautifulSoup( requests.get(f"https://secure.runescape.com/m=hiscore_oldschool/hiscorepersonal?user1={self.username}").text, 'html.parser')

        # Get overall stat if exists
        try:
            overall_slice = self.__html.find_all("td", {"align" : "right"})[3:6]
            overall_rank = int(overall_slice[0].text.replace(",",""))
            overall_level = int(overall_slice[1].text.replace(",",""))
            overall_xp = int(overall_slice[2].text.replace(",",""))
            self._skill_stats["Overall"] = [overall_rank, overall_level, overall_xp, "https://www.runescape.com/img/rsp777/title2/hiscore.gif"]
            skills = self.__html.find_all("td", {"align" : "right"})[6:] # Define slice containing Skills
        except:
            self._skill_stats["Overall"] = ["Unknown", "Unknown", "Unknown", "https://www.runescape.com/img/rsp777/title2/hiscore.gif"] # Unknown if user has no overall stat
            skills = self.__html.find_all("td", {"align" : "right"})[3:] # Define slice containing Skills if user does not have overall stat

        # Loop over each skill and get rank, level and xp, appending this to self.skill_stats
        total_level = 0
        total_xp = 0
        for skill_nr in range(23):
            current_skill_slice = skills[skill_nr * 4 : skill_nr * 4 + 4]

            # Check if current image urr has 1.gif in it (which means it is a skill)
            if "1.gif" in current_skill_slice[0].find("img")["src"]:

                # Gather information from slice
                current_skill_icon = current_skill_slice[0].find("img")["src"]
                current_skill = current_skill_slice[0].find("img")["src"].split("_")[-1].replace("1.gif","").capitalize()
                current_skill_rank = int(current_skill_slice[1].text.replace(",","")) # Rank
                current_skill_level = int(current_skill_slice[2].text.replace(",","")) # Level
                current_skill_xp = int(current_skill_slice[3].text.replace(",","")) # XP

                total_level += current_skill_level # For calculating average level
                total_xp += current_skill_xp
                
                # Find Lowest Skill
                if current_skill_level < self.lowest_skill[1]:
                    self.lowest_skill[0] = current_skill
                    self.lowest_skill[1] = current_skill_level
                    
                # Find Lowest XP
                if current_skill_xp < self.lowest_xp[1]:
                    self.lowest_xp[0] = current_skill
                    self.lowest_xp[1] = current_skill_xp
                    
                # Count 99's
                if current_skill_level == 99:
                    self.lvl99.append(current_skill)
                if len(self.lvl99) == 23:
                    self.lvl99.append("Max")
                    
                # Get Highest XP
                if current_skill_xp > self.highest_xp[1]:
                    self.highest_xp[0] = current_skill
                    self.highest_xp[1] = current_skill_xp
    
                # Append skill, rank, level and xp to self.skill_stats
                self._skill_stats[current_skill] = [current_skill_rank,current_skill_level,current_skill_xp, current_skill_icon]
            else:
                break

        # Calculate average level
        self._average_level = int(total_level / 23)
        self._average_xp = int(total_xp / 23)
        return self._skill_stats

    def _collect_clues(self):
        self._clue_stats = {}

        # Loop over all td elements in the html document
        for index, element in enumerate(self.__html.find_all("td", {"align" : "right"})):
            try:
                # If the element has a link which contains the word "clue"
                # We know what index to start gathering clue information
                if "clue" in element.find("img")["src"]:
                    clue_start_index = index # Break when finding first element with clue in url
                    break
            except:
                continue 

        # Create html slice of elements from where we found the clue start index
        clues = self.__html.find_all("td", {"align" : "right"})[clue_start_index:]
        
        for clue_nr in range(7):
            current_clue_slice = clues[clue_nr * 3 : clue_nr * 4 + 3]
            try:
                if "clue" in current_clue_slice[0].find("img")["src"]:
                    current_clue_icon = current_clue_slice[0].find("img")["src"] # Clue icon url
                    current_clue = current_clue_slice[0].find("img")["src"].split("_")[-1].replace(".png","")[11:].capitalize() # Clue Name
                    
                    current_clue_rank = int(current_clue_slice[1].text.replace(",","")) # Rank
                    current_clue_score = int(current_clue_slice[2].text.replace(",","")) # Score
                    
                    self._clue_stats[current_clue] = [current_clue_rank, current_clue_score, current_clue_icon]
            
                else:
                    continue
            except:
                break
        return self._clue_stats


    def _collect_other(self):
        self._other_stats = {}

        # Loop over all td elements in the html document
        for index, element in enumerate(self.__html.find_all("td", {"align" : "right"})):
            try:
                # If the element has a link which contains the word "clue"
                # We get the last element in the clue list, where we start gathering other stats
                if "clue" in element.find("img")["src"]:
                    other_start_index = index + 3
            except:
                continue 
    
        # Create html slice of elements from where we found the clue start index
        other = self.__html.find_all("td", {"align" : "right"})[other_start_index:]
        try:
            for other_nr in range(100):
                current_other_slice = other[other_nr * 3 : other_nr * 4 + 3]
    
                current_other_icon = current_other_slice[0].find("img")["src"] # Clue icon url
                current_other = current_other_slice[0].find("img")["src"].split("_")[-1].replace(".png","")[:].capitalize() # Clue Name
                
                current_other_rank = int(current_other_slice[1].text.replace(",","")) # Rank
                current_other_score = int(current_other_slice[2].text.replace(",","")) # Score
     
                self._other_stats[current_other] = [current_other_rank, current_other_score, current_other_icon]
        except:
            pass
        return self._other_stats

    # Return Rank of spesific Skill
    def rank(self, skill):
        try:
            return self._skill_stats[skill][0]
        except:
            return f"Unable to return {skill} rank."
     
    # Return Level of spesific Skill
    def level(self, skill):
        try:
            return self._skill_stats[skill][1]
        except:
            return f"Unable to return {skill} level."
    
    # Return XP in spesific skill 
    def xp(self, skill):
        try:
            return self._skill_stats[skill][2]
        except:
            return f"Unable to return {skill} xp."

    # Display All Stats
    def skills(self, raw=False, display=True):
        if self.player_exists == True:
            if raw == True:
                return self._skill_stats
            else:
                print("                 |     Rank     |     Level    |      XP")
                for skill in self._skill_stats:
                    if "Unknown" in self._skill_stats[skill]:
                        continue
                    skill_rank = f"{self._skill_stats[skill][0]:,d}" # Add thousand delimeters
                    skill_level = f"{self._skill_stats[skill][1]:,d}" # Add thousand delimeters
                    skill_xp = f"{self._skill_stats[skill][2]:,d}" # Add thousand delimeters
                    if display == True:
                        print(f"{skill:^15}  |  {skill_rank:^10}  |  {skill_level:^10}  |  {skill_xp:^10}")
        else:
            print("User does not exist.")

    # Display all clue stats
    def clues(self, raw=False, display=True):
        if self.player_exists == True:
            if raw == True:
                return self._clue_stats
            else:
                print("                 |     Rank     |    Score")
                for clue in self._clue_stats:
                    clue_rank = f"{self._clue_stats[clue][0]:,d}"
                    clue_score = f"{self._clue_stats[clue][1]:,d}"
                    if display == True:
                        print(f"{clue:^15}  |  {clue_rank:^10}  |  {clue_score:^10}")
        else:
            print("User does not exist.")

    def other(self, raw=False, display=True):
        if self.player_exists == True:
            if raw == True:
                return self._other_stats
            else:
                print("                      |     Rank     |    Score")
                for other in self._other_stats:
                    other_rank = f"{self._other_stats[other][0]:,d}"
                    other_score = f"{self._other_stats[other][1]:,d}"
                    if display == True:
                        print(f"{other:^20}  |  {other_rank:^10}  |  {other_score:^10}")
        else:
            print("User does not exist.")

    def update_stats(self):
        # Update Stats
        self._collect_skills()
        self._collect_clues()
        self._collect_other()

    def compare(self, from_save=False):
        changes = {}

        if from_save == False:
            # Create copy of stats
            original_skill_stats = copy.deepcopy(self._skill_stats)
            original_clue_stats = copy.deepcopy(self._clue_stats)
            original_other_stats = copy.deepcopy(self._other_stats)
        else:
            # TODO
            # - Load in stats from save file
            pass
        
        self.update_stats()

        # ---------- Skill Changes --------
        for skill in self._skill_stats:
            original_skill_stats.setdefault(skill, [0, 0, 0, "https://www.runescape.com/img/rsp777/title2/support.png"])
            # Check changes in xp
            if self._skill_stats[skill][2] != original_skill_stats[skill][2]:
                xp_gain = self._skill_stats[skill][2] - original_skill_stats[skill][2]
                changes[skill] = ["xp", xp_gain]
            
            # Check changes in level
            if self._skill_stats[skill][1] != original_skill_stats[skill][1]:
                xp_gain = self._skill_stats[skill][1] - original_skill_stats[skill][1]
                changes[skill] = ["level", xp_gain]

        # ---------- Clue Changes ---------
        for clue in self._clue_stats:
            original_clue_stats.setdefault(clue, [0, 0, "https://www.runescape.com/img/rsp777/title2/support.png"])
            # Check changes in clue count
            if self._clue_stats[clue][1] != original_clue_stats[clue][1]:
                clue_count_change = self._clue_stats[clue][1] - original_clue_stats[clue][1]
                changes[clue] = ["clue", clue_count_change]

        # ---------- Other Changes ---------
        for other in self._other_stats:
            original_other_stats.setdefault(other, [0, 0, "https://www.runescape.com/img/rsp777/title2/support.png"])
            # Check if any other changes
            if self._other_stats[other][1] != original_other_stats[other][1]:
                other_count_change = self._other_stats[other][1] - original_other_stats[other][1]
                changes[other] = ["other", other_count_change]
                
        return changes, self._skill_stats, self._clue_stats, self._other_stats, original_skill_stats, original_clue_stats, original_other_stats
    

    def save_to_file(self):
        with open(f"./Saved/{self.username}.pkl", "wb") as f:
            pickle.dump(self, f)
       
    
    # Functions for testing changes in skill stats
    def _add_skill_xp(self, skill, xp):
        self._skill_stats.setdefault(skill, [0, 0, 0, "https://www.runescape.com/img/rsp777/title2/support.png"])
        self._skill_stats[skill][2] += xp

    def _add_skill_level(self, skill, levels):
        self._skill_stats.setdefault(skill, [0, 0, 0, "https://www.runescape.com/img/rsp777/title2/support.png"])
        self._skill_stats[skill][1] += levels
    
    def _add_clue_count(self, clue, count):
        self._clue_stats.setdefault(clue, [0, 0, "https://www.runescape.com/img/rsp777/title2/support.png"])
        self._clue_stats[clue][1] += count

    def _add_other_count(self, other, count):
        self._other_stats.setdefault(other, [0, 0, "https://www.runescape.com/img/rsp777/title2/support.png"])
        self._other_stats[other][1] += count

                
    