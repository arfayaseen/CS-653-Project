import os

directory = '../'

for filename in os.listdir(directory):
    if filename.startswith('imgset2_4-3') and filename.endswith('.txt'):
        filename = os.path.splitext(filename)[0] + '.txt'
        filepath = os.path.join(directory, filename)
        with open(filepath, 'w') as file:
            file.write('M.03 23  E.03 24  11:45')
        