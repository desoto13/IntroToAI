import nltk
import sys
import os
import string
import math

FILE_MATCHES = 1
SENTENCE_MATCHES = 1


def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python questions.py corpus")

    # Calculate IDF values across files
    files = load_files(sys.argv[1])
    file_words = {
        filename: tokenize(files[filename])
        for filename in files
    }
    file_idfs = compute_idfs(file_words)

    # Prompt user for query
    query = set(tokenize(input("Query: ")))

    # Determine top file matches according to TF-IDF
    filenames = top_files(query, file_words, file_idfs, n=FILE_MATCHES)

    # Extract sentences from top files
    sentences = dict()
    for filename in filenames:
        for passage in files[filename].split("\n"):
            for sentence in nltk.sent_tokenize(passage):
                tokens = tokenize(sentence)
                if tokens:
                    sentences[sentence] = tokens

    # Compute IDF values across sentences
    idfs = compute_idfs(sentences)

    # Determine top sentence matches
    matches = top_sentences(query, sentences, idfs, n=SENTENCE_MATCHES)
    for match in matches:
        print(match)


def load_files(directory):
    """
    Given a directory name, return a dictionary mapping the filename of each
    `.txt` file inside that directory to the file's contents as a string.
    """
    mapping = dict()
    for filename in os.listdir(directory):
        #print("filename: ", filename)
        files = os.path.join(directory, filename)
        #print("files: ", files)
        with open(files, "r", encoding='latin1') as f:
            mapping[filename] = f.read()
    return mapping

def tokenize(document):
    """
    Given a document (represented as a string), return a list of all of the
    words in that document, in order.

    Process document by coverting all words to lowercase, and removing any
    punctuation or English stopwords.
    """
    all_words = nltk.word_tokenize(document)
    process_document = list()
    for word in all_words:
        if word not in nltk.corpus.stopwords.words("english"):
            if word not in string.punctuation:
                process_document.append(word.lower())
    return process_document


def compute_idfs(documents):
    """
    Given a dictionary of `documents` that maps names of documents to a list
    of words, return a dictionary that maps words to their IDF values.

    Any word that appears in at least one of the documents should be in the
    resulting dictionary.
    """
    unique_words = set()
    
    for doc_name in documents:
        unique_words.update(documents[doc_name])
    
    idf = dict()
    for word in unique_words:
        total_number = sum(word in documents[doc_name] for doc_name in documents) + 1
        idf_score = math.log(len(documents)/total_number)
        idf[word] = idf_score
    return idf
        

def top_files(query, files, idfs, n):
    """
    Given a `query` (a set of words), `files` (a dictionary mapping names of
    files to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the filenames of the the `n` top
    files that match the query, ranked according to tf-idf.
    """
    tf_idfs = dict()
    tfidfs_score = list()
    for doc in files:
        tf_idfs[doc] = 0
        for word in query:
            tf_idfs[doc] += files[doc].count(word) + idfs[word]
    tfidfs_score = list(key for key, value in sorted(tf_idfs.items(), key=lambda item: item[1], reverse=True))[:n]
    return tfidfs_score


def top_sentences(query, sentences, idfs, n):
    """
    Given a `query` (a set of words), `sentences` (a dictionary mapping
    sentences to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the `n` top sentences that match
    the query, ranked according to idf. If there are ties, preference should
    be given to sentences that have a higher query term density.
    """
    list_topsentences = dict()
    for sentence in sentences:
        list_topsentences[sentence] = (sum (idfs[word] for word in query if word in sentences[sentence]),
        sum(word in query for word in sentences[sentence])/len(sentences[sentence]))
    topsentences = sorted(list(list_topsentences.keys()), key = lambda x: list_topsentences[x], reverse = True)[:n]
    return topsentences


if __name__ == "__main__":
    main()
