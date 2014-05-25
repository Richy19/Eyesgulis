#!/usr/bin/env python3
# A04 decoder logic by Eyes, inspired by Monocle
# -*- coding: utf-8 -*-
import sys
import hashlib
import binascii

def decode(msg, key, hashsys='sha1', verbose=False, very_verbose=False):
	ascii = "qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM',.?!@/ '~[]{}-_=+<>|$%^&*():;`\""
	msg = msg.replace('\r', ' ')
	msg = msg.replace('\n', ' ')
	msg = msg.replace('  ', ' ')
	key = key.replace('\r', '').replace('\n', '')
	new_msg = msg.split(' ')
	strlen = len(new_msg)
	swap = True
	decoded = ""

	try:
		hash = hashlib.new(str(hashsys))
	except ValueError:
		print("Error: hash {h} is not supported, defaulting to sha1".format(h=hashsys))
		hashsys = 'sha1'

	for n, x in enumerate(new_msg):
		if verbose or very_verbose:
			print("Decoding message part {x} [{n1}/{n2}]".format(x=x, n1=n+1, n2=len(new_msg)))
		part_decoded = False
		aa = None
		ii = None
		if n != 0 and n % 2 != 0:
			if ':' in new_msg[n-1]:
				sp = new_msg[n-1].split(':')
				new_msg[n-1] = sp[0]
				random_bit = sp[1]
			else:
				random_bit = ''
			full_hash = new_msg[n] + new_msg[n-1]
			for a in ascii:
				for i in ascii:
					hash = hashlib.new(str(hashsys))
					if random_bit == '':
						hash.update(a.encode() + i.encode() + key.encode())
					else:
						rndbit = binascii.unhexlify(random_bit.encode('utf-8'))
						hash.update(a.encode() + i.encode() + rndbit + key.encode())
					if hash.hexdigest() == full_hash:
						if very_verbose:
							print("{fh} == {h}, decoded".format(fh=full_hash, h=hash.hexdigest()))
						decoded += a + i
						aa = a
						ii = i
						part_decoded = True
						break
					else:
						if very_verbose:
							print("{fh} != {h}, continuing".format(fh=full_hash, h=hash.hexdigest()))
						continue
		else:
			continue
		if part_decoded:
			if verbose:
				print("{fh} -> {a}{i}".format(fh=full_hash, a=aa, i=ii))
		else:
			print("No result found for hash, are you using the right key?")
	#for i in ascii:
		#decoded = decoded.replace(i+i, i)
		
	decoded = decoded.replace("/", "")
	return decoded

if __name__ == "__main__":
	import argparse

	parser = argparse.ArgumentParser(description='Decodes text using A04.')
	parser.add_argument('--msg', help='message to decode', metavar='MSG', nargs='+')
	parser.add_argument('--key', help='secret key for decoding', metavar='KEY', nargs='+')
	parser.add_argument('--hash', default='sha1', choices=hashlib.algorithms_available, help='the hashing mechanism (default: %(default)s)', metavar='MECHANISM')
	parser.add_argument('-v', '--verbose', action='store_true', default=False, help='ask for additional output (default: do not)')
	parser.add_argument('-V', '--very_verbose', action='store_true', default=False, help='even more verbose output')

	args = parser.parse_args()

	if args.msg is None:
		args.msg = input('Message to decode: ')
	else:
		args.msg = ' '.join(args.msg)
	if args.key is None:
		args.key = input('Key for message: ')
	else:
		args.key = ' '.join(args.msg)
	print('Decoding...')
	print('Decoded message:', decode(args.msg, args.key, args.hash, args.verbose, args.very_verbose))
