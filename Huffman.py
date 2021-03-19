from bitstring import BitArray
from pathlib import Path
import codecs
import pickle as pk

# Creates letter_binary and size arrays needed in compress() and decompress() functions
letter_binary = []
size = []

# Sort() function sorts the Huffman Tree into ordered levels
def Sort(array): 
    l = len(array)
    # Iterates through the Huffman Tree and sorts in terms of length of binary representation for each character (from shortest to longest)
    for i in range(0, l): 
        for j in range(0, l-i-1): 
            if (len(array[j][1]) > len(array[j + 1][1])): 
                x = array[j] 
                array[j] = array[j + 1] 
                array[j + 1] = x
    return array

# Compresses the file passed to the function
def compress(file):
    print("Compressing...")
    print("")
    # Opens and reads the file, with UTF-8 encoding
    with codecs.open(file,'r',encoding='utf8') as f:
        text = f.read()
    # Iterates through the characters in the file, adding each unique character to letter_frequency and letters arrays
    # A count is kept for the number of times each character is used in the file and is added to the letter_frequency array (alongside the character)
    letters = []
    letter_frequency = []
    for letter in text:
        if letter not in letter_frequency:
            frequency = text.count(letter)
            letter_frequency.append(frequency)
            letter_frequency.append(letter)
            letters.append(letter)
    # Creates the initial nodes for the Huffman Tree
    nodes = []
    while len(letter_frequency) > 0:
        nodes.append(letter_frequency[0:2])
        letter_frequency = letter_frequency[2:]
    nodes.sort()
    tree = []
    tree.append(nodes)
    # Iterates through characters, allocating each one a 1 or a zero, based on whether the character is in the present in the node before
    # Also creates new nodes if there is more than one character associated to the node before
    while len(nodes)>1:
        x = 0
        new_node = []
        nodes.sort()
        nodes[x].append("0")
        nodes[x+1].append("1")
        first_node = (nodes[x][0] + nodes[x + 1][0])
        second_node = (nodes[x][1] + nodes[x + 1][1])
        new_node.append(first_node)
        new_node.append(second_node)
        new_nodes = []
        new_nodes.append(new_node)
        new_nodes = new_nodes + nodes[2:]
        nodes = new_nodes
        tree.append(nodes)
    tree.sort(reverse=True)
    # Removes all duplicate items in the Huffman Tree
    unique_nodes = []
    for level in tree:
        for node in level:
            if node not in unique_nodes:
                unique_nodes.append(node)
            else:
                level.remove(node)
    # Builds the unique binary code for each character based on its path in the Huffman Tree
    if len(letters) == 1:
        letter_code = [letters[0],"0"]
        letter_binary.append(letter_code*len(text))
    else:
        for letter in letters:
            lettercode = ""
            for node in unique_nodes:
                if len(node)>2 and letter in node[1]:
                    lettercode = lettercode + node[2]
            letter_code = [letter,lettercode]
            letter_binary.append(letter_code)
    # Creates new array, containing only the character and binary code for each character in the Huffman Tree
    tree_levels = []
    tree_level = []
    for letter in letter_binary:
        tree_level.append(letter[0])
        tree_level.append(letter[1])
        tree_levels.append(tree_level)
        tree_level = []
    # Sorts and prints the Huffman Tree using the Sort() function
    print("Huffman Tree of File:")
    print(Sort(tree_levels))
    print("")
    # Creates bitstring of the text in the file, using binary codes of each character
    binary_string = ""
    for character in text:
        for item in letter_binary:
            if character in item:
                binary_string = binary_string + item[1]
    # Prints the binary representation of the file
    print("Compressed File:")
    print(binary_string)
    print("")
    # Writes the bitstring and the Huffman Tree to a bin file (compressed file)
    a = BitArray(bin=binary_string)
    with open('output_file.bin', 'wb') as f:
        a.tofile(f)
        pk.dump(tree, f)
    # Calculates the size of the original file, the compressed file and the size reduction
    uncompressed_file_size = Path(file).stat().st_size
    compressed_file_size_bytes = Path('output_file.bin').stat().st_size
    compressed_file_size = len(binary_string)
    size.append(compressed_file_size)
    print("Original file size: ", uncompressed_file_size, " bytes")
    print("Compressed file size: ", compressed_file_size_bytes, " bytes")
    print("This is a reduction of ", (1 - (compressed_file_size_bytes/uncompressed_file_size))*100, "%")


# Decompresses the file passed to the function
def decompress(file):
    print("")
    print("")
    print("Decrompressing...")
    print("")
    # Opens and reads the file
    with codecs.open(file, 'rb') as f:
        b = BitArray(f.read())
    # Allocates the contents of the file to 'bitstring'
    binary_string = b.bin
    # Converts the string of binary to the original text
    decompressed = ""
    code = ""
    for digit in binary_string[0:size[0]]:
        code = code + digit
        x = 0
        for letter in letter_binary:
            if code == letter[1]:
                decompressed = decompressed + letter_binary[x][0]
                code = ""
            x = x + 1
    # Prints the decompressed file
    print("Here is the original text:")
    print(decompressed)



compress("TheHoundOfTheBaskervilles.txt")
decompress("output_file.bin")
    
