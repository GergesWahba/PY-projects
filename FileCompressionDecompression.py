import heapq
import os
import pickle
import tkinter as tk
from tkinter import filedialog

# Suppress default window
root = tk.Tk()
root.withdraw()

# Node class for Huffman Tree
class HuffmanNode:
    def __init__(self, char, freq):
        self.char = char
        self.freq = freq
        self.left = None
        self.right = None

    def __lt__(self, other):
        return self.freq < other.freq

# Step 1: Frequency dictionary
def build_frequency_dict(text):
    freq = {}
    for char in text:
        freq[char] = freq.get(char, 0) + 1
    return freq

# Step 2: Huffman tree
def build_huffman_tree(freq_dict):
    heap = [HuffmanNode(char, freq) for char, freq in freq_dict.items()]
    heapq.heapify(heap)
    while len(heap) > 1:
        node1 = heapq.heappop(heap)
        node2 = heapq.heappop(heap)
        merged = HuffmanNode(None, node1.freq + node2.freq)
        merged.left = node1
        merged.right = node2
        heapq.heappush(heap, merged)
    return heap[0]

# Step 3: Generate Huffman codes
def generate_codes(root):
    codes = {}
    def traverse(node, code):
        if node:
            if node.char is not None:
                codes[node.char] = code
            traverse(node.left, code + "0")
            traverse(node.right, code + "1")
    traverse(root, "")
    return codes

# Step 4: Encode text
def encode_text(text, codes):
    return ''.join(codes[char] for char in text)

# Step 5: Pad text
def pad_encoded_text(encoded_text):
    extra_padding = 8 - len(encoded_text) % 8
    padded_info = "{0:08b}".format(extra_padding)
    return padded_info + encoded_text + "0" * extra_padding

# Convert to bytes
def get_byte_array(padded_encoded_text):
    b = bytearray()
    for i in range(0, len(padded_encoded_text), 8):
        byte = padded_encoded_text[i:i+8]
        b.append(int(byte, 2))
    return b

# Compress
def compress():
    input_file = filedialog.askopenfilename(title="Select file to compress")
    if not input_file:
        print("❌ No file selected.")
        return

    with open(input_file, 'r') as file:
        text = file.read()

    freq_dict = build_frequency_dict(text)
    root = build_huffman_tree(freq_dict)
    codes = generate_codes(root)
    encoded_text = encode_text(text, codes)
    padded_encoded_text = pad_encoded_text(encoded_text)
    byte_array = get_byte_array(padded_encoded_text)

    output_file = filedialog.asksaveasfilename(defaultextension=".bin", title="Save compressed file as")
    if not output_file:
        print("❌ No output file selected.")
        return

    with open(output_file, 'wb') as output:
        pickle.dump(codes, output)  # Save dictionary
        output.write(bytes(byte_array))  # Save binary

    print(f"✅ Compressed '{input_file}' to '{output_file}'")

# Decompress
def remove_padding(padded_encoded_text):
    padded_info = padded_encoded_text[:8]
    extra_padding = int(padded_info, 2)
    return padded_encoded_text[8:-extra_padding]

def decode_text(encoded_text, codes):
    reverse_codes = {v: k for k, v in codes.items()}
    current_code = ""
    decoded_text = ""

    for bit in encoded_text:
        current_code += bit
        if current_code in reverse_codes:
            decoded_text += reverse_codes[current_code]
            current_code = ""

    return decoded_text

def decompress():
    input_file = filedialog.askopenfilename(title="Select compressed file")
    if not input_file:
        print("❌ No file selected.")
        return

    with open(input_file, 'rb') as file:
        codes = pickle.load(file)
        bit_data = file.read()

    bit_string = ''.join(f"{byte:08b}" for byte in bit_data)
    encoded_text = remove_padding(bit_string)
    decompressed_text = decode_text(encoded_text, codes)

    output_file = filedialog.asksaveasfilename(defaultextension=".txt", title="Save decompressed text as")
    if not output_file:
        print("❌ No output file selected.")
        return

    with open(output_file, 'w') as out_file:
        out_file.write(decompressed_text)

    print(f"✅ Decompressed '{input_file}' to '{output_file}'")

# Main menu
if __name__ == "__main__":
    print("Huffman Compression Tool")
    print("1. Compress a file")
    print("2. Decompress a file")
    choice = input("Choose an option (1 or 2): ").strip()

    if choice == "1":
        compress()
    elif choice == "2":
        decompress()
    else:
        print("❌ Invalid choice. Please enter 1 or 2.")