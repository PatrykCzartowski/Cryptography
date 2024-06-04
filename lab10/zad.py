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


def hide_message(message_bytes, argument):
# --- OPTION 1 ---
    if argument == 1:
        with open('cover.html', 'r') as f:
            cover = f.read()
        
        lines_number = cover.count('\n')
        message_length = len(message_bytes)*8
    
        if(message_length > lines_number):
            print("Message is too long")
            return
    
        cover_lines = cover.split('\n')

        cover_lines = [line.rstrip() for line in cover_lines]
        
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
    
# --- OPTION 2 ---
    elif argument == 2:
        with open('cover.html', 'r') as f:
            cover = f.read()
        
        cover_lines = [line.rstrip() for line in cover_lines]
        
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
                    line = cover_lines[iter] + "  \n"
                    file.write(line)
                else:
                    file.write(cover_lines[iter] + " \n")
                iter += 1
            
        for i in range(iter, lines_number):
            file.write(cover_lines[i] + "\n")
        
        file.close()
    
# --- OPTION 3 ---
    elif argument == 3:
        with open('cover.html', 'r') as f:
            cover = f.read()
        
        cover_lines = cover.split('\n')
        cover_styles = []
        cover_styles_start = None
        cover_styles_end = None
        
        for line in cover_lines:
            if line.find('<style>') != -1:
                cover_styles_start = cover_lines.index(line)
            if line.find('</style>') != -1:
                cover_styles_end = cover_lines.index(line)
                break
        
        for i in range(cover_styles_start+1, cover_styles_end):
            if cover_lines[i].find('}') == -1 and cover_lines[i].find('{') == -1:
                cover_styles.append(cover_lines[i])
        
        message_length = len(message_bytes)*8
        cover_styles_length = len(cover_styles)
        
        if(message_length > cover_styles_length):
            print("Message is too long")
            return
        
        file = open('watermark.html', 'w')
        
        for i in range (0, cover_styles_start+1):
            file.write(cover_lines[i] + "\n")
        
        iter = 0
        for byte in message_bytes:
            byte = hex_to_bin(byte)
            for i in range(8):
                if byte[i] == '1':
                    line = cover_styles[iter].replace(":", "==")
                    file.write(line + "\n")
                else:
                    line = cover_styles[iter].replace(":", "=")
                    file.write(line + "\n")
                iter += 1
        
        for i in range(iter, len(cover_lines)):
            file.write(cover_lines[i] + "\n")
        
        file.close()
        
# --- OPTION 4 --- #
    elif argument == 4:
        with open('cover.html', 'r') as f:
            cover = f.read()
            
        cover_lines = cover.split('\n')
        cover_paragraphs_indexes = []
        
        cover_paragraphs_indexes = [i for i, line in enumerate(cover_lines) if '<p>' in line]
               
        message_length = len(message_bytes)*8
        cover_paragraphs_length = len(cover_paragraphs_indexes)
        if(message_length > cover_paragraphs_length):
            print("Message is too long")
            return
        
        file = open('watermark.html', 'w')
        
        iter = 0
        for byte in message_bytes:
            byte = hex_to_bin(byte)
            for i in range(8):
                if byte[i] == '1':
                    cover_lines.insert(cover_paragraphs_indexes[iter], "<font> </font>")
                elif byte[i] == '0':
                    cover_lines.insert(cover_paragraphs_indexes[iter], "<font></font>")
                
                cover_paragraphs_indexes = [i for i, line in enumerate(cover_lines) if '<p>' in line]
                iter += 1
                
        for line in cover_lines:
            file.write(line + "\n")
        
        file.close()
    else:
        print("Invalid second argument")

def extract_message(argument):
# --- OPTION 1 ---
    if argument == 1:
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
                message += ''.join(hex_byte) + " "
        print(message)

# --- OPTION 2 ---
    elif argument == 2:
        with open ('watermark.html', 'r') as f:
            watermark = f.read()
            watermark_lines = watermark.split('\n')
    
        extracted_message = [] 
        for line in watermark_lines:
            if line[len(line)-2:] == '  ':
                extracted_message.append('1')
            else:
                extracted_message.append('0')
        
        extracted_message = [extracted_message[i:i+8] for i in range(0, len(extracted_message), 8)]
        message = ""
    
        for byte in extracted_message:
            hex_byte = bin_to_hex(''.join(byte))
            if hex_byte != '0':
                message += ''.join(hex_byte) + " "
        print(message)
        
# --- OPTION 3 ---
    elif argument == 3:
        with open('watermark.html', 'r') as f:
            watermark = f.read()
        
        watermark_lines = watermark.split('\n')
        watermark_styles = []
        watermark_styles_start = None
        watermark_styles_end = None
        
        for line in watermark_lines:
            if line.find('<style>') != -1:
                watermark_styles_start = watermark_lines.index(line)
            if line.find('</style>') != -1:
                watermark_styles_end = watermark_lines.index(line)
                break
        
        for i in range(watermark_styles_start+1, watermark_styles_end):
            if watermark_lines[i].find('}') == -1 and watermark_lines[i].find('{') == -1:
                watermark_styles.append(watermark_lines[i])

        
        extracted_message = [] 
        for line in watermark_styles:
            if line.find('==') != -1:
                extracted_message.append('1')
            elif line.find('=') != -1:
                extracted_message.append('0')
        
        extracted_message = [extracted_message[i:i+8] for i in range(0, len(extracted_message), 8)]
  
        message = ""
        for byte in extracted_message:
            message += bin_to_hex(''.join(byte)) + " "
        print(message)
        
# --- OPTION 4 ---
    elif argument == 4:
        
        with open ('watermark.html', 'r') as f:
            watermark = f.read()
            watermark_lines = watermark.split('\n')
            
        extracted_message = []
        for line in watermark_lines:
            if line.find('<font> </font>') != -1:
                extracted_message.append('1')
            elif line.find('<font></font>') != -1:
                extracted_message.append('0')
        
        extracted_message = [extracted_message[i:i+8] for i in range(0, len(extracted_message), 8)]
        
        message = ""
        for byte in extracted_message:
            message += bin_to_hex(''.join(byte)) + " "
        print(message)
    
    else:
        print("Invalid second argument")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-e', type=int)
    parser.add_argument('-d', type=int)
    
    args = parser.parse_args()
    
    with open('mess.txt', 'r') as f:
        message = f.read()
        message_bits = message.split(" ")
        
    if args.e:
        hide_message(message_bits, args.e)
    elif args.d:
        extract_message(args.d)
        
if __name__ == "__main__":
    main()