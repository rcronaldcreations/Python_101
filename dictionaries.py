# import maya.cmds as cmds

# Declare an empty dict
mydictionary = {}

# Append new items to it
mydictionary['fruit'] = [['apple', [1.0, 1.0, 1.0]], ['orange', [2.0, 2.0, 2.0]]]
mydictionary['veg'] = [['kale', [1.0, 1.0, 1.0]], ['carrots', [2.0, 2.0, 2.0]]]

for key, value in mydictionary.items():
    print(key, value)

for i in range(len(mydictionary)):
    print(mydictionary['fruit'][i])
    print(mydictionary['veg'][i])
