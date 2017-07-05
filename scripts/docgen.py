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
    print("\t\toptional flags:")
    print("\t\t\t-i   : add instances on the specification (disabled by default)")
    print("\nExamples:")
    print("%s example.owl ex template.html example.owl.html -i" % script)
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


def getDictionaries(model, classes, properties):
    """
    Extract all resources instanced in the ontology
    (aka "everything that is skos:Concept")
    """
    instances = []
    for i in model.find_statements(RDF.Statement(None, rdf.type, skos.ConceptScheme)):
        uri = str(i.subject.uri)
        print("Found Dictionary:", uri)
        if not uri in instances:
            instances.append(uri)
    print("Dictionaries listed")
    return instances


def specgen(specloc, template, instances=True, mode="spec"):
    """The meat and potatoes: Everything starts here."""

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

    # Get class/properties and range/domain info
    # Gets classes labels from uris from graph and sorts them
    class_list = [x.split("#")[1] for x in sorted(graph.subjects(None, OWL.Class))]
    prop_list = [x.split("#")[1] for x in sorted(graph.subjects(None, OWL.ObjectProperty))]

    global domain_dict
    global range_dict
    domain_dict, range_dict = get_domain_range_dict(graph)

    skos_concepts = [str(s) for s, p, o in graph.triples((None, RDF.type, SKOS.ConceptScheme))]
    print(skos_concepts)
    # for x in skos_concepts:
    #     query_str = "select ?x where {?x <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <" + str(x) + ">}"
    #     for row in graph.query(query_str):
    #         print(row.x)

    instances = []
    for owl_class in class_list:
        class_uri = spec_ns[owl_class]
        for s, p, o in graph.triples((None, RDF.type, class_uri)):
            instances.append(str(s))

    instances = sorted(list(set(instances)))
    print(instances)
    for x in instances:
        print(x)
            # for s, p, o in graph.triples((None, RDF.type, class_uri)):
            #     print(s)

    # for one in classes:
    #     print "Check class:", one
    #         uri = str(i.subject.uri)
    #         print "Check instance:", uri, one
    #         if not uri in instances:
    #             instances.append(uri)

        # print(row.subj)

    # test = graph.subjects(None, skos_concepts[0])
    # print(test)
    # for x in test:
    #     print(x)

    return template


# Sets directory for terminology --> to get rid of
def set_term_dir(directory):
    global termdir
    termdir = directory


def main():
    if (len(sys.argv) < 5 or len(sys.argv) > 6):
        print("hello")
        print_usage()

    specloc = sys.argv[1]
    spec_pre = sys.argv[2]
    specdoc = sys.argv[2] + "-docs"
    temploc = sys.argv[3]
    dest = sys.argv[4]
    template = None
    set_term_dir(specdoc)

    print(specloc)
    print(spec_pre)
    print(specdoc)
    print(temploc)
    print(dest)
    # template

    try:
        f = open(temploc, "r")
        template = f.read()
    except Exception as e:
        print("Error reading from template \"" + temploc + "\": " + str(e))
        print_usage()

    instances = False
    if len(sys.argv) > 5 and sys.argv[5] == '-i':
        instances = True

    specgen(specloc, template, instances=instances)

    # save(dest, specgen(specloc, template, instances=instances))


if __name__ == "__main__":
    main()
