import hashlib
import time

def generate_hash(file_path, hash_algorithm):
    start_time = time.time()
    hash_obj = hashlib.new(hash_algorithm)
    with open(file_path, 'rb') as file:
        for chunk in iter(lambda: file.read(4096), b''):
            hash_obj.update(chunk)
    end_time = time.time()
    hash_time = end_time - start_time
    print(f"Generating the hash using {hash_algorithm} took {hash_time} seconds.")
    return hash_obj.hexdigest()

def save_hash(file_path, hash_algorithm):
    hash_file_path = file_path.split('.')[0] + '_hash.txt'
    file_hash = generate_hash(file_path, hash_algorithm)
    with open(hash_file_path, 'w') as file:
        file.write(file_hash)

def verify_integrity(file_path, hash_file_path, hash_algorithm):
    current_hash = generate_hash(file_path, hash_algorithm)
    with open(hash_file_path, 'r') as file:
        saved_hash = file.read()
    return current_hash == saved_hash


generate_hash('text_1.txt', 'md5')
generate_hash('text_2.txt', 'md5')
generate_hash('text_3.txt', 'md5')
print("-------")
generate_hash('text_1.txt', 'sha256')
generate_hash('text_2.txt', 'sha256')
generate_hash('text_3.txt', 'sha256')
print("-------")
generate_hash('text_1.txt', 'blake2s')
generate_hash('text_2.txt', 'blake2s')
generate_hash('text_3.txt', 'blake2s')

#save_hash('test_file.txt', 'md5')
#if verify_integrity('test_file.txt', 'test_file_hash.txt', 'md5'):
    #print('File is not corrupted')
#else:
    #print('File is corrupted')