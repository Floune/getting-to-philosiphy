import requests
from bs4 import BeautifulSoup
import sys
import json

visited = []

def findLink(liens):
	zob = open("exclude.txt", "r+")
	zoblines = zob.readlines()
	zob.close();
	nopes = []
	for line in zoblines:
		nopes.append(line.strip())

	for lien in liens:
		if not lien in visited and not lien in nopes and lien[0] != '#':
			return lien

	return None

def findTags(tags):
	links = []
	for tag in tags:
		found = tag.findAll('a')

		for link in found:
			if link.has_attr('href'):
				links.append(link['href'])

	if len(links) > 0 :
		lien = findLink(links)
		print(lien[6:])
		return lien

def recursmort(adresse):
	visited.append(adresse)
	htmlEnVrac = requests.get('https://fr.wikipedia.org'+adresse).content
	soup = BeautifulSoup(htmlEnVrac, 'html.parser')
	laDiv = soup.find('div', {'class': "mw-parser-output"})
	potentialTags = laDiv.findAll(['p', 'ul'], {'class': ''}, recursive=False)
	tag = findTags(potentialTags)

	if tag == '/wiki/Philosophie':
		filsDeJ = open("data-pures/" + sys.argv[1] + ".json", "w+")
		json.dump(visited, filsDeJ)
		filsDeJ.close()
		print('On a trouvé Philo en ' + str(len(visited)) + ' coups !')
	elif tag != None:
		recursmort(tag)
	else:
		print(visited)
		print('Cest la fin apres ' + str(len(visited)))


def start():
	if len(sys.argv) <= 1:
		print('Argument missing')
		print('Exiting...')
		exit()
	value = '/wiki/' + sys.argv[1]
	recursmort(value)

start()