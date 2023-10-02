print("hello there")
import os
backSlash = '\\'
os.system(f'''"{__file__[:__file__.replace(backSlash,'/').rfind('/')] + '/data/obi-wan kenobi pfp.jpg'}"''')

def abracadabra():
    print("simsalabim")