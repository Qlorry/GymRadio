import json
import os

file = open("Radio/RadioROKS.m3u", "r+")
filedata = file.readlines()
file.close()
index = 1
while index < len(filedata):
    print(filedata[index + 2])
    url = filedata[index + 2]
    name = url.split("/")[-1]
    print(name.replace("\n", ""))
    index += 5
