#!/usr/bin/python3
# Usage:
# ./createTaxonomy ontology.owl Class lang

import rdflib
import argparse

# TODO:

# Optional labels on edges

# Handle external terms ex cwrc:NaturalPerson subclass of foaf:Person
# auto do relations depending if it's a class or object property

# do something with lonely nodes
# option to used uris vs labels, default goes with label if available else uses last bit of uri

# Important nspaces
RDF = rdflib.Namespace("http://www.w3.org/1999/02/22-rdf-syntax-ns#")
VANN = rdflib.Namespace("http://purl.org/vocab/vann/")
OWL = rdflib.Namespace("http://www.w3.org/2002/07/owl#")

all_nodes = []
relations = {
    "broaderTransitive": "http://www.w3.org/2004/02/skos/core#broaderTransitive",
    "related": "http://www.w3.org/2004/02/skos/core#related",
    "narrowerTransitive": "http://www.w3.org/2004/02/skos/core#narrowerTransitive",
    "contraryTo": "http://sparql.cwrc.ca/ontologies/cwrc#contraryTo",
    "subjectCentricPredicate": "http://sparql.cwrc.ca/ontologies/cwrc#subjectCentricPredicate",
    "subPropertyOf": "http://www.w3.org/2000/01/rdf-schema#subPropertyOf",
    "subClassOf": "http://www.w3.org/2000/01/rdf-schema#subClassOf",
    "inverseOf": "http://www.w3.org/2002/07/owl#inverseOf",
    "SymmetricProperty": "http://www.w3.org/2002/07/owl#SymmetricProperty",
    "sameAs": "http://www.w3.org/2002/07/owl#sameAs",
}
relation_style = {
    "broaderTransitive": "",
    "related": " [style=dashed,dir=none ]",  # label=related]",
    "narrowerTransitive": " [dir=back ]",  # label=narrowerTransitive]",
    "contraryTo": " [color=red dir=none ]",  # label=contraryTo]",
    "subPropertyOf": "[color=blue ]",  # label=subPropertyOf]",
    "subClassOf": "[color=blue ]",  # label=subClassOf]",
    "subjectCentricPredicate": "[style=dashed,color=green ]",  # label=subClassOf]",
    "inverseOf": "[color=red dir=both ]",  # label=inverseOf]",
    "SymmetricProperty": "[color=green dir=both ]",  # label=SymmetricProperty]",
    "sameAs": "[dir=none ]",  # label=sameAs]",
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
    onto_prefix = [str(o) for s, p, o in o_graph.triples(((None, VANN.preferredNamespacePrefix, None)))]

    # getting all namespaces from o_graph & creating a dictionary of the names spaces - {identifier:uri}
    all_ns = [n for n in o_graph.namespace_manager.namespaces()]
    namespace_dict = {key: value for (key, value) in all_ns}

    if onto_prefix:
        onto_prefix = onto_prefix[0]
    else:
        onto_prefix = None
# TODO: GET uri to only show relations for cwrc properties
    # print(onto_prefix)
    # print(namespace_dict)
    # print(namespace_dict[onto_prefix])
    # print(*namespace_dict, sep="\n")
    # exit()
    if onto_prefix in namespace_dict:
        class_uri = namespace_dict[onto_prefix]
    elif '' in namespace_dict:
        class_uri = namespace_dict['']
        # print(class_uri)
    else:
        class_uri = [x for x in o_graph.subjects(RDF.type, OWL.Ontology)]
        if class_uri:
            class_uri = class_uri[0]
        else:
            print("Unable to able to find the uri of your ontology")
            # TODO: create optional argument that specifies the uri
            # Please rerun with the following command
            exit()
            # print("Please provide the uri of your ontology")
            # class_uri = rdflib.URIRef(input("URI:"))

        onto_prefix = {value: key for (key, value) in all_ns}[class_uri]
        # spec_uri =

    if ":" in taxonomy:
        temp = taxonomy.split(":")[0]
        class_uri = namespace_dict[temp]
        taxonomy = taxonomy.split(":")[1]

    class_uri += taxonomy
    return(class_uri)


def get_deprecated_terms():
    query_str = """select * where {?uri <http://www.w3.org/2003/06/sw-vocab-status/ns#term_status> ?literal.}"""
    return sorted([str(row.uri) for row in o_graph.query(query_str) if str(row.literal) == "deprecated"])


def get_label(uri, lang):
    query_str = """select distinct ?label  where {OPTIONAL { <%s> rdfs:label ?label. }.filter(langMatches(lang(?label), "%s"))}""" % (
        uri, lang)
    # if no label should return clean uri term
    # for some reason not grabbing labels :/ on test.owl
    label = "__" + get_uri_term(uri) + "__"

    for row in o_graph.query(query_str):
        label = row.label
    return label


def get_uri_term(uri):
    index = max(uri.rfind('#'), uri.rfind('/')) + 1
    return str(uri)[index:]


def get_symmetric(instances):
    relation = "SymmetricProperty"
    relation_list = []
    # for s, p, o in o_graph.triples((None, RDF.type, rdflib.term.URIRef(relations[relation]))):
    #     print(s, p, o)
    for x in instances:
        # print(type(x))
        # print(o_graph)
        # if (x, RDF.type, relations[relation]) in o_graph:
        #     print(x)
        #     print(relations[relation])

        if (x, RDF.type, rdflib.term.URIRef(relations[relation])) in o_graph:
            # print(relations[relation])
            origTerm = "__" + get_uri_term(str(x)).replace("-", "_") + "__"
            relation_list.append(origTerm + "->" + origTerm + relation_style[relation])
    # exit()
    return relation_list


def get_relation(instances, relation):
    global all_nodes
    relation_list = []
    for x in instances:
        query_str = "SELECT * WHERE { <%s>  <%s> ?upper . }" % (x, relations[relation])
        origTerm = "__" + get_uri_term(str(x)).replace("-", "_") + "__"
        all_nodes.append(x)
        for row in o_graph.query(query_str):
            new_term = "__" + get_uri_term(str(row[0])).replace("-", "_") + "__"
            all_nodes.append(row[0])
            relation_list.append(
                origTerm + "->" + new_term + relation_style[relation])
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
    global all_nodes
    lang = args.LANG

    open_graph(ontology_file)
    class_uri = get_class_uri(taxonomy)
    deprecated_uris = get_deprecated_terms()
    instances = sorted([s for s, p, o in o_graph.triples(
        (None, RDF.type, class_uri)) if str(s) not in deprecated_uris])

    if args.subPropertyOf:
        relation_list = get_relation(instances, "subPropertyOf")  # + get_relation(instances, "inverseOf")
        if args.inverseOf:
            relation_list += get_relation(instances, "inverseOf")
    elif args.subClassOf:
        relation_list = get_relation(instances, "subClassOf")
    elif args.inverseOf:
        relation_list = get_relation(instances, "inverseOf")
    elif args.subjectCentricPredicate:
        relation_list = get_relation(instances, "subjectCentricPredicate")
    else:
        relation_list = get_relation(instances, "broaderTransitive")

    if args.all:
        relation_list += get_relation(instances, "related") + get_relation(instances, "contraryTo")
    else:
        if args.related:
            relation_list += get_relation(instances, "related")
        if args.contraryTo:
            relation_list += get_relation(instances, "contraryTo")
        if args.sameAs:
            relation_list += get_relation(instances, "sameAs")
        if args.SymmetricProperty:
            relation_list += get_symmetric(instances)

    # organizing node details --> abrahamicReligions [label="Abrahamic religions" URL="http://sparql.cwrc.ca/ontologies/cwrc#abrahamicReligions"]
    lonely_nodes = [x for x in instances if not any(
        get_uri_term(x).replace("-", "_") in term for term in relation_list)]
    # print(*instances, sep="\n")
    # print()
    # all_nodes = list(set(all_nodes))
    # print(*all_nodes, sep="\n")
    # print(len(instances))
    # print(len(all_nodes))
    # diagraph_nodes = ["__" + get_uri_term(str(x)).replace("-", "_") + "__" +
    #                   " [label=\"" + get_label(x, lang) + "\" " + "URL=\"" + str(x) + "\"]" for x in instances if x not in lonely_nodes]

    diagraph_nodes = ["__" + get_uri_term(str(x)).replace("-", "_") + "__" +
                      " [label=\"" + get_label(x, lang) + "\" " + "URL=\"" + str(x) + "\"]" for x in all_nodes if x not in lonely_nodes]

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
