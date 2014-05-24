#!/usr/bin/env python3
# A04 decoder logic by Eyes, inspired by Monocle
import sys
import hashlib

def decode(msg, key, hashsys):
	ascii = "qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM',.?!@/ "
	msg = msg.replace('\r', ' ')
	msg = msg.replace('\n', ' ')
	msg = msg.replace('  ', ' ')
	new_msg = msg.split(' ')
	strlen = len(new_msg)
	swap = True
	decoded = ""

	for n, x in enumerate(new_msg):
		print("Decoding message part {x} [{n1}/{n2}]".format(x=x, n1=n+1, n2=len(new_msg)))
		part_decoded = False
		aa = None
		ii = None
		if n != 0 and n % 2 != 0:
			full_hash = new_msg[n] + new_msg[n-1]
			for a in ascii:
				for i in ascii:
					hash = hashlib.new(hashsys)
					hash.update(a.encode() + i.encode() + key.encode())
					if hash.hexdigest() == full_hash:
						decoded += a + i
						aa = a
						ii = i
						part_decoded = True
						break
					else:
						continue
		else:
			continue
		if part_decoded:
			print("{fh} -> {a}{i}".format(fh=full_hash, a=aa, i=ii))
		else:
			print("No result found for hash, are you using the right key?")
	#for i in ascii:
		#decoded = decoded.replace(i+i, i)
		
	decoded = decoded.replace("/", "")
	return decoded

if __name__ == "__main__":
	msg = None
	key = None
	hashsys = 'sha1'
	for arg in sys.argv[1:]:
		if arg.startswith('--msg='):
			msg = arg[6:]
		if arg.startswith('--key='):
			key = arg[6:]
		if arg.startswith('--hash='):
			if arg[7:] in hashlib.algorithms_available:
				hashsys = arg[7:]
			else:
				print("Error: hash {h} is not supported, defaulting to sha1".format(h=arg[7:]))

	if msg is None:
		msg = input("Message to decode: ")
	if key is None:
		key = input("Key for message: ")
	

	print("Decoded output:", decode(msg, key, hashsys))
