#!/usr/bin/env python3
import hashlib
import random
import sys
import binascii

def encode(msg, key, hashsys='sha1', verbose=False, mutate=False):
	try:
		hash = hashlib.new(str(hashsys))
	except ValueError:
		print("Error: hash {h} is not supported, defaulting to sha1".format(h=hashsys))
		hashsys='sha1'

	msg = msg.replace('\r', "").replace('\n', '')
	key = key.replace('\r', "").replace('\n', '')
	encoded_msg = []
	mutation_key = []
	for x in ([msg[i:i+2] for i in range(0, len(msg), 2)]):
		if len(x) == 1:
			x = x + ' '
		if mutate:
			random_bit = chr(int(random.randrange(127, 3500)))
			random_bit_en = binascii.hexlify(random_bit.encode()).decode()
		else:
			random_bit = ''
			random_bit_en = ''
		hash = hashlib.new(str(hashsys))
		if verbose:
			print("Message to be hashed is", x, random_bit, key)
		#if len(random_bit_en) < 5:
		#	random_bit_en += '00'
		hash.update(x.encode()+random_bit.encode()+key.encode())
		encoded_msg.append(hash.hexdigest()[int(len(hash.hexdigest())/2):])
		encoded_msg.append(hash.hexdigest()[:int(len(hash.hexdigest())/2)])
		mutation_key.append(random_bit_en)
	
	return encoded_msg, mutation_key

if __name__ == '__main__':
	import argparse

	parser = argparse.ArgumentParser(description='Encodes text using A04.')
	parser.add_argument('-m', '--msg', help='message to encode', metavar='MSG', nargs='+')
	parser.add_argument('-k', '--key', help='secret key for encoding', metavar='KEY', nargs='+')
	parser.add_argument('-H', '--hash', default='sha1', choices=hashlib.algorithms_available, help='the hashing mechanism (default: %(default)s)', metavar='MECHANISM')
	parser.add_argument('-v', '--verbose', action='store_true', default=False, help='ask for additional output (default: do not)')
	parser.add_argument('-M', '--mutate', action='store_true', default=False, help='Mutate the message each run')

	args = parser.parse_args()

	if args.msg is None:
		args.msg = input('Message to encode: ')
	else:
		args.msg = ' '.join(args.msg)
	if args.key is None:
		args.key = input('Key for message: ')
	else:
		args.key = ' '.join(args.key)
	
	encoded = encode(args.msg, args.key, args.hash, args.verbose, args.mutate)
	
	print('\nEncoded message:', ' '.join(encoded[0]))
	if encoded[1] != []:
		print('Mutation key:', ':'.join(encoded[1]))
