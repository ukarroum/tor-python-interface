""""
 * ************* Interface Tor Python ***************
 *
 * Ecrit par Yassir Karroum [ukarroum17@gmail.com] [https://github.com/ukarroum]
 * Le 30 juillet 2016
 *
 * Un simple script qui permet d'utiliser tor facilement avec python.
 * Il propose plusieurs fonctions :

        - init_tor : Permet d'initialiser tor en le lancant.
        - kill_tor : Met fin au processus de TOR.
        - get_html : Récupere le code HTML d'une page passé en parametre en passant par TOR
        - new_identity : Permet de modifier votre adresse ip (en fait le changement de circuit ne change pas foércément
                        l'ip mais le nombre des noeuds de sorties est trés grand donc celà change généralement votre ip)
        - get_ip   : Récupere votre ip.

    Le script nécéssite plusieurs dépendances : Stem, PYCurl et tor.
    Ils peuvent etre installés via ces 3 commandes (sous debian et dérivés) :

    # pip3 install stem
    # apt-get install python3-pycurl
    # apt-get install tor

 */
"""

import stem.process
from stem.util import term
import pycurl
import io
import re

SOCKS_PORT = 7000

tor_process = 0
use_tor = False   # Si tor est utilisé le parametre devient true

# En choisissant de passer par les relais d'un meme pays
# Les résultats deviennent plus cogérents entre eux.

use_contry_code = False
country_code = "fr"  # Un choix arbitraire qui est du à un nombre plutot elevé des relais francais.


def init_tor():

    global tor_process

    if use_contry_code:
        tor_process = stem.process.launch_tor_with_config(
            config={
                'SocksPort': str(SOCKS_PORT),
                'ExitNodes': '{' + country_code + '}'
            }
        )
    else:
        tor_process = stem.process.launch_tor_with_config(
            config={
                'SocksPort': str(SOCKS_PORT)
            }
        )

    global use_tor
    use_tor = True


def kill_tor():

    tor_process.kill()


def get_html(url):
    """
    Uses pycurl to fetch a site using the proxy on the SOCKS_PORT.
    """

    output = io.BytesIO()

    query = pycurl.Curl()
    query.setopt(pycurl.URL, url)

    if use_tor:
        query.setopt(pycurl.PROXY, 'localhost')
        query.setopt(pycurl.PROXYPORT, SOCKS_PORT)
        query.setopt(pycurl.PROXYTYPE, pycurl.PROXYTYPE_SOCKS5_HOSTNAME)

    query.setopt(pycurl.USERAGENT, 'Mozilla/5.0 (X11; Linux x86_64; rv:45.0) Gecko/20100101 Firefox/45.0')
    query.setopt(pycurl.WRITEFUNCTION, output.write)

    try:
        query.perform()
        return output.getvalue()
    except pycurl.error as exc:
        return "Unable to reach %s (%s)" % (url, exc)


def new_identity():
    if use_tor:
        print(term.format("Nouvelle identite : "+get_ip()+"\n", term.Color.BLUE))
        kill_tor()
        init_tor()
    else:
        print(term.format("Lancement de Tor.\n", term.Attr.BOLD))
        init_tor()


def get_ip():

    html = get_html("https://check.torproject.org/")
    pattern = re.compile("[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}")
    return pattern.search(str(html)).group(0)
