import argparse

def hex_to_bin(hex_number):
    decimal_number = int(hex_number, 16)
    binary_number = bin(decimal_number)[2:]
    padded_binary_number = binary_number.zfill(8)
    return padded_binary_number

def bin_to_hex(binary_number):
    decimal_number = int(binary_number, 2)
    hexadecimal_number = hex(decimal_number)[2:]
    return hexadecimal_number.upper()


def hide_message(message_bytes):
    with open('cover.html', 'r') as f:
        cover = f.read()
        
    lines_number = cover.count('\n')
    message_length = len(message_bytes)*8
    
    if(message_length > lines_number):
        print("Message is too long")
        return
    
    cover_lines = cover.split('\n')
    
    file = open('watermark.html', 'w')
    
    iter = 0
    for byte in message_bytes:
        byte = hex_to_bin(byte)
        for i in range(8):
            if byte[i] == '1':
                line = cover_lines[iter] + " \n"
                file.write(line)
            else:
                file.write(cover_lines[iter] + "\n")
            iter += 1
            
    for i in range(iter, lines_number):
        file.write(cover_lines[i] + "\n")
        
    file.close()

def extract_message():
    with open ('watermark.html', 'r') as f:
        watermark = f.read()
        watermark_lines = watermark.split('\n')
    
    extracted_message = [] 
    for line in watermark_lines:
        if line[len(line)-1:] == ' ':
            extracted_message.append('1')
        else:
            extracted_message.append('0')
        
    extracted_message = [extracted_message[i:i+8] for i in range(0, len(extracted_message), 8)]
    message = ""
    
    for byte in extracted_message:
        hex_byte = bin_to_hex(''.join(byte))
        if hex_byte != '0':
         message += bin_to_hex(''.join(byte)) + " "
    print(message)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-e', action='store_true')
    parser.add_argument('-d', action='store_true')
    
    args = parser.parse_args()
    
    with open('mess.txt', 'r') as f:
        message = f.read()
        message_bits = message.split(" ")
        
    if args.e:
        hide_message(message_bits)
    elif args.d:
        extract_message()
        
if __name__ == "__main__":
    main()