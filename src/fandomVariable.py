fandomList = ["celeste", "hypixel", "hypixelskyblock", "animalcrossing", "animalcrossingnewhorizons", "rlcraft", "riskofrain", "riskofrain2", "minecraft" ]

def getFandomVariable(trimString):
  fandom = ""
  for i in fandomList:
    if i in trimString:
      fandom = i
      break
  if fandom != "":
    return fandom
  else:
    print("We couldn't figure out what fandom you are trying to access! Try again.")