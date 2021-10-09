import itertools
import sys

'''
Create custom wordlist for targeted passwords
'''

def targeted_wordlist(word, iters_num):
    #chrs = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
    alphanum = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
    # Num of iterations
    #n = 3

    #word = word_perms(word)

    for xs in itertools.product(alphanum, repeat=iters_num):
        print(word + ''.join(xs))



def word_perms(word):
    words_list = []
    res = itertools.permutations(word, len(word))
    for words in res:
        word = ''.join(words)
        words_list.append(word)

    return words_list

def main():
    word = sys.argv[1]
    perms = word_perms(word)
    for i in range(len(perms)):
        print(targeted_wordlist(perms[i], 3))

main()
#wordlist = targeted_wordlist('jonny')
#print(wordlist)

#wordlist = targeted_wordlist(word_perms('jonny'))
#print(wordlist)
