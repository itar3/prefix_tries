class Node():
    def __init__(self, data=None, size=27):
        self.data = data
        self.words = []
        self.child = [None] * size


class Trie():
    def __init__(self):
        self.root = Node()
        self.most_common_word = [0, [0]]

    def insert(self, word, id = 0):
        current = self.root
        for char in word:
            index = ord(char) - 97
            if current.child[index] is None:
                current.child[index] = Node()
            current = current.child[index]


            if word not in current.words:
                current.words.append(word)

        if current.child[26] is None:
            current.child[26] = Node()
            current.child[26].data = [word, [id]]
        else:
            current.child[26].data[1].append(id)

    def search(self, word):
        current = self.root
        for char in word:
            index = ord(char) - 97
            if current.child[index] is None:
                return ['not found']
            current = current.child[index]
        if current.child[26] is None:
            return ["not found"]
        else:
            retval = current.child[26].data

        return retval

    # def search_for_common(self, prefix):
    #     self.most_common_word = [None, []]
    #     current = self.root
    #     for char in prefix:
    #         index = ord(char) - 97
    #         if current.child[index] is None:
    #             return ['not found']
    #         current = current.child[index]
    #
    #     possible_words_list = current.words
    #     for word in possible_words_list:
    #         possible_most_common = self.search(word)
    #         if len(possible_most_common[1]) >= len(self.most_common_word[1]):
    #             self.most_common_word = possible_most_common
    #
    #     return self.most_common_word[0]







###############################################################################

def data_to_trie(data_file, trie):
    f = open(data_file, 'r')
    data_input = []
    for lines in f:
        lines = lines.strip().split(':')
        data_input.append(lines)
    f.close()
    for i in range(len(data_input)):
        id = data_input[i][0]
        word = ''
        seen = []

        for j in range(len(data_input[i][1])):
            char = data_input[i][1][j]
            if j == len(data_input[i][1]) - 1:
                word += char
                if word not in seen:
                    trie.insert(word, id)
                    seen.append(word)
                word = ''
                
            if char == " ":
                if word not in seen:
                    trie.insert(word, id)
                    seen.append(word)
                word = ''
            else:
                word += char

def lookup(data_file, query_file):

    trie = Trie()
    data_to_trie(data_file, trie)

    output = []
    file = open(query_file, 'r')
    for line in file:
        line = line.split()
        if line == []:
            continue
        to_out = trie.search(line[0])
        if len(to_out) < 2:
            output.append(to_out)
        else:
            output.append(to_out[1])

    file.close()

    file = open('song_ids.txt', 'w')
    for i in output:
        for j in i:
            file.write(j)
            file.write(" ")
        file.write('\n')
    file.close()


def most_common(data_file, query_file):
    trie = Trie()

    data_to_trie(data_file, trie)

    output = []
    file = open(query_file, 'r')
    for line in file:
        line = line.split()
        if line == []:
            continue
        to_out = trie.search_for_common(line[0])
        output.append(to_out)
    file.close()

    file = open('most_common_lyrics.txt', 'w')
    for i in output:
        for j in i:
            file.write(j)
        file.write('\n')
    file.close()


def palindromic_substring(s):
    trie = Trie()
    substring_reverse = []
    for start in range(len(s) - 1, -1, -1):
        word = s[start]
        for end in range(start - 1, -1, -1):
            word += s[end]
            substring_reverse.append(word)

    for word in substring_reverse:
        trie.insert(word)


    substring_normal_list = []
    for start in range(len(s)):
        word = s[start]
        for end in range(start + 1, len(s)):
            word += s[end]
            substring_normal_list.append((word, start, end))

    out = []
    for word in substring_normal_list:

        possible_palindrome = word[0]
        start_index = word[1]
        end_index = word[2]

        substring_match = (trie.search(possible_palindrome), start_index, end_index)
        substring_match_palindrome = substring_match[0][0]
        if len(substring_match_palindrome) >= 2:
            if possible_palindrome[0] == substring_match_palindrome[-1] and possible_palindrome[1] == substring_match_palindrome[-2]:
                out.append((start_index, end_index))

    print(out)

lookup('test', 'query_file')

palindromic_substring('abbba')