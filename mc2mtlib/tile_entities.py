import re
from .itemstack import *

def convert_chest(te):
    formspec = "size[8,9]"+\
               "list[current_name;main;0,0;8,4;]"+\
               "list[current_player;main;0,5;8,4;]"
    fields = {"infotext": "Chest",
              "formspec": formspec}
    inventory = {"main": (0, [MTItemStack()]*32)}
    # Transfer the content of TE inventory into the MT one.
    items = {}
    try:
        items = te["Items"]
    except KeyError:
        items = {}

    # EXAMPLE [TAG_Compound: {3 Entries}, TAG_Compound: {3 Entries}, TAG_Compound: {3 Entries}]

    for item in items:
       iid = item['id'].value
       print(item)
       

    return (fields, inventory)

def escape(s):
    s2 = ""
    for c in s:
        if c in ["'", '"', "\\"]:
            s2 += "\\"
            s2 += c
        elif c == "\n":
            s2 += "\\n"
        elif c == "\t":
            s2 += "\\t"
        else:
            s2 += c
    return s2

def convert_sign(te):
    t = ""
    for i in range(1, 5):
        line = te.get("Text"+str(i), "").valuestr().strip('"')
        if '{"text":"' in line:
            parts = line.split('"')
            line = parts[3]
        if line != "":
            t += line
            t += "\n"
    t = t.strip()
    fields = {"infotext": "sign",
              "text": t,
              "formspec": "size[6,4]textarea[0,-0.3;6.5,3;text;;${text}]button_exit[2,3.4;2,1;ok;Write]"}

    # TODO PLAY WITH BETTER FROMSPEC
    #fields = {"infotext": "sign",
    #          "text": t,
    #          "__signslib_new_format": "1",
    #          "formspec": "size[6,4]textarea[0,-0.3;6.5,3;text;;${text}]button_exit[2,3.4;2,1;ok;Write]background[-0.5,-0.5;7,5;bg_signs_lib.jpg]"}
    return (fields, {})

def convert_pot(te):
    c = str(te.get("Item"))+":"+str(te.get("Data"))
    # translation table for flowers
    # highly approximate, based on color only
    t = {
        "minecraft:air:0" : 0,
        "minecraft:brown_mushroom:0" : 1,
        "minecraft:red_mushroom:0" : 2,
        "minecraft:cactus:0" : 3,
        "minecraft:deadbush:0" : 4,
        "minecraft:red_flower:0" : 5,
        "minecraft:red_flower:1" : 6,
        "minecraft:red_flower:2" : 7,
        "minecraft:red_flower:3" : 8,
        "minecraft:red_flower:4" : 9,
        "minecraft:red_flower:5" : 10,
        "minecraft:red_flower:6" : 11,
        "minecraft:red_flower:7" : 12,
        "minecraft:red_flower:8" : 13,
        "minecraft:sapling:0" : 14,
        "minecraft:sapling:1" : 15,
        "minecraft:sapling:2" : 16,
        "minecraft:sapling:3" : 17,
        "minecraft:sapling:4" : 18,
        "minecraft:sapling:5" : 19,
        "minecraft:tallgrass:2" : 20,
        "minecraft:yellow_flower:0" : 21
    }
    try:
        fields = { "_plant": t[c] }
        return (fields, {})
    except:
        print('Unknown flower pot type: ' + c)
        return None

te_convert = {"minecraft:birch_sign": convert_sign,
              "minecraft:oak_sign": convert_sign,
              "minecraft:crimson_sign": convert_sign,
              "minecraft:crimson_wall_sign": convert_sign,
              "minecraft:spruce_sign": convert_sign,
              "minecraft:spruce_wall_sign": convert_sign,
              "minecraft:warped_wall_sign": convert_sign,
              "minecraft:warped_sign": convert_sign,
              "minecraft:jungle_sign": convert_sign,
              "minecraft:jungle_wall_sign": convert_sign,
              "minecraft:acacia_sign": convert_sign,
              "minecraft:acacia_wall_sign": convert_sign,
              "minecraft:dark_oak_sign": convert_sign,
              "minecraft:dark_oak_wall_sign": convert_sign,
              "minecraft:sign": convert_sign,
              "minecraft:oak_wall_sign": convert_sign,
              "minecraft:birch_wall_sign": convert_sign,
              "minecraft:flower_pot": convert_pot}

# DISABLING CHEST FOR NOW
#te_convert = {"minecraft:chest": convert_chest,
#              "minecraft:sign": convert_sign,
#              "minecraft:oak_wall_sign": convert_sign,
#              "minecraft:birch_wall_sign": convert_sign,
#              "minecraft:flower_pot": convert_pot}

