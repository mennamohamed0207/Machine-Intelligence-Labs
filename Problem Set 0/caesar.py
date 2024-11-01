from typing import Tuple, List
import utils

'''
    The DecipherResult is the type defintion for a tuple containing:
    - The deciphered text (string).
    - The shift of the cipher (non-negative integer).
        Assume that the shift is always to the right (in the direction from 'a' to 'b' to 'c' and so on).
        So if you return 1, that means that the text was ciphered by shifting it 1 to the right, and that you deciphered the text by shifting it 1 to the left.
    - The number of words in the deciphered text that are not in the dictionary (non-negative integer).
'''
DechiperResult = Tuple[str, int, int]

def caesar_dechiper(ciphered: str, dictionary: List[str]) -> DechiperResult:
    '''
        This function takes the ciphered text (string)  and the dictionary (a list of strings where each string is a word).
        It should return a DechiperResult (see above for more info) with the deciphered text, the cipher shift, and the number of deciphered words that are not in the dictionary. 
    '''
    dictionary = set(dictionary)
    def shift_char(c, shift):
        if c.isalpha():
            return chr(((ord(c) - ord('a') - shift) % 26) + ord('a'))
        return c

    best_result = None

    for shift in range(26):
        deciphered = ''.join(shift_char(char, shift) for char in ciphered)
        
        count = sum(1 for word in deciphered.split() if word not in dictionary)
        
        if best_result is None or count < best_result[2]:
            best_result = (deciphered, shift, count)

    return best_result