from io import StringIO 
 
 
# The arbitrary string.
string ='This is initial string.'
 
# Using the StringIO method to set
# as file object. Now we have an
# object file that we will able to
# treat just like a file.
file = StringIO(string)
 
# this will read the file
print(file.read())
 
# We can also write this file.
file.write(" Welcome to geeksforgeeks.\n")
file.write(" Welcome to geeksforgeeks.")
 
# This will make the cursor at
# index 0.
file.seek(0)
 
# This will print the file after
# writing in the initial string.
print('The string after writing is:', file.read())