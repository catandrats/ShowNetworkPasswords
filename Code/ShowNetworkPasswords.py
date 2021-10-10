'''
Python version = 3.7
Operating system = Windows
'''

import subprocess
import tkinter as tk
'''
Builds gui
passin = Networks(list), Passwords(list)
'''
def buildGui(networklist, passwordlist):
    networkcount = len(networklist)
    root = tk.Tk()
    root.title('Network Passwords')
    frame = tk.Frame(root)
    tk.Label(frame, text = "Network\t\n").grid(row=0, column=0)#Network names listed below this
    tk.Label(frame, text = "|\n").grid(row=0, column=1)#Divider
    tk.Label(frame, text = "Password\n").grid(row=0, column=2)#Network passwords listed below this
    currentrow = 1# row in grid
    while currentrow <= networkcount:#Cycle once per network in memory
        currentindex = currentrow - 1
        tk.Label(frame, text = str(networklist[currentindex])).grid(row=currentrow, column=0)
        tk.Label(frame, text = "|").grid(row=currentrow, column=1)
        tk.Label(frame, text = str(passwordlist[currentindex])).grid(row=currentrow, column=2)
        currentrow = currentrow + 1
    frame.pack(padx=10, pady=10)
    root.mainloop()
'''
passin = NONE
returnlist = [Networks(list), Password(list)]
'''
def fetchNetworksandPasswords():
    data = subprocess.check_output(['netsh', 'wlan', 'show', 'profiles']).decode('utf-8').split('\n')
    networks = []
    for x in data:
        if 'All User Profile' in x:
            colon = x.index(' : ')
            new_x_one = x[colon:]
            new_x_two = new_x_one.replace(' : ', '')
            new_x_final = new_x_two.replace('\r', '')
            networks.append(new_x_final)
    profiles = [i.split(":")[1][1:-1] for i in data if "All User Profile" in i]
    passwordlist = []
    for i in profiles:
        results = subprocess.check_output(['netsh', 'wlan', 'show', 'profile', i, 'key=clear']).decode('utf-8').split('\n')
        results = [b.split(":")[1][1:-1] for b in results if "Key Content" in b]
        for y in results:
            passwordlist.append(str(y))
    returnlist = []
    returnlist.append(networks)
    returnlist.append(passwordlist)
    return returnlist
'''
This is just for ease of use should you choose to incorperate this into your own python project.
Just call this function to make the Gui pop up.
'''
def tellnetworkpasswordstoGui():
    uselists = fetchNetworksandPasswords()
    buildGui(uselists[0], uselists[1])
tellnetworkpasswordstoGui()