import requests
from bs4 import BeautifulSoup
import os
import ast
from difflib import get_close_matches

os.chdir(os.path.dirname(os.path.abspath(__file__))) #path directory of this script to get stuff

def make_data(name):
    database = {}
    filethis = open("database/" + name + ".txt", 'w')
    filethis.write("{}")
    filethis.close()
    return database
if not os.path.exists('database'): 
    os.makedirs('database') 

weapondata = make_data("weapon")
assistdata = make_data("assist")
specialdata = make_data("special")
skilldata = make_data("skill") #includes a, b, c, and s
unitdata = make_data("unit")

for k in range(0, 50000, 500): #we basically do this everytime lol
    skilljson = "https://feheroes.fandom.com/api.php?action=cargoquery&format=json&limit=500&tables=Skills&fields=Name%2C%20Scategory%2C%20SP%2C%20CanUseMove%2C%20CanUseWeapon%2C%20Properties&offset=" + str(k) #weapons, assist, special, and all skills
    #print(skilljson)
    r = requests.get(skilljson)
    soup = r.json()
    print(len(soup['cargoquery']))
    if len(soup['cargoquery']) == 0: #no more json
        break
    for i in soup['cargoquery']: #don't use get the skill restrictions, yet...
        name = i['title']['Name']
        skilltype = i['title']['Scategory']
        sp = i['title']['SP']
        property = i['title']["Properties"]
        if skilltype == 'weapon': #if refined then it will show up 5 times lmao, otherwise no different skills have the same name!!! yessss
            if property is not None and "arcane" in property:
                weapondata[name] = {"Category": "Weapon", "SP": str(300)} #arcanes are at default 300, but refined its 350
            else:
                weapondata[name] = {"Category": "Weapon", "SP": sp}
        elif skilltype == 'assist':
            assistdata[name] = {"Category": "Assist", "SP": sp}
        elif skilltype == 'special':
            specialdata[name] = {"Category": "Special", "SP": sp}
        elif skilltype == 'passivea':
            skilldata[name] = {"Category": "ASkill", "SP": sp}
        elif skilltype == 'passiveb':
            skilldata[name] = {"Category": "BSkill", "SP": sp}
        elif skilltype == 'passivec':
            skilldata[name] = {"Category": "CSkill", "SP": sp}
        elif skilltype == 'sacredseal':
            skilldata[name] = {"Category": "SSkill", "SP": sp} #sacred seal exclusive
        elif skilltype == 'captain':
            skilldata[name] = {"Category": "Captain", "SP": str(sp)} #captain skills
        elif skilltype == 'passivex':
            skilldata[name] = {"Category": "Xskill", "SP": str(sp)} #cx skills
        else:
            print(name, skilltype, sp, property) #Is adding new types of skills every 6 months lmao
print("Weapons:", len(weapondata))
print("Assists:", len(assistdata))
print("Specials:", len(specialdata))
print("Skills:", len(skilldata))

filethis = open("database/weapon.txt", 'w')
filethis.write(str(weapondata))
filethis.close()

filethis = open("database/assist.txt", 'w')
filethis.write(str(assistdata))
filethis.close()

filethis = open("database/special.txt", 'w')
filethis.write(str(specialdata))
filethis.close()

filethis = open("database/skill.txt", 'w')
filethis.write(str(skilldata))
filethis.close()

for k in range(0, 5000, 500): #unit data
    unitjson = "https://feheroes.fandom.com/api.php?action=cargoquery&format=json&limit=500&tables=Units&fields=Name%2C%20Title%2C%20GameSort%2C%20TagID%2C%20IntID%2C%20WeaponType%2C%20MoveType%2C%20Properties&offset=" + str(k)
    r = requests.get(unitjson)
    soup = r.json()
    print(len(soup['cargoquery']))
    if len(soup['cargoquery']) == 0: #no more json
        break
    for i in soup['cargoquery']: #don't use get the skill restrictions, yet...
        if "EID" in i['title']['TagID']: #enemy
            continue #skip loop
        id = int(i['title']['IntID'])
        name = i['title']['Name']
        title = i['title']['Title']
        weapon = i['title']['WeaponType']
        move = i['title']['MoveType']
        game = int(i['title']['GameSort'])
        unitdata[id] = {"Name": name, "Ephlet": title, "WeaponType": weapon, "MoveType": move, "GameNum": game}
        property = i['title']['Properties']
        if property is None:
            pass
        elif "legendary" in property:
            unitdata[id]["UnitType"] = "Legendary"
        elif "mythic" in property:
            unitdata[id]["UnitType"] = "Mythic"
        elif "duo" in property:
            unitdata[id]["UnitType"] = "Duo"
        elif "harmonized" in property:
            unitdata[id]["UnitType"] = "Harmonized"
        elif "ascended" in property:
            unitdata[id]["UnitType"] = "Ascended"
        elif "rearmed" in property:
            unitdata[id]["UnitType"] = "Rearmed"
        elif "attuned" in property:
            unitdata[id]["UnitType"] = "Attuned"
        #else:
        #    print(property) #type 
            

database2 = {}
for i in range(1, len(unitdata) + 1): #sort by... string number?
    database2[i] = unitdata[i]

unitdata = database2.copy()
name_eph = []
for id in unitdata: #for indexing
    name_eph.append(unitdata[id]["Name"] + ": " + unitdata[id]["Ephlet"])

for k in range(0, 5000, 500): #getting growths
    unitstatjson = 'https://feheroes.fandom.com/api.php?action=cargoquery&format=json&limit=500&tables=UnitStats&fields=_pageName%20%3D%20Page%2C%20%20WikiName%2C%20Lv1HP5%2C%20Lv1Atk5%2C%20Lv1Spd5%2C%20Lv1Def5%2C%20Lv1Res5%2C%20HPGR3%2C%20AtkGR3%2C%20SpdGR3%2C%20DefGR3%2C%20ResGR3&offset=' + str(k)
    r = requests.get(unitstatjson)
    soup = r.json()
    print(len(soup['cargoquery']))
    if len(soup['cargoquery']) == 0: #no more json
        break
    for i in soup['cargoquery']:
        if "ENEMY" in i['title']['WikiName']: #enemy
            continue #skip loop
        ne = i['title']['Page']
        ix = name_eph.index(ne) + 1 #find index of name eph + 1 to equal char id
        unitdata[ix]['BaseHp'] = int(i['title']['Lv1HP5'])
        unitdata[ix]['BaseAtk'] = int(i['title']['Lv1Atk5'])
        unitdata[ix]['BaseSpd'] = int(i['title']['Lv1Spd5'])
        unitdata[ix]['BaseDef'] = int(i['title']['Lv1Def5'])
        unitdata[ix]['BaseRes'] = int(i['title']['Lv1Res5'])
        unitdata[ix]['GrowthHp'] = int(i['title']['HPGR3'])
        unitdata[ix]['GrowthAtk'] = int(i['title']['AtkGR3'])
        unitdata[ix]['GrowthSpd'] = int(i['title']['SpdGR3'])
        unitdata[ix]['GrowthDef'] = int(i['title']['DefGR3'])
        unitdata[ix]['GrowthRes'] = int(i['title']['ResGR3'])

for k in range(0, 5000, 500): #bvid
    bvidjson = "https://feheroes.fandom.com/api.php?action=cargoquery&format=json&limit=500&tables=HeroBVIDs&fields=Hero%2C%20BVID&offset="+ str(k) #name and bvid
    r = requests.get(bvidjson)
    soup = r.json()
    print(len(soup['cargoquery']))
    if len(soup['cargoquery']) == 0: #no more json
        break
    for i in soup['cargoquery']: #don't use get the skill restrictions, yet...
        ne = i['title']['Hero']
        ix = name_eph.index(ne) + 1 #find index of name eph + 1 to equal char id
        unitdata[ix]['BVID'] = i['title']['BVID']

for k in range(0, 1000, 500): #getting the duel numbers for legendaries (if applies), and blessings
    legendjson = "https://feheroes.fandom.com/api.php?action=cargoquery&format=json&limit=500&tables=LegendaryHero&fields=_pageName%20%3D%20Page%2C%20LegendaryEffect%2C%20Duel&offset=" + str(k)
    r = requests.get(legendjson)
    soup = r.json()
    print(len(soup['cargoquery']))
    if len(soup['cargoquery']) == 0: #no more json
        break
    for i in soup['cargoquery']:
        ne = i['title']['Page']
        ix = name_eph.index(ne) + 1 #find index of name eph + 1 to equal char id
        unitdata[ix]['Blessing'] = i['title']['LegendaryEffect']
        if int(i['title']['Duel']) != 0: #if legendary hero has a duel skills
            unitdata[ix]['Duel'] = int(i['title']['Duel'])

for k in range(0, 1000, 500): #getting the duel numbers for duos
    duojson = "https://feheroes.fandom.com/api.php?action=cargoquery&format=json&limit=500&tables=DuoHero&fields=_pageName%20%3D%20Page%2C%20Duel&offset=" + str(k)
    r = requests.get(duojson)
    soup = r.json()
    print(len(soup['cargoquery']))
    if len(soup['cargoquery']) == 0: #no more json
        break
    for i in soup['cargoquery']:
        ne = i['title']['Page']
        ix = name_eph.index(ne) + 1 #find index of name eph + 1 to equal char id
        unitdata[ix]['Duel'] = int(i['title']['Duel'])

for k in range(0, 1000, 500): #getting the duel blessing for mythics
    mythicjson = "https://feheroes.fandom.com/api.php?action=cargoquery&format=json&limit=500&tables=MythicHero&fields=_pageName%20%3D%20Page%2C%20MythicEffect&offset=" + str(k)
    r = requests.get(mythicjson)
    soup = r.json()
    print(len(soup['cargoquery']))
    if len(soup['cargoquery']) == 0: #no more json
        break
    for i in soup['cargoquery']:
        ne = i['title']['Page']
        ix = name_eph.index(ne) + 1 #find index of name eph + 1 to equal char id
        unitdata[ix]['Blessing'] = i['title']['MythicEffect']

print("Units:", len(unitdata))

filethis = open("database/unit.txt", 'w')
filethis.write(str(unitdata))
filethis.close()

    