#!/usr/bin/env python3
import hashlib
import sys

input_str = None
key_str = None

def encode(msg, key, hash):
	msg = msg.replace('\r', "").replace('\n', '')
	key = key.replace('\r', "").replace('\n', '')
	encoded_msg = []
	for x in ([msg[i:i+2] for i in range(0, len(input_str), 2)]):
		if len(x) == 1:
			x = x + ' '
		hash = hashlib.new(hash)
		hash.update(x.encode()+key_str.encode())
		encoded_msg.append(hash.hexdigest()[int(len(hash.hexdigest())/2):])
		encoded_msg.append(hash.hexdigest()[:int(len(hash.hexdigest())/2)])
	return encoded_msg

if __name__ == '__main__':
	hash = 'sha1'
	for arg in sys.argv[1:]:
		if arg.startswith('--msg='):
			input_str = arg[6:]
		if arg.startswith('--key='):
			key_str = arg[6:]
		if arg.startswith('--hash='):
			if arg[7:] in hashlib.algorithms_available:
				hash = arg[7:]
			else:
				print("Error: hash {h} does not exist, using sha1".format(h=arg[7:]))

	if input_str is None:
		input_str = input("Message to encode: ")
	if key_str is None:
		key_str = input("Key for message: ")
	print("\nEncoded message:", ' '.join(encode(input_str, key_str, hash)))

