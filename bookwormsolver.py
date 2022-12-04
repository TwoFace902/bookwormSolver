import json
import pygetwindow
from PIL import ImageGrab
from PIL import ImageFilter
from PIL import Image
import numpy
import cv2
import time
import imgModel

base = "dictionaryoutput\word"
alpha = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']

def countl(word):
	mapper = {letter:0 for letter in alpha}
	for letter in word:
		mapper[letter] = mapper[letter] + 1
	return mapper

def mapCompare(listmap, wordmap):
	outList = []
	for cword in listmap:
		valid = True
		for letter in alpha:
			if(listmap[cword][letter] > wordmap[letter]):
				valid = False
				break
		if (valid == True and qucheck(cword) == False):
			outList.append(cword)
	return outList

def qucheck(word):
	index = word.find('q')
	if index == -1 or index == len(word)-1:
		return False
	if word[index+1] == 'u':
		return False
	return True

def editImage(old):
	fn = lambda x : 255 if x > 10 else 0
	new = old.resize((1000,1000))
	new = new.convert('L').point(fn, mode='1')
	return new

def getCurrentLetters(letterModel):
	curstr = ''
	sneed = pygetwindow.getWindowsWithTitle('Bookworm Adventures Deluxe 1.0')[0]
	for i in range(0,200,50):
		for j in range(0,200,50):
			left = sneed.left+305+i
			right = sneed.left+355+i
			top = sneed.top+335+j
			bottom = sneed.top+385+j
			letter = ImageGrab.grab(bbox=(left,top,right,bottom))
			letter = editImage(letter)
			cur = imgModel.modelResultToLetter(letterModel(imgModel.pilImageToTensor(letter)))
			if cur[0] == 'Q':
				curstr += 'QU'
			else:
				curstr += cur[0]
	return curstr.lower()

if __name__=='__main__':
	letterModel = imgModel.buildModel()
	letterModel.load_weights("weights/gputraining")

	lenmap = {number+1:{} for number in range(16)}
	for i in range(16):
		file = base+str(i+1)+".json"
		f = open(file,'r')
		lenmap[i+1] = json.load(f)
		f.close()
	while(1):
		userinput = getCurrentLetters(letterModel)
		print("Assumed Input: ", userinput)
		userMap = countl(userinput)
		for i in range(16,0,-1):
			curList = mapCompare(lenmap[i],userMap)
			if len(curList) > 0:
				print(curList)
				break
		time.sleep(2)
