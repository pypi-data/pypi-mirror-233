import os
import csv
from nlptools.utils.sentence_tokenizer import sent_tokenize
from nlptools.morphology.tokenizers_words import simple_word_tokenize

def corpus_tokenizer(dir_path, output_csv, row_id = 1, global_sentence_id = 1):
    row_id = row_id - 1
    global_sentence_id = global_sentence_id - 1
    with open(output_csv, 'w', newline='', encoding="utf-8") as csvfile:
        fieldnames = ['Row_ID', 'Docs_Sentence_Word_ID', 'Global Sentence ID', 'Sentence ID', 'Sentence', 'Word Position', 'Word']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        
        for root, dirs, files in os.walk(dir_path):
            for file in files:
                if file.endswith('.txt'):
                    file_path = os.path.join(root, file)
                    with open(file_path, 'r', encoding="utf-8") as f:
                        content = f.read()
                        sentences = sent_tokenize(content, dot=True, new_line=True, question_mark=False, exclamation_mark=False)
                        for sentence_id, sentence in enumerate(sentences, start=1):
                            words = simple_word_tokenize(sentence)
                            global_sentence_id += 1
                            for word_pos, word in enumerate(words, start=1):
                                row_id += 1
                                dir_name = os.path.basename(root)
                                doc_sentence_filename = file.split(".txt")[0]
                                docs_sentence_word_id = f"{dir_name}_{doc_sentence_filename}_{global_sentence_id}_{sentence_id}_{word_pos}"
                                writer.writerow({'Row_ID': row_id,
                                                 'Docs_Sentence_Word_ID': docs_sentence_word_id,
                                                 'Global Sentence ID': global_sentence_id,
                                                 'Sentence ID': sentence_id,
                                                 'Sentence': sentence,
                                                 'Word Position': word_pos,
                                                 'Word': word})
