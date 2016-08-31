__author__ = 'manda.sun'
import sys
sys.path.append("..")

if __name__ == "__main__":
    f = open("turtle_file.txt", "r")
    lines = f.readlines()
    for line in lines:
        if line.startswith('#'):
            continue
        sep = line.strip().split('|')
        fi = open("../result/turtle3_result", "r")

        no = str(int(fi.readline().strip().split('|')[0]) + 1)
        fi.close()
        sep[0] = no
        money = str(int(sep[5]) - int(sep[6]))
        sep[5] = money  #money

        record = "|".join(sep)
        # print record
        fi = open("../result/turtle3_result", "r+")
        content = fi.read()
        fi.seek(0)
        fi.write(record + "\n" + content)
        fi.close()


