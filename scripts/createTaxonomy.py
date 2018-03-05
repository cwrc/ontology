#!/usr/bin/python3
# Usage:
# ./createTaxonomy ontology.owl Class lang

import rdflib
import argparse

# Important nspaces
RDF = rdflib.Namespace("http://www.w3.org/1999/02/22-rdf-syntax-ns#")
VANN = rdflib.Namespace("http://purl.org/vocab/vann/")
relations = {
    "broaderTransitive": "http://www.w3.org/2004/02/skos/core#broaderTransitive",
    "related": "http://www.w3.org/2004/02/skos/core#related",
    "narrowerTransitive": "http://www.w3.org/2004/02/skos/core#narrowerTransitive",
    "contraryTo": "http://sparql.cwrc.ca/ontologies/cwrc#contraryTo",
}
relation_style = {
    "broaderTransitive": "",
    "related": " [style=dashed,dir=none]",
    "narrowerTransitive": " [dir=back]",
    "contraryTo": " [color=red dir=none]",
}


def open_graph(o_file):
    global o_graph
    o_graph = rdflib.Graph()
    namespace_manager = rdflib.namespace.NamespaceManager(rdflib.Graph())
    o_graph.namespace_manager = namespace_manager
    try:
        o_graph.open("store", create=True)
        o_graph.parse(o_file)
    except Exception as e:
        raise e
        print_usage()


def get_namespace():
    global onto_url
    onto_pre = [str(o) for s, p, o in o_graph.triples(((None, VANN.preferredNamespacePrefix, None)))][0]

    # getting all namespaces from o_graph & creating a dictionary of the names spaces - {identifier:uri}
    all_ns = [n for n in o_graph.namespace_manager.namespaces()]
    namespace_dict = {key: value for (key, value) in all_ns}
    if onto_pre in namespace_dict:
        onto_url = namespace_dict[onto_pre]
    else:
        onto_url = namespace_dict['']


def get_deprecated_terms():
    query_str = """select * where {?uri vs:term_status ?literal.}"""
    return sorted([str(row.uri) for row in o_graph.query(query_str) if str(row.literal) == "deprecated"])


def get_label(uri, lang):
    query_str = """select distinct ?label  where {OPTIONAL { <%s> rdfs:label ?label. }.filter(langMatches(lang(?label), "%s"))}""" % (
        uri, lang)
    label = ""
    for row in o_graph.query(query_str):
        label = row.label
    return label


def get_uri_term(uri):
    index = max(uri.rfind('#'), uri.rfind('/')) + 1
    substring = str(uri)[index:]
    return (substring)


def get_relation(instances, relation):
    relation_list = []
    for x in instances:
        query_str = "SELECT * WHERE { <%s>  <%s> ?upper . }" % (x, relations[relation])
        origTerm = "__" + get_uri_term(str(x)).replace("-", "_") + "__"
        for row in o_graph.query(query_str):
            relation_list.append(
                origTerm + "->" + "__" + get_uri_term(str(row[0])).replace("-", "_") + "__" + relation_style[relation])
    return relation_list


def main():
    parser = argparse.ArgumentParser(
        description='Generate a diagraph of relations within an ontology.', add_help=True)
    parser.add_argument('file', action="store", help="file of ontology")
    parser.add_argument('taxonomy', action="store", help="Class you'd like to build a taxonomy of")
    parser.add_argument('LANG', action="store")
    parser.add_argument('-all', '-a', action="store_true")
    parser.add_argument('-hide', action="store_true")
    parser.add_argument('-related', '-r', action="store_true")
    parser.add_argument('-contrary', '-c', action="store_true")
    parser.add_argument('-format', '-f', action="store", dest="format",
                        help="'margin=0;size=\"25,25\";ratio=compress;'")
    args = parser.parse_args()

    ontology_file = args.file
    taxonomy = args.taxonomy
    lang = args.LANG

    open_graph(ontology_file)
    get_namespace()

    deprecated_uris = get_deprecated_terms()
    class_uri = onto_url + taxonomy
    instances = sorted([s for s, p, o in o_graph.triples(
        (None, RDF.type, class_uri)) if str(s) not in deprecated_uris])

    relation_list = get_relation(instances, "broaderTransitive")

    if args.all:
        relation_list += get_relation(instances, "related") + get_relation(instances, "contraryTo")
    else:
        if args.related:
            relation_list += get_relation(instances, "related")
        if args.contrary:
            relation_list += get_relation(instances, "contraryTo")

    # organizing node details --> abrahamicReligions [label="Abrahamic religions" URL="http://sparql.cwrc.ca/ontologies/cwrc#abrahamicReligions"]
    lonely_nodes = [x for x in instances if not any(
        get_uri_term(x).replace("-", "_") in term for term in relation_list)]
    diagraph_nodes = ["__" + get_uri_term(str(x)).replace("-", "_") + "__" +
                      " [label=\"" + get_label(x, lang) + "\" " + "URL=\"" + str(x) + "\"]" for x in instances if x not in lonely_nodes]

    subgraph_nodes = ["__" + get_uri_term(str(x)).replace("-", "_") + "__" +
                      " [label=\"" + get_label(x, lang) + "\" " + "URL=\"" + str(x) + "\"]" for x in lonely_nodes]
    # printing Diagraph
    print("digraph %s_Taxonomy {" % taxonomy)
    if args.format:
        print(args.format)
    else:
        print("margin=0;")
        print("size=\"25,25\";")
        print("ratio=compress;")

    print(*relation_list, sep='\n')
    print(*diagraph_nodes, sep='\n')

    if not args.hide:
        print("subgraph b{margin=0;rank = sink;")
        print(*subgraph_nodes, sep='\n')
        print("}")

    print("}")


if __name__ == '__main__':
    main()
