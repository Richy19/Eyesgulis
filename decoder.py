#!/usr/bin/env python3
# A04 decoder logic by Eyes, inspired by Monocle
import sys
import hashlib

def decode(msg, key):
	ascii = "qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM',.?!@/ "
	msg = msg.replace('\r', ' ')
	msg = msg.replace('\n', ' ')
	msg = msg.replace('  ', ' ')
	new_msg = msg.split(' ')
	strlen = len(new_msg)
	swap = True
	decoded = ""

	for x in new_msg:
		print("Decoding message part", x)
		found = False
		for i in ascii:
			for a in ascii:
				sha1 = hashlib.sha1()
				sha1.update(i.encode() + a.encode() + key.encode())
				if swap:
					if sha1.hexdigest()[:20] == x:
						print("Unswapped\t", sha1.hexdigest(), i, a)
						decoded = decoded+i+a
						swap = False
						found = True
						break
				else:
					if sha1.hexdigest()[20:] == x:
						print("Swapped\t", sha1.hexdigest(), i, a)
						decoded = decoded+i+a
						swap = True
						found = True
						break
		if not found:
			#print(i, a, decoded)
			decoded = i + a + decoded
	for i in ascii:
		decoded = decoded.replace(i+i, i)
	decoded = decoded.replace("/", "")
	return decoded

if __name__ == "__main__":
	msg = input("Message to decode: ")
	#msg = open('./f').read()
	key = input("Key for message: ")
	print("Decoded output:", decode(msg, key))		
