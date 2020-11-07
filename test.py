def read_move():
    input_text = input()
    input_splitted = input_text.split()
    print(input_splitted)
    if input_splitted[0] == 'q' or input_splitted[0] == 'Q':
        return 0,0,0
    if input_splitted[0] == 'A' or input_splitted[0] == 'B' or input_splitted[0] == 'C':
        return 1,input_splitted[0],input_splitted[1]





print(read_move())