import customtkinter
import keyboard 
import winsound
import time
import threading 

class Reminder:    
    def __init__(self, length: float, soundLocation: str ,name:str):
        self.length = length
        self.soundLocation = soundLocation
        self.name = name
    


def  saveCurrentSettings(): 
    global closeApplicationShortcut
    global openSettingsWindowShortcut
    
    remindersSaveStr = ""
    global reminders
    for reminder in reminders:
        remindersSaveStr += "\n"+str( reminder.length)+"\n"+reminder.soundLocation+"\n"+reminder.name
    
    
    with open(saveFileLocation,"w") as saveFile:
        saveFile.write(closeApplicationShortcut+"\n"+openSettingsWindowShortcut+remindersSaveStr) 
    
    
saveFileLocation = "OptionsSaveFile.txt"


closeApplicationShortcutOffset = 0
openSettingsWindowShortcutOffset = 1
##? save file structure:
# closeApplicationShortcut \n
# openSettingsWindowShortcut \n

# 1'st ReminderLength \n
# 1'st ReminderSoundLocation \n
# 1'st ReminderName \n
# 2'nd ReminderLength \n
# 2'nd ReminderSoundLocation \n
# 2'nd ReminderName \n
# ...
lengthOffsetInsideReminderClass = 0
soundLocationOffsetInsideReminderClass = 1
nameOffsetInsideReminderClass = 2

remindersArrayOffset = 2
reminderClassSaveSize = 3

reminders = []
#* loads settings from save file


try:
    with open(saveFileLocation,"r") as saveFile:
        currentSettings = saveFile.read().splitlines()
    closeApplicationShortcut =currentSettings[closeApplicationShortcutOffset]
    #print(r"{"+closeApplicationShortcut+"}") 
    openSettingsWindowShortcut =currentSettings[openSettingsWindowShortcutOffset]
    #print(r"{"+openSettingsWindowShortcut+"}") 
    
    for reminderIndex in range(round((len(currentSettings) - remindersArrayOffset)/reminderClassSaveSize)):
        
        reminderClassBeginningIndex = reminderIndex*reminderClassSaveSize +remindersArrayOffset
        reminderLength: float = float( currentSettings[reminderClassBeginningIndex +lengthOffsetInsideReminderClass])
        reminderSoundLocation: str =  currentSettings[reminderClassBeginningIndex +soundLocationOffsetInsideReminderClass]
        reminderName: str =  currentSettings[reminderClassBeginningIndex +nameOffsetInsideReminderClass]
                
        reminders.append(Reminder(length= reminderLength,soundLocation= reminderSoundLocation,name=reminderName))
#* if there is no save file it'll create a standard one
except OSError:
    print("no file")
    closeApplicationShortcut = "ctrl+shift+x"
    openSettingsWindowShortcut = "ctrl+shift+a"
    saveCurrentSettings()
    
        

def runReminder(reminder: Reminder):
    global closeAllThreads
    while True:
        winsound.PlaySound(reminder.soundLocation,0)
        time.sleep(reminder.length)

for reminder in reminders:
    threading.Thread(target= runReminder, args=(reminder,), daemon= True).start()

closeApplicationShortcutTextBox = customtkinter.CTkEntry

class ReminderDisplayUi :
    def __init__(self, name : customtkinter.CTkEntry, length : customtkinter.CTkEntry, soundLocation : customtkinter.CTkEntry, frame :customtkinter.CTkFrame):
       self.name = name
       self.length = length
       self.soundLocation = soundLocation
       self.frame = frame
    def destroy(self):
        self.frame.destroy()
       
allReminderDisplays = []
root = None
def  displayUi():
    for reminderDisplay in allReminderDisplays:
        reminderDisplay.destroy()
    allReminderDisplays.clear()
    print("displayUi")

    customtkinter.set_appearance_mode("system")
    customtkinter.set_default_color_theme("green")
    global root
    if(root is not None):
        root.quit()
        root.destroy()
   
        
    
    root = customtkinter.CTk()
    root.geometry("1000x1200")
    frame = customtkinter.CTkFrame(master= root, border_width= 20)
    
   
    
    applyButton = customtkinter.CTkButton(master= root, width= 250, text= "Apply", font=("Arial",20),command=ApplyButtonPressed)
    applyButton.place(relx = .5, rely =  .95, anchor = "center")
    
    
    neFrame = customtkinter.CTkFrame(root, width= 400, height = 1000)
    neFrame.grid_configure(row= len(reminders)+1, sticky="ne",)
    neFrame.place(relx = .9, rely =  .03, anchor = "ne")
    
    addReminderButton = customtkinter.CTkButton(master= neFrame, width= 350, text= "Add new reminder", font=("Arial",20), command= AddNewReminder)
    addReminderButton.place(relx = .5, rely =  .02, anchor = "n")
    addReminderButton.grid(row=0, column=0, padx=20, pady=20, sticky="n")
     
    remindersStartY = .2 
    reminderSize = .2
    reminderIndex = 0
    for reminder in reminders:
        reminderFrame = customtkinter.CTkFrame(neFrame, width= 400, height = 110)
        #reminderFrame.place(relx = .5, rely = remindersStartY +reminderSize*reminderIndex, anchor = "n")  
        reminderFrame.grid(row=reminderIndex +1, column=0, padx=5, pady=5, sticky="n")
        
        reminderNameTextBox = customtkinter.CTkEntry(master= reminderFrame, width= 350,font=("Arial",25), height = 15,placeholder_text="name")
        reminderNameTextBox.place(relx = .5 , rely =  .05, anchor = "n")
        if(reminder.name != ""):
            reminderNameTextBox.insert(0,reminder.name)

        reminderLengthTextBox = customtkinter.CTkEntry(master= reminderFrame,placeholder_text="delay", width= 350, height = 15,font=("Arial",20))
        reminderLengthTextBox.place(relx = .5 , rely =  .4, anchor = "n")
        if(reminder.length != ""):
            reminderLengthTextBox.insert(0,reminder.length)
        
        reminderSoundLocalizationTextBox = customtkinter.CTkEntry(master= reminderFrame,placeholder_text="localization of sound for this reminder", width= 350, height = 15,font=("Arial",20))
        reminderSoundLocalizationTextBox.place(relx =  .5, rely = .7, anchor = "n")
        if(reminder.soundLocation != ""):
            reminderSoundLocalizationTextBox.insert(0,reminder.soundLocation)
        
        deReference = reminderIndex
        removeReminderButton = customtkinter.CTkButton(master= reminderFrame, width= 50, text= "remove", font=("Arial",20), command= lambda: RemoveReminder(reminderIndex=deReference),hover_color= "red", fg_color= "red")
        removeReminderButton.place(relx = .8, rely =  .02, anchor = "nw")
        
        allReminderDisplays.append(ReminderDisplayUi(name=reminderNameTextBox, length= reminderLengthTextBox,soundLocation= reminderSoundLocalizationTextBox, frame=reminderFrame))
        
        reminderIndex +=1

        
        
    nwFrame = customtkinter.CTkFrame(root, width= 300, height = 200)
    nwFrame.place(relx = .1, rely =  .03, anchor = "nw")
    
    closeApplicationShortcutTextHeader = customtkinter.CTkLabel(master= nwFrame, width= 250, text= "Shortcut to close the app", font=("Arial",20))
    closeApplicationShortcutTextHeader.place(relx = .5, rely =  .0, anchor = "n")

    global closeApplicationShortcutTextBox
    closeApplicationShortcutTextBox = customtkinter.CTkEntry(master= nwFrame,placeholder_text="shortcut for closing the app", width= 250,font=("Arial",20))
    closeApplicationShortcutTextBox.place(relx = .5, rely =  .25, anchor = "n")
    closeApplicationShortcutTextBox.insert(0,closeApplicationShortcut)
    
    
    openSettingsShortcutTextHeader = customtkinter.CTkLabel(master= nwFrame, width= 250, text= "Shortcut to open settings ui", font=("Arial",20))
    openSettingsShortcutTextHeader.place(relx = .5, rely =  .5, anchor = "n")

    global openSettingsShortcutTextBox
    openSettingsShortcutTextBox = customtkinter.CTkEntry(master= nwFrame,placeholder_text="Shortcut to open settings ui", width= 250,font=("Arial",20))
    openSettingsShortcutTextBox.place(relx = .5, rely =  .75, anchor = "n")
    openSettingsShortcutTextBox.insert(0,openSettingsWindowShortcut)
    
    
    
    
    
    winsound.MessageBeep(3)
    root.mainloop()
    
    
def ApplyButtonPressed():
    global closeApplicationShortcut
    #remove old hotkey
    keyboard.remove_hotkey(closeApplicationShortcut)
    
    closeApplicationShortcut= closeApplicationShortcutTextBox.get()
    
    
    global  openSettingsWindowShortcut 
    #remove old hotkey
    keyboard.remove_hotkey(openSettingsWindowShortcut)

    openSettingsWindowShortcut= openSettingsShortcutTextBox.get()
    
    reminderIndex= 0
    for reminderDisplay in allReminderDisplays:
        #print(reminderDisplay.length.get())
        
        reminderClass = reminders[reminderIndex]
        
        reminderClass.length =float( reminderDisplay.length.get())
        reminderClass.soundLocation =str( reminderDisplay.soundLocation.get())
        reminderClass.name =str( reminderDisplay.name.get())
        reminderIndex+= 1

    #print("closeApplicationShortcutTextBox"+ closeApplicationShortcutTextBox.get())
    #print("openSettingsShortcutTextBox"+ openSettingsShortcutTextBox.get())
    SetupShortcuts()
    saveCurrentSettings()
    
    
    winsound.MessageBeep(3)
    

def AddNewReminder():
    global reminders
    reminder =Reminder(5,"","")
    reminders.append(reminder)
    threading.Thread(target= runReminder, args=(reminder,), daemon= True).start()
   
    displayUi()


def RemoveReminder(reminderIndex):
    global reminders
    print(str (reminderIndex) +"/" + str (len(reminders)))
    del reminders[reminderIndex]
    displayUi()
    ApplyButtonPressed()
    

        

    
    
    
closeApp = False
def CloseApp():
    global closeApp 
    closeApp = True

def SetupShortcuts ():
    global closeApplicationShortcut
    global openSettingsWindowShortcut
    
    #keyboard.unhook_all_hotkeys()
    keyboard.add_hotkey(hotkey= closeApplicationShortcut, callback= CloseApp)
    keyboard.add_hotkey(hotkey= openSettingsWindowShortcut, callback=displayUi )
SetupShortcuts()

while not closeApp:
    time.sleep (1)
