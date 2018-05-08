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
    "subPropertyOf": "http://www.w3.org/2000/01/rdf-schema#subPropertyOf",
    "subClassOf": "http://www.w3.org/2000/01/rdf-schema#subClassOf",
}
relation_style = {
    "broaderTransitive": "",
    "related": " [style=dashed,dir=none]",
    "narrowerTransitive": " [dir=back]",
    "contraryTo": " [color=red dir=none]",
    "subPropertyOf": "[color=blue]",
    "subClassOf": "[color=blue]",
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


def get_class_uri(taxonomy):
    onto_pre = [str(o) for s, p, o in o_graph.triples(((None, VANN.preferredNamespacePrefix, None)))][0]

    # getting all namespaces from o_graph & creating a dictionary of the names spaces - {identifier:uri}
    all_ns = [n for n in o_graph.namespace_manager.namespaces()]
    namespace_dict = {key: value for (key, value) in all_ns}

    if onto_pre in namespace_dict:
        class_uri = namespace_dict[onto_pre]
    else:
        class_uri = namespace_dict['']

    if ":" in taxonomy:
        temp = taxonomy.split(":")[0]
        class_uri = namespace_dict[temp]
        taxonomy = taxonomy.split(":")[1]

    class_uri += taxonomy
    return(class_uri)


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
    return str(uri)[index:]


def get_relation(instances, relation):
    relation_list = []
    for x in instances:
        query_str = "SELECT * WHERE { <%s>  <%s> ?upper . }" % (x, relations[relation])
        origTerm = "__" + get_uri_term(str(x)).replace("-", "_") + "__"
        for row in o_graph.query(query_str):
            relation_list.append(
                origTerm + "->" + "__" + get_uri_term(str(row[0])).replace("-", "_") + "__" + relation_style[relation])
    return relation_list


def make_list(node_list):
    html_str = ""
    for x in node_list:
        html_str += '<a href="#%s">%s</a>,\n' % (x.split("#")[1], get_label(x, lang))
    return html_str


def main():
    parser = argparse.ArgumentParser(
        description='Generate a diagraph of relations within an ontology.', add_help=True)
    parser.add_argument('file', action="store", help="file of ontology")
    parser.add_argument('taxonomy', action="store",
                        help="Class/Datatype you'd like to build a taxonomy of, ex. PoliticalAffiliation or owl:Class")
    parser.add_argument('LANG', action="store")
    parser.add_argument('-all', '-a', action="store_true")
    parser.add_argument('-hide', action="store_true")
    parser.add_argument('-disconnected', '-lonely', action="store_true")
    parser.add_argument('-format', '-f', action="store", dest="format",
                        help="'margin=0;size=\"25,25\";ratio=compress;'")

    for x in relations.keys():
        parser.add_argument('-' + x, '-' + x[:4], action="store_true")

    args = parser.parse_args()
    ontology_file = args.file
    taxonomy = args.taxonomy
    global lang
    lang = args.LANG

    open_graph(ontology_file)
    class_uri = get_class_uri(taxonomy)
    deprecated_uris = get_deprecated_terms()
    instances = sorted([s for s, p, o in o_graph.triples(
        (None, RDF.type, class_uri)) if str(s) not in deprecated_uris])

    if args.subPropertyOf:
        relation_list = get_relation(instances, "subPropertyOf")
    elif args.subClassOf:
        relation_list = get_relation(instances, "subClassOf")
    else:
        relation_list = get_relation(instances, "broaderTransitive")

    if args.all:
        relation_list += get_relation(instances, "related") + get_relation(instances, "contraryTo")
    else:
        if args.related:
            relation_list += get_relation(instances, "related")
        if args.contraryTo:
            relation_list += get_relation(instances, "contraryTo")

    # organizing node details --> abrahamicReligions [label="Abrahamic religions" URL="http://sparql.cwrc.ca/ontologies/cwrc#abrahamicReligions"]
    lonely_nodes = [x for x in instances if not any(
        get_uri_term(x).replace("-", "_") in term for term in relation_list)]
    diagraph_nodes = ["__" + get_uri_term(str(x)).replace("-", "_") + "__" +
                      " [label=\"" + get_label(x, lang) + "\" " + "URL=\"" + str(x) + "\"]" for x in instances if x not in lonely_nodes]

    subgraph_nodes = ["__" + get_uri_term(str(x)).replace("-", "_") + "__" +
                      " [label=\"" + get_label(x, lang) + "\" " + "URL=\"" + str(x) + "\"]" for x in lonely_nodes]
    # printing Diagraph
    # if args.disconnected:
    #     print("<div>")
    #     # print(*lonely_nodes, sep='\n')
    #     print(make_list(lonely_nodes))
    #     print("</div>")
    # print(*relation_list, sep="")
    # exit()

    print("digraph %s_Taxonomy {" % taxonomy.replace(":", ""))
    if args.format:
        print(args.format)
    else:
        print("margin=0;")
        print("size=\"25,25\";")
        print("ratio=compress;")

    if not args.disconnected:
        print(*relation_list, sep='\n')
        print(*diagraph_nodes, sep='\n')

    if not args.hide:
        print("subgraph b{margin=0;rank = sink;")
        print(*subgraph_nodes, sep='\n')
        print("}")

    print("}")


if __name__ == '__main__':
    main()
