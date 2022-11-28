import json

def countl(word):
	alpha = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
	mapper = {letter:0 for letter in alpha}
	for letter in word:
		mapper[letter] = mapper[letter] + 1
	return mapper




if __name__=='__main__':
	filetag = open("output_uncompressed.txt")
	wordlist= filetag.read().splitlines()
	lenmap = {number+1:{} for number in range(16)}
	for word in wordlist:
		wlen = len(word)
		for i in range(16):
			if(wlen == i+1):
				lenmap[i+1][word] = countl(word)
	for i in range(16):
		print(i+1)
		file = "word"+str(i+1)+".json"
		f = open(file,'w')
		json.dump(lenmap[i+1],f)
		f.close()