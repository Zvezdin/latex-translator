import regex as re
import hashlib
import pickle

import abc

class Language(abc.ABC):
	def __init__(self):
		self.replaceDict = {} #dict of type keyInText => replacedText.
		self.name = ""
		self.html = False #causes the translation to be formatted as and saved as an html document.
		self.htmlWrapper = [r"<span class='notranslate'>", r"</span>"] #html, in which replace hashes will be wrapped
		#this is needed for google translate, as otherwise there is no way to tell google to ignore our keys.
		pass

	@abc.abstractmethod
	def encode(self, text):
		pass

	@abc.abstractmethod
	def decode(self, text):
		pass

	def searchRegex(self, regex, text):
		return re.search(regex, text)

	def replaceFirstRegex(self, regex, text, replaceFunction):
		pass

	def replaceAllRegex(self, regex, text, replaceFunction):
		def replaceWrapper(match):
			matchText = match.group(0) #the text of the single match
			print("Found matching text %s" % matchText)
			key = replaceFunction(matchText) #the encoded key of it

			print("The key of it is %s" % key)
			self.replaceDict[key] = matchText #save what we replaced and the key we replaced it with

			if self.html:
				return self.htmlWrapper[0] + key + self.htmlWrapper[1] #tag so google translate ignores this key
			return key
		
		return re.sub(regex, replaceWrapper, text)

	def replaceAllRegexText(self, regex, text, replaceWith):
		return re.sub(regex, replaceWith, text)

	def saveReplaceDict(self, file):
		with open(file, 'wb') as f:
			pickle.dump(self.replaceDict, f, pickle.HIGHEST_PROTOCOL)

	def loadReplaceDict(self, file):
		with open(file, 'rb') as f:
			self.replaceDict = pickle.load(f)

	def hashText(self, text):
		return hashlib.sha512(text.encode('utf-8')).hexdigest()