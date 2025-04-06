import heapq

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

    return priority_queue[0]  # returns root


def gen_codes(node, current_code="", code_table=None):
    if code_table is None:
        code_table = {}  # initialize dictionary to store symbol and frequency

    if node.symbol is not None:  # if node is a leaf node
        code_table[node.symbol] = current_code
        return code_table
    if node.left:  # traverse left subtree
        gen_codes(node.left, current_code + '0', code_table)
    if node.right:  # traverse right subtree
        gen_codes(node.right, current_code + '1', code_table)

    return code_table


def encode(text, code_table):
    encode_string = ''
    for symbol in text:
        char = code_table[symbol]
        encode_string += char
    return encode_string


def decode(encoded_text, root):
    decode_string = []
    node = root
    for bit in encoded_text:
        if bit == '0':
            node = node.left
        else:
            node = node.right
        if node.symbol is not None:
            decode_string.append(node.symbol)
            node = root

    return ''.join(decode_string)


def pre_order(node, output_file):
    # If the node is None, return
    if node is None:
        return

    # Print the symbol and frequency for this node to the output file
    if node.symbol is not None:
        output_file.write(f'{node.symbol}:{node.frequency}\n')

    # Traverse left subtree
    pre_order(node.left, output_file)

    # Traverse right subtree
    pre_order(node.right, output_file)


def print_codes(freq_table, output_file):
    # Build Huffman Tree and get the root node
    root = build_tree(freq_table)

    # Write the frequency table in preorder
    output_file.write("Preorder traversal of the Huffman Tree:\n")
    pre_order(root, output_file)
    output_file.write("\n")

    # Generate Huffman codes
    codes = gen_codes(root)

    # Write the Huffman codes for each symbol to the output file
    output_file.write("Huffman Codes:\n")
    for symbol in sorted(codes.keys()):
        output_file.write(f'{symbol}: {codes[symbol]}\n')

    return root, codes


# Example frequency table
freq_table = {
    'A': 19, 'B': 16, 'C': 17, 'D': 11, 'E': 42, 'F': 12, 'G': 14, 'H': 17,
    'I': 16, 'J': 5, 'K': 10, 'L': 20, 'M': 19, 'N': 24, 'O': 18, 'P': 13,
    'Q': 1, 'R': 25, 'S': 35, 'T': 25, 'U': 15, 'V': 5, 'W': 21, 'X': 2,
    'Y': 8, 'Z': 3
}

def extractinputfiles(filename, outputfile):
    root, codes = print_codes(freq_table, outputfile)
    # opens and reads input file
    with open(filename, 'r') as file:
        lines = file.readlines()  # makes lines equal to the lines in input file
        for line in lines:  # iterates through input file
            line = line.strip()  # strips white spaces from lines
            if line:  # ignores blank spaces
                if line.isdigit() == False:
                    text_to_encode = line.upper()
                    encoded_text = encode(text_to_encode, codes)
                    outputfile.write(f'Encoded text: {encoded_text}\n')
                else:
                    text_to_decode = line
                    decoded_text = decode(text_to_decode, root)
                    outputfile.write(f'Decoded text: {decoded_text}\n')


# Open the output file for writing
with open('HuffmanOutputs.txt', 'w') as outputfile:
    extractinputfiles('HuffmanInputs.txt', outputfile)

