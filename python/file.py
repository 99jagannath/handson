import os
for template_file in os.listdir('C:\handson\python\logs'):
    print(template_file)
    if 'error' in template_file:
        print('yes')
    else:
        print('NO')