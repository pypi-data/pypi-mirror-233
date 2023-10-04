from green_form import give_me_green_form

def give_me_blue_form():
    give_me_green_form()
    print("Here is the blue form !")


if __name__=="__main__":
    give_me_blue_form()
