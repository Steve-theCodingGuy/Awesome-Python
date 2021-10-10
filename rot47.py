#!/usr/bin/python3

import argparse
from utilities.colors import color
from utilities.tools import clear

# encryption/decryption in same function - rotates the character ASCIIs by 47 % 94 to keep them within valid range
def transform(msg):

    # list with the ASCII values of the plaintext
    msgASCII = [ord(char) for char in msg]      # char to ASCII
    transASCII = []
    for ch in msgASCII:
        if ch in range(33,127):
            transASCII.append(33+((ch+14)%94))
        else:
            transASCII.append(ch)
    transform = ''.join(map(chr,transASCII))
    return transform



def parsefile(filename):
    message = ''
    try:
        with open(filename) as f:
            for line in f:
                message+=line
    except FileNotFoundError:
        print('{}[-] File not found{}\n{}[!] Please make sure the file with the filename exists in the current working directory{}'.format(color.RED,color.END,color.YELLOW,color.END))
        quit()
    return message

def run():
    try:
        clear()
        # prompt for choice of action
        choice = input('{}[?]{} Encrypt or Decrypt? [e/d] : '.format(color.BLUE,color.END))
        if choice == 'e' or choice == 'E':
            # whether to load a file for the plaintext or type it from the console
            filechoice = input('{}[?]{} Load from a file? [y/N] : '.format(color.BLUE,color.END)).lower()
            if filechoice != 'y':
                pt = input('{}[?]{} Enter the Plaintext : '.format(color.BLUE,color.END))        # plaintext input
            else:
                filename = input('{}[?]{} Enter the filename: '.format(color.BLUE,color.END))
                pt = parsefile(filename)
            ciphertext = transform(pt)                      # calling the enc() function with the input
            print('{}[+]{} The Ciphertext is : {}{}{}'.format(color.GREEN,color.END,color.RED,ciphertext,color.END))
        elif choice == 'd' or choice == 'D':
            # whether to load a file for the plaintext or type it from the console
            filechoice = input('{}[?]{} Load from a file? [y/N] : '.format(color.BLUE,color.END)).lower()
            if filechoice != 'y':
                ct = input('{}[?]{} Enter the Ciphertext : '.format(color.BLUE,color.END))       # ciphertext input
            else:
                filename = input('{}[?]{} Enter the filename: '.format(color.BLUE,color.END))
                ct = parsefile(filename)
            plaintext = transform(ct)                       # calling dec() function with the input
            print('{}[+]{} The Plaintext is : {}{}{}'.format(color.GREEN,color.END,color.RED,plaintext,color.END))
        else:
            print('{}[-] Please provide a valid coice of action{}'.format(color.RED,color.END))
        quit()
    except KeyboardInterrupt:
        print('\n{}[!] Exiting...{}'.format(color.RED,color.END))

# main driver function
# parses arguments 
# prompts the user for necessary inputs if arguments not provided 
def main():
    try:
        clear()
        
        # script description
        parser = argparse.ArgumentParser(description='ROT47 Encryption & Decryption')
        # encryption group option (single option --encrypt)
        enc_group = parser.add_argument_group('Encryption Options')
        enc_group.add_argument('-e','--encrypt', help='Encrypt a given Plaintext', default=False, action='store_true')
        # decryption group options (--decrypt and --brute)
        dec_group = parser.add_argument_group('Decryption Options')
        dec_group.add_argument('-d','--decrypt', help='Decrypt a given Ciphertext', default=False, action='store_true')
        # file option - whether to load from a file
        parser.add_argument('-f','--file', help='Load the Plaintext/ Ciphertext from a file', default=False, action='store_true')
        # message (either plain or cipher)  -   handled later on based on options
        parser.add_argument('TEXT', help='Plaintext or Ciphertext (based on mode)')

        try:        # if all options and positional argument (TEXT) provided
            args = parser.parse_args() 
        except:     # if positional argument TEXT not provided - prompts user with necessary options
            # prompt for choice of action
            choice = input('{}[?]{} Encrypt or Decrypt? [e/d] : '.format(color.BLUE,color.END))
            if choice == 'e' or choice == 'E':
                # whether to load a file for the plaintext or type it from the console
                filechoice = input('{}[?]{} Load from a file? [y/N] : '.format(color.BLUE,color.END)).lower()
                if filechoice != 'y':
                    pt = input('{}[?]{} Enter the Plaintext : '.format(color.BLUE,color.END))        # plaintext input
                else:
                    filename = input('{}[?]{} Enter the filename: '.format(color.BLUE,color.END))
                    pt = parsefile(filename)
                ciphertext = transform(pt)
                print('{}[+]{} The Ciphertext is : {}{}{}'.format(color.GREEN,color.END,color.RED,ciphertext,color.END))
            elif choice == 'd' or choice == 'D':
                # whether to load a file for the plaintext or type it from the console
                filechoice = input('{}[?]{} Load from a file? [y/N] : '.format(color.BLUE,color.END)).lower()
                if filechoice != 'y':
                    ct = input('{}[?]{} Enter the Ciphertext : '.format(color.BLUE,color.END))       # ciphertext input
                else:
                    filename = input('{}[?]{} Enter the filename: '.format(color.BLUE,color.END))
                    ct = parsefile(filename)
                plaintext = transform(ct)
                print('{}[+]{} The Plaintext is : {}{}{}'.format(color.GREEN,color.END,color.RED,plaintext,color.END))
            else:
                print('{}[-] Please provide a valid coice of action{}'.format(color.RED,color.END))
            quit()

        # parsing command line argumets (provided the necvessary ones are given)
        if args.encrypt:                            # if encrypt flag is on
            if args.decrypt:                        # decrypt flag should be off
                print('{}[-] Please select only one option among Encrypt or Decrypt at a time{}'.format(color.RED,color.END))
                quit()
            else:                                   # good to go - call enc() function and display result
                if args.file:
                    pt = parsefile(args.TEXT)
                    ciphertext = transform(pt)
                else:
                    ciphertext = transform(args.TEXT)
                print('{}[+]{} The Ciphertext is : {}{}{}'.format(color.GREEN,color.END,color.RED,ciphertext,color.END))

        elif args.decrypt:                          # if decrypt flag is on
            if args.file:
                ct = parsefile(args.TEXT)
                plaintext = transform(ct)
            else:
                plaintext = transform(args.TEXT)
            print('{}[+]{} The Plaintext is : {}{}{}'.format(color.GREEN,color.END,color.RED,plaintext,color.END))

        # if no arguments are provided except for positional (TEXT)
        else:
            print('{}[-] At least one of Encryption or Decryption action is required{}'.format(color.RED,color.END))

    except KeyboardInterrupt:
        print('\n{}[!] Exiting...{}'.format(color.RED,color.END))
        quit()

if __name__ == '__main__':
    main()

