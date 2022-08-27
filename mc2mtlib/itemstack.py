class MCItemStack:
    def __init__(self):
        pass

class MTItemStack:
    def __init__(self):
        pass

    def fromMCItemStack(self, mcstack):
        pass

    def empty(self):
        return True

    def serialize(self, os):
        pass

def serialize_inv_list(os, inv_list):
    for item in inv_list[1]:
        if item == '':
            os.write(bytes("Empty", "utf-8"))
        else:
            os.write(bytes("Item "+str(item), "utf-8"))
        os.write(bytes("\n", "utf-8"))
    os.write(bytes("EndInventoryList\n", "utf-8"))

def serialize_inv(os, inv):
    for name, inv_list in inv.items():
        os.write(bytes("List "+name+" "+str(len(inv_list[1]))+"\n", "utf-8"))
        serialize_inv_list(os, inv_list)
    os.write(bytes("EndInventory\n", "utf-8"))

