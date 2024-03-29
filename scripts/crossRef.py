#!/usr/bin/python3
import urllib.request
from lxml import etree
import rdflib
import re
import sys
from bs4 import BeautifulSoup
import requests
import socket
import urllib
import urllib3
# TODO:
# handling of broken links:
 # append to https://web.archive.org/web/*/
 # Wayback Machine: URI
 # Clean up exception handling

# Expected Usage:
# ./crossRef.py test.owl
# Will output updated rdf-xml input_file with appropriate <a> in cdata tags to link to appropriate label and link
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

# NOTE: May need to update this user-agent header
headers = {}
headers['User-Agent'] = "Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.27 Safari/537.17"
URL_DICT = {}

if len(sys.argv) != 3:
    print("Insufficent Arguments provided")
    print("Expected Usage:")
    print(sys.argv[0] + " input.[owl/rdf/xml] output.[owl/rdf/xml]")
    exit()

input_file = sys.argv[1]
output_file = sys.argv[2]

# Opening with etree parser for manipulation of text
parser = etree.XMLParser(strip_cdata=False)
try:
    with open(input_file, "r", encoding="UTF-8") as source:
        tree = etree.parse(source, parser=parser)
        root = tree.getroot()
except etree.XMLSyntaxError as e:
    print("Unable to parse provided rdf-xml input_file:", e, "\n\n\n")
    raise e

# Opening with rdflib for querying of labels
o_graph = rdflib.Graph()
namespace_manager = rdflib.namespace.NamespaceManager(rdflib.Graph())
o_graph.namespace_manager = namespace_manager
try:
    o_graph.open("store", create=True)
    o_graph.parse(input_file)
except Exception as e:
    raise e

namespace_dict = {key: value for (key, value) in o_graph.namespace_manager.namespaces()}
spec_url = namespace_dict['']

genre_graph = None
genre_namespace_dict = None
genre_spec_url = None
if "cwrc" in input_file:
    genre_graph = rdflib.Graph()
    namespace_manager = rdflib.namespace.NamespaceManager(rdflib.Graph())
    genre_graph.namespace_manager = namespace_manager
    try:
        genre_graph.open("store", create=True)
        genre_graph.parse("genre.rdf")
    except Exception as e:
        raise e

    genre_namespace_dict = {key: value for (key, value) in genre_graph.namespace_manager.namespaces()}
    genre_spec_url = genre_namespace_dict['']


def get_full_uri(uri, spec=spec_url):
    return spec[:-1] + uri


def format_XML(root):
    rough_string = '<?xml version="1.0" encoding="UTF-8"?>\n'
    rough_string += (etree.tostring(root, encoding="utf-8", pretty_print=True)).decode('utf-8')
    # rough_string += etree.tostring(root, encoding="unicode", pretty_print=True)

    # Accounting for oddities in lxml not properly ignoring CDATA sections
    rough_string = rough_string.replace("&lt;", "<")
    rough_string = rough_string.replace("&gt;", ">")
    rough_string = rough_string.replace("(<a", "<a")
    rough_string = rough_string.replace("(<i", "<i")
    rough_string = rough_string.replace("<![CDATA[ ", "<![CDATA[")
    rough_string = rough_string.replace("<![CDATA[<a", "<a")
    rough_string = rough_string.replace("<![CDATA[<i", "<i")
    rough_string = rough_string.replace("a>)", "a>")
    rough_string = rough_string.replace("i>)", "i>")
    rough_string = rough_string.replace("a>]]>", "a>")
    rough_string = rough_string.replace("i>]]>", "i>")

    if "CDATA" in rough_string:
        print("CDATA not properly removed, try rerunning this script to output to file")
        exit()

    rough_string = rough_string.replace("<a", "<![CDATA[<a")
    rough_string = rough_string.replace("<i>", "<![CDATA[<i>")
    rough_string = rough_string.replace("/a>", "/a>]]>")
    rough_string = rough_string.replace("/i>", "/i>]]>")

    return(rough_string)


def get_webpage_title(url):
    # TODO: investigate what's wrong with old way because bs4 is slow
    title = url
    connection_errors = (urllib3.exceptions.MaxRetryError, socket.gaierror, urllib.error.URLError,
                         urllib3.exceptions.NewConnectionError, requests.exceptions.ConnectionError)
    global URL_DICT
    if url in URL_DICT:
        return URL_DICT[url]
    try:
        r = requests.get(url, headers=headers)
        soup = BeautifulSoup(r.content, "lxml")
    except connection_errors as e:
        print("<!-- %s is currently inaccessible -->" % url)
        print("<!-- Unable to retrieve title from webpage.\n-->")
    else:
        try:
            title = soup.find("title").text
        except AttributeError:
            print(url)
            print(soup)
            title = url
    if title == url:
        title = str(url) + " Via Wayback Machine"

    URL_DICT[url] = title
    return title


def _get_webpage_title(url):
    title = url
    webpage = None
    global URL_DICT
    connection_errors = (urllib3.exceptions.MaxRetryError, socket.gaierror, urllib.error.URLError,
                         urllib3.exceptions.NewConnectionError, requests.exceptions.ConnectionError)
    if url in URL_DICT:
        return URL_DICT[url]

    try:
        webpage = urllib.request.urlopen(url).read().decode('utf-8')
    except UnicodeDecodeError:
        webpage = None
    if not webpage:
        try:
            req = urllib.request.Request(url, headers=headers)
            webpage = urllib.request.urlopen(req).read()
        except connection_errors:
            webpage = None
    if webpage:
        try:
            title = str(webpage).split('<title>')[1].split('</title>')[0]
        except IndexError:
            print(str(webpage).split('<title>'))
            title = url
    else:
        print("<!-- %s is currently inaccessible -->" % url)
        print("<!-- Unable to retrieve title from webpage.\n-->")

    if title != url:
        URL_DICT[url] = title
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
                    elif "genre:" in uri and genre_graph:
                        language = x.get("{http://www.w3.org/XML/1998/namespace}lang")
                        if language is None:
                            language = "EN"
                        full_uri = get_full_uri(uri.split(":")[1], genre_spec_url + "#")
                        # label = get_label(full_uri, language, genre_graph)
                        # hyperlink = create_hyperlink(full_uri, label)
                        hyperlink = create_hyperlink(full_uri, uri)
                    else:
                        if ".pdf" in str(uri):
                            hyperlink = create_hyperlink(uri, str(uri))
                        else:
                            hyperlink = create_hyperlink(uri, get_webpage_title(uri))

                    x.text = x.text.replace(string, hyperlink)


def create_hyperlink(uri, label):
    if "Via Wayback Machine" in label:
        uri = "https://web.archive.org/web/*/" + uri
    return ('<![CDATA[<a href="%s" title="%s">%s</a>]]>' % (uri, uri, label))


def get_label(uri, lang, graph=o_graph):
    query_str = """
        select distinct ?label  where {
            OPTIONAL { <%s> rdfs:label ?label. }.
            filter(
                langMatches(lang(?label), "%s")
            )
        }""" % (uri, lang)
    label = "[%s]" % uri
    for row in graph.query(query_str):
        label = row.label

    return label


def find_elements():
    return [x for x in root if len(x) > 1]


def main():
    elements = find_elements()
    for element in elements:
        get_definitions(element)
    # format_XML(root)

    with open(output_file, "w") as output:
        # tree.write(output, encoding="UTF-8")
        output.write(format_XML(root))

if __name__ == '__main__':
    main()
