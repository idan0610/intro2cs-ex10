import os
from WordTracker import WordTracker
from WordExtractor import WordExtractor


class PathIterator:
    """
    An iterator which iterates over all the directories and files
    in a given path (note - in the path only, not in the
    full depth). There is no importance to the order of iteration.
    """

    def __init__(self, path):
        """
        This function builds a new PathIterator object

        :param path: string, the path the iterator will work on
        :return: None
        """
        self.__path = path
        self.__files_and_folders_list = os.listdir(self.__path)
        self.__index = 0

    def __iter__(self):
        """
        This function returns the iterator that iterates over path

        :return: self, the iterator
        """
        return self

    def __next__(self):
        """
        The function makes a single iteration over a file or folder in path

        :return:
        """
        if self.__index == len(self.__files_and_folders_list):
            # The iterator iterated all file and folders in list, so the
            # iteration is stopping
            raise StopIteration()
        else:
            # Take the current file or folder in list, join it the full path
            # raise the index to move the next file on next iteration and
            # return the current
            current = os.path.join(self.__path, \
                                self.__files_and_folders_list[self.__index])
            self.__index += 1
            return current


def path_iterator(path):
    """
    Returns an iterator to the current path's filed and directories.
    Note - the iterator class is not outlined in the original
     version of this file - but rather is should be designed
     and implemented by you.
    :param path: A (relative or an absolute) path to a directory.
    It can be assumed that the path is valid and that indeed it
    leads to a directory (and not to a file).
    :return: An iterator which returns all the files and directories
    in the *current* path (but not in the *full depth* of the path).
    """
    it = PathIterator(path)
    return it


def __print_tree_helper(path, sep, counter):
    """
    This function is used by print_tree to print the tree of files and folders
    of some path in recursion

    :param path: A (relative or an absolute) path to a directory.
    It can be assumed that the path is valid and that indeed it
    leads to a directory (and not to a file).
    :param sep: A string separator which indicates the depth of
     current hierarchy.
    :param counter: int, used to determine how much the sep will be printed
    :return: None
    """
    it = path_iterator(path)
    for i in it:
        # For each file or folder in the iterator, extract the name of the
        # file or folder and print it with the correct amount of seps
        current = i[len(path)+1:]
        print ((sep * (counter)) + current)
        if os.path.isdir(i):
            # If current is folder, call recursively the function, where the
            # new path is the path to the folder
            __print_tree_helper(i, sep, counter+1)



def __file_with_all_words_helper(path, word_tracker):
    """
    This function is used by file_with_all_words to find the file containing
    all the words of word list

    :param path: A (relative or an absolute) path to a directory.
    It can be assumed that the path is valid and that indeed it
    leads to a directory (and not to a file).
    :param word_tracker: WordTracker object, used to determine each word in
    file if it is on the word list
    :return: found: string if a file with all words was found,
                    None if no file was found
    """
    it = path_iterator(path)
    for i in it:
        # For each file or folder in it
        if os.path.isfile(i):
            # If current is file, create a new WordExtractor with current file
            # is parameter
            word_extractor = WordExtractor(i)
            for j in word_extractor:
                # Check each word in current file to determine if the word is
                # in the word list using the word tracker object
                if word_tracker.encounter(j):
                    if word_tracker.encountered_all():
                        # After each word from word list located in file, check
                        # the file has all words of word list. If so, return
                        # the file
                        return i
            # If the file does not have all words from word list, reset the
            # word tracker and continue the next file
            word_tracker.reset()
        elif os.path.isdir(i):
            # If current is folder, call the function recursively the the new
            # path the current folder
            found =  __file_with_all_words_helper(i, word_tracker)
            if found == None:
                # If no file was found with all words, continue the nex file
                continue
            else:
                # If a file was found, return it and end the recursion
                return found
    return None # Only if no file was found


def print_tree(path, sep='  '):
    """
    Print the full hierarchical tree of the given path.
    Recursively print the full depth of the given path such that
    only the files and directory names should be printed (and not
    their full path), each in its own line preceded by a number
    of separators (indicated by the sep parameter) that correlates
    to the hierarchical depth relative to the given path parameter.
    :param path: A (relative or an absolute) path to a directory.
    It can be assumed that the path is valid and that indeed it
    leads to a directory (and not to a file).
    :param sep: A string separator which indicates the depth of
     current hierarchy.
    """
    # Take the name of the parent path and print it
    head, tail = os.path.split(path)
    print(tail)
    # Print all sub files and folder using __print_tree_helper
    __print_tree_helper(path, sep, 1)


def file_with_all_words(path, word_list):
    """
    Find a file in the full depth of the given path which contains
    all the words in word_list.
    Recursively go over  the files in the full depth of the given
    path. For each, check whether it contains all the words in
     word_list and if so return it.
    :param path: A (relative or an absolute) path to a directory.
    In the full path of this directory the search should take place.
    It can be assumed that the path is valid and that indeed it
    leads to a directory (and not to a file).
    :param word_list: A list of words (of strings). The search is for
    a file which contains this list of words.
    :return: The path to a single file which contains all the
    words in word_list if such exists, and None otherwise.
    If there exists more than one file which contains all the
    words in word_list in the full depth of the given path, just one
    of theses should be returned (does not matter which).
    """
    # Create a WordTracker object to the word list
    word_tracker = WordTracker(word_list)
    # Check all sub files and folders to find a file contain all words from
    # word list using __file_with_all_words_helper
    return __file_with_all_words_helper(path, word_tracker)