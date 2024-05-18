import re
import sys
def validate_password(password):
    # if len(password) < 8:
    #     print("less char")
    #     return False
    
    pattern = "(^.*(?=.{8,})(?=.*[a-zA-Z])(?=.*[!@#$%^&*_0-9]).*$)"

    if not re.match(pattern, password):
        print("no special char or digit")
        return False

    return True


pass_list = ['acvdfededw', 'asdfgh23', 'sderfvg#', 'sdssg', "sdfer34#","a12345678"]

for  passwd in pass_list:
    print(passwd, validate_password(passwd))


ans = []

if ans:
    print("gfdgfd")

print(sys.argv)

def get_wc_server_port(wc_server):
  pattern = r'([A-Za-z_]+)'
  pattern = r'([A-Za-z_]+)(\d+)'
  match = re.match(pattern, wc_server)
  print(match)
  print(match.group(2))
  # server_prefix = match.group(1)
  # target_host_index = match.group(2)
  # print(server_prefix, target_host_index)
get_wc_server_port('dfsdfdsf12')

def validate_password(password, username, full_name):
    # Condition 1: Check if the password contains username or its substrings
    if len(username) >= 3 and username.lower() in password.lower():
        return False

    # Condition 2: Check if the password contains substrings of full_name tokens
    delimiters = ',.-_ #\t'
    tokens = re.split('[' + re.escape(delimiters) + ']', full_name)
    print(tokens)
    print(type(tokens))
    for token in tokens:
        if len(token) >= 3 and token.lower() in password.lower():
            return False

    # Condition 3: Check if the password contains characters from at least 3 of the specified categories
    categories = [
        r'[A-Za-z\u00C0-\u024F\u0400-\u04FF]',   # European characters
        r'\d',                                   # Digits
        r'[~!@#$%^&*_\-+=`|(){}[\]:;"\'<>,.?/]'  # Non-alphanumeric characters
    ]
    category_count = sum(1 for category in categories if re.search(category, password))
    if category_count < 3:
        return False

    return True

# Example usage:
password = "Password123!"
username = "opc"
full_name = "opc"
print(validate_password(password, username, full_name))  # Output: True
