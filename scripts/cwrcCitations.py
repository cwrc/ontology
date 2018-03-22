#!/usr/bin/python3
import urllib.request
from bs4 import BeautifulSoup
from lxml import etree
import rdflib
import sys

# This script works by identifying BIBO nodes and their uris which correspond to a bibliographic entry on CWRC
# <bibo:Book xmlns:bibo="http://purl.org/ontology/bibo/" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#" rdf:about="#8049540f-3673-4ca0-920c-cb5326d7c466">
#   ...
# </bibo:Book>
# corresponds to this entry http://beta.cwrc.ca/islandora/object/cwrc:8049540f-3673-4ca0-920c-cb5326d7c466
# It will scrape the available citation if page available
# The structure of this page is subject to change as beta.cwrc.ca grows
# As of March 22nd 2018 it grabs text from
# <div class="csl-bib-body"><div style="  text-indent: -25px; padding-left: 25px;"><div class="csl-entry">Petersen, T. <span style="font-style: italic;" >Art & Architecture Thesaurus</span>. no date. Oxford University Press, no date.</div></div></div></div>
# Using the class="csl-bib-body" of a div

if len(sys.argv) != 2:
    print("Insufficent Arguments provided")
    print("Expected Usage:")
    print(sys.argv[0] + " file.owl")
    exit()

RDF = rdflib.Namespace("http://www.w3.org/1999/02/22-rdf-syntax-ns#")

file = sys.argv[1]
o_graph = rdflib.Graph()
namespace_manager = rdflib.namespace.NamespaceManager(rdflib.Graph())
o_graph.namespace_manager = namespace_manager
try:
    o_graph.open("store", create=True)
    o_graph.parse(file)
except Exception as e:
    raise e

# TODO: figure out why this break serialization
# It still works just reports error messages, this may be due to structuring of the bibonodes in the rdf


def etreetag_to_uri(tag):
    return rdflib.term.URIRef(str(tag)[1:].replace("}", ""))

parser = etree.XMLParser(strip_cdata=False)
with open(file, "rb") as source:
    tree = etree.parse(source, parser=parser)
    root = tree.getroot()
    types = sorted(list(set([etreetag_to_uri(x.tag) for x in root])))
    # grabbing bibo nodes
    bibo_nodes = [x for x in types if ("purl.org/ontology/bibo/" in str(x)) if "Collection" not in x]


def get_citation(url):
    citation = "http://beta.cwrc.ca/islandora/object/" + url
    try:
        page = urllib.request.urlopen(citation).read().decode('utf-8')
    except urllib.error.URLError:
        print("<!-- %s is currently inaccessible -->" % citation)
        print("<!-- Unable to retrieve citation from webpage.\n-->")
    soup = BeautifulSoup(page, 'html.parser')
    # Grabs citation from a div element looking like this --> this is subject to change with changes in cwrc
    # <div class="csl-bib-body"><div style="  text-indent: -25px; padding-left: 25px;"><div class="csl-entry">Petersen, T. <span style="font-style: italic;" >Art & Architecture Thesaurus</span>. no date. Oxford University Press, no date.</div></div></div></div>
    citation_block = soup.find("div", attrs={"class": "csl-bib-body"})
    citation = citation_block.text
    return citation


def main():
    citation_urls = []
    for x in bibo_nodes:
        citation_urls += ["cwrc:" + str(s).split("#")[1] for s, p,
                          o in o_graph.triples((None, RDF.type, x)) if "-partof" not in s]
    citation_dict = {}
    for x in citation_urls:
        citation_dict[get_citation(x)] = x

    print("<div class= 'bibliography'")
    for x in sorted(citation_dict.keys()):
        print('<p id="%s">' % citation_dict[x])
        print(x)
        link_str = "http://beta.cwrc.ca/islandora/object/" + citation_dict[x]
        print('[<a href="%s">link</a>]' % link_str)
        print("</p>")
    print("</div>")


if __name__ == '__main__':
    main()
