# filename: extract_keywords.py
import re

sentence = "The quick brown fox jumps over the lazy dog."
# 정규 표현식을 사용하여 단어를 추출하고 소문자로 변환
words = re.findall(r'\b\w+\b', sentence.lower())
# 고유한 단어를 추출
unique_keywords = set(words)
print(unique_keywords)