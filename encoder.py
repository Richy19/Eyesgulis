#!/usr/bin/env python3
import hashlib
import sys

def encode(msg, key, hashsys='sha1'):
	try:
		hash = hashlib.new(str(hashsys))
	except ValueError:
		print("Error: hash {h} is not supported, defaulting to sha1".format(h=hashsys))
		hashsys='sha1'

	msg = msg.replace('\r', "").replace('\n', '')
	key = key.replace('\r', "").replace('\n', '')
	encoded_msg = []
	for x in ([msg[i:i+2] for i in range(0, len(msg), 2)]):
		if len(x) == 1:
			x = x + ' '
		hash = hashlib.new(str(hashsys))
		hash.update(x.encode()+key.encode())
		encoded_msg.append(hash.hexdigest()[int(len(hash.hexdigest())/2):])
		encoded_msg.append(hash.hexdigest()[:int(len(hash.hexdigest())/2)])
	return encoded_msg

if __name__ == '__main__':
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
				print("Error: hash {h} does not exist, using sha1".format(h=arg[7:]))

	if msg is None:
		msg = input("Message to encode: ")
	if key is None:
		key = input("Key for message: ")

	print("\nEncoded message:", ' '.join(encode(msg, key, hashsys)))
