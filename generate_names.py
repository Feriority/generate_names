"""Generates random names by Markov chain, given a file of samples.

Treats runs of letters as a single character, so that (for example) a double
consonant that only appears in the middle of a name will never start a name,
and also so that a character that is only repeated up to n times will never
be repeated more within a name.
"""
import argparse
import random
from collections import defaultdict


class _START_TOKEN(object):
    """Class to indicate the start of a string.  Use the singleton START_TOKEN
    instead of creating new instances.
    """
    def __mul__(self, x):
        """Any number of START_TOKENs is a START_TOKEN"""
        return self
START_TOKEN = _START_TOKEN()


def process_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--path', type=str, default='name_list', help='Path of the sample names.')
    parser.add_argument('--count', type=int, default=25, help='Number of names to generate.')

    args = parser.parse_args()
    return args.path, args.count

def read_names(name_path):
    with open(name_path) as f:
        names = (name.strip().lower() for name in f.readlines())
    return names

def make_chain(names):
    """Given a list of names, build the markov chain as a defaultdict
    of defaultdicts of ints, like so:
        chain[first_token][second_token] == number of occurances
            of second character following first character

    A token here is usually, but not necessarily a single character.  Runs
    of a repeated character will be treated as a single token, to avoid
    placing repeated characters in places they wouldn't make sense, or
    repeating a character more times than it should be repeatable (ie 'tt'
    might be valid, but not 'ttt').
    """
    chain = defaultdict(lambda: defaultdict(int))
    for name in names:
        chain['length'][len(name)] += 1
        complete_group = None
        current_group = START_TOKEN
        count = 1
        for c in name:
            # If c is the same as the current group, extend it
            if c == current_group:
                count += 1
            else:
                # If c is different, end the current group, set its probability,
                # and make c the new current group.
                if complete_group is not None:
                    chain[complete_group][current_group * count] += 1
                complete_group = current_group * count
                current_group = c
                count = 1
        # Whatever we had left over is the final group
        chain[complete_group][current_group * count] += 1
    return chain

def normalize_chain(chain):
    """Given a chain with the same format as those output by make_chain,
    normalize the dict so that for a given first_token, the value of each
    second_token sums to 1 while preserving the proportions.
    """
    for pre, post in chain.items():
        total = sum(post.values())
        for k in post.keys():
            post[k] = post[k]*1.0/total

def generate_name(chain):
    """Generate a random name by walking the markov chain."""
    name = []
    old_token = START_TOKEN
    name_len = weighted_choice(chain['length'])
    for i in range(name_len):
        post = chain[old_token]
        token = weighted_choice(post)
        if token is None:
            # None means our token had no following tokens in the sample set
            break
        name.append(token)
        old_token = token
    name[0] = name[0].upper()
    return ''.join(name)

def weighted_choice(prob_dict):
    """Given a dictionary where the values are floats that sum to 1, choose
    a key randomly, weighted by the values.
    """
    index = random.random()
    curr = 0
    for k, prob in prob_dict.items():
        curr += prob
        if curr >= index:
            return k

if __name__ == '__main__':
    name_list, count = process_args()
    names = read_names(name_list)
    chain = make_chain(names)
    normalize_chain(chain)
    for i in range(count):
        print(generate_name(chain))
