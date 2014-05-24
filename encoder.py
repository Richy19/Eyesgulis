#!/usr/bin/env python3
import hashlib
import sys

input_str = input("Message to encode: ")
key_str = input("Key for message: ")

input_str = input_str.replace('\r', ' ').replace('\n', ' ')
key_str = key_str.replace('\r',  ' ').replace('\n', ' ')
#print(input_str)
new_msg = [input_str[i:i+2] for i in range(0, len(input_str), 2)]
#print(new_msg)
encoded_msg = []

for x in new_msg:
	if len(x) == 1:
		x = x + ' '
	sha1 = hashlib.sha1()
	sha1.update(x.encode() + key_str.encode())
	encoded_msg.append(sha1.hexdigest()[20:])
	encoded_msg.append(sha1.hexdigest()[:20])
print(' '.join(encoded_msg))
