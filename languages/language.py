import regex as re
import hashlib
import pickle

import abc

class Language(abc.ABC):
	def __init__(self):
		self.replaceDict = {} #dict of type keyInText => replacedText.
		self.name = ""
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