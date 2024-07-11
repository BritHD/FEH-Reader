class Unit():
    def __init__(self, name, ephlet, id, classtype, movetype, rarity, weapon, assist, special, Askill, Bskill, Cskill, Sskill, asset, asset2, flaw, lvl, merge, unittype, duel, unitbless):
        self.name = name
        self.ephlet = ephlet #to diffeferient different units or alts
        self.id = id #character id
        self.classtype = classtype #the icon weapon type
        self.movetype = movetype #infantry, flyier, armor, or calv
        self.rarity = rarity
        self.weapon = weapon
        self.assist = assist
        self.special = special
        self.Askill = Askill
        self.Bskill = Bskill
        self.Cskill = Cskill
        self.Sskill = Sskill
        self.asset = asset
        self.asset2 = asset2
        self.flaw = flaw
        self.lvl = lvl
        self.merge = merge #merge number

        self.unittype = unittype #duo, harmonized, rearmed, ascended, legendary, mythic, or they are a normie
        self.duel = duel #duel put in bst IF they are a duo unit OR legendary unit with pair up
        self.unitbless = unitbless #blessing, if legendary or mythic then to their default blessing (should be the same as image says anyways)
        #none is "None" string here

    def addstats(self, unitstat, bst):
        self.stats = unitstat
        self.hp = unitstat[0]
        self.atk = unitstat[1]
        self.spd = unitstat[2]
        self.deff = unitstat[3]
        self.res = unitstat[4]
        self.bst = bst

    def addarena(self, arenascore):
        self.rawarenascore = arenascore

    def __str__(self):

        string = ("Name: " + self.name + "\n"
        "Ephlet: " + self.ephlet + "\n"
        "Level: " + str(self.lvl) + "\n"
        "Rarity: " + str(self.rarity) + "\n"
        "Merges: " + str(self.merge) + "\n"
        "Weapon: " + self.weapon + "\n"
        "Assist: " + self.assist + "\n" 
        "Special: " + self.special + "\n"
        "A Skill: " + self.Askill + "\n"
        "B Skill: " + self.Bskill + "\n" 
        "C Skill: " + self.Cskill + "\n"
        "S Skill: " + self.Sskill + "\n"
        "Asset: " + self.asset + "\n"
        "Asset2: " +self.asset2 + "\n"
        "Flaw: " + self.flaw + "\n"
        "Blessing: " + self.unitbless
        )
        return string
    
class Stats():
    def __init__(self, unitstat):

        self.hp = unitstat[0]
        self.atk = unitstat[1]
        self.spd = unitstat[2]
        self.deff = unitstat[3]
        self.res = unitstat[4]
        self.stats = unitstat

    def high_low_rank(self):
        stat = self.stats.copy()
        statsrank = [0, 0, 0, 0, 0] #listy of rank, 0 by default

        for i in range(1, 6): #for every rank (1-5)
            highest = 0
            for l in range(0, len(stat)): #check for every stat
                if stat[l] > highest:
                    highest = stat[l] #highest stat is now this
                    indexnum = l #indexnumber of highest stat
            statsrank[indexnum] = i    #index of stat is the rank now
            stat[indexnum] = 0 #pop or make 0 of the highest stat in the stat bar
        
        return statsrank #return the rank of stats
                
    def __str__(self):

        string = ("Hp: " + str(self.hp) + "\n"
        "Atk: " + str(self.atk) + "\n"
        "Spd: " + str(self.spd) + "\n"
        "Def: " + str(self.deff) + "\n"
        "Res: " + str(self.res)
        )
        return string

    

