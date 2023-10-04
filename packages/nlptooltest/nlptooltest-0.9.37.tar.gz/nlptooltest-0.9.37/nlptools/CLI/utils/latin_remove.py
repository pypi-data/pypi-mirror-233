"""
sina_remove_latin 

--About: 
The sina_remove_latin  tool performs delete latin characters from the input text.

--Usage:
sina_remove_latin  --text "your text"


--Example:
sina_remove_punctuation --text "123test"

output => 123   #without latin char
      
--Note:
This tool for latin characters, if the input text is an Arabic characters or numbers the output
will be the same input 
"""

import argparse
from nlptools.utils.parser import remove_latin


def main():
    parser = argparse.ArgumentParser(description='remove latin characters from the text')

    parser.add_argument('--text', type=str, required=True, help='The input text')
    args = parser.parse_args()
    result = remove_latin(args.text)
 
    print(result)
    if __name__ == '__main__':
        main()

#sina_remove_latin --text "123test"