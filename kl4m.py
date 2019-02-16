import numpy as np
import json
import sys

def main():
    argvs = sys.argv
    article_name = argvs[1]

    # load keymap file
    f = open(article_name,"r")
    keymap = json.load(f)
    f.close()

    # load article file
    f = open("data/article.txt","r")
    article = f.read()
    f.close()

    # count
    last_pos = position([1,5])
    total_distance = 0

    for c in article:
        if c in keymap:
            pos1 = position(keymap[c])
            total_distance += distance(pos1, last_pos)
            last_pos = pos1

    return total_distance

def position(keyindex):
    return np.array((47*keyindex[0],77*keyindex[1]))

def distance(pos1, pos2):
    return np.linalg.norm(pos1 - pos2)
    

if __name__ == "__main__":
    result = main()
    print(result)
