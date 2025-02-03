
directory = "indices"

def read_token_index()->dict:
    file = open("token_index.txt", "r")
    result = dict()
    for line in file:
        line = line.split(",")
        result[line[0]] = int(line[1])
    return result


def return_docids(token:str, token_index:dict)->set:
    position = token_index[token]
    initial = token[0]
    if initial.isdigit():
        initial = "numeric"
    path = directory + "/" + initial + ".txt"
    file = open(path, "r")
    file.seek(position)
    file.readline()
    temp = file.readline().strip()
    file.close()
    return eval(temp)


def return_positions(token:str, docid: int, token_index:dict)->list:
    position = token_index[token]
    initial = token[0]
    if initial.isdigit():
        initial = "numeric"
    path = directory + "/" + initial + ".txt"
    file = open(path, "r")
    file.seek(position)
    file.readline()
    file.readline()
    line = file.readline()
    while "#@" in line:
        line = line.split('||')
        if int(line[0]) == docid:
            return eval(line[2])
        line = file.readline()
    file.close()


if __name__ == "__main__":
    d = read_token_index()
    #print(return_docids("by", d))
    print(return_positions("donald", 1, d))
    print(type(return_positions("donald", 1, d)))
    