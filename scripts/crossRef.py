#!/usr/bin/python3
import urllib.request
from lxml import etree
import rdflib
import re
import sys

# Expected Usage:
# ./crossRef.py test.owl
# Will output updated rdf file with appropriate <a> in cdata tags to link to appropriate label and link
# Using @@#uri@@ and @@hyperlink@@
# Suggested usage
# ./crossRef.py test.owl > updated_test.owl

# in rdfs:comment or skos:definition
# Where @@#uri@@ used it will be replaced with appropriate
# rdfs:label hyperlinked to uri in a cdata section within that definition/comment
# ex.
"""
<skos:definition xml:lang="en">
  A personal property...For more information on this property, see @@#Gender@@.
</skos:definition>
<skos:definition xml:lang="fr">
  Une propriété personnelle...Pour plus d’information, voir @@#Gender@@.
</skos:definition>
"""
# will become this
"""
<skos:definition xml:lang="en">
  A personal property...For more information on this property, see <![CDATA[<a href="#Gender">gender</a>]]>.
</skos:definition>
<skos:definition xml:lang="fr">
  Une propriété personnelle...Pour plus d’information, voir <![CDATA[<a href="#Gender">genre</a>]]>.
</skos:definition>
"""
# Also replaces hyperlinks with title scraped from webpage
# ex.
# <skos:definition lang="en">
#   See also: @@https://en.wikipedia.org/wiki/Nonconformist@@
# </skos:definition>
# becomes
# <skos:definition lang="en">
#   See also: <![CDATA[<a href="https://en.wikipedia.org/wiki/Nonconformist">Nonconformist - Wikipedia</a>]]>
# </skos:definition>
# (Note this will increase the time it takes for script to run with many requests)


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
    rough_string += (etree.tostring(root, encoding="utf-8", pretty_print=True)).decode('utf-8')
    # rough_string += etree.tostring(root, encoding="unicode", pretty_print=True)
    # Accounting for oddities in lxml not properly ignoring CDATA sections
    rough_string = rough_string.replace("&lt;", "<")
    rough_string = rough_string.replace("&gt;", ">")
    rough_string = rough_string.replace("<![CDATA[<a", "<a")
    rough_string = rough_string.replace("<![CDATA[<i", "<i")
    rough_string = rough_string.replace("a>]]>", "a>")
    rough_string = rough_string.replace("i>]]>", "i>")

    rough_string = rough_string.replace("<a href=", "<![CDATA[<a href=")
    rough_string = rough_string.replace("<i>", "<![CDATA[<i>")
    rough_string = rough_string.replace("</a>", "</a>]]>")
    rough_string = rough_string.replace("</i>", "</i>]]>")
    print(str(rough_string))


def get_webpage_title(url):
    title = url
    try:
        webpage = urllib.request.urlopen(url).read().decode('utf-8')
        title = str(webpage).split('<title>')[1].split('</title>')[0]
    except urllib.error.URLError:
        print("<!-- %s is currently inaccessible -->" % url)
        print("<!-- Unable to retrieve title from webpage.\n-->")
    return title


def get_definitions(element):
    for x in element:
        if "definition" or "comment" or "note" in str(x.tag):
            if x.text and "@@" in x.text:
                pattern = re.compile('@@(.*?)@@')
                matches = pattern.finditer(x.text)
                original_strings = [str(uri.group(0)) for uri in matches]

                for string in original_strings:
                    uri = string[2:-2]
                    if uri[0] == '#':
                        language = x.get("{http://www.w3.org/XML/1998/namespace}lang")
                        if language is None:
                            language = "EN"
                        if x.text.find(string + "s") != -1:
                            string += "s"
                            hyperlink = create_hyperlink(uri, get_label(get_full_uri(uri), language) + "s")
                        else:
                            hyperlink = create_hyperlink(uri, get_label(get_full_uri(uri), language))
                    else:
                        hyperlink = create_hyperlink(uri, get_webpage_title(uri))

                    x.text = x.text.replace(string, hyperlink)


def create_hyperlink(uri, label):
    return ('<![CDATA[<a href="%s" title="%s">%s</a>]]>' % (uri,uri, label))


def get_label(uri, lang):
    query_str = """
        select distinct ?label  where {
            OPTIONAL { <%s> rdfs:label ?label. }.
            filter(
                langMatches(lang(?label), "%s")
            )
        }""" % (uri, lang)
    label = "[%s]" % uri
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
