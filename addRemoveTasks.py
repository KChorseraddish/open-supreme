import json, time

def main():
    with open("tasks.json", "r") as jFile:
        jsonFile = json.load(jFile)
    with open("profiles.json", "r") as f:
        pFile = json.load(f)
        
    if len(jsonFile) == 0:
        if len(pFile["users"]) != 0:
            print("\nCreating a task since none were found")
            addTask(jsonFile)
        else:
            print("Close this program and make a profile before adding tasks")
            time.sleep(500)
    else:
        allTasks = []
        for task in jsonFile:
            allTasks.append(task)
        print(f"Current Tasks: {allTasks}\n")
        response = input("Would you like to add, delete, view, or edit tasks?\n'0': Add\n'1': Delete\n'2': View\n'3': Edit\n> ")

        if response.upper() == "add".upper() or response == "0":
            if len(pFile["users"]) == 0:
                print("Make sure you create a profile before you add tasks")
                time.sleep(1.75)
            else:
                addTask(jsonFile)
        elif response.upper() == "delete".upper() or response == "1":
            deleteTask(jsonFile)
        elif response.upper() == "view".upper() or response == "2":
            viewTask(jsonFile)
        elif response.upper() == "edit".upper() or response == "3":
            editTask(jsonFile)
        else:
            print("Syntax error with choice, restarting\n")
            time.sleep(1.25)
            main()


def addTask(tasksFile):
    with open("profiles.json", "r") as pFile:
        profileFile = json.load(pFile)
        
    profile = -1            
    taskName = input("Task Name: ").strip()
    keywords = input("Enter all keywords separated by a comma: ").strip()
    keywords = [k_w.strip() for k_w in keywords.split(",")]
    print(keywords)
    
    category = input("Category: ").strip()
    color = input("Color: ").strip()
    size = input("Size (N/A for sizeless items): ").strip()
    proxy = input("Proxy with port ex. 1.1.1.1:111 (press enter if n/a): ").strip()

    delay = ""
    while type(delay) != float:
        delay = input("Checkout Delay: ")
        try:
            delay = float(delay)
        except:
            pass

    if len(proxy) < 3:
        proxy = ""
    
    print("\n")
    for a, b in enumerate(profileFile["users"]):
        print(b["name"],",", b["address"], a)
    print("\n")
    
    while int(profile) < 0 or int(profile) > len(profileFile["users"]) - 1:       
        profile = input("Profile Selection (number next to profile name): ")
    profile = "profile" + str(profile)

    print("Adding task\n")
        
    tasksFile[taskName] = {}
    tasksFile[taskName]["KWs"] = keywords
    tasksFile[taskName]["category"] = category
    tasksFile[taskName]["color"] = color
    tasksFile[taskName]["size"] = size
    tasksFile[taskName]["profile"] = profile
    tasksFile[taskName]["proxy"] = proxy
    tasksFile[taskName]["delay"] = delay

    with open("tasks.json", "w") as f:
            json.dump(tasksFile, f)
            time.sleep(2.5)

def deleteTask(tasksFile):
    whichTask = input("Enter the name of the task you wish to delete: ")
    if whichTask not in tasksFile:
        print(f"Could not find task '{whichTask}'\n")
        deleteTask(tasksFile)
    else:
        print(f"Deleting task '{whichTask}'\n")
        del tasksFile[whichTask]

        with open("tasks.json", "w") as f:
            json.dump(tasksFile, f)

        time.sleep(2)

def viewTask(tasksFile):
    def printTask(tasksFile,task):
        if task == "All":
            for item in tasksFile:
                print(f"\nTask Name: {item}")
                print(f"Keywords: {tasksFile[item]['KWs']}")
                print(f"Category: {tasksFile[item]['category']}")
                print(f"Color: {tasksFile[item]['color']}")
                print(f"Size: {tasksFile[item]['size']}")
                print(f"\nProfile: {tasksFile[item]['profile']}")
                print(f"Proxy: {tasksFile[item]['proxy']}")
                print(f"Delay: {tasksFile[item]['delay']}\n")
        else:
            print(f"\nTask Name: {task}")
            print(f"Keywords: {tasksFile[task]['KWs']}")
            print(f"Category: {tasksFile[task]['category']}")
            print(f"Color: {tasksFile[task]['color']}")
            print(f"Size: {tasksFile[task]['size']}")
            print(f"\nProfile: {tasksFile[task]['profile']}")
            print(f"Proxy: {tasksFile[task]['proxy']}")
            print(f"Delay: {tasksFile[task]['delay']}\n")
    whichTask = input("Enter the name of the task you wish to view. Enter 'All' to see all tasks. ")
    if whichTask not in tasksFile and whichTask != "All":
        print(f"Could not find task '{whichTask}'\n")
        viewTask(tasksFile)
    else:
        printTask(tasksFile,whichTask)
        
def editTask(tasksFile):
    whichTask = input("Enter the name of the task you wish to edit: ")
    while whichTask not in tasksFile:
        print(f"Could not find task '{whichTask}'\n")
        whichTask = input("Enter the name of the task you wish to edit: ")
 
    parts = ["task name"]
    for part in tasksFile[whichTask]:
        parts.append(part)
    whichPart = input(f"\nWhich part of the task would you like to edit?\n({', '.join(parts)}): ")

    if whichPart not in parts:
        print(f"Error, {whichPart} not found in {whichTask}")
        time.sleep(1.5)
        editTask(tasksFile)
        
    elif whichPart == "task name":
        newName = input(f"Enter new task name for '{whichTask}': ")
        print(f"Name of task '{whichTask}' changed to '{newName}'\n")
        tasksFile[newName] = tasksFile[whichTask]
        del tasksFile[whichTask]
        
    elif whichPart == "KWs":
        print(f"\n{whichTask}'s {whichPart} are currently {tasksFile[whichTask][whichPart]}")
        newKws = input("Enter new keywords with a comma in between each one: ")
        newKws = [k_w.strip() for k_w in newKws.split(",")]
        print(f"Changed {whichTask}'s keywords from {tasksFile[whichTask][whichPart]} to {newKws}\n")
        tasksFile[whichTask][whichPart] = newKws
        
    elif whichPart == "proxy":
        if tasksFile[whichTask][whichPart] == "":
            print(f"\n'{whichTask}' currently has no proxy")
        else:
            print(f"\n{whichTask}'s {whichPart} is currently {tasksFile[whichTask][whichPart]}")
        newProx = input("Enter a new value for 'proxy' (press enter if n/a): ")

        if len(newProx) < 4:
            newProx = ""
        tasksFile[whichTask]["proxy"] = newProx
        print(f"'proxy' in task '{whichTask}' changed to {newProx}\n")

    elif whichPart == "delay":
        print(f"\n{whichTask}'s {whichPart} is currently {tasksFile[whichTask][whichPart]}")
        
        new_delay = ""
        while type(new_delay) != float:
            new_delay = input("Enter new checkout delay: ")
            try:
                new_delay = float(new_delay)
            except:
                pass
        tasksFile[whichTask]["delay"] = new_delay
        
    else:
        print(f"\n{whichTask}'s {whichPart} is currently '{tasksFile[whichTask][whichPart]}'")
        newChange = input(f"Enter what you would like to change the {whichPart} to: ")
        print(f"{whichPart} in task '{whichTask}' changed to {newChange}\n")
        tasksFile[whichTask][whichPart] = newChange

    with open("tasks.json", "w") as f:
            json.dump(tasksFile, f)
    time.sleep(2)  
          
while True:
    main()
