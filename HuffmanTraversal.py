import heapq
import time
# creates node class
class Node:
    def __init__(self, symbol=None, frequency=None, left=None, right=None):
        self.symbol = symbol
        self.frequency = frequency
        self.left = left
        self.right = right

    # compares the frequency of the nodes
    def __lt__(self, other):
        if self.frequency == other.frequency:  # if there is a tie between frequencies
            if self.symbol and other.symbol:  # if both nodes are leaf nodes
                return self.symbol < other.symbol  # compares nodes alphabetically
            else:
                return False
        return self.frequency < other.frequency


def build_tree(freq_table):
    priority_queue = []  # initialize pq
    for symbol, frequency in freq_table.items():  # iterate through freq table dictionary
        if frequency <= 0:
            print('Invalid frequency:{frequency} for symbol:{symbol}')
        node = Node(symbol, frequency)  # create node using symbol and frequency
        priority_queue.append(node)  # append node to priority queue
        heapq.heapify(priority_queue)  # places lowest frequency on the top of pq

    while len(priority_queue) > 1:
        left = heapq.heappop(priority_queue)  # pops node with lowest freq
        right = heapq.heappop(priority_queue)  # pops node with lowest freq

        internal_node = Node(None, left.frequency + right.frequency)  # create internal node by summing the 2 lowest frequencies
        internal_node.left = left
        internal_node.right = right

        heapq.heappush(priority_queue, internal_node)  # pushes internal node back into priority queue

    return priority_queue[0]  # returns root, represents entire Huffman tree


def gen_codes(node, current_code="", code_table=None):
    if code_table is None:
        code_table = {}  # initialize dictionary to store symbols and frequencies

    if node.symbol is not None:  # if node is a leaf node
        code_table[node.symbol] = current_code
        return code_table
    if node.left:  # traverse left subtree
        gen_codes(node.left, current_code + '0', code_table)
    if node.right:  # traverse right subtree
        gen_codes(node.right, current_code + '1', code_table)

    return code_table#returns dictionary, will be passed into encode function 


def encode(text, code_table):#creates encode function using text string
    encode_string = ''
    for symbol in text:
        char = code_table[symbol]#finds symbol key in the dictionary
        encode_string += char#concatinates symbol binary code to string
    return encode_string#returns full binary code


def decode(encoded_text, root):#creates decode function using root
    decode_string = []
    node = root #the node starts from the root
    for bit in encoded_text:#iterates  through the digits
        if bit == '0':
            node = node.left#traverse left child
        elif bit == '1':
            node = node.right#traverse right child if bit==1

        if node.symbol is not None:#node has a symbol, therefor it is a leaf
            decode_string.append(node.symbol)#append symbol to string
            node = root#resets node to the root, begins decoding next symbol

    return ''.join(decode_string)#returns decoded string


def pre_order(node, output_file):
    
    if node is None:#base case to determine if node is a branch
        return

    
    if node.symbol is not None:#if node is a leaf, print the symbol and freq
        output_file.write(f'{node.symbol}:{node.frequency}\n')

    
    pre_order(node.left, output_file)#traverse left subtree

    
    pre_order(node.right, output_file)#traverse right subtree


def print_codes(freq_table, output_file):
   
    root = build_tree(freq_table)#builds tree 

    
    output_file.write("Preorder traversal of the Huffman Tree:\n")
    pre_order(root, output_file)#call preorder to print the tree in correct orrientation
    output_file.write("\n")

   
    codes = gen_codes(root)#generates codes from root

   
    output_file.write("Huffman Codes:\n")
    for symbol in sorted(codes.keys()):#prints symbols alphabetically
        output_file.write(f'{symbol}: {codes[symbol]}\n')#writes symbols with codes

    return root, codes


# Example frequency table
freq_table = {
    'A': 19, 'B': 16, 'C': 17,
    'D': 11, 'E': 42, 'F': 12,
    'G': 14, 'H': 17,'I': 16,
    'J': 5, 'K': 10, 'L': 20,
    'M': 19, 'N': 24, 'O': 18,
    'P': 13,'Q': 1, 'R': 25,
    'S': 35, 'T': 25, 'U': 15,
    'V': 5, 'W': 21, 'X': 2,
    'Y': 8, 'Z': 3
}

def extractinputfiles(filename, outputfile):
    #defines variables to hold root node of huffmantree,
    #and dictionary containing the codes
    #passes codes dictionary to encode function
    #passes Huffman tree root to decode function
    root, codes = print_codes(freq_table, outputfile)
    # opens and reads input file
    with open(filename, 'r') as file:
        lines = file.readlines()  # makes lines equal to the lines in input file
        for line in lines:  # iterates through input file
            line = line.strip()  # strips white spaces from lines
            if line:  # ignores blank spaces
                if line.isdigit() == False:
                    text_to_encode = line.upper()
                    
                    start = time.perf_counter()#starts timer 
                    encoded_text = encode(text_to_encode, codes)
                    end = time.perf_counter()
                    time_elapsed = (end-start)* 10**3
                    outputfile.write(f'Elapsed time: {time_elapsed}\n')
                    outputfile.write(f'Text to encode is: {line}\n')
                    outputfile.write(f'Encoded text: {encoded_text}\n')
                    outputfile.write(f'-'* 50 +'\n')
                        
                else:
                    text_to_decode = line
                    start = time.perf_counter()
                    decoded_text = decode(text_to_decode, root)
                    end = time.perf_counter()
                    time_elapsed = (end-start)* 10**3
                    for bit in line:
                        if bit not in {'0', '1'}:#error checking, ensure bit is either 1 or 0 
                            outputfile.write(f"Invalid bit '{bit}' in the encoded text. Expected '0' or '1'.")
                            return
                        
                    outputfile.write(f'Elapsed time: {time_elapsed}\n')
                    outputfile.write(f'Code to decode is: {line}\n')
                    outputfile.write(f'Decoded text: {decoded_text}\n')
                    outputfile.write(f'-'* 50 +'\n')


# Open the output file for writing
with open('HuffmanOutputs.txt', 'w') as outputfile:
    extractinputfiles('HuffmanInputs.txt', outputfile)

                    
                    