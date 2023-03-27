import os


i = 0
path=R"C:\Users\Juan Manuel Sanchez\Desktop\BD125X2\RECHAZADAS/"
for filename in os.listdir(path):
    my_dest ="R" + str(i) + ".jpg"
    my_source =path + filename
    my_dest =path + my_dest
    # rename() function will
    # rename all the files
    os.rename(my_source, my_dest)
    i += 1