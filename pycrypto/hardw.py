import os
import subprocess

from Crypto.Cipher import AES
from Crypto.Hash import SHA256
from Crypto import Random

key = ''

def encrypt(key,filepath):
    chunksize = 64 * 1024
    filename = os.path.basename(filepath)
    e_filename = "e-" + filename
    # construct a filepath for encrypted file
    e_filepath = "%s/%s" %(os.path.split(filepath)[0],e_filename)

    filesize   = str(os.path.getsize(filename)).zfill(16)
    IV = Random.new().read(16)

    encryptor = AES.new(key, AES.MODE_CBC, IV)
    with open(filepath, 'rb') as infile:
        with open(e_filepath, 'wb') as outfile:
            outfile.write(filesize.encode('utf-8'))
            outfile.write(IV)
            while True:
                chunk = infile.read(chunksize)
                if len(chunk) == 0:
                    break
                elif len(chunk) % 16 != 0:
                    chunk += b' ' * (16 - (len(chunk) % 16))
                outfile.write(encryptor.encrypt(chunk))

def decrypt(key,e_filepath):
    chunksize = 64*1024
    e_filename = os.path.basename(e_filepath)
    filename = e_filename[2:]
    # construct a filepath for dencrypted file
    filepath = "%s/%s" % (os.path.split(e_filepath)[0], filename)

    with open(e_filepath, 'rb') as infile:
        IV = infile.read(16)

        decryptor = AES.new(key, AES.MODE_CBC, IV)

        with open(filepath, 'wb') as outfile:
            while True:
                chunk = infile.read(chunksize)
                if len(chunk) == 0:
                    break
                outfile.write(decryptor.decrypt(chunk))

def getKey():
    hardware_uuid = ''
    serial_number = ''
    mac_addr = ''

    command1 = "system_profiler SPHardwareDataType"
    p1 = subprocess.Popen(command1.split(), stdout=subprocess.PIPE)
    out, err = p1.communicate()
    for line in out.decode().split('\n'):
        line = line.lstrip()
        if line.startswith('Serial Number (system):'):
            serial_number = line.split(': ')[1]
        elif line.startswith('Hardware UUID:'):
            hardware_uuid = line.split(': ')[1]


    command2 = "ifconfig en1"
    p2 = subprocess.Popen(command2.split(), stdout=subprocess.PIPE)
    out, err = p2.communicate()
    for line in out.decode().split('\n'):
        line = line.lstrip()
        if line.startswith('ether'):
            mac_addr = line.split(' ')[1]

    k = "%s%s%s" %(hardware_uuid, serial_number, mac_addr)
    hasher = SHA256.new(k.encode('utf-8'))
    return hasher.digest()

def Main():
    choice = input("Would you like to (e)ncrypt or (d)ecrypt?: ")

    if choice == 'e':
        filename = input("File to encrypt: ")
        encrypt(getKey(), filename)
        print ("Done")
    elif choice == 'd':
        filename = input("File to decrypt: ")
        decrypt(getKey(), filename)
        print ("Done")
    else:
        print ("No valid option selected, closing ...")


if __name__ == '__main__':
    Main()
