import sys

# # Some condition or error occurs
# def fun():
#     print("An error occurred.")
#     sys.exit(1)


# try:

#     fun()
# except Exception as ex:
#     print(ex)

# fun()

class customException(Exception):

    def __init__(self, msg) -> None:
        self.msg = msg


def test(a):
    try:
        if a > 10:
            raise customException("value grater than 10")
        else:
            print("value is correct")
    except customException as e:
        print(e.msg)
        

test(12)
