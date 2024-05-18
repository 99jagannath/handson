import os
import stat
import shutil
import datetime
my_dir = "./logs"
# for fname in os.listdir(my_dir):
#     item = os.path.join(my_dir,fname)
#     if fname.startswith("nginx"):
#         os.chmod(item , stat.S_IWRITE)
#         print(item)
#         os.remove(item)

# for filename in os.listdir(my_dir):
#     print(filename)
#     time = os.path.getmtime(filename)
#     print(time)
#     if filename.startswith('nginx'):
#         print(filename)
#         filepath = os.path.join(my_dir, filename)
#         print(filepath)
#         try:
#             shutil.rmtree(filepath)
#         except OSError:
#             os.remove(filepath)

root_dir = "logs"

def get_directories(root_dir):

    for child in Path(root_dir).iterdir():

        if child.is_file():
            print(child, datetime.fromtimestamp(getmtime(child)).date())
      
        else:
            print(child, datetime.fromtimestamp(getmtime(child)).date())
            get_directories(child)
