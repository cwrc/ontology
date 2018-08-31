#!/usr/bin/python3
import sys
import rdflib
import time
import urllib.request

# temp log library for debugging
# from log import *
# log = Log("log/docgen")
# log.test_name("Debugging Document Generator")

"""TODO:
1) Double check validity of uris when they're relative uris
    search ontology for if it's a term
2) Fix Protege support
    -Full uris vs relative ones
    - Named Individual support

3) External testing
 # Handle ontologies that use rdfs:comment as definitions
 # Handle terms that don't have a label but a foaf name
 # Handle definitions with no language attributes

4) Fix inverse term with language support
5) Create relations.json by loading ontologies in the namespace
6) Collapse inferred inverse relations with declarative ones?

7) Move out translations to external file

8) General error handling
 - unable to load ontology
 - missing json file
 - no namespace uri
 - no namespace prefix
"""
spec_url = None
spec_ns = None
spec_pre = None
lang = None
o_graph = None
deprecated_uris = None
inverse_r = None
symmetric_r = None

# Important nspaces
RDF = rdflib.Namespace("http://www.w3.org/1999/02/22-rdf-syntax-ns#")
RDFS = rdflib.Namespace("http://www.w3.org/2000/01/rdf-schema#")
SKOS = rdflib.Namespace("http://www.w3.org/2004/02/skos/core#")
OWL = rdflib.Namespace("http://www.w3.org/2002/07/owl#")
FOAF = rdflib.Namespace("http://xmlns.com/foaf/0.1/")
VANN = rdflib.Namespace("http://purl.org/vocab/vann/")
PROV = rdflib.Namespace("http://www.w3.org/ns/prov#")
DCTERMS = rdflib.Namespace("http://purl.org/dc/terms/")

trans_dict = {
    "specification": ["Specification", "Spécifications"],
    "draft": ["Working Draft", "Brouillon de travail"],
    "previous_ver": ["Previous Version", "Ancienne version"],
    "current_ver": ["This Version", "Version courante"],
    "latest_ver": ["Latest Version", "Version à jour"],
    "last_ver": ["Last update", "Dernière version"],
    "authors": ["Authors", "Auteurs"],
    "contrib": ["Contributors", "Contributeurs"],
    "subjects": ["Subject Headings", "Sujets"],
    "listterm": ["Detailed references for all terms, classes and properties",
                 "Références détaillées pour tous les termes, classes et propriétés"],
    "classes": ["Classes", "Classes"],
    "props": ["Properties", "Propriétés"],
    "dicts": ["Dictionaries", "Dictionnaires"]
}
term_main_uris = [rdflib.term.URIRef('http://www.w3.org/2000/01/rdf-schema#label'), rdflib.term.URIRef(
    'http://www.w3.org/2004/02/skos/core#definition'), rdflib.term.URIRef(
    'http://www.w3.org/2004/02/skos/core#altLabel'),
    rdflib.term.URIRef('http://www.w3.org/2000/01/rdf-schema#comment')]
term_ignore_uris = [rdflib.term.URIRef('http://www.w3.org/1999/02/22-rdf-syntax-ns#value'), rdflib.term.URIRef(
    'http://rdfs.org/ns/void#inDataset'), rdflib.term.URIRef('http://www.w3.org/2000/01/rdf-schema#isDefinedBy')]


def parse_relations():
    import json
    import os.path
    # TODO add error handling for missing relation json file
    with open(os.path.join(os.path.dirname(__file__), 'relations.json')) as f:
        data = json.load(f)

    global inverse_r
    global symmetric_r
    inverse_r = data["inverse"]
    symmetric_r = [rdflib.term.URIRef(x) for x in data["symmetric"]]
    symmetric_r += set(sorted(o_graph.subjects(None, OWL.SymmetricProperty)))


def print_usage():
    # add use of arg parser
    script = sys.argv[0]
    print("Usage:")
    print("\t%s ontology template destination lang\n" % script)
    print("\t\tontology    : path to ontology file")
    print("\t\ttemplate    : HTML template path")
    print("\t\tdestination : specification destination")
    print("\t\tlanguage flags:")
    print("\t\t\ten   : english")
    print("\t\t\tfr   : french")
    print("\nExample:")
    print("%s example.owl template.html destination.html en" % script)
    sys.exit(-1)


def create_symmetric_dict():
    symmetric_dict = {}
    for x in symmetric_r:
        symmetric_dict[str(x)] = {}
        for s, o in o_graph.subject_objects(x):
            symmetric_dict[str(x)][str(o)] = str(s)
    return(symmetric_dict)


def create_inverse_dict():
    inverse_dict = {}
    for x in inverse_r.keys():
        temp_list = [y for y in set(sorted(o_graph.objects(None, rdflib.term.URIRef(x)))) if spec_url in y]
        temp_dict = {}
        for temp_class in temp_list:
            query_str = "select ?x where {?x <" + x + "> <" + str(temp_class) + ">}"
            temp_dict[str(temp_class)] = [str(row.x)
                                          for row in o_graph.query(query_str) if str(row.x) not in deprecated_uris]
            if temp_dict[str(temp_class)] == []:
                del temp_dict[str(temp_class)]

        inverse_dict[x] = temp_dict
    return(inverse_dict)


def get_uri_term(uri):
    string = str(uri)
    index = max(uri.rfind('#'), uri.rfind('/')) + 1
    return string[index:]


def create_link_lists(list, name):
    string = "<p>%s\n" % name
    for x in list:
        title = str(get_label_dict(get_full_uri(x)))
        string += '\t<span class="list-item"><a href="#%s" title="%s">%s</a>,</span>\n' % (x, title, x)
    string += "</p>\n"
    ' '.join(string.split())
    return(string)


def open_graph(specloc):
    # Creating rdf o_graph
    global o_graph
    o_graph = rdflib.Graph()
    try:
        o_graph.open("store", create=True)
        o_graph.parse(specloc)
    except Exception as e:
        raise e
        print_usage()


def etreetag_to_uri(tag):
    return rdflib.term.URIRef(str(tag)[1:].replace("}", ""))


def get_high_lvl_nodes():
    file = sys.argv[1]

    from lxml import etree
    parser = etree.XMLParser(strip_cdata=False, remove_comments=True)
    with open(file, "rb") as source:
        tree = etree.parse(source, parser=parser)
        root = tree.getroot()

    ignore_uris = [rdflib.term.URIRef("http://rdfs.org/ns/void#Dataset"),
                   rdflib.term.URIRef("http://www.w3.org/2002/07/owl#Ontology"),
                   rdflib.term.URIRef("http://www.w3.org/1999/02/22-rdf-syntax-ns#Description"),
                   rdflib.term.URIRef("http://www.w3.org/2002/07/owl#DeprecatedClass"),
                   # Most instances are also typed as concepts, resulting in redundant types in the main listing
                   rdflib.term.URIRef("http://www.w3.org/2004/02/skos/core#Concept"),
                   rdflib.term.URIRef("http://www.w3.org/2002/07/owl#DeprecatedProperty")]

    types = {etreetag_to_uri(x.tag) for x in root if etreetag_to_uri(x.tag) not in ignore_uris}
    bibo_nodes = {x for x in types if ("purl.org/ontology/bibo/" in str(x))}

    return list(types - bibo_nodes)


def create_row(list, listitem=True):
    string = "<td>\n"
    if listitem:
        string += "<ul>\n"
    for x in list:
        title = str(get_label_dict(get_full_uri(x)))
        if listitem:
            string += '\t\t<li><a href="#%s" title="%s">%s</a></li>\n' % (x, title, x)
        else:
            string += '\t\t<a href="#%s" title="%s">%s</a>\n' % (x, title, x)
    if listitem:
        string += "</ul>\n"
    string += "</td>\n"
    ' '.join(string.split())
    return(string)


def newAZ(nodes):
    types = [x for x in nodes if spec_url not in x]
    instanceTypes = sorted(list(set(nodes) - set(types)))
    if rdflib.term.URIRef('http://www.w3.org/2002/07/owl#NamedIndividual') in types:
        types.remove(rdflib.term.URIRef('http://www.w3.org/2002/07/owl#NamedIndividual'))

    string = ""
    string += '<div class="global-ref">'

    string += '<table class="table table-hover">'
    string += '<thead>\n\t<tr>'
    string += '    <th scope="col">rdf:type</th>'
    string += '    <th scope="col">Instance</th>'
    string += '  </tr>\n\t</thead>\n<tbody>'
    for x in types:
        instances = [get_uri_term(x) for x in o_graph.subjects(None, x) if spec_url in x]
        if instances:
            string += '<tr>'
            name = '<a href="%s" style="font-weight:bold;">%s:</a>' % (get_link(x), get_prefix(x))
            string += '  <th scope="row">%s</th>' % name
            string += create_row(sorted(instances))
            string += '</tr>'
    string += '</tbody>\n</table>'

    for x in types:

        if any((y, RDF.type, x) in o_graph for y in instanceTypes):
            string += '<br/>\n'
            string += '<table class="table table-hover">\n'
            string += '<thead>\n\t<tr>'
            string += '    <th scope="col">%s</th>' % get_prefix(x)
            string += '    <th scope="col">Instance</th>'
            string += '  </tr>\n\t</thead>\n<tbody>'
            for y in instanceTypes:
                if (y, RDF.type, x) in o_graph:
                    title_str = ""
                    if spec_url in y:
                        title_str = ' title="' + str(get_label_dict(y)) + '" '
                    else:
                        title_str = ' target="_blank"'
                    name = '<a href="%s"%s style="font-weight:bold;">%s:</a>' % (
                        get_link(y), title_str, get_prefix(y))
                    instances = [get_uri_term(s) for s in o_graph.subjects(
                        RDF.type, y) if str(s) not in deprecated_uris]
                    string += '<tr>'
                    string += '  <th scope="row">%s</th>' % name
                    string += create_row(sorted(instances))
                    string += '</tr>'
            string += '</tbody>'
            string += '</table>'
    string += '</div>'

    return string


def grandchildren_exist(instances):
    for x in instances:
        if any(s in s for s in o_graph.subjects(RDF.type, x) if str(s) not in deprecated_uris):
            return True
    return False


def all_terms_html(nodes):
    types = sorted([x for x in nodes if spec_url not in x])
    if rdflib.term.URIRef('http://www.w3.org/2002/07/owl#NamedIndividual') in types:
        types.remove(rdflib.term.URIRef('http://www.w3.org/2002/07/owl#NamedIndividual'))
    string = ""
    for x in types:
        instances = [get_uri_term(x) for x in o_graph.subjects(None, x) if spec_url in x]
        if instances:
            string += '<div class="type">'
            string += '<h3 id="%s">%s<span> (%s)</span></h3>\n' % (get_prefix(x), get_prefix(x), len(instances))
            string += '<table class="table list-table"><tbody><tr>' + \
                create_row(sorted(instances)) + '</tr></tbody></table>'
            string += create_terms_html(sorted(instances), get_prefix(x))
            string += '<div/>'

    for x in types:
        instances = sorted([x for x in o_graph.subjects(None, x)])
        if any((y, RDF.type, x) in o_graph for y in instances) and grandchildren_exist(instances):
            string += '<h3>%s Instances</h3>\n' % get_prefix(x)
            for y in instances:
                if any(s in s for s in o_graph.subjects(RDF.type, y) if str(s) not in deprecated_uris):
                    instances2 = [get_uri_term(s) for s in o_graph.subjects(
                        RDF.type, y) if str(s) not in deprecated_uris]
                    string += '<div class="instancestype">'
                    title = str(get_label_dict(y))
                    string += '<h4 id="%s" title="%s"><a href="%s">%s</a><span> (%s)</span></h4>\n' % (get_prefix(y), title, get_link(y),
                                                                                                       get_prefix(y), len(instances2))
                    string += '<p class="h4 text-muted">%s</p>' % title
                    string += '<table class="table list-table"><tbody><tr>' + \
                        create_row(sorted(instances2)) + '</tr></tbody></table>'
                    # string += create_term_html(get_uri_term(y))
                    string += '</div>'
                    string += create_terms_html(sorted(instances2), get_prefix(y))
    return string


def specgen(template, language):
    global spec_url
    global spec_ns
    global spec_pre
    global ns_list
    global namespace_dict
    global symmetric_dict
    global inverse_dict

    # getting all namespaces from o_graph
    all_ns = [n for n in o_graph.namespace_manager.namespaces()]

    # creating a dictionary of the names spaces - {identifier:uri}
    namespace_dict = {key: value for (key, value) in all_ns}

    if spec_pre in namespace_dict:
        spec_url = namespace_dict[spec_pre]
    elif "" in namespace_dict:
        spec_url = namespace_dict['']
    else:
        spec_url = [x for x in o_graph.subjects(RDF.type, OWL.Ontology)]
        if spec_url:
            spec_url = spec_url[0]
        else:
            print("Unable to able to find the uri of your ontology")
            print("Please provide the uri of your ontology")
            spec_url = rdflib.URIRef(input("URI:"))
        # spec_url = rdflib.URIRef("http://semanticweb.cs.vu.nl/2009/11/sem/")
        spec_pre = {value: key for (key, value) in all_ns}[spec_url]

    spec_ns = rdflib.Namespace(spec_url)
    deprecated_html = create_deprecated_html(o_graph)

    parse_relations()
    symmetric_dict = create_symmetric_dict()
    inverse_dict = create_inverse_dict()

    azlist_html = newAZ(get_high_lvl_nodes())
    terms_html = all_terms_html(get_high_lvl_nodes())

    if spec_pre:
        if "{_header_}" in template:
            template = template.replace("{_header_}", get_header_html())

    template = template.replace("{_azlist_}", azlist_html)
    template = template.replace("{_terms_}", terms_html)
    if deprecated_uris:
        template = template.replace("{_deprecated_}", deprecated_html)
    else:
        template = template.replace("{_deprecated_}", "")
    # bibliography_html = all_terms_html(bibo_nodes)
    # template = template.replace("{_bibliography_}", newAZ(bibo_nodes) + bibliography_html)

    return template


def create_term_main(term, uri):
    label = str(get_label_dict(uri))
    defn = get_definition_list(uri)
    comment = get_comment_list(uri)

    inverse_uri = None
    if (uri, RDF.type, OWL.ObjectProperty) in o_graph and defn == [] and comment == []:
        if (uri, OWL.inverseOf, None) in o_graph:
            inverse_uri = [o for o in o_graph.objects(uri, OWL.inverseOf)][0]
        elif (None, OWL.inverseOf, uri) in o_graph:
            inverse_uri = [s for s in o_graph.subjects(OWL.inverseOf, uri)][0]

    html_str = '<p id="top">[<a href="#definition_list">back to top</a>]</p>\n'
    html_str += '<h5>%s</h5>\n' % (label)
    if inverse_uri:
        if lang == "fr":
            html_str += """<div class="defn">Inverse de a """
            html_str += '<a href="%s">%s</a>' % (get_link(inverse_uri), str(get_label_dict(inverse_uri)))
            html_str += ' dont la définition est la suivante: <div class="inverse"'
            html_str += '%s</div></div>' % (get_defn_html(get_definition_list(inverse_uri)))
        else:
            html_str += """<div class="defn">This is the inverse of """
            html_str += '<a href="%s">%s</a>' % (get_link(inverse_uri), str(get_label_dict(inverse_uri)))
            html_str += ' whose definition is as follows: <div class="inverse"'
            html_str += '%s</div></div>' % (get_defn_html(get_definition_list(inverse_uri)))
    else:
        html_str += """<div class="defn">%s</div>""" % (get_defn_html(defn))

    if comment:
        html_str += get_comment_html(comment)

    alt_terms = [o for o in o_graph.objects(uri, SKOS.altLabel)]
    if alt_terms:
        html_str += '<div class="altlabel">\n'
        html_str += '<p>[skos:altLabel: \n'
        html_str += '\n'
        for x in alt_terms:
            html_str += '<span>%s</span>\n' % (x)
        html_str += ']</p>\n'
        html_str += '</div>\n'
    return html_str


def create_term_extra(term_dict, uri, term):
    html_str = ""
    pred_dict = {}
    for x in term_dict:
        pred_dict.update(get_prefix_ns_with_link(x).items())

    html_str += """<table class="term_extra table table-hover">\n"""
    html_str += """\t<tbody>\n"""
    html_str += "<tr>\n"
    html_str += "<th>URI:</th>\n"
    html_str += """<td class="uri"><a href="#%s">%s</a></td>\n""" % (term, uri)
    html_str += "</tr>\n"
    html_str += "<th>Tag:</th>\n"
    html_str += """<td>%s:%s</td>\n""" % (spec_pre, term)
    html_str += "</tr>\n"

    # TODO: figure out why this occurs
    pred_dict.pop("foaf1:subject", None)
    for x in sorted(pred_dict.keys()):
        html_str += "<tr>\n"
        title_str = ""
        if pred_dict[x][0] == '#':
            title_str = ' title="' + str(get_label_dict(get_full_uri(pred_dict[x][1:]))) + '" '
        else:
            title_str = ' target="_blank"'

        html_str += """<th><a href="%s"%s>%s</a>:</th>\n""" % (pred_dict[x], title_str, x)
        pred_uri = pred_dict[x]
        if pred_dict[x][0] == '#':
            pred_uri = get_full_uri(pred_dict[x][1:])

        html_str += "<td>"
        for y in term_dict[pred_uri]:
            if x == "owl:oneOf":
                html_str += 'Contents Currently Unavailable'
            elif type(y) is not rdflib.term.Literal:
                title_str = ""
                if spec_url in y:
                    title_str = ' title="' + str(get_label_dict(y)) + '" '
                else:
                    title_str = ' target="_blank"'
                html_str += '<a href="%s"%s>%s</a>' % (
                    get_link(y), title_str, get_prefix(y))
            else:
                html_str += '%s' % (y)
            html_str += ' '
        html_str += "</td>"
        html_str += "</tr>\n"
    html_str += create_term_symmetric_html(uri)
    html_str += create_term_inverse_html(uri)

    instance_list = [get_uri_term(str(s)) for s in o_graph.subjects(
        RDF.type, uri) if str(s) not in deprecated_uris]
    if instance_list:
        html_str += "<tr class=\"instances\">\n"
        html_str += """<th><a href="#%s" title="%s Instances" >Instances</a>:</th>\n""" % (
            spec_pre + "%3A" + term, spec_pre + ":" + term)
        # html_str += create_row(sorted(instance_list), listitem=False)
        html_str += create_row(sorted(instance_list))
        html_str += "</tr>\n"

    html_str += "</tbody>\n"
    html_str += "</table>\n"
    return html_str


def create_term_inverse_html(uri):
    html_str = ""
    for x in inverse_dict.keys():
        if str(uri) in inverse_dict[x]:
            html_str += "<tr>\n"
            html_str += """<th>%s:</th>\n""" % inverse_r[x]
            html_str += "<td>\n"
            for y in sorted(inverse_dict[x][str(uri)]):
                if str(y) not in deprecated_uris:
                    html_str += '<a href="%s" title="%s">%s</a> ' % (
                        get_link(y), str(get_label_dict(rdflib.term.URIRef(y))), get_prefix(y))
            html_str += "</td>\n"
            html_str += "</tr>\n"

    return html_str


def create_term_symmetric_html(uri):
    html_str = ""
    for x in symmetric_dict.keys():
        if str(uri) in symmetric_dict[x]:
            html_str += "<tr>\n"
            html_str += """<th>*%s:</th>\n""" % get_prefix(x)
            html_str += "<td>\n"

            sym_uri = symmetric_dict[x][str(uri)]
            if str(sym_uri) not in deprecated_uris:
                html_str += '<a href="%s" title="%s">%s</a> ' % (
                    get_link(sym_uri), str(get_label_dict(rdflib.term.URIRef(sym_uri))), get_prefix(sym_uri))
            html_str += "</td>\n"
            html_str += "</tr>\n"

    return html_str


def create_terms_html(term_list, list_type):
    html_str = ""
    for uri in term_list:
        html_str += create_term_html(uri)
    return html_str


def create_term_html(uri):
    html_str = ""
    full_uri = get_full_uri(uri)
    html_str += '<section class="specterm" id="%s">\n' % uri
    html_str += create_term_main(uri, full_uri)

    term_dict = {}
    predicates = sorted(list(set([p for p in o_graph.predicates(full_uri, None)
                                  if (p not in term_main_uris) and (p not in term_ignore_uris)])))

    for predicate in predicates:
        objects = [o for o in o_graph.objects(full_uri, predicate) if(type(o) == rdflib.term.Literal and (
            o.language == lang or o.language is None)) or (type(o) is not rdflib.term.Literal)]
        term_dict[predicate] = sorted(objects)

    html_str += create_term_extra(term_dict, full_uri, uri) + '\n</section>\n'
    return html_str


def get_comment_list(uri):
    comment = o_graph.objects(uri, RDFS.comment)
    test = [str(x) for x in comment if x.language == lang]
    # comment = [str(x) for x in comment]
    if test:
        return test

    for s, p, o in o_graph.triples((uri, RDFS.comment, None)):
        return[o]


def get_label_dict(uri):
    temp = get_uri_term(uri)
    label = o_graph.objects(uri, RDFS.label)
    for x in label:
        temp = x
        if x.language == lang:
            return x
    return (temp)


def get_prefix(uri):
    uri_list = []
    if "#" in uri:
        uri_list.append(uri.split("#")[0] + "#")
        uri_list.append(uri.split("#")[1])
    else:
        if uri[-1] == '/':
            temp = uri[:-1].split("/")
        else:
            temp = uri.split("/")
        ident = temp[-1]
        uri_list.append(uri.split(ident)[0])
        uri_list.append(ident)

    for k, v in namespace_dict.items():
        if uri_list[0] == str(v):
            if k == "":
                # Must be base xml
                temp = uri_list[0].split("/")[-1][:-1]
                tempkey = (temp) + ":" + uri_list[1]
                return tempkey
            else:
                tempkey = str(k) + ":" + uri_list[1]
                return tempkey

    return uri


def get_link(uri):
    if spec_url in uri:
        return("#" + uri.split(spec_url)[1])
    else:
        return uri


def get_prefix_ns_with_link(uri):
    uri_list = []
    if "#" in uri:
        uri_list.append(uri.split("#")[0] + "#")
        uri_list.append(uri.split("#")[1])
    else:
        if uri[-1] == '/':
            temp = uri[:-1].split("/")
        else:
            temp = uri.split("/")
        ident = temp[-1]
        uri_list.append(uri.split(ident)[0])
        uri_list.append(ident)

    uri_dict = {}
    for k, v in namespace_dict.items():
        if uri_list[0] == str(v):
            if k == "":
                # Must be base xml
                temp = uri_list[0].split("/")[-1][:-1]
                tempkey = (temp) + ":" + uri_list[1]
                uri_dict[tempkey] = "#" + uri_list[1]
            else:
                tempkey = str(k) + ":" + uri_list[1]
                uri_dict[tempkey] = uri

    if len(uri_dict.keys()) == 0:
        uri_dict[uri] = uri
    return uri_dict


def get_definition_list(uri):
    defn = o_graph.objects(uri, SKOS.definition)
    return [str(x) for x in defn if x.language == lang and str(x) != ""]


def get_comment_html(comm_list):
    html_str = "<div class=\"comment\">"
    if lang == "fr":
        html_str += "<p>Note: "
    else:
        html_str += "<p>Comment: "
    for x in comm_list:
        if x:
            html_str += "%s<br/>" % x
    html_str += "</p></div>\n"
    return html_str


def get_defn_html(defn_list):
    counter = 1
    html_str = ""
    for x in defn_list:
        if x:
            if len(defn_list) != 1:
                html_str += "<p><em>%d</em>- %s</p>\n" % (counter, x)
            else:
                html_str += "<p>%s</p>\n" % (x)
        counter += 1
    return html_str


def get_dl_html(prefix_str, term_dict, prefix):
    html_str = ""
    if prefix in term_dict:
        if term_dict[prefix]:
            html_str += "<dl>\n"
            html_str += "<dt>%s:</dt>\n" % prefix_str
            for x in term_dict[prefix]:
                label = None
                if spec_pre in x:
                    label = get_label_dict(get_full_uri(x.split(":")[1]))
                if label:
                    html_str += '<dd><a href="%s" style="font-family: monospace;" title="%s">%s</a></dd>' % (
                        term_dict[prefix][x], str(label), str(x))
                else:
                    html_str += '<dd><a href="%s" style="font-family: monospace;">%s</a></dd>' % (
                        term_dict[prefix][x], str(x))
            html_str += "</dl>\n"
    return html_str


def get_dep_term_html(term_dict):
    label = str(term_dict["label"])
    uri = str(term_dict["uri"])
    term = get_uri_term(uri)
    comment = term_dict["comment"]
    defn = term_dict["defn"]
    replacement = str(term_dict["replacement"])

    html_str = ""
    html_str += '<div class="specterm" id="%s">\n' % term
    html_str += '<p id="top">[<a href="#deprecated_list">back to top</a>]</p>'
    html_str += '<h5>%s:%s</h5>\n' % (spec_pre, term)
    html_str += """<p class="uri">URI: <a href="%s">%s</a></p>\n""" % (uri, uri)
    if label:
        html_str += "<p><em>%s</em></p>" % label
    if defn:
        html_str += """<p>%s</p>""" % (str(defn))
    if comment:
        html_str += "<p>Comment: %s</p>" % comment
    if replacement:
        if spec_pre in replacement:
            html_str += """<p class="uri">Replaced by: <a href="#%s">%s</a></p>\n""" % (replacement.split("#")[
                1], get_prefix(replacement))
        else:
            if replacement != "None":
                html_str += """<p class="uri">Replaced by: <a href="%s">%s</a></p>\n""" % (
                    replacement, get_prefix(replacement))

    html_str += "</div>\n"
    return html_str


def get_deprecated_terms(o_graph):
    query_str = """
select * where {
    ?uri <http://www.w3.org/2003/06/sw-vocab-status/ns#term_status> ?literal.
}
    """
    global deprecated_uris
    deprecated_uris = [str(row.uri) for row in o_graph.query(query_str) if str(row.literal) == "deprecated"]
    deprecated_uris = sorted(deprecated_uris)
    terms = [get_uri_term(s) for s in deprecated_uris]

    html_str = '<h3 id="deprecated_list" >Global Cross Reference of Deprecated Terms</h3>'
    html_str += '<div class="az_list deprecated_list">'
    html_str += create_link_lists(terms, "Deprecated Terms:<br/>")
    html_str += '</div><h3>Terms and details</h3>'
    html_str += "<div class=\"deprecated_term\">"

    for uri in deprecated_uris:
        query_str = """
        select ?label ?y ?comment ?defn where {
            OPTIONAL { <%s> rdfs:comment ?comment. FILTER(langMatches(lang(?comment), "%s"))}.
            OPTIONAL { <%s> rdfs:label ?label.  FILTER(langMatches(lang(?label), "%s"))}.
            OPTIONAL { <%s> skos:definition ?defn. FILTER(langMatches(lang(?defn), "%s"))}.
            OPTIONAL { <%s> dcterms:isReplacedBy ?y. }.
        }
            """ % (uri, lang, uri, lang, uri, lang, uri)

        label = ""
        comment = ""
        defn = ""
        replacement = ""
        for row in o_graph.query(query_str):
            label = row.label

            temp = row.comment
            if temp:
                if temp.language == lang:
                    comment = temp

            defn = row.defn
            replacement = row.y

        term_dict = {
            "uri": uri,
            "label": label,
            "comment": comment,
            "defn": defn,
            "replacement": replacement,
        }
        html_str += get_dep_term_html(term_dict)
    html_str += "</div>"
    return html_str


def get_full_uri(string):
    return spec_url + string


def create_deprecated_html(o_graph):
    return get_deprecated_terms(o_graph)


def get_contributors():
    query_str = """
        select distinct ?x ?y where {
            ?person loc:ctb ?name .
                ?name foaf:name ?x .
            OPTIONAL { ?name foaf:homepage ?y }.
        }
    """
    names = {}
    for row in o_graph.query(query_str):
        if row.x.language == lang or row.x.language is None:
            names[str(row.x)] = str(row.y)

    name_list = [str(x) for x in names.keys()]
    name_list = sorted(sorted(name_list), key=lambda n: n.split()[1])
    html_str = "<dt>%s:</dt>\n" % trans_dict["contrib"][l_index]
    for x in name_list:
        html_str += "<dd>\n"
        if names[x] != 'None':
            html_str += '<a href="%s" target="_blank">%s</a>' % (names[x], x)
        else:
            html_str += x
        html_str += "</dd>\n"
    return html_str


def get_authors_html():
    query_str = """
        select distinct ?x ?y where {
            ?person dcterms:creator ?name .
                ?name foaf:name ?x .
            OPTIONAL { ?name foaf:homepage ?y }.
        }
    """
    names = {}
    for row in o_graph.query(query_str):
        names[str(row.x)] = str(row.y)

    # sort names based on last name
    name_list = [str(x) for x in names.keys()]
    name_list = sorted(sorted(name_list), key=lambda n: n.split()[1])
    html_str = "<dt>%s:</dt>\n" % trans_dict["authors"][l_index]
    for x in name_list:
        html_str += "<dd>\n"
        if names[x] != 'None':
            html_str += '<a href="%s" target="_blank">%s</a>' % (names[x], x)
        else:
            html_str += x
        html_str += "</dd>\n"
    return html_str


def save(template, dest, stdout=False):
    if stdout:
        print(template)
    else:
        f = open(dest, "w")
        f.write(template)
        f.close()


def get_webpage_title(url):
    title = url
    try:
        webpage = urllib.request.urlopen(url).read()
        title = str(webpage).split('<title>')[1].split('</title>')[0]
    except urllib.error.URLError:
        print("%s is currently inaccessible" % url)
        print("Unable to retrieve title from webpage.\n")
    return title


def get_header_html():
    header = get_header()
    # print(header)
    html_str = """<h1 id="title">%s %s %s</h1>\n""" % (header["title"][0],
                                                       trans_dict["specification"][l_index],
                                                       header["version"][0])
    if header["logo"]:
        html_str += """<img src="%s" class="logo" width="350"/>\n""" % header["logo"][0]

    html_str += """<h2 id="subtitle">%s</h2>\n""" % header["desc"][0]
    html_str += """<h3 id="mymw-doctype">%s &mdash; %s""" % (trans_dict["draft"][l_index], header["date_str"])

    url = "/".join(spec_url.split("/")[:-1]) + "/" + spec_pre + "-" + header["date"]
    latest_url = url.replace("-" + header["date"], "")
    curr_url = url
    version_type = "English"

    if lang == "en":
        version_type = "Française"
        url += "-FR.html"
    else:
        url += "-EN.html"

    html_str += """ (<a href="%s">Version %s</a>)</h3>\n""" % (url, version_type)
    html_str += "<dl>\n"
    if header["prior"]:
        prior = header["prior"][0]
        html_str += """<dt>%s:</dt>\n""" % trans_dict["previous_ver"][l_index]
        html_str += """<dd><a href="%s">%s</a>\n""" % (prior, prior)
        html_str += """(<a href="%s.rdf">owl - rdf/xml</a>, """ % (prior)
        html_str += """<a href="%s.ttl">ttl</a>, <a href="%s.nt">nt</a>)\n""" % (prior, prior)
        html_str += """</dd>\n"""

    html_str += """<dt>%s:</dt>\n""" % (trans_dict["current_ver"][l_index])
    html_str += """<dd><a href="%s.html">%s.html</a>\n""" % (curr_url, curr_url)
    html_str += """(<a href="%s.rdf">owl-rdf/xml</a>,\n""" % (curr_url)
    html_str += """<a href="%s.ttl">ttl</a>,\n""" % (curr_url)
    html_str += """<a href="%s.nt">nt</a>)\n""" % (curr_url)
    html_str += """</dd>\n"""

    html_str += """<dt>%s:</dt>\n""" % (trans_dict["latest_ver"][l_index])
    if lang == "en":
        html_str += """<dd><a href="%s.html">%s.html</a>\n""" % (latest_url, latest_url)
    else:
        html_str += """<dd><a href="%s-FR.html">%s.html</a>\n""" % (latest_url, latest_url)

    html_str += """(<a href="%s.rdf">owl-rdf/xml</a>,\n""" % (latest_url)
    html_str += """<a href="%s.ttl">ttl</a>,\n""" % (latest_url)
    html_str += """<a href="%s.nt">nt</a>)\n""" % (latest_url)

    if lang == "en":
        html_str += """<a href="%s-FR.html">(Version %s)</a>\n""" % (latest_url, version_type)
    else:
        html_str += """<a href="%s.html">(Version %s)</a>\n""" % (latest_url, version_type)

    html_str += """</dd>\n"""
    html_str += """<dt>%s: %s</dt>\n""" % (trans_dict["last_ver"][l_index], header["version"][0])
    html_str += """<dd>Date: %s</dd>\n""" % header["date_str"]
    html_str += get_authors_html()
    html_str += get_contributors()
    html_str += "<dt>%s:</dt>\n" % trans_dict["subjects"][l_index]
    for subj in header["subj"]:
        html_str += "<dd>\n"
        html_str += '<a href="%s" target="_blank">%s</a>' % (subj, get_webpage_title(subj))
        html_str += "</dd>\n"

    html_str += "</dl>\n"
    return(html_str)


def get_header():
    import datetime
    header_info = {}
    ontology_uri = rdflib.URIRef(spec_url[:-1])

    header_info["desc"] = [str(o) for o in o_graph.objects(
        ontology_uri, DCTERMS.description) if o.language == lang]
    header_info["title"] = [str(o) for o in o_graph.objects(ontology_uri, DCTERMS.title) if o.language == lang]
    header_info["version"] = [str(o) for o in o_graph.objects(ontology_uri, OWL.versionInfo)]
    header_info["logo"] = [str(o) for o in o_graph.objects(ontology_uri, FOAF.logo)]
    header_info["prior"] = [str(o) for o in o_graph.objects(ontology_uri, OWL.priorVersion)]
    header_info["rights"] = [str(o) for o in o_graph.objects(ontology_uri, DCTERMS.rights)]
    header_info["subj"] = [str(o) for o in o_graph.objects(ontology_uri, DCTERMS.subject)]
    pre_date = [str(o) for o in o_graph.objects(ontology_uri, DCTERMS.date)][0].split("-")
    if len(pre_date) != 3:
        header_info["date_str"] = str(datetime.date.today().strftime("%d %B %Y"))
        header_info["date"] = str(datetime.date.today())
    else:
        header_info["date"] = "-".join(pre_date)
        header_info["date_str"] = str(datetime.date(int(pre_date[0]), int(
            pre_date[1]), int(pre_date[2])).strftime("%d %B %Y"))

    return header_info


def main():
    global lang
    global spec_pre
    global dest
    global l_index

    if (len(sys.argv) > 5):
        print("Too many arguments provided")
        print_usage()
    elif (len(sys.argv) < 5):
        print("Too few arguments provided")
        print_usage()
    specloc = sys.argv[1]
    temploc = sys.argv[2]
    dest = sys.argv[3]
    lang = sys.argv[4]
    template = None

    if lang.lower() not in ["en", "fr"]:
        print("Language selected is currently not supported")
        print_usage()

    lang = lang.lower()
    l_index = 0
    if lang == "fr":
        l_index = 1

    try:
        f = open(temploc, "r")
        template = f.read()
    except Exception as e:
        print("Error reading from template \"" + temploc + "\": " + str(e))
        print_usage()

    open_graph(specloc)
    # TODO add alternate way of getting the namespace uri/prefix
    spec_pre = [str(o) for o in o_graph.objects(None, VANN.preferredNamespacePrefix)]
    if spec_pre:
        spec_pre = spec_pre[0]
    else:
        spec_pre = None
    #     # exit()

    print("\n" * 3)

    template = specgen(template, lang)
    template += "<!-- specification regenerated by DocGen on %s-->" % time.strftime("%A, %B %d at %I:%M:%S %p %Z")
    save(template, dest)


if __name__ == "__main__":
    main()
