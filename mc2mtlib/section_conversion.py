from . import block_conversion
from .tile_entities import te_convert

def convert_section(
        filename,
        chunk_x,
        chunk_z,
        section_y,
        chunk
):
    converted_itemstring = {}
    converted_section = {
        'pos' : (0,0,0),
        'param0' : [0]*4096,
        'param1' : [255]*4096,
        'param2' : [0]*4096,
        'mappings' : [],
        'meta' : {},
    }

    # Convert block coordinates
    r,region_x,region_z,mca = filename.split(".")
    x = ( int(region_x) << 5) | (chunk_x)
    z = (-int(region_z) << 5) | (31-chunk_z) # Z axis is flipped
    converted_section["pos"] = (x,section_y-4,z) # shift world down 64 blocks (so sea level is around y=0 in minetest)

    # Loop on all blocks
    count = 0
    tile_cnt=0
    section = chunk.get_section(section_y)
    if not section: return

    te_metadata = None
    te_pos = 0
    for block in chunk.stream_blocks(0,section_y,True):

        # Only handling signs for now.
        if( "sign" in block.id):
          print("BLOCK regian X:%d Z:%d Section Y:%d Chunk X:%d Z:%d Count:%d"%(int(region_x),int(region_z),section_y, chunk.x, chunk.z, count));
          print("BLOCK ID:%s BLOCK:%s PROP:%s "%(block.id,repr(block),block.properties));
          myy = (section_y*16)+(count // 256)
          mysection = (count // 256) * 256
          myz = (chunk.z*16)+((count - mysection) // 16)  
          myx = (chunk.x*16)+(count - mysection - (((count - mysection) // 16) * 16))

          print("--> MINECRAFT WORLD COORDINATES X:%d Y:%d Z:%d "%(myx, myy, myz))
          a_tile_entity = chunk.get_tile_entity(myx,myy, myz)
          print(a_tile_entity)
         
          if (myy>>4) == section_y:
            #print("--> Executing conversion for minetest.....")
            myy &= 0xf
            myy = myy -16
            # within the chunk x position has to be inverted to convert to minetest:-
            myx = chunk.x*16 + 15-myx%16
                
          te_pos = ( (-myz-1)&0xf, myy&0xf, (-myx- 1)&0xf )
          print("--> MT POS for Metadata: %s"%repr(te_pos));

          # process tile_entity
          f = te_convert.get(block.name().lower(), lambda arg: (None))
          te_metadata = f(a_tile_entity)
          if te_metadata == None:
              print("No conversion found for %s"%block.name())
          else:
              print("block meta is %s"%repr(te_metadata))
          tile_cnt += 1

        y = count // 256
        z = 15 - (count // 16 % 16) # Z axis is flipped
        x = ( count % 16 )        
        count += 1
        itemstring,param1,param2 = block_conversion.convert_block(block)
        if itemstring not in converted_itemstring:
            converted_section["mappings"].append(itemstring)
            index = converted_section["mappings"].index(itemstring)
            converted_itemstring[itemstring] = index
        param0 = converted_itemstring[itemstring]
        converted_section["param0"][block_conversion.coord(z,y,x)] = param0
        converted_section["param1"][block_conversion.coord(z,y,x)] = param1
        converted_section["param2"][block_conversion.coord(z,y,x)] = param2
        if te_metadata != None:
          print ("params coordinates: %d "%(block_conversion.coord(z,y,x)));
          converted_section["meta"][te_pos] = te_metadata
          te_metadata = None # reset for next one

    if(tile_cnt > 0):
      print("SIGNS: Found %d tile entities in chunk X:%d Z:%d"%(tile_cnt,chunk.x,chunk.z));
    
    # End
    return converted_section
