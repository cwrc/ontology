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
# As of March 23nd 2018 it grabs the div element from
# <div class="csl-entry">Petersen, T. <span style="font-style: italic;" >Art & Architecture Thesaurus</span>. no date. Oxford University Press, no date.</div>
# Using the class="csl-entry" of a div

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


def etreetag_to_uri(tag):
    return rdflib.term.URIRef(tag[1:].replace("}", ""))

parser = etree.XMLParser(strip_cdata=False)
with open(file, "rb") as source:
    tree = etree.parse(source, parser=parser)
    root = tree.getroot()
    types = sorted(list(set([str(x.tag) for x in root])))
    # grabbing bibo nodes
    bibo_nodes = [etreetag_to_uri(x) for x in types if (
        "purl.org/ontology/bibo/" in str(x)) if "Collection" not in x]


def get_citation(url):
    citation = "https://cwrc.ca/islandora/object/" + url
    try:
        page = urllib.request.urlopen(citation).read().decode('utf-8')
        soup = BeautifulSoup(page, 'html.parser')
        # Grabs citation from a div element looking like this --> this is subject to change with changes in cwrc
        # <div class="csl-entry">Petersen, T. <span style="font-style: italic;" >Art & Architecture Thesaurus</span>. no date. Oxford University Press, no date.</div>
        citation = soup.find("div", attrs={"class": "csl-entry"})
        return citation
    except urllib.error.URLError:
        print("<!-- %s is currently inaccessible -->" % citation)
        print("<!-- Unable to retrieve citation from webpage.\n-->")
    return None


def main():
    citation_urls = []
    for x in bibo_nodes:
        citation_urls += ["cwrc:" + str(s).split("#")[1] for s, p,
                          o in o_graph.triples((None, RDF.type, x)) if "-partof" not in s]
    citation_dict = {}
    # print(citation_urls)
    for x in citation_urls:
        citation_element = get_citation(x)
        if citation_element:
            citation_dict[citation_element.text] = [x, citation_element]

    print('<div class= "bibliography">')
    soup = BeautifulSoup("", 'html.parser')
    for x in sorted(citation_dict.keys()):
        print('<div class="citation" id="%s">' % citation_dict[x][0])
        link_str = "https://cwrc.ca/islandora/object/" + citation_dict[x][0]
        new_tag = soup.new_tag("a", href=link_str)
        new_tag.string = "link"
        citation_dict[x][1].append(' [')
        citation_dict[x][1].append(new_tag)
        citation_dict[x][1].append(']')
        print(citation_dict[x][1])
        print("</div>")
    print("</div>")


if __name__ == '__main__':
    main()
