import requests
from bs4 import BeautifulSoup
import sys
import json
from flask import jsonify

def findLink(liens, visited):
	zob = open("app/exclude.txt", "r+")
	zoblines = zob.readlines()
	zob.close();
	nopes = []
	for line in zoblines:
		nopes.append(line.strip())

	for lien in liens:
		print(lien)
		if not lien in visited and not lien in nopes and lien[0] != '#' and not "/wiki/Aide" in lien and not "/wiki/API_" in lien:
			return lien

	return None

def findTags(tags, visited):
	links = []
	for tag in tags:
		found = tag.findAll('a')

		for link in found:
			if link.has_attr('href'):
				links.append(link['href'])

	if len(links) > 0 :
		lien = findLink(links, visited)
		print(lien[6:])
		return lien

def saveSuccess(visited):
	file = open('data-pures/results.json', 'r+')
	stored = file.read()
	storedJson = json.loads(stored)
	storedJson['words'].append({search : visited})
	current = json.dumps(storedJson)
	file.seek(0)
	file.write(current)
	file.truncate()
	file.close()

def recursmort(adresse, visited):
	visited.append(adresse)
	htmlEnVrac = requests.get('https://fr.wikipedia.org'+adresse).content
	soup = BeautifulSoup(htmlEnVrac, 'html.parser')
	laDiv = soup.find('div', {'class': "mw-parser-output"})
	potentialTags = laDiv.findAll(['p', 'ul'], {'class': ''}, recursive=False)
	tag = findTags(potentialTags, visited)

	if tag == '/wiki/Philosophie':
		saveSuccess(visited)
		print('On a trouvé Philo en ' + str(len(visited)) + ' coups !')
	elif tag != None:
		recursmort(tag, visited)
	else:
		print('Cest la fin apres ' + str(len(visited)))


def start(word):
	if testWord(word) == 1: return ["entrée inexistante"]
	visited = []
	global search
	search = word
	value = '/wiki/' + word
	response = recursmort(value, visited)
	return visited

def testWord(word):
	adress = 'https://fr.wikipedia.org/wiki/' + word
	htmlEnVrac = requests.get(adress).content
	soup = BeautifulSoup(htmlEnVrac, 'html.parser')
	notFound = soup.body.findAll(text="Wikipédia ne possède pas d'article avec ce nom.")
	return len(notFound)
