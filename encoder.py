#!/usr/bin/env python3
import hashlib
import sys

input_str = input("Message to encode: ")
key_str = input("Key for message: ")

new_msg = [input_str[i:i+2] for i in range(0, len(input_str), 2)]
encoded_msg = []

for x in new_msg:
	sha1 = hashlib.sha1()
	sha1.update(x.encode() + key_str.encode())
	encoded_msg.append(sha1.hexdigest()[20:])
	encoded_msg.append(sha1.hexdigest()[:20])
print(' '.join(encoded_msg))
