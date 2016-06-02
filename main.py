#!/usr/bin/env python

import argparse
import re
import unicodedata

cmd_parser = argparse.ArgumentParser(description="Parse ofx files from Banco do Brasil to simplify description")
cmd_parser.add_argument("input", help="Input file")
cmd_parser.add_argument("output", help="Output file")
args = cmd_parser.parse_args()

payment_regex = ".*:\d*\s*(.*)"
transfer_regex = ".*/\d{2}\s*(\d*\s*\d*-\d?.*)"
withdraw_regex = ".*(Saque).*"

xml_entry = "<MEMO>%s</MEMO>"
space_regex = re.compile("\s+")

cleanup_patterns = [re.compile(xml_entry % p) for p in (payment_regex, transfer_regex, withdraw_regex)]

print "Reading file"
with open(args.input, 'r') as myfile:
	original_data=unicodedata.normalize('NFD',
		myfile.read().decode('iso-8859-1')).encode('ascii', 'ignore')

def replace(match):
	memo = match.group(0)
	for pattern in cleanup_patterns:
		match_result = pattern.match(memo)
		if match_result:
			clear_space = re.subn(space_regex, " ", match_result.group(1))[0]
			return xml_entry % clear_space
	print "Unrecognized pattern", memo
	return memo

processed_data = re.subn(xml_entry % ".*", replace, original_data)[0]

print "Writing file"
with open(args.output, 'w') as myfile:
	myfile.write(processed_data)
