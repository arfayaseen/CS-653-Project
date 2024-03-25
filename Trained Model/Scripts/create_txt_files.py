import os

directory = '../'

for filename in os.listdir(directory):
    if filename.endswith('.tif'):
        filepath = os.path.join(directory, filename)

        # create text files
        filename = os.path.splitext(filename)[0] + '.gt.txt'
        filepath = os.path.join(directory, filename)
        file = open(filepath, 'w')