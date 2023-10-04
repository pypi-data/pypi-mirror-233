"""
sina_remove_punctuation 

--About: 
The sina_remove_punctuation tool performs delete punctuation marks from the input text.

--Usage:
sina_remove_punctuation --text TEXT

      --text TEXT
        the input text including punctuation marks like: [ , ] , ? , ! , { , } , " , . , @ , # , $ , ...


--Example:
sina_remove_punctuation --text "te%s@t...!!?"

output => test
      
"""

import argparse
from nlptools.utils.parser import remove_punctuation
#from nlptools.utils.parser import read_file
#from nlptools.utils.parser import write_file


def main():
    parser = argparse.ArgumentParser(description='remove punctuation marks from the text')

    parser.add_argument('--text',required=True,help="input text")
   # parser.add_argument('myFile', type=argparse.FileType('r'),help='Input file csv')
    args = parser.parse_args()
    result = remove_punctuation(args.text)
 
    print(result)
    if __name__ == '__main__':
        main()

#sina_remove_punctuation --text "your text"

