import requests
from bs4 import BeautifulSoup
import sys
import urllib.parse
import json

exclude = ['/wiki/Alphabet_phon%C3%A9tique_international', '/wiki/Aide:Homonymie']
visited = []
search = None

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
		print('Lien suivant:', clean(lien))
		return lien


def recursmort(adresse):
	visited.append(clean(adresse))
	htmlEnVrac = requests.get('https://fr.wikipedia.org'+adresse).content
	soup = BeautifulSoup(htmlEnVrac, 'html.parser')
	laDiv = soup.find('div', {'class': "mw-parser-output"})
	potentialTags = laDiv.findAll(['p', 'li'], {'class': ''}, recursive=False)
	tag = findTags(potentialTags)

	if tag == '/wiki/Philosophie':
		print('On a trouvé Philo en ' + str(len(visited)) + ' coups !')
		saveSuccess()
	elif tag != None:
		recursmort(tag)
	else:
		print(visited)
		print('Cest la fin apres ' + str(len(visited)))
		saveDeadend()


def clean(uri):
	return urllib.parse.unquote_plus(uri).replace('/wiki/', '')

def saveSuccess():
	file = open('results.json', 'r+')
	stored = file.read()
	print(stored)
	storedJson = json.loads(stored)
	storedJson['words'].append({search : visited})
	current = json.dumps(storedJson)
	file.seek(0)
	file.write(current)
	file.truncate()
	file.close()

def saveDeadend():
	print('woops')

def cli():
	global search
	search = sys.argv[1]
	recursmort('/wiki/' + urllib.parse.quote(search))

cli()