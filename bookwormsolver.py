import json
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

if __name__=='__main__':
	lenmap = {number+1:{} for number in range(16)}
	for i in range(16):
		file = base+str(i+1)+".json"
		f = open(file,'r')
		lenmap[i+1] = json.load(f)
		f.close()
	userinput = ""
	while(userinput != '-1'):
		print("Input: ", end='')
		userinput = input()
		userMap = countl(userinput)
		for i in range(16,0,-1):
			curList = mapCompare(lenmap[i],userMap)
			if len(curList) > 0:
				print(curList)
				break