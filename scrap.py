import requests
from bs4 import BeautifulSoup
import sys

visited = []

def findLink(liens):
	zob = open("exclude.txt", "r+")
	zoblines = zob.readlines()
	nopes = []
	for line in zoblines:
		nopes.append(line.strip())

	for lien in liens:
		if not lien in nopes and lien[0] != '#':
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
		print('Lien suivant:', lien)
		return lien

#mots qui plantent: Homo
def recursmort(adresse):
	visited.append(adresse)
	htmlEnVrac = requests.get('https://fr.wikipedia.org'+adresse).content
	soup = BeautifulSoup(htmlEnVrac, 'html.parser')
	laDiv = soup.find('div', {'class': "mw-parser-output"})
	potentialTags = laDiv.findAll(['p', 'ul'], {'class': ''}, recursive=False)
	tag = findTags(potentialTags)

	if tag == '/wiki/Philosophie':
		print('On a trouvé Philo en ' + str(len(visited)) + ' coups !')
	elif tag != None:
		recursmort(tag)
	else:
		print(visited)
		print('Cest la fin apres ' + str(len(visited)))



value = '/wiki/'+sys.argv[1]

recursmort(value)

