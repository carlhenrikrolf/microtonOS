import os

def ls(paths):
    for path in paths:
        try:
            ls = os.listdir(path)
        except:
            continue
        break
    filenames = []
    for item in ls:
        if item[0] != "_" and "." in item:
            filenames.append("")
            for letter in item:
                if letter == ".":
                    break
                else:
                    filenames[-1] += letter
    return filenames