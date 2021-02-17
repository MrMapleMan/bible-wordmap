import os
import subprocess
import re
from operator import itemgetter
from collections import Counter
import time

fa = re.findall

# Get last column if needed
if os.path.exists('verses-only.txt'):
  print "Found verses-only.txt. Continuing..."
else:
  print "Did not find verses-only.txt. Creating it."
  subprocess.call("awk -F'\t' print( '$6' ) bible.csv > verses-only.txt", shell=True)

# Read verses-only
with open('verses-only.txt') as f:
  verses = f.read().lower()

print "\n{:16}{:>12,}".format("Verses read:",len(fa('\n',verses)))
print "{:16}{:>12,}".format("Characters read:",len(verses))
allWords = fa('\\b[a-zA-Z-_]+\\b',verses)
print "{:16}{:>12,}".format("Words read:",len(allWords))
uniqueWords = list(set(allWords))

t1_counter = time.time()
x = Counter(allWords)
t2_counter = time.time()

wordTracker = {}
t1_tracker = time.time()
for i in uniqueWords:
  wordTracker[i] = 0
for i in allWords:
  wordTracker[i] += 1
t2_tracker = time.time()
sortedWordTracker = sorted(wordTracker.iteritems(),key=lambda x: x[1],reverse=True)
print "\n{:^7} {:^6}".format("Word","Count")
print "-"*(7+1+6)
for i in sortedWordTracker[:50]:
  print "{:>7} {:>6,}".format(i[0],i[1])

print "\nMethod 1 (Counter): %f seconds\nMethod 2 (John): %f seconds" %(t2_counter-t1_counter,t2_tracker-t1_tracker)

with open('results.csv','w+') as f:
  for i in sortedWordTracker:
    f.write(i[0]+','+str(i[1])+'\n')

  # OLD METHOD
  #uniqueWordsCounts = []
  # for word in uniqueWords:
  #   x= len([j for j in allWords if j==word])
  #   uniqueWordsCounts.append(x)
  # zippedUniqueWords = zip(uniqueWords,uniqueWordsCounts)
  # print sorted(zippedUniqueWords[:100],key=itemgetter(1),reverse=True)


