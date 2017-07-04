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

RDF = rdflib.Namespace(ns_list["rdf"])
RDFS = rdflib.Namespace(ns_list["rdfs"])
SKOS = rdflib.Namespace(ns_list["skos"])
OWL = rdflib.Namespace(ns_list["owl"])
VS = rdflib.Namespace(ns_list["vs"])
PROV = rdflib.Namespace(ns_list["prov"])


def __getScriptPath():
    path = sys.argv[0]
    if path.startswith("./"):
        return path
    else:
        base = "/".join(path.split("/")[:-1])
        for one in os.environ["PATH"].split(":"):
            if base == one:
                return path.split("/")[-1]
        return path


# Print msg explaining usage of application
def print_usage():
    # Print msg explaining usage of application
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

    if mode == "spec":
        # Build HTML list of terms.
        azlist = buildazlist(classlist, proplist, instalist, diclist)
    elif mode == "list":
        # Build simple <ul> list of terms.
        azlist = build_simple_list(classlist, proplist, instalist)

    # # Generate Term HTML
    # termlist = docTerms('Property', proplist, m)
    # termlist = docTerms('Class', classlist, m) + termlist
    # termlist = docTerms('Dictionary', diclist, m) + termlist
    # for thisdic in diclist:
    #    print getShortName(thisdic) 
    #    termlist = docTerms('Concept', getConcepts(m, thisdic), m) + termlist
    # if instances:
    #     termlist += docTerms('Instance', instalist, m)
    # # Generate RDF from original namespace.
    # u = urllib.urlopen(specloc)
    # rdfdata = u.read()
    # rdfdata = re.sub(r"(<\?xml version.*\?>)", "", rdfdata)
    # rdfdata = re.sub(r"(<!DOCTYPE[^]]*]>)", "", rdfdata)
    # #rdfdata.replace("""<?xml version="1.0"?>""", "")
    
    # # print template % (azlist.encode("utf-8"), termlist.encode("utf-8"), rdfdata.encode("ISO-8859-1"))
    # template = re.sub(r"^#format \w*\n", "", template)
    # template = re.sub(r"\$VersionInfo\$", owlVersionInfo(m).encode("utf-8"), template) 
    
    # # NOTE: This works with the assumtpion that all "%" in the template are escaped to "%%" and it
    # #       contains the same number of "%s" as the number of parameters in % ( ...parameters here... )
    # try:
    #     template = unicode(template)
    # except UnicodeDecodeError, e:
    #     template = unicode(template.decode('utf-8'))
    
    # try:
    #     template = template % (unicode(azlist), unicode(termlist))
    #     template += "<!-- specification regenerated by SpecGen5 at %s -->" % time.strftime('%X %x %Z')
    # except TypeError, e:
    #     print "Error filling the template! Please, be sure you respected both '%s' on your template" % "%s"

    return Template


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
