#!/usr/bin/python3
import urllib.request
from lxml import etree
import rdflib
import re
import sys

if len(sys.argv) != 2:
    print("Insufficent Arguments provided")
    print("Expected Usage:")
    print(sys.argv[0] + " file.owl")
    exit()

file = sys.argv[1]
parser = etree.XMLParser(strip_cdata=False)
with open(file, "rb") as source:
    tree = etree.parse(source, parser=parser)
    root = tree.getroot()

o_graph = rdflib.Graph()
namespace_manager = rdflib.namespace.NamespaceManager(rdflib.Graph())
o_graph.namespace_manager = namespace_manager
try:
    o_graph.open("store", create=True)
    o_graph.parse(file)
except Exception as e:
    raise e

namespace_dict = {key: value for (key, value) in o_graph.namespace_manager.namespaces()}
spec_url = namespace_dict['']


def get_full_uri(uri):
    return spec_url[:-1] + uri


def printXML(root):
    rough_string = '<?xml version="1.0" encoding="UTF-8"?>\n'
    rough_string += etree.tostring(root, encoding="unicode", pretty_print=True)
    # Accounting for oddities in lxml not properly ignoring CDATA sections
    rough_string = rough_string.replace("&lt;", "<")
    rough_string = rough_string.replace("&gt;", ">")
    rough_string = rough_string.replace("<![CDATA[<a", "<a")
    rough_string = rough_string.replace("a>]]>", "a>")

    rough_string = rough_string.replace("<a href=", "<![CDATA[<a href=")
    rough_string = rough_string.replace("</a>", "</a>]]>")
    print(str(rough_string))


def get_webpage_title(url):
    title = url
    try:
        webpage = urllib.request.urlopen(url).read()
        title = str(webpage).split('<title>')[1].split('</title>')[0]
    except urllib.error.URLError:
        print("<!-- %s is currently inaccessible -->" % url)
        print("<!-- Unable to retrieve title from webpage.\n-->")
    return title


def get_definitions(element):
    for x in element:
        if str(x.tag)[-10:] == "definition":
            if x.text and "@@" in x.text:
                pattern = re.compile('@@(.*?)@@')
                matches = pattern.finditer(x.text)
                original_strings = [str(uri.group(0)) for uri in matches]

                for string in original_strings:
                    uri = string[2:-2]
                    if '#' in uri:
                        language = x.get("{http://www.w3.org/XML/1998/namespace}lang")
                        hyperlink = create_hyperlink(uri, get_label(get_full_uri(uri), language))
                    else:
                        hyperlink = create_hyperlink(uri, get_webpage_title(uri))

                    x.text = x.text.replace(string, hyperlink)


def create_hyperlink(uri, label):
    return ('<![CDATA[<a href="%s">%s</a>]]>' % (uri, label))


def get_label(uri, lang):
    query_str = """
                select distinct ?label  where {
                                OPTIONAL { <%s> rdfs:label ?label. }.
                                filter(
                                                langMatches(lang(?label), "%s")
                                )
                }
                                """ % (uri, lang)
    label = ""
    for row in o_graph.query(query_str):
        label = row.label

    return label


def find_elements():
    return [x for x in root if len(x) > 1]


def main():
    elements = find_elements()
    for element in elements:
        get_definitions(element)
    printXML(root)


if __name__ == '__main__':
    main()
