val = []
for x in range(13):
    for y in range(18):
        val.append({"texture":f"Overworld_Tileset_{x:02d}_{y:02d}"})
for x in range(13):
    for y in range(12):
        val.append({"texture":f"Dungeon_Tileset_{x:02d}_{y:02d}"})


print(val)