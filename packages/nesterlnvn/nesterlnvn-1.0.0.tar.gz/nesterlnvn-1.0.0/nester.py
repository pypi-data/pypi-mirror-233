# nester.py module
def print_lol(the_list, level=0):
    # print all nested items
    for item in the_list:
        if isinstance(item, list):
            print_lol(item, level+1)
        else:
            for tab_stop in range(level):
                print("\t", end='')
            print(item)