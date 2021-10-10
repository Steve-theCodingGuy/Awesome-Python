#!/usr/bin/python3

import argparse
from utilities.colors import color
from utilities.tools import clear

# encryption function that takes the plaintext and number of steps to rotate
# and returns the encrypted text (plaintext rotated by steps no. of ASCII characters)
def encrypt(plain,offset):

    plain_bak = plain
    plain=''
    for p in plain_bak:
        if p.isalpha():
            plain+=p

    # list with the ASCII values of the plaintext
    plainASCII = [ord(char) for char in plain]
    cipherASCII = []
    steps = offset
    # rotating the ASCII values by 'steps' no. of steps
    # x=32 is kept the same to preserve space characters
    
    for x in plainASCII:
        if x in range(97,123):
            if x+(steps%26)>122:              # lowercase letters
                cipherASCII.append(x+(steps%26)-26)
            else:
                cipherASCII.append(x+(steps%26))
        elif x in range(65,91):          # uppercase letters
            if x+(steps%26)>90:
                cipherASCII.append(x+(steps%26)-26)
            else:
                cipherASCII.append(x+(steps%26))
        elif x in range(48,58):          # numeric values
            if x+(steps%10)>57:
                cipherASCII.append(47+((steps%10)-(57-x)))
            else:
                cipherASCII.append(x+(steps%10))
        else:
            cipherASCII.append(x)
        steps+=1
    
    # coverting the ASCII values of the cipherASCII (rotated) 
    # into their corresponding characters as the ciphertext
    cipher = ''.join(map(chr,cipherASCII))
    #print(cipher)
    # add special characters to final text
    for i in range(len(plain_bak)): 
        if not plain_bak[i].isalpha():
            cipher = cipher[:i] + plain_bak[i] + cipher[i:]
    return cipher

# decryption function that takes the ciphertext and the number of steps originally rotated
# the step count also remain None (if not explicitly passed by user) - which triggers a brute force from step values -26 to +26
# returns the plaintext based on the given step count or all possible results in case of bruteforce
def decrypt(cipher,offset=None):
    

    cipher_bak = cipher
    cipher=''
    for c in cipher_bak:
        if c.isalpha():
            cipher+=c

    # list with the ASCII values of the ciphertext
    cipherASCII = [ord(char) for char in cipher]
    plainASCII = []
    steps = offset

    # if step count is given by user
    if steps or steps==0:        
        # reverse rotating the ASCII values by 'steps' no. of steps        
        for x in cipherASCII:
            if x in range(97,123):
                if x-(steps%26)<97:              # lowercase letters
                    plainASCII.append(123-(97-(x-(steps%26))))
                else:
                    plainASCII.append(x-(steps%26))
            elif x in range(65,91):          # uppercase letters
                if x-(steps%26)<65:
                    plainASCII.append(91-(65-(x-(steps%26))))
                else:
                    plainASCII.append(x-(steps%26))
            elif x in range(48,58):          # numeric values
                if x-(steps%10)<48:
                    plainASCII.append(58-(48-(x-(steps%10))))
                else:
                    plainASCII.append(x-(steps%10))
            else:
                plainASCII.append(x)
            steps+=1
        
        plain = ''.join(map(chr,plainASCII))
        #print(plainASCII)
        # add special characters to final text
        for i in range(len(cipher_bak)):
            if not cipher_bak[i].isalpha():
                plain = plain[:i] + cipher_bak[i] + plain[i:]
        return plain

    # if step count is not provided - bruteforce
    else:
        offset = -26 # initialising steps from -26
        for offset in range(26):
            steps = offset
            plainASCII=[]
            for x in cipherASCII:                
                if x in range(97,123):
                    if x-(steps%26)<97:              # lowercase letters
                        plainASCII.append(123-(97-(x-(steps%26))))
                    else:
                        plainASCII.append(x-(steps%26))
                elif x in range(65,91):          # uppercase letters
                    if x-(steps%26)<65:
                        plainASCII.append(91-(65-(x-(steps%26))))
                    else:
                        plainASCII.append(x-(steps%26))
                elif x in range(48,58):          # numeric values
                    if x-(steps%10)<48:
                        plainASCII.append(58-(48-(x-(steps%10))))
                    else:
                        plainASCII.append(x-(steps%10))
                else:
                    plainASCII.append(x)
                steps+=1

            plain = ''.join(map(chr,plainASCII))
            # add special characters to final text
            for i in range(len(cipher_bak)):
                if not cipher_bak[i].isalpha():
                    plain = plain[:i] + cipher_bak[i] + plain[i:]
            # prints all possible combinations for rotation steps -26 to +26
            print('{}[!]{} Offset = {}\t: {}{}{}'.format(color.GREEN,color.END,offset,color.RED,plain,color.END))
            offset+=1            
        return

# preparatory function for encryption that takes in the 
# plaintext and step counts from user and calls the encrypting function with those values
# returns the ciphertext as returned from encryption function along with the step count given by user
def enc(plain):

    # taking input for the number of steps to rotate
    # int between -26 to +26 (with or without the signs allowed)
    try:
        offset = int(input('{}[?]{} Enter the offset (+x or -x): '.format(color.BLUE,color.END)))
        # checking if the given input is within the valid range
        if offset not in range(-26,27):
            raise ValueError()
        # calling the encrypt function with the plaintext and steps to rotate        
        ciphertext = encrypt(plain, offset)

    # catching and handling ValueError to end gracefully
    except ValueError:
        print('{}[-]{} Please enter a number between 1-26 with + or - sign'.format(color.RED,color.END))
        quit()

    return ciphertext,offset

# preparatory function for decryption that takes in the 
# ciphertext and step counts (if given) from user and calls the encrypting function with those values
# returns the ciphertext as returned from encryption function along with the step count given by user   -   for known step count
# returns None,None to caller function as bruteforce results are displayed by the decrypting function   -   for bruteforce
def dec(cipher):

    offset = None
    # taking input for the number of steps to reverse rotate
    # int between -26 to +26 (with or without the signs allowed)
    # this is the original number of steps as used during encryption
    try:
        offset = int(input('{}[?]{} Enter the offset \n{}[!]{} Leave empty to try bruteforce (+x or -x): '.format(color.BLUE,color.END,color.CYAN,color.END)))

        # checking if the given input is within the valid range
        if offset not in range(-26,27):
            raise ValueError()
        # calling the encrypt function with the plaintext and steps to rotate        
        plaintext = decrypt(cipher=cipher, offset=offset)        

    # catching and handling ValueError to end gracefully
    except ValueError:
        if not offset:
            decrypt(cipher=cipher,offset=offset)
        else:
            print('{}[-]{} Please enter a number between 1-26 with + or - sign'.format(color.RED,color.END))
            quit()
    
    if offset or offset==0:
        return plaintext,offset
    else:
        return None,None


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
            ciphertext,offset = enc(pt)                      # calling the enc() function with the input
            print('{}[+]{} The Ciphertext with offset {}{}{} is : {}{}{}'.format(color.GREEN,color.END,color.YELLOW,offset,color.END,color.RED,ciphertext,color.END))
        elif choice == 'd' or choice == 'D':
            # whether to load a file for the plaintext or type it from the console
            filechoice = input('{}[?]{} Load from a file? [y/N] : '.format(color.BLUE,color.END)).lower()
            if filechoice != 'y':
                ct = input('{}[?]{} Enter the Ciphertext : '.format(color.BLUE,color.END))       # ciphertext input
            else:
                filename = input('{}[?]{} Enter the filename: '.format(color.BLUE,color.END))
                ct = parsefile(filename)
            plaintext,offset = dec(ct)                       # calling dec() function with the input
            if offset or offset==0:                                       # if not bruteforce - then only print results
                print('{}[+]{} The Plaintext with offset {}{}{} is : {}{}{}'.format(color.GREEN,color.END,color.YELLOW,offset,color.END,color.RED,plaintext,color.END))
            else:
                print('{}[!]{} The bruteforce attack completed successfully!'.format(color.GREEN,color.END))
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
        parser = argparse.ArgumentParser(description='Incremental Rotational Encryption & Decryption')
        # encryption group option (single option --encrypt)
        enc_group = parser.add_argument_group('Encryption Options')
        enc_group.add_argument('-e','--encrypt', help='Encrypt a given Plaintext', default=False, action='store_true')
        # decryption group options (--decrypt and --brute)
        dec_group = parser.add_argument_group('Decryption Options')
        dec_group.add_argument('-d','--decrypt', help='Decrypt a given Ciphertext', default=False, action='store_true')
        dec_group.add_argument('-B','--brute', help='Bruteforce decryption (to be used only with -d, --decrypt)', default=False, action='store_true')
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
                ciphertext,offset = enc(pt)                      # calling the enc() function with the input
                print('{}[+]{} The Ciphertext with offset {}{}{} is : {}{}{}'.format(color.GREEN,color.END,color.YELLOW,offset,color.END,color.RED,ciphertext,color.END))
            elif choice == 'd' or choice == 'D':
                # whether to load a file for the plaintext or type it from the console
                filechoice = input('{}[?]{} Load from a file? [y/N] : '.format(color.BLUE,color.END)).lower()
                if filechoice != 'y':
                    ct = input('{}[?]{} Enter the Ciphertext : '.format(color.BLUE,color.END))       # ciphertext input
                else:
                    filename = input('{}[?]{} Enter the filename: '.format(color.BLUE,color.END))
                    ct = parsefile(filename)
                plaintext,offset = dec(ct)                       # calling dec() function with the input
                if offset or offset==0:                                       # if not bruteforce - then only print results
                    print('{}[+]{} The Plaintext with offset {}{}{} is : {}{}{}'.format(color.GREEN,color.END,color.YELLOW,offset,color.END,color.RED,plaintext,color.END))
                else:
                    print('{}[!]{} The bruteforce attack completed successfully!'.format(color.GREEN,color.END))
            else:
                print('{}[-] Please provide a valid coice of action{}'.format(color.RED,color.END))
            quit()

        # parsing command line argumets (provided the necvessary ones are given)
        if args.encrypt:                            # if encrypt flag is on
            if args.decrypt:                        # decrypt flag should be off
                print('{}[-] Please select only one option among Encrypt or Decrypt at a time{}'.format(color.RED,color.END))
                quit()
            if args.brute:                          # bruteforce flag should be off
                print('{}[-] Bruteforce can only be used during Decryption{}'.format(color.RED,color.END))
                quit()
            else:                                   # good to go - call enc() function and display result
                if args.file:
                    pt = parsefile(args.TEXT)
                    ciphertext,offset = enc(pt)
                    print('{}[+]{} The Ciphertext with {}{}{} steps is : {}{}{}'.format(color.GREEN,color.END,color.YELLOW,offset,color.END,color.RED,ciphertext,color.END))
                else:
                    ciphertext,offset = enc(args.TEXT)
                    print('{}[+]{} The Ciphertext with offset {}{}{} is : {}{}{}'.format(color.GREEN,color.END,color.YELLOW,offset,color.END,color.RED,ciphertext,color.END))

        elif args.decrypt:                          # if decrypt flag is on
            if args.brute:                          # if bruteforce option is also on
                if args.file:
                    ct = parsefile(args.TEXT)
                    decrypt(ct,None)
                else:
                    decrypt(args.TEXT,None)             # call decrypt function directly - steps not required
            else:                                   # no bruteforce - steps known
                #print('[+] Normal decryption')
                if args.file:
                    ct = parsefile(args.TEXT)
                    plaintext,offset = enc(ct)
                    if offset or offset==0:
                        print('{}[+]{} The Plaintext with {}{}{} steps is : {}{}{}'.format(color.GREEN,color.END,color.YELLOW,offset,color.END,color.RED,ciphertext,color.END))
                    else:
                        print('{}[!]{} The bruteforce attack completed successfully!'.format(color.GREEN,color.END))
                else:
                    plaintext,offset = dec(args.TEXT)    # call dec() function and display result
                    if offset or offset==0:
                        print('{}[+]{} The Plaintext with {}{}{} steps is : {}{}{}'.format(color.GREEN,color.END,color.YELLOW,offset,color.END,color.RED,plaintext,color.END))
                    else:
                        print('{}[!]{} The bruteforce attack completed successfully!'.format(color.GREEN,color.END))

        # if no arguments are provided except for positional (TEXT)
        else:
            print('{}[-] At least one of Encryption or Decryption action is required{}'.format(color.RED,color.END))

    except KeyboardInterrupt:
        print('\n{}[!] Exiting...{}'.format(color.RED,color.END))
        quit()

if __name__ == '__main__':
    main()

