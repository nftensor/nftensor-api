#fimbrethil

import bittensor as bt
from PIL import Image, ImageDraw, ImageFont, ImageColor


#from user, input
input = "Who is Rob Maron, employee of Foundry Digital LLC?"

#query bittensor with user input
resp = bt.prompt( input, hotkey = "5F4tQyWrhfGVcNhoqeiNsR6KjD4wMZ2kfhLj4oHYuyHbZAc3")

#take first sentence of resp
per = resp.split(".")
que = resp.split("?")
exc = resp.split("!")

if(len(per[0]) < len(que[0]) and len(per[0]) < len(exc[0])):
    out = per[0] + "."  
elif(len(que[0]) < len(per[0]) and len(que[0]) < len(exc[0])):
    out = que[0] + "?"   
else:
    out = exc[0] + "!"


