generate_names
==============

Markov name generator.

Outputs a list of names (by default, 25; change with the --count flag) based
on an input plain text file with a list of sample names, one per line.  By
default, looks for the list in a name_list file in the same directory, but
accepts an alternate location via the --path flag.

Written for python 3, but tested in python 2.7.5 and it worked (though I make
no promises).

The sample name_list that comes with the repo is a list of names for Legend of
The First City, a _Legend_ campaign setting by NPC; the names themselves were
created by Ether for the campaign.
