# -*- coding: utf-8 -*-
"""
Created on Tue Nov 1 4:25:30 2016

@author: Zhecan Wang
"""

# Explore Google's huge Word2Vec model.

import gensim
import logging
import random
import matplotlib.pyplot as plt

# Logging code taken from http://rare-technologies.com/word2vec-tutorial/
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)


                
class Inspection(object):
    """Inspection on word2vec model"""
    def __init__(self):
        self.path = 'GoogleNews-vectors-negative300.bin'
        self.similarity = []

    def loadModel(self):
        # Load Google's pre-trained Word2Vec model.
        self.model = gensim.models.Word2Vec.load_word2vec_format(self.path, binary=True)  


    def contentRetrieve(self):
        # Does the model include stop words?
        print("Does it include the stop words like \'a\', \'and\', \'the\'? %d %d %d" % ('a' in model.vocab, 'and' in model.vocab, 'the' in model.vocab))

        # Retrieve the entire list of "words" from the Google Word2Vec model.
        vocab = model.vocab.keys()

        fileNum = 1

        wordsInVocab = len(vocab)
        wordsPerFile = int(100E3)

        # Write out the words in 100k chunks.
        for wordIndex in range(0, wordsInVocab, wordsPerFile):
            # Write out the chunk to a numbered text file.    
            with open("vocabulary/vocabulary_%.2d.txt" % fileNum, 'w') as f:
                # For each word in the current chunk...        
                for i in range(wordIndex, wordIndex + wordsPerFile):
                    # Write it out and escape any unicode characters.            
                    f.write(vocab[i].encode('UTF-8') + '\n')
            
            fileNum += 1

    def writeToFile(self):
        with open( "randomSimilarityDist"+ ".txt", "a") as f:
        # with codecs.open( "randomSimilarityDist"+ ".txt", "a", encoding="utf-8") as f:  
            for simi in self.similarity:
                try:
                    f.write(str(simi) + "\n")
                except Exception as e:
                    print e
                    print simi
        self.similarity = []

    def SimilarityDistrib(self):
        fileNum = 1
        file = open("vocabulary/vocabulary_%.2d.txt" % fileNum, 'r')
        words = list(file)
        random.shuffle(words)
        counter = 0

        for i in range(0, len(words), 2):
            word1, word2 = str(words[i]).strip(), str(words[i + 1]).strip()
            try:
                simi = self.model.similarity(word1, word2)
                print (word1, word2)
                print simi
                self.similarity.append(simi)

            except Exception as e:
                print e
                print (word1, word2)
            
            counter += 1
            if counter % 10 == 0:
                print counter
                self.writeToFile()
                print "finish writing to file"
    
    def plotDist(self):
        f = open("randomSimilarityDist.txt", 'r')
        data = []        
        for line in f:
            data.append(float(line))
        plt.hist(data, bins = 20)
        plt.xlabel("Value")
        plt.ylabel("Frequency")
        plt.show()

    def run(self):
        self.loadModel()
        self.SimilarityDistrib()
        self.plotDist()

if __name__ == '__main__':
    Inspection().run()
    
