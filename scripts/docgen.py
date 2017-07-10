#!/usr/bin/python3

import os
import codecs
import sys
import time
import re
import urllib
import rdflib

classranges = {}
classdomains = {}
spec_url = None
spec_ns = None
spec_pre = "cwrc"
lang = None

ns_list = {
    "content": "http://purl.org/rss/1.0/modules/content/",
    "dbpedia": "http://dbpedia.org/resource/",
    "dc": "http://purl.org/dc/elements/1.1/",
    "dct": "http://purl.org/dc/terms/",
    "doap": "http://usefulinc.com/ns/doap#",
    "foaf": "http://xmlns.com/foaf/0.1/",
    "geo": "http://www.w3.org/2003/01/geo/wgs84_pos#",
    "mil": "http://rdf.muninn-project.org/ontologies/military#",
    "naval": "http://rdf.muninn-project.org/ontologies/naval#",
    "ott": "http://rdf.muninn-project.org/ontologies/ott#",
    "owl": "http://www.w3.org/2002/07/owl#",
    "prov": "http://www.w3.org/ns/prov#",
    "rdf": "http://www.w3.org/1999/02/22-rdf-syntax-ns#",
    "rdfs": "http://www.w3.org/2000/01/rdf-schema#",
    "sioc": "http://rdfs.org/sioc/ns#",
    "skos": "http://www.w3.org/2004/02/skos/core#",
    "status": "http://www.w3.org/2003/06/sw-vocab-status/ns#",
    "vs": "http://www.w3.org/2003/06/sw-vocab-status/ns#",
    "xsd": "http://www.w3.org/2001/XMLSchema#"
}

# Important nspaces
RDF = rdflib.Namespace(ns_list["rdf"])
RDFS = rdflib.Namespace(ns_list["rdfs"])
SKOS = rdflib.Namespace(ns_list["skos"])
OWL = rdflib.Namespace(ns_list["owl"])
VS = rdflib.Namespace(ns_list["vs"])
PROV = rdflib.Namespace(ns_list["prov"])


def ns_list_to_ns_Dict():
    pass

# Print msg explaining usage of application


def print_usage():
    script = sys.argv[0]
    print("Usage:")
    print("\t%s ontology prefix template destination [flags]\n" % script)
    print("\t\tontology    : path to ontology file")
    print("\t\tprefix      : prefix for CURIEs")
    print("\t\ttemplate    : HTML template path")
    print("\t\tdestination : specification destination (by default)")
    print("\t\tlanguage flags:")
    print("\t\t\ten   : english")
    print("\t\t\tfr   : french")
    print("\nExamples:")
    print("%s example.owl ex template.html example.owl.html en" % script)
    sys.exit(-1)


def insert_dictionary(where, key, value):
    if key not in where:
        where[key] = []
    if value not in where[key]:
        where[key].append(value)


def get_domain_range_dict(graph):
    range_list = set(sorted(graph.objects(None, RDFS.range)))
    domain_list = set(sorted(graph.objects(None, RDFS.domain)))

    domain_dict = {}
    for domain_class in domain_list:
        query_str = "select ?x where {?x rdfs:domain <" + str(domain_class) + ">}"
        dom_props = []
        for row in graph.query(query_str):
            dom_props.append(str(row.x))
        domain_dict[str(domain_class)] = dom_props

    range_dict = {}
    for range_class in range_list:
        query_str = "select ?x where {?x rdfs:range <" + str(range_class) + ">}"
        rang_props = []
        for row in graph.query(query_str):
            rang_props.append(str(row.x))
        range_dict[str(range_class)] = rang_props

    return domain_dict, range_dict


def get_instances(graph, class_list):
    instances = []
    for owl_class in class_list:
        class_uri = spec_ns[owl_class]
        for s, p, o in graph.triples((None, RDF.type, class_uri)):
            instances.append(str(s).split("#")[1])

    instances = sorted(list(set(instances)))
    return instances


def create_link_lists(list, name):
    string = "<p>%s" % name
    for x in list:
        string += '\t<a href="#%s">%s</a>,' % (x, x)
    string += "</p>"
    return(string)


def get_azlist_html(az_dict, list):
    string = '<div class="az_list">'
    for key in list:
        string += create_link_lists(az_dict[key], key)
    string += '</div>'
    return string


def get_rdfs(graph, uri):
    # "Returns label and comment given an RDF.Node with a URI in it"
    comment = ''
    label = ''
    # if (type(urinode) == str):
    #     urinode = RDF.Uri(urinode)
    print(lang)
        # print("\n")
    # print(graph.preferredLabel(uri, lang, RDFS.label))
    # print(graph.preferredLabel(uri, lang, RDFS.label))
    # print(type(graph.preferredLabel(uri, lang, RDFS.label)))
    label = None
    test = graph.preferredLabel(uri, lang, RDFS.label)[0]
    # for x in test:
    #     print(x)
    # print(type(test))
    # print(len(test))
    if len(test) == 2:
        label = test[1]
    print(label)
    print("\nComment:")
    for s, p, o in graph.triples((uri, RDFS.comment, None)):
        print(s)
        print(p)
        print(o)
        print(type(o))

    # test = graph.comment(uri)
    # print(test)

    # print(test[0])
    # print(test[1])
    # label = [o for s, p, o in graph.triples((uri, RDFS.label, None))]
    # print(type(label))
    # print(label)
    print("\n\n")
    # print(graph.preferredLabel(label, lang))
    # l = graph.find_statements(RDF.Statement(urinode, rdfs.label, None))
    # if l.current():
    #     label = l.current().object.literal_value['string']
    # c = graph.find_statements(RDF.Statement(urinode, skos.definition, None))
    # if c.current():
    #     comment = c.current().object.literal_value['string']
    # c = graph.find_statements(RDF.Statement(urinode, rdfs.comment, None))
    # if c.current():
    #     comment = c.current().object.literal_value['string']
    return label, comment


def terms_html(name, list, graph):
    # print("haha")
    doc = ""
    print(spec_pre)
    for item in list:
        doc += """<div class="specterm" id="%s">\n""" % (item)
        doc += """\t<h3>%s: %s:%s</h3>\n""" % (name, spec_pre, item)
        term_uri = spec_ns[item]
        doc += """\t<p class="uri">URI: <a href="%s">%s</a></p>\n""" % (term_uri, term_uri)
        label, comment = get_rdfs(graph, term_uri)
        # break
        # print "Term is %s" % term
        # print "Type is %s" % type(term)
        # print(nsTest)
    # try:
    #     term_uri = term.uri
    # except:
    #     term_uri = term
    # doc += """<p style="font-family:monospace; font-size:0.em;">URI: <a href="%s">%s</a></p>""" % (term_uri, term_uri)
    # label, comment = get_rdfs(m, term)
    # print "Term is %s" % term
    # print "Type is %s" % type(term)
        doc += "</div>\n\n"
    return doc


def specgen(specloc, template, language):
    global spec_url
    global spec_ns
    global ns_list

    # Creating rdf graph
    graph = rdflib.Graph()
    namespace_manager = rdflib.namespace.NamespaceManager(rdflib.Graph())
    graph.namespace_manager = namespace_manager
    try:
        graph.open("store", create=True)
        graph.parse(specloc)
    except Exception as e:
        raise e
        print_usage()

    # getting all namespaces from graph
    all_ns = [n for n in graph.namespace_manager.namespaces()]

    # creating a dictionary of the names spaces - {identifier:uri}
    global namespace_dict
    namespace_dict = {key: value for (key, value) in all_ns}

    spec_url = namespace_dict['']
    spec_ns = rdflib.Namespace(spec_url)
    ns_list[spec_pre] = spec_url

    # Gets sorted classes & property labels
    class_list = [x.split("#")[1] for x in sorted(graph.subjects(None, OWL.Class))]
    prop_list = [x.split("#")[1] for x in sorted(graph.subjects(None, OWL.ObjectProperty))]

    global domain_dict
    global range_dict
    domain_dict, range_dict = get_domain_range_dict(graph)

    # Dict_list in specgen
    skos_concepts = [str(s).split("#")[1] for s, p, o in graph.triples((None, RDF.type, SKOS.ConceptScheme))]

    instance_list = get_instances(graph, class_list)

    # Build HTML list of terms.
    az_dict = {
        "Classes:": class_list,
        "Properties:": prop_list,
        "Instances:": instance_list,
        "Dictionaries:": skos_concepts,
    }
    temp_list = ["Classes:", "Properties:", "Instances:", "Dictionaries:"]
    azlist_html = get_azlist_html(az_dict, temp_list)

    termlist = terms_html("Property", prop_list, graph)
    print("\n\n\n\n")
    # print(termlist)
    return template


# Sets directory for terminology --> to get rid of
def set_term_dir(directory):
    global termdir
    termdir = directory


def main():
    global lang
    if (len(sys.argv) != 6):
        print_usage()

    specloc = sys.argv[1]
    spec_pre = sys.argv[2]
    specdoc = spec_pre + "-docs"
    temploc = sys.argv[3]
    dest = sys.argv[4]
    lang = sys.argv[5]
    template = None

    set_term_dir(specdoc)

    try:
        f = open(temploc, "r")
        template = f.read()
    except Exception as e:
        print("Error reading from template \"" + temploc + "\": " + str(e))
        print_usage()

    if lang.lower() not in ["en", "fr"]:
        print("Language selected is currently not supported")
        print_usage()

    specgen(specloc, template, lang)

    # save(dest, specgen(specloc, template, instances=instances))


if __name__ == "__main__":
    main()
