#!/usr/bin/python3

import argparse
from time import sleep
from utilities.colors import color
from utilities.tools import clear
from algos.morse import charsets

def encrypt(pt):
    pt=pt.lower()
    ct = ''

    for char in pt:
        if char in charsets.alpha:
            ct+=charsets.alpha[char]+' '
        elif char in charsets.num:
            ct+=charsets.num[char]+' '
        elif char in charsets.punct:
            ct+=charsets.punct[char]+' '
        else:
            ct+=char+' '

    #print('[+] Morse code is : {}'.format(ct.strip()))
    return ct.strip()


def decrypt(ct):
    
    pt = ''
    lines = ct.split('\n')
    ct=''

    for line in lines:
        ct+=line + ' / '


    for char in ct.split(' '):
        if char in charsets.alpha.values():
            pt+=[key for key,val in charsets.alpha.items() if val==char][0].upper()
        elif char in charsets.num.values():
            pt+=[key for key,val in charsets.num.items() if val==char][0].upper()
        elif char in charsets.punct.values():
            pt+=[key for key,val in charsets.punct.items() if val==char][0].upper()
        else:
            pt+=char

    #print('[+] Plaintext is : {}'.format(pt.strip()))
    return pt.strip()


# plays the Morse code audio 
# fetches the audio files from a folder (required!)
def playSound(code):
    try:
        import pygame.mixer, pygame.time
    except ModuleNotFoundError:
        print('{}[-] PyGame module not installed! Cannot play audio...{}\n{}[!] Please make sure the PyGame module is installed for the Audio feature to work properly{}\n[*] You can install it from the requirements file using the following command:\n{}    pip install -r requirements.txt{}\n[!] You can also install it manually with the command:\n{}    pip install PyGame{}'.format(color.RED,color.END,color.YELLOW,color.END,color.BLUE,color.END,color.BLUE,color.END))
        quit()
    DELAY = 0.2  # Time between sounds
    mixer = pygame.mixer
    mixer.init()

    for char in code:                               # for each character in original message
        flag=0
        PATH = "utilities/morse_code_audio/"        # play the respective morse code audio (files named as "CHARACTER_morse_code.ogg")
        if char == ' ':                             # if character is space
            sleep(7 * DELAY)                        # add delay of 7 units (standard Morse practice)
        else:
        # check if the character is one of the following
        # these audio files are named outside the convention due to file naming restrictions
            if char == ':':
                PATH += 'colon_morse_code.ogg'
            elif char == '/':
                PATH += 'slash_morse_code.ogg'
            elif char == '?':
                PATH += 'question_morse_code.ogg'
            elif char == '"':
                PATH += 'quotation_morse_code.ogg'

        # otherwise, if character is not among the above
            else:
                PATH += char + '_morse_code.ogg'    # follow naming convention and modify path
            
            try:
                sound = mixer.Sound(PATH)               # load the sound from path
            except FileNotFoundError:
                print('{}[-] Audio File not found{}\n{}[!] Please ensure that the Utilities directory is present in the same directory as this script and its contents remain unchanged!{}'.format(color.RED,color.END,color.YELLOW,color.END))
                quit()
            beep = sound.play()                     # play the sound and capture the channel as beep
            while beep.get_busy():      # if audio playing (check channel status)
                if not flag:
                    print('{}\t{}\t{}{}'.format(color.BLUE, char.upper(), encrypt(char), color.END))
                    flag=1
                pygame.time.wait(100)   # wait for it to finish
            sleep(3 * DELAY)            # once finished, add delay for next character


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
        pt,ct = None,None
        choice = input('{}[?]{} Encrypt or Decrypt? [e/d] : '.format(color.BLUE,color.END))
        if choice == 'e' or choice == 'E':
            # whether to load a file for the plaintext or type it from the console
            filechoice = input('{}[?]{} Load from a file? [y/N] : '.format(color.BLUE,color.END)).lower()
            if filechoice != 'y':
                pt = input('{}[?]{} Enter the Plaintext : '.format(color.BLUE,color.END))        # plaintext input
            else:
                filename = input('{}[?]{} Enter the filename: '.format(color.BLUE,color.END))
                pt = parsefile(filename)
            morse = encrypt(pt)                      # calling the enc() function with the input
            print('{}[+]{} The Morse Code is : {}{}{}'.format(color.GREEN,color.END,color.RED,morse,color.END))
        elif choice == 'd' or choice == 'D':
            # whether to load a file for the plaintext or type it from the console
            filechoice = input('{}[?]{} Load from a file? [y/N] : '.format(color.BLUE,color.END)).lower()
            if filechoice != 'y':
                ct = input('{}[?]{} Enter the Morse Code : '.format(color.BLUE,color.END))       # ciphertext input
            else:
                filename = input('{}[?]{} Enter the filename: '.format(color.BLUE,color.END))
                ct = parsefile(filename)
            plaintext = decrypt(ct)                       # calling dec() function with the input
            print('{}[+]{} The Plaintext is : {}{}{}'.format(color.GREEN,color.END,color.RED,plaintext,color.END))
        else:
            print('{}[-] Please provide a valid coice of action{}'.format(color.RED,color.END))
            quit()

        play = input('{}[?]{} Do you want to play the Morse Code? [y/n] : '.format(color.BLUE,color.END))
        if play[0].lower() == 'y':
            if pt:
                playSound(pt)
            elif ct:
                playSound(plaintext)
        quit()
    except KeyboardInterrupt:
        print('\n{}[!] Exiting...{}'.format(color.RED,color.END))
        quit()


# main driver function
# parses arguments 
# prompts the user for necessary inputs if arguments not provided 
def main():
    try:
        clear()
        
        # script description
        parser = argparse.ArgumentParser(description='Morse Code Encryption & Decryption')
        parser.add_argument('-s','--sound', help='Play the Morse Code', default=False, action='store_true')
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
            pt,ct = None,None
            choice = input('{}[?]{} Encrypt or Decrypt? [e/d] : '.format(color.BLUE,color.END))
            if choice == 'e' or choice == 'E':
                # whether to load a file for the plaintext or type it from the console
                filechoice = input('{}[?]{} Load from a file? [y/N] : '.format(color.BLUE,color.END)).lower()
                if filechoice != 'y':
                    pt = input('{}[?]{} Enter the Plaintext : '.format(color.BLUE,color.END))        # plaintext input
                else:
                    filename = input('{}[?]{} Enter the filename: '.format(color.BLUE,color.END))
                    pt = parsefile(filename)
                morse = encrypt(pt)                      # calling the enc() function with the input
                print('{}[+]{} The Morse Code is : {}{}{}'.format(color.GREEN,color.END,color.RED,morse,color.END))
            elif choice == 'd' or choice == 'D':
                # whether to load a file for the plaintext or type it from the console
                filechoice = input('{}[?]{} Load from a file? [y/N] : '.format(color.BLUE,color.END)).lower()
                if filechoice != 'y':
                    ct = input('{}[?]{} Enter the Morse Code : '.format(color.BLUE,color.END))       # ciphertext input
                else:
                    filename = input('{}[?]{} Enter the filename: '.format(color.BLUE,color.END))
                    ct = parsefile(filename)
                plaintext = decrypt(ct)                       # calling dec() function with the input
                print('{}[+]{} The Plaintext is : {}{}{}'.format(color.GREEN,color.END,color.RED,plaintext,color.END))
            else:
                print('{}[-] Please provide a valid coice of action{}'.format(color.RED,color.END))
                quit()

            play = input('{}[?]{} Do you want to play the Morse Code? [y/n] : '.format(color.BLUE,color.END))
            if play[0].lower() == 'y':
                if pt:
                    playSound(pt)
                elif ct:
                    playSound(plaintext)
            quit()

        # parsing command line argumets (provided the necvessary ones are given)
        if args.encrypt:                            # if encrypt flag is on
            if args.decrypt:                        # decrypt flag should be off
                print('{}[-] Please select only one option among Encrypt or Decrypt at a time{}'.format(color.RED,color.END))
                quit()
            else:                                   # good to go - call enc() function and display result
                if args.file:
                    pt = parsefile(args.TEXT)
                    morse = encrypt(pt)
                else:
                    morse = encrypt(args.TEXT)
                print('{}[+]{} The Morse Code is : {}{}{}'.format(color.GREEN,color.END,color.RED,morse,color.END))

        elif args.decrypt:                          # if decrypt flag is on
            if args.file:
                ct = parsefile(args.TEXT)
                plaintext = decrypt(ct)
            else:
                plaintext = decrypt(args.TEXT)    # call dec() function and display result
            print('{}[+]{} The Plaintext is : {}{}{}'.format(color.GREEN,color.END,color.RED,plaintext,color.END))
        # if no arguments are provided except for positional (TEXT)
        else:
            print('{}[-] At least one of Encryption or Decryption action is required{}'.format(color.RED,color.END))

        if args.sound:
            if args.file and args.encrypt:
                lines = parsefile(args.TEXT).split('\n')
                msg=''
                for line in lines:
                    msg+=line+' '
                #print(msg)
                #quit()
                playSound(msg)
            elif args.file and args.decrypt:
                playSound(plaintext)
            else:
                playSound(args.TEXT)

    except KeyboardInterrupt:
        print('\n{}[!] Exiting...{}'.format(color.RED,color.END))
        quit()


if __name__ =='__main__':
    main()

