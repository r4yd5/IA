import os


i = 0
path="recorte_aceptadas/"
for filename in os.listdir(path):
    my_dest ="a" + str(i) + ".jpg"
    my_source =path + filename
    my_dest =path + my_dest
    # rename() function will
    # rename all the files
    os.rename(my_source, my_dest)
    i += 1