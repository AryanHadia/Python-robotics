from Colors import Colors_HSV as CH
from Main import VisualCamera as Vc

def menu():
    print("============================================")
    print("colors:")
    for _ in CH().colors_list(): # for every color in the list
        print(_)
    print("exite = 0")
    print("You can stop program with pressing (q)")
    print("============================================")

menu()
option = input("Please select one color and type it: ").lower()

if option != "0": # while option != quit
    try :
        while option not in CH().colors_list() : # if the colors not found
            menu()
            print (f"Please select one of the menu options !! this color ({option}) is not defined !!")
            option = input("Please select one color and type it: ").lower()
            if option == "0":
                break
        Vc().configuring_frame(color = option)
    except Exception as e: # showing error
        raise ValueError (f"failed to get option | ERROR: {e}")