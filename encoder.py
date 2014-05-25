#!/usr/bin/env python3
import hashlib
import sys

def encode(msg, key, hashsys='sha1', verbose=False):
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
	import argparse

	parser = argparse.ArgumentParser(description='Encodes text using A04.')
	parser.add_argument('--msg', help='message to encode', metavar='MSG')
	parser.add_argument('--key', help='secret key for encoding', metavar='KEY')
	parser.add_argument('--hash', default='sha1', choices=hashlib.algorithms_available, help='the hashing mechanism (default: %(default)s)', metavar='MECHANISM')
	parser.add_argument('-v', '--verbose', action='store_true', default=False, help='ask for additional output (default: do not)')

	args = parser.parse_args()

	if args.msg is None:
		args.msg = input('Message to encode: ')
	if args.key is None:
		args.key = input('Key for message: ')

	print('\nEncoded message:', ' '.join(encode(args.msg, args.key, args.hash, args.verbose)))
