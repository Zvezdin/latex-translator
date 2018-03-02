from language import Language

import regex as re

#encodeDict = {'{': 'BACKSLASHSH', '\\': '==zz', '%': '14853644785'}


class LanguageLaTeX(Language):
	def __init__(self):
		super().__init__()

		self.name = "latex"
		#used to match any latex command, optionally with a body {} and/or arguments []. Also works with nested commands.
		#note - this also includes \textbf, \caption and similar, which means that currently there is no translation for them. This will change in the future.
		#note2 - may cause issies with commands like \$\[\]
		self.command = r'(?s)(\\[^0-9[\]{}\\ ]+)+(({([^{}]|(?2))*})|(\[.*?\]))*'
		#matches latex quotes
		self.Lquote = r"``"
		self.Rquote = r"''"
		#used to match environment pairs. Also works with nested environments.
		self.environment = r'(?s)\\begin{(?P<env>.*?)}(.|(?R))*?\\end{(?P=env)}'
		#used to match math commands. Works with math environments like '$x=3$', '$$x=3$$' and ignores the command '\$'
		self.math = r'(?<=[^\\])\$(\$)?[^\$]*?\$(?(1)\$)'
		#used to match latex comment, which begins with one or more '%' and ends in a newline.
		self.comment = r'(?<=[^\\])(?m)%.*?$'
		#TODO what about quotes line ``hey''?
		#TODO special environments like document, abstract or enumerate, itemize?
		self.specialEnvironments = [r'document', r'abstract', r'enumerate', r'itemize', r'frame', r'column', r'columns', r'alertblock', r'block']

	def encode(self, text):
		#comments
		if self.html:
			text = '<!DOCTYPE html>\n' + text #make it sound like this is html

		#comments
		text = self.replaceAllRegex(self.comment, text, self.hashText)
		#quotes
		text = self.replaceAllRegex(self.Lquote, text, self.hashText)
		text = self.replaceAllRegex(self.Rquote, text, self.hashText)

		#abstract, begin and enumerate special environments
		for env in self.specialEnvironments:
			name = ''
			for char in env:
				name += '['+char+']'
			try:
				text = self.replaceAllRegex(r'\\begin{'+name+'}', text, self.hashText)
				text = self.replaceAllRegex(r'\\end{'+name+'}', text, self.hashText)
			except:
				print("Error replacing environment %s" %env)
				continue #if env is not in text

		#other environments
		text = self.replaceAllRegex(self.environment, text, self.hashText)

		#math
		text = self.replaceAllRegex(self.math, text, self.hashText)

		#commands
		text = self.replaceAllRegex(self.command, text, self.hashText)

		if self.html:
			text = text.replace('\n', '<br>')
			#text = text+'\n</pre>'

		return text

	def decode(self, text):
		keys = list(self.replaceDict.keys())

		missingDict = self.replaceDict.copy() # the presence of a key in this dict will mean that
		#the key was not able to be replaced and is therefore missing

		while True:
			replacedSomething = False #if we have replaced something, make sure to also iterate all of our lastly missing keys
			#to see if they are found in the newly replaced text
			for key in keys:
				if key.lower() in text:
					replaceWith = self.replaceDict[key].replace('\\', '\\\\') #replace a single '\' char to two. Regex breaks otherwise.
					text = self.replaceAllRegexText('(?i)' + key, text, replaceWith)

					replacedSomething = True
				else:
					missingDict.pop(key, None)
			if not replacedSomething:
				break

		for key in self.htmlWrapper: #clear any left HTML tags
			text = self.replaceAllRegexText('(?i)' + key, text, '')

		for key in missingDict:
			print("Error- key not in text!", key)
			print("You'll have to replace it yourself")
			print(self.replaceDict[key])
		return text
