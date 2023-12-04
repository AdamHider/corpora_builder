import os
import pandas as pd
import re
 
source = "target/crh-RU_ru/crh-RU.txt"

totalChars = 0
totalWords = 0
totalSentences = 0

with open(source, encoding="utf-8") as f:
    lines = f.readlines()
    for line in lines:
        if len(line.strip()) > 0:
            totalChars += len(line.strip())
            totalWords += len(line.strip().split())
            totalSentences += 1
f.close()


print(f"Total sentences: {totalSentences}")
print(f"Total words: {totalWords}")
print(f"Total chars: {totalChars}")

