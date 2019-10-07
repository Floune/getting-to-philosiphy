import requests
from bs4 import BeautifulSoup
import sys

exclude = ['/wiki/Alphabet_phon%C3%A9tique_international', '/wiki/Aide:Homonymie']
visited = []
def findLink(liens):
	for lien in liens:
		if not lien in exclude and lien[0] != '#':
			exclude.append(lien)
			return lien

	return None

def findTags(tags):
	links = []
	for tag in tags:
		found = tag.findAll('a')
		for link in found:
			links.append(link['href'])
			
	if len(links) > 0 :
		lien = findLink(links)
		print('Lien suivant:', lien)
		return lien


def recursmort(adresse):
	visited.append(adresse)
	htmlEnVrac = requests.get('https://fr.wikipedia.org'+adresse).content
	soup = BeautifulSoup(htmlEnVrac, 'html.parser')
	laDiv = soup.find('div', {'class': "mw-parser-output"})
	potentialTags = laDiv.findAll(['p', 'li'], {'class': ''}, recursive=False)
	tag = findTags(potentialTags)

	if tag == '/wiki/Philosophie':
		print(visited)
		print('On a trouvé Philo en ' + str(len(visited)) + ' coups !')
	elif tag != None:
		recursmort(tag)
	else:
		print(visited)
		print('Cest la fin apres ' + str(len(visited)))



value = '/wiki/'+sys.argv[1]

recursmort(value)

