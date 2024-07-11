#calculations for stats based on unit data, so after we ge the unit data
import os
from UnitClass import *
import ast
from difflib import get_close_matches

os.chdir(os.path.dirname(os.path.abspath(__file__))) #path directory of this script to get stuff

growthdata = {
    1:[6, 8, 9, 11, 13, 14, 16, 18, 19, 21, 23, 24, 26, 28, 30, 31, 33],
    2:[7, 8, 10, 12, 14, 15, 17, 19, 21, 23, 25, 26, 28, 30, 32, 34, 36],
    3:[7, 9, 11, 13, 15, 17, 19, 21, 23, 25, 27, 29, 31, 33, 35, 37, 39],
    4:[8, 10, 12, 14, 16, 18, 20, 22, 24, 26, 28, 31, 33, 35, 37, 39, 41],
    5:[8, 10, 13, 15, 17, 19, 22, 24, 26, 28, 30, 33, 35, 37, 39, 42, 44]
}
unitlist = []
statindex = {"HP": 0, "ATK": 1, "SPD": 2, "DEF": 3, "RES": 4}
growthindex = {20: 0, 25: 1, 30: 2, 35: 3, 40: 4, 45: 5, 50: 6, 55: 7, 60: 8, 65: 9, 70: 10, 75: 11, 80: 12, 85: 13, 90: 14, 95: 15, 100: 16} #iindex for growth rates

def arena_score(unit): #add duel skills or duo/paired legendary to replace bst (tho, i guess legendary/duo can have natural higher bst over duel skills.... i think....)
    score = 0
    bst = unit.bst
    lvl = unit.lvl
    rarity = unit.rarity
    merge = unit.merge
    unittype = unit.unittype #see if they are legendary or mythic, all pair up legends have at least 175 duel numbers, duos have at least 185
    duelskill = unit.duel #if they are a duel unit (legendary pair up or duo unit)
    weapon = unit.weapon
    assist = unit.assist
    special = unit.special
    Askill = unit.Askill
    Bskill = unit.Bskill
    Cskill = unit.Cskill
    Sskill = unit.Sskill
    #print(bst)

    weapon = find_skill(weapon, dataweapon)
    assist = find_skill(assist, dataassist)
    special = find_skill(special, dataspecial)
    Askill = find_skill(Askill, dataskill)
    Bskill = find_skill(Bskill, dataskill)
    Cskill = find_skill(Cskill, dataskill)
    Sskill = find_skill(Sskill, dataskill)


    if duelskill == "None": #they are a normie (not duo or pair up legendary)
        duelskill = 0

    if "Duel" in Askill and lvl == 40 and rarity == 5: #if askill has a duel skill
        if "1" in Askill: #diffent tiers , 160
            if bst < 160 and 160 > duelskill: #duel skill is 
                duelskill = 160
        elif "2" in Askill: #165
            if bst < 165 and 165 > duelskill:
                duelskill = 165
        elif "3" in Askill: #170
            if bst < 170 and 170 > duelskill:
                duelskill = 170
        elif "4" in Askill: #175 for legend/mythic, 180 for others
            if bst < 175 and 175 > duelskill and (unittype == "Legendary" or unittype == "Mythic"):
                duelskill = 175
            elif bst < 180 and 180 > duelskill and (unittype != "Legendary" or unittype != "Mythic"):
                duelskill = 180

    if duelskill != 0 and duelskill > bst: #not 0 and if duelunit has less bst than their duel skill
        bstbin = duelskill
    else:
        bstbin = bst - (bst % 5) #get bst bin (cut out anything over multples of five)

    
    if rarity == 5: #pls check this again
        score += (55 + int(lvl * (91/39))) #148 for lvl 40
    if rarity == 4:
        score += (53 + int(lvl * (84/39)))
    if rarity == 3:
        score += (51 + int(lvl * (79/39)))
    if rarity == 2:
        score += (49 + int(lvl * (73/39)))
    if rarity == 1:
        score += (47 + int(lvl * (68/39)))

    score += (bstbin/5)  #1 points every 5 bst
    score += merge * 2 #2 for every merge
    totalsp = 0 #2 points for every 100 sp of total sp (use base inheritence)
    for i in [weapon, assist, special, Askill, Bskill, Cskill, Sskill]:
        if i != "None":
            if i in dataweapon.keys():
                totalsp += int(dataweapon[i]['SP'])
            elif i in dataassist.keys():
                totalsp += int(dataassist[i]['SP'])
            elif i in dataspecial.keys():
                totalsp += int(dataspecial[i]['SP'])
            elif i in dataskill.keys():
                totalsp += int(dataskill[i]['SP'])
            #print(totalsp)
    score += int(totalsp/100) #1 for every 100sp
    #do i, count blessing since it depends on your team composion???? anyways + 4 * number of legendaries (legendarys don't get the plus 4 bonus)
    #maybe do it for like, a team compostion button........

    #score += 150 #adding the the base score(this should be after TEAM calculations)
    #also double score if bonus unit but we don


    return int(score)

def total_bst(unitstats):
    bst = unitstats[0] + unitstats[1] + unitstats[2] + unitstats[3] + unitstats[4]
    return bst

def add_merge(unit, bstats): #adding any merges after flaw and asset, 0 doesn't do anything, we don't have flaw since we already got rid of it......
    
    merge = unit.merge #number of merges (should never be 0)
    #level = unit.lvl #lvl 1 and lvl 40 is diferent calculations

    basestats = Stats(bstats) #get class unmerges stats, initialize
    rank = basestats.high_low_rank() #get rank
    addedmerge = [0,0,0,0,0] #what we return

    if merge >= 1: #+ 1 merge, always happens
        addedmerge[rank.index(1)] += 1 #get index of 1st highest (desn't matter if its the flaw)
        addedmerge[rank.index(2)] += 1 #2nd highest 
        addedmerge[rank.index(3)] += 1 #get highest 3rd stat, this increases even if you have a flaw
        if merge >= 2: #+2
            addedmerge[rank.index(3)] += 1 #3 rank
            addedmerge[rank.index(4)] += 1 #4 rank
            if merge >= 3:
                addedmerge[rank.index(5)] += 1 #5 rank
                addedmerge[rank.index(1)] += 1 #1 rank
                if merge >= 4:
                    addedmerge[rank.index(2)] += 1
                    addedmerge[rank.index(3)] += 1
                    if merge >= 5:
                        addedmerge[rank.index(4)] += 1
                        addedmerge[rank.index(5)] += 1
                        if merge >= 6:
                            addedmerge[rank.index(1)] += 1
                            addedmerge[rank.index(2)] += 1
                            if merge >= 7:
                                addedmerge[rank.index(3)] += 1
                                addedmerge[rank.index(4)] += 1
                                if merge >= 8:
                                    addedmerge[rank.index(5)] += 1
                                    addedmerge[rank.index(1)] += 1
                                    if merge >= 9:
                                        addedmerge[rank.index(2)] += 1
                                        addedmerge[rank.index(3)] += 1
                                        if merge == 10:
                                            addedmerge[rank.index(4)] += 1
                                            addedmerge[rank.index(5)] += 1
    return addedmerge #return the added stats from merge, and bst with only one merge

def stat_at_40(unit): #stats at lvl 40, don't calculate rarity yet
    rarity = unit.rarity
    asset = unit.asset
    asset2 = unit.asset2 #impliment this floral or regular asset, cannot tell difference from image
    flaw = unit.flaw
    merge = unit.merge
    index = unit.id

    basestats = [int(datastat[index]['BaseHp']), int(datastat[index]['BaseAtk']), int(datastat[index]['BaseSpd']), int(datastat[index]['BaseDef']), int(datastat[index]['BaseRes'])]
    basegrowth = [int(datastat[index]['GrowthHp']), int(datastat[index]['GrowthAtk']), int(datastat[index]['GrowthSpd']), int(datastat[index]['GrowthDef']), int(datastat[index]['GrowthRes'])]

    if asset != "None": #if has an asset
        basestats[statindex[asset]] += 1
        basegrowth[statindex[asset]] += 5

    if asset2 != "None": #if has an asset
        basestats[statindex[asset2]] += 1
        basegrowth[statindex[asset2]] += 5

    if flaw != "None": #if have a flaw
        basestats[statindex[flaw]] -= 1
        basegrowth[statindex[flaw]] -= 5

    if merge > 0: #has merges, also no flaw....
        addedbasestats = add_merge(unit, basestats) #make merges after flaw and asset, before adding growth values and after rarity application, and uses 5 star stats anyways
        
    #if rarity < 5: # rarity is less than 5
    #    stat_at_1_with_rarity(unit, rarity, asset, flaw)

    for i in range(0, 5): #adding growth values and merge to each stat lvl 1 -> 40
        basestats[i] += growthdata[rarity][growthindex[basegrowth[i]]] #added growth values
        if merge > 0: #add merge
            basestats[i] += addedbasestats[i]

    if merge == 0:
        bst = total_bst(basestats) #get bst of raw stat without merges
    else: #merges, get 
        if asset == "None":
            bst = total_bst(basestats) + 3 #regular merge up
        else: #has asset
            growthasset = basegrowth[statindex[asset]] #find growth rate of the asset
            if growthasset == 95 or growthasset == 75 or growthasset == 50 or growthasset == 30: #super asset/boon
                bst = total_bst(basestats) + 4
            else: #regular asset/boon
                bst = total_bst(basestats) + 3

    return basestats, bst #return lvl 40 stats if that rarity and bst of that unit (0 or 1 merge)

def stat_at_1_with_rarity(unit, rarity, asset, flaw): #base stats at lvl 1, don't use it on 5 since, we already have that, use to get at lower rarityies
    pass

def stat_at_that_lvl(unit, rarity, lvl, asset, flaw):
    pass

def find_skill(string, listcheck): #if string has wrong spelling, find the one close to it
    if string in listcheck.keys() or string == "None":
        return string
    else: 
        cut = .9
        while True:
            try:
                close_match = get_close_matches(string, listcheck.keys(), cutoff = cut)
                newstring = close_match[0] #use the first one
                break
            except:
                cut -= .1
        return newstring

with open("database/unit.txt", "r") as data: 
    datastat = ast.literal_eval(data.read())
with open("database/weapon.txt", "r") as data: 
    dataweapon = ast.literal_eval(data.read())
with open("database/assist.txt", "r") as data: 
    dataassist = ast.literal_eval(data.read())
with open("database/special.txt", "r") as data: 
    dataspecial= ast.literal_eval(data.read())
with open("database/skill.txt", "r") as data: 
    dataskill= ast.literal_eval(data.read())
with open("demo.txt", "r") as data: 
    database = data.readlines() #lines

heroephlet = []

for id in datastat:
    heroephlet.append(datastat[id]["Name"] + ": "+ datastat[id]["Ephlet"])


useskill = input("Use S skills in calculations?: ")
if useskill in ['Y', 'y']:
    usingSskill = True
else:
    usingSskill = False

for i in range(0, len(database), 17): #for every, block, also get the database
    str_name = database[i].split(": ")[1].strip()
    str_ephlet = database[i + 1].split(": ")[1].strip()
    int_lvl = int(database[i + 2].split(": ")[1])
    rarity = int(database[i + 3].split(": ")[1])
    int_merge = int(database[i + 4].split(": ")[1])
    str_weapon = database[i + 5].split(": ")[1].strip()
    str_assist = database[i + 6].split(": ")[1].strip()
    str_special = database[i + 7].split(": ")[1].strip()
    str_a = database[i + 8].split(": ")[1].strip()
    str_b = database[i + 9].split(": ")[1].strip()
    str_c = database[i + 10].split(": ")[1].strip()
    str_s = database[i + 11].split(": ")[1].strip()
    asset = database[i + 12].split(": ")[1].strip()
    asset2 = database[i + 13].split(": ")[1].strip()
    flaw = database[i + 14].split(": ")[1].strip()
    blessing = database[i + 15].split(": ")[1].strip()
    if (str_name + ": " + str_ephlet) not in heroephlet: #hero name or ephlet has the wrong spelling (usually hero name)
        #print(str_name + ": " + str_ephlet)
        Found = False #found name = false
        for l in heroephlet:
            if l.split(": ")[1] == str_ephlet: #if found matching ephlet
                str_name = l.split(": ")[0]
                Found = True
                break
        
        if Found == False: #if it can't find the ephlet, its an ephlet error (darn accents!!!!)
            close_match = get_close_matches((str_name + ": " + str_ephlet), heroephlet, cutoff = 0.8)
            #print(close_match)
            str_ephlet = close_match[0].split(": ")[1] #use the first one
        
        #save this for name error
    
    index = heroephlet.index(str_name + ": " + str_ephlet) + 1 #get the unit id
    weapon = datastat[index]['WeaponType'] 
    move = datastat[index]['MoveType'] 

    if 'UnitType' in datastat[index].keys(): #if duel exists
        unittype = datastat[index]['UnitType']
    else:
        unittype = "None"
    
    if 'Duel' in datastat[index].keys(): #if duel exists
        duel = datastat[index]['Duel']
    else:
        duel = "None"

    if usingSskill: #have s skills towards calualtions
        unitlist.append(Unit(str_name, str_ephlet, index, weapon, move, rarity, str_weapon, str_assist, str_special, str_a, str_b, str_c, str_s, asset, asset2, flaw, int_lvl, int_merge, unittype, duel, blessing))
    else: #get rid of them
        unitlist.append(Unit(str_name, str_ephlet, index, weapon, move, rarity, str_weapon, str_assist, str_special, str_a, str_b, str_c, 'None', asset, asset2, flaw, int_lvl, int_merge, unittype, duel, blessing))


newlist = []

for i in unitlist:
    if i.lvl == 40 and i.rarity == 5: #only 5 star lvl 40s for now
        unitstat, bst = stat_at_40(i)
        i.addstats(unitstat, bst) #add unit stats
        arenascore = arena_score(i) #calculate arena
        i.addarena(arenascore)
        #print(i.name, i.ephlet, i.merge, i.rawarenascore)
        newlist.append(i)

newlist.sort(key = lambda x : x.rawarenascore, reverse= True)
for i in newlist:
    print(i.name + ": " + i.ephlet, i.merge, i.rawarenascore, i.unitbless)