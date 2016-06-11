#!/usr/bin/env python3
EOF = ""
EOL = "\n"


class WordExtractor(object):
    """
    This class should be used to iterate over words contained in files.
     The class should maintain space complexity of O(1); i.e, regardless
     of the size of the iterated file, the memory requirements ofa class
     instance should be bounded by some constant.
     To comply with the space requirement, the implementation may assume
     that all words and lines in the iterated file are bounded by some
     constant, so it is allowed to read words or lines from the
     iterated file (but not all of them at once).
    """

    def __init__(self, filename):
        """
        Initiate a new WordExtractor instance whose *source file* is
        indicated by filename.
        :param filename: A string representing the path to the instance's
        *source file*
        """
        self.__file = open(filename)
        self.__current_line = ""
        self.__words_list = []

    def __iter__(self):
        """
        Returns an iterator which iterates over the words in the
        *source file* (i.e - self)
        :return: An iterator which iterates over the words in the
        *source file*
        """
        return self

    def __next__(self):
        """
        Make a single word iteration over the source file.
        :return: current_word:  A word from the file.
        """
        if len(self.__words_list) == 0:
            # The words list contain the words of the current line. If the list
            # is empty, then the function will find the next line with words,
            # if exist.
            found = False  # Will be True if a new line with word will be found
            while not found:
                self.__current_line = self.__file.readline()
                if self.__current_line == EOF:
                    # The new line is the end of the file, so the fill will
                    # close to save memory and the iteration will stop
                    self.__file.close()
                    raise StopIteration()
                elif self.__current_line == EOL:
                    # If the line is empty, but not on end of file, continue
                    # for next line
                    continue
                else:
                    # If the new line is not empty
                    found = True

            # Make a new list of words of the new line
            self.__words_list = self.__current_line.split()

        # Take the first word from the list and return it. Delete the first
        # word from the list
        current_word = self.__words_list.pop(0)
        return current_word