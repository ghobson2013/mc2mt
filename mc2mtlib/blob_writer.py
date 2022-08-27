import io,zlib
from .serialize import *
from .itemstack import *
from .block_conversion import coord

def write_blob(converted_section):

    out = io.BytesIO()
    writeU8(out, 27)      # Version 27
    writeU8(out, 0b0110)  # flags
    writeU16(out, 0xF000) # recompute light
    writeU8(out, 2)       # content_width
    writeU8(out, 2)       # params_width

    # Node Data
    node_data = io.BytesIO()
    for param0 in converted_section["param0"]: writeU16(node_data,param0)                  
    for param1 in converted_section["param1"]: writeU8(node_data,param1)
    for param2 in converted_section["param2"]: writeU8(node_data,param2)
    out.write(zlib.compress(node_data.getvalue()))
    node_data.close()
    
    # Nodemeta  
    meta = converted_section["meta"]
    
    node_metadata = io.BytesIO()
    writeU8(node_metadata, 1)  # Version
    writeU16(node_metadata, len(meta)) # length
    if meta != {}:
      for pos, data in meta.items():
        #print("adding meta for POS:%s  DATA:%s "%(repr(pos),data));
        writeU16(node_metadata, coord(pos[0],pos[1],pos[2]))
        writeU32(node_metadata, len(data[0]))
        for name, val in data[0].items():
          #print("--> %s: %s"%(name,str(val)));
          writeString(node_metadata, name)
          writeLongString(node_metadata, str(val))
        #print("serializing inventory %s "%data[1]);
        serialize_inv(node_metadata, data[1])
    out.write(zlib.compress(node_metadata.getvalue()))
    node_metadata.close()
    
    writeU8(out, 0)           # Static object version
    writeU16(out, 0)          # Number of static objects
    writeU32(out, 0xffffffff) # BLOCK_TIMESTAMP_UNDEFINED

    # Name-ID mapping
    mappings = converted_section["mappings"]
    writeU8(out, 0)             # Version
    writeU16(out, len(mappings)) # number of mappings
    for n in range(len(mappings)):
        b = bytes(mappings[n],"utf-8") 
        writeU16(out, n)
        writeU16(out, len(b))
        out.write(b)

    # Node timer
    writeU8(out, 2+4+4) # Timer data len
    writeU16(out, 0)    # Number of timers
    
    #End
    ret = out.getvalue()
    out.close()
    return ret
