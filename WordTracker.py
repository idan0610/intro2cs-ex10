#!/usr/bin/env python3


class WordTracker(object):
    """
    This class is used to track occurrences of words.
     The class uses a fixed list of words as its dictionary
     (note - 'dictionary' in this context is just a name and does
     not refer to the pythonic concept of dictionaries).
     The class maintains the occurrences of words in its
     dictionary as to be able to report if all dictionary's words
     were encountered.
    """

    def __init__(self, word_list):
        """
        Initiates a new WordTracker instance.
        :param word_list: The instance's dictionary.
        """
        self.__word_list = word_list.copy()
        self.__sorted_list = self.merge_sort(self.__word_list)
        self.__found_words = []
        self.reset()

    def merge_sort(self, words):
        """
        This function makes a merge sort for the list of words according the
        algorithm of merge sort

        :param words: list of words
        :return: sorted list of words
        """
        if len(words) <= 1:
            # Stop condition for the recursion
            return words

        # Split the list to 2 lists in the middle, and call the function
        # recursively with the 2 lists
        middle = len(words) // 2
        left = self.merge_sort(words[:middle])
        right = self.merge_sort(words[middle:])

        # Sort the final lists left and right using merge()
        words = self.merge(left, right)
        return words

    def merge(self, left, right):
        """
        This function creates a new list where its words are from lists left
        and right and sorted
        :param left: list of words
        :param right: list of words
        :return: sorted list of words
        """
        words = left + right
        l, r = 0, 0
        for i in range(len(words)):
            if l < len(left):
                # If there is a word with index l in left list, put the word
                # in left_val
                left_val = left[l]
            else:
                left_val = None

            if r < len(right):
                # If there is a word with index r in right list, put the word
                # in right_val
                right_val = right[r]
            else:
                right_val = None

            if (left_val and right_val and left_val < right_val) or \
                    right_val is None:
                # If there are words on left_val and right_val and left_vav <
                # right_val or there isn't word on right_val
                words[i] = left_val
                l += 1  # Move to next word from left list
            elif (left_val and right_val and left_val >= right_val) or \
                    left_val is None:
                # If there are words on left_val and right_val and left_vav >=
                # right_val or there isn't word on left_val
                words[i] = right_val
                r += 1  # Move to next word from right list
        return words

    def binary_search(self, word):
        """
        This function makes a binary search for word
        :param word:
        :return:
        """
        left = 0
        right = len(self.__sorted_list) - 1
        index = -1

        while right >= left:
            # Find the middle index of the list and the word on that index
            middle_index = (left + right) // 2
            middle = self.__sorted_list[middle_index]

            if middle == word:
                # The word was found, save its index and break the loop
                index = middle_index
                break
            elif middle > word:
                # the current word > the requested word, move the
                # right index to middle_index - 1
                right = middle_index - 1
            else:
                # the current word <  the requested word, move the
                # left index to middle_index + 1
                left = middle_index + 1
        return index

    def __contains__(self, word):
        """
        Check if the input word in contained within dictionary.
         For a dictionary with n entries, this method guarantees a
         worst-case running time of O(n) by implementing a
         binary-search.
        :param word: The word to be examined if contained in the
        dictionary.
        :return: True if word is contained in the dictionary,
        False otherwise.
        """

        # Try to find the index of word in the dictionary
        index = self.binary_search(word)

        if index != -1:
            # If the word was found
            return True
        else:
            return False

    def encounter(self, word):
        """
        A "report" that the give word was encountered.
        The implementation changes the internal state of the object as
        to "remember" this encounter.
        :param word: The encountered word.
        :return: True if the given word is contained in the dictionary,
        False otherwise.
        """

        # Try to find the index of word in the dictionary
        index = self.binary_search(word)

        if index != -1:
            # If the word was found, change the found words in the same index
            # to True
            self.__found_words[index] = True
            return True
        else:
            return False

    def encountered_all(self):
        """
        Checks whether all the words in the dictionary were
        already "encountered".
        :return: True if for each word in the dictionary,
        the encounter function was called with this word;
        False otherwise.
        """
        if False in self.__found_words:
            return False
        else:
            return True

    def reset(self):
        """
        Changes the internal representation of the instance such
        that it "forget" all past encounters. One implication of
        such forgetfulness is that for encountered_all function
        to return True, all the dictionaries' entries should be
        called with the encounter function (regardless of whether
        they were previously encountered ot not).
        """

        # Reset the list of found words to False for every word
        self.__found_words = [False]*len(self.__word_list)