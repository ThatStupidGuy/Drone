import json

def getFromJson(file_name):
    hex_strs = {}
    with open(file_name, 'r') as f:
        messages_file = json.loads(f.read())
        messages = messages_file["messages"]
        for message in messages:
            key = list(message.keys())[0]
            text = message[key]
            hex_strs[key] = text

    return hex_strs

def getJsonHex(file_name):
    hex_strs = getFromJson(file_name)
    for hex_str in hex_strs:
        splitHexes = hex_strs[hex_str].split()
        new_hexes = b""
        for splitHex in splitHexes:
            new_hexes += bytes.fromhex(splitHex)
        hex_strs[hex_str] = new_hexes
        print(hex_strs[hex_str])
    return hex_strs

def getTxtHex(file_name):
    hex_str = ""
    with open(file_name, 'r') as f:
        for line in f:
            hex_str += line[:49]
    
    splitHexes = hex_str.split()
    newHexes = ""
    for splitHex in splitHexes:
        newHexes += " " + splitHex

    print(newHexes)

class HexFormatter():
    def format_file(self, file_name):
        if 'json' in file_name:
            return getJsonHex(file_name)
        else:
            getTxtHex(file_name)
        