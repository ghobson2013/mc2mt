materials = {
    "acacia" : "acacia_wood",
    "andesite" : "stone",
    "birch" : "aspen_wood",
    "brick" : "brick",
    "cobblestone" : "cobble",
    "cut_red_sandstone" : "desert_stone_block",
    "cut_sandstone" : "sandstone_block",
    "dark_oak" : "wood",
    "dark_prismarine" : "ice",
    "diorite" : "silver_sandstone",
    "smooth_diorite": "silver_sandstone",
    "end_stone_brick" : "sandstonebrick",
    "granite" : "desert_cobble",
    "jungle" : "junglewood",
    "mossy_cobblestone" : "mossycobble",
    "mossy_stone_brick" : "mossycobble",
    "nether_brick" : "desert_stonebrick",
    "oak" : "wood",
    "petrified_oak" : "wood",
    "polished_andesite" : "stone",
    "polished_diorite" : "silver_sandstone",
    "polished_granite" : "stone",
    "prismarine" : "ice",
    "prismarine_brick" : "ice",
    "purpur" : "goldblock",
    "quartz" : "steelblock",
    "red_nether_brick" : "desert_stonebrick",
    "red_sandstone" : "desert_stone",
    "sandstone" : "sandstone",
    "smooth_quartz" : "steelblock",
    "smooth_red_sandstone" : "desert_stone_block",
    "smooth_sandstone" : "sandstone_block",
    "smooth_stone" : "stone_block",
    "spruce" : "pine_wood",
    "stone" : "stone",
    "stone_brick" : "stonebrick",
}

# Materials
def id2material(block):
    parts = block.id.split("_")
    for i in range(1,len(parts)):
        key_part = ("_".join(parts[:i]))
        if key_part in materials: return materials[key_part]
    for i in range(1,len(parts)):
        key_part = ("_".join(parts[i:]))
        if key_part in materials: return materials[key_part]
    return "wood"

# Flowing Liquids
def level2flowingliquid(block):
    return int(prop(block,"level"))//2

# Facedir
def rotation2facedir(block):
    return {
        "15":1,"0":1,"1":1,"2":1,
        "3":2,"4":2,"5":2,"6":2,
        "7":3,"8":3,"9":3,"10":3,
        "11":4,"12":4,"13":4,"14":4,
    }.get(prop(block,"rotation"),0)

def rail2shape(block):
    return {
        "east_west": 2, "north_south": 1, "ascending_east": 3, "ascending_south": 4
    }.get(prop(block,"shape"),0)

def cardinal2facedir(block):
    if prop(block,'north')=='true': return 1
    if prop(block,'south')=='true': return 0
    if prop(block,'east')=='true': return 2
    if prop(block,'west')=='true': return 3
    return 0

def cardinalVine2facedir(block):
    if prop(block,'north')=='true': return 5
    if prop(block,'south')=='true': return 4
    if prop(block,'east')=='true': return 3
    if prop(block,'west')=='true': return 2
    if prop(block,'up')=='true': return 0
    return 0

def type2facedir(block):
    atype = {
        "bottom":0,"top":22,"double":0
    }.get(prop(block,"type"),0)  
    #print ("BLOCK %s %s --> %d "%(block,repr(block.properties),atype));
    return atype

def facing2facedir(block):
    return {
        "north":2,"east":3,"south":0,"west":1,"up":4,"down":8
    }.get(prop(block,"facing"),0)
   

def carpetFacing2facedir(block):
    return {
        "north":8,"east":16,"south":4,"west":12
    }.get(prop(block,"facing"),0)

# Wallmounted
def facing2wallmounted(block):
    if prop(block,"up") in ["true"]:
        return {
            "north":5,"east":3,"south":4,"west":2
        }.get(prop(block,"facing"),0)
    else:
        return {
            "north":5,"east":3,"south":4,"west":2
        }.get(prop(block,"facing"),0)

# lever  MT doesnt support floor lever
def lever2wallmounted(block):
    if prop(block,"face") in ["wall"]:
        return {
            "north":2,"east":3,"south":0,"west":1
        }.get(prop(block,"facing"),0)
    else:
        return {
            "north":0,"east":1,"south":2,"west":3
        }.get(prop(block,"facing"),0)

    
# Stairs
def stair2facedir(block):
    if prop(block,"shape") == "straight":
        if prop(block,"half") == "bottom" :
            return { "north":0,"east":1,"south":2,"west":3 }.get(prop(block,"facing"),0)
        else:        
            return { "north":20,"east":23,"south":22,"west":21 }.get(prop(block,"facing"),20)
    
    if prop(block,"shape") == "outer_right":
        if prop(block,"half") == "bottom" :
            return { "north":2,"east":1,"south":0,"west":3 }.get(prop(block,"facing"),0)
        else:
            return { "north":20,"east":23,"south":22,"west":21 }.get(prop(block,"facing"),20)
    
    if prop(block,"shape") in ["outer_left"]:
        if prop(block,"half") == "bottom" :
            return { "north":0,"east":1,"south":2,"west":3 }.get(prop(block,"facing"),0)
        else:
            return { "north":21,"east":20,"south":23,"west":22 }.get(prop(block,"facing"),20)
    
    if prop(block,"shape") == "inner_right":
        if prop(block,"half") == "bottom" :
            return { "north":1,"east":2,"south":3,"west":0 }.get(prop(block,"facing"),0)
        else:
            return { "north":20,"east":23,"south":22,"west":21 }.get(prop(block,"facing"),20)
    else: # Inner Left 
        if prop(block,"half") == "bottom" :
            return { "north":0,"east":1,"south":2,"west":3 }.get(prop(block,"facing"),0)
        else:
            return { "north":21,"east":20,"south":23,"west":22 }.get(prop(block,"facing"),20)


def shape2stair(block):
    return "stairs:stair" + {
        "straight":"",
        "outer_right":"_outer",
        "outer_left":"_outer",
        "inner_right":"_inner",
        "inner_left":"_inner"
    }.get(prop(block,"shape"),"") +\
    "_" + id2material(block)

def material2slab(block):
    return "stairs:slab_" + id2material(block)

# Doors
def door2ab(block):
    if str(block.properties["half"]) == "upper": return "air"
    material = "iron" in block.id and "steel" or "wood"
    return "doors:door_" + material + {
        ("true","right"):"_b",
        ("true","left"):"_a",
        ("false","left"):"_b",
        ("false","right"):"_a"
    }.get((prop(block,"open"),prop(block,"hinge")),"_a")

def door2facedir(block):
    return ( {
        "north":0,"east":1,"south":2,"west":3
    }.get(prop(block,"facing"),0) + {
        "true":0,"false":1
    }.get(prop(block,"open"),0) * {
        "right":-1,"left":1
    }.get(prop(block,"hinge"),0) ) % 4

# Utilities
def prop(block,key,default=None):
    return str(block.properties.get(key,default))
