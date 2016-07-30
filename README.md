# Interface Tor Python

Un petit script qui permet de facilement utiliser tor avec python.

# Technologies Utilisés

* [Beautiful Soup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/): Une bibliothéque de scrapping qui permet de naviguer 
facilement dans une page html pour la récupération de l'ip.
* [Stem](https://stem.torproject.org/) : Une bibliotehque qui permet d'intégrer TOR à Python.
* [PyCUrl](http://pycurl.io/): Une bibliotehque pour récuperer le code HTML des pages, URLLib m'a posé pas mal de problèmes pour passer par TOR.

# Dependances

``` 
# apt-get install python3-bs4
# pip3 install stem
# apt-get install python3-pycurl
# apt-get install tor
```

# Fonctions


* **init_tor** : Permet d'initialiser tor en le lancant.
* **kill_tor** : Met fin au processus de TOR.
* **get_html** : Récupere le code HTML d'une page passé en parametre en passant par TOR
* **new_identity** : Permet de modifier votre adresse ip (en fait le changement de circuit ne change pas foércément
                        l'ip mais le nombre des noeuds de sorties est trés grand donc celà change généralement votre ip)
* **get_ip**   : Récupere votre ip.