import argparse
import sys, os
sys.path.insert(0, os.path.realpath('languages'))

from language import Language
from language_latex import LanguageLaTeX

languages = [LanguageLaTeX()]

def run(action, inputF, outputF, encodingF, language, html):
	for lan in languages:
		if lan.name == language:
			language = lan
			language.html = html
			break

	with open(inputF, 'r') as f:
		inputText = f.read()

	if action == 'encode':
		outputText = language.encode(inputText)
		language.saveReplaceDict(encodingF)
	elif action == 'decode':
		language.loadReplaceDict(encodingF)
		outputText = language.decode(inputText)

	with open(outputF, 'w') as f:
		f.write(outputText)

if __name__ == "__main__": #if this is the main file, parse the command args
	parser = argparse.ArgumentParser(description="Tool that encodes a LaTeX file for automatic translation and then decodes the result back into a LaTeX file.")
	parser.add_argument('action', choices=['encode', 'decode'], help="Encodes the given file to a text file, ready for translation. Or decodes a translated text file back.")
	parser.add_argument('inputF', help="The input file for the action.")
	parser.add_argument('outputF', help="The output file for the action. If using Google Translate, this must be a .txt file!")
	parser.add_argument('encodingF', help="An additional file, needed for the encoding and encoding operations. An encoded file cannot be decoded without the original encoding file!")
	parser.add_argument('--language', default='latex', choices=[lan.name for lan in languages], help='A styling language to be translated. Not to be confused with human languages, this is different.')
	parser.add_argument('--html', dest='html', action="store_true", help="Saves/Treats the encoded file as an html.")
	parser.set_defaults(html=False)

	args, _ = parser.parse_known_args()

	run(args.action, args.inputF, args.outputF, args.encodingF, args.language, args.html)
