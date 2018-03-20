#!/usr/bin/python3
import sys
import rdflib
import time
import urllib.request

# temp log library for debugging
# from log import *
# log = Log("log/docgen")
# log.test_name("Debugging Document Generator")

spec_url = None
spec_ns = None
spec_pre = None
lang = None
bibo_nodes = None
o_graph = None
deprecated_uris = None

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
    "subjects": ["Subject Headings", "Sujects"],
    "listterm": ["Detailed references for all terms, classes and properties",
                 "Références détaillées pour tous les termes, classes et propriétés"],
    "classes": ["Classes", "Classes"],
    "props": ["Properties", "Propriétés"],
    "dicts": ["Dictionaries", "Dictionnaires"]
}
term_main_uris = [rdflib.term.URIRef('http://www.w3.org/2000/01/rdf-schema#label'), rdflib.term.URIRef(
    'http://www.w3.org/2004/02/skos/core#definition'),
    rdflib.term.URIRef('http://www.w3.org/2000/01/rdf-schema#comment')]
term_ignore_uris = [rdflib.term.URIRef('http://www.w3.org/1999/02/22-rdf-syntax-ns#value'), rdflib.term.URIRef(
    'http://rdfs.org/ns/void#inDataset'), rdflib.term.URIRef('http://www.w3.org/2000/01/rdf-schema#isDefinedBy')]


def print_usage():
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


def get_domain_range_dict():
    range_list = set(sorted(o_graph.objects(None, RDFS.range)))
    domain_list = set(sorted(o_graph.objects(None, RDFS.domain)))

    domain_dict = {}
    for domain_class in domain_list:
        query_str = "select ?x where {?x rdfs:domain <" + str(domain_class) + ">}"
        domain_dict[str(domain_class)] = [str(row.x) for row in o_graph.query(query_str)]

    range_dict = {}
    for range_class in range_list:
        query_str = "select ?x where {?x rdfs:range <" + str(range_class) + ">}"
        range_dict[str(range_class)] = [str(row.x) for row in o_graph.query(query_str)]

    return domain_dict, range_dict


def get_uri_term(uri):
    string = str(uri)
    index = max(uri.rfind('#'), uri.rfind('/')) + 1
    substring = string[index:]
    return (substring)


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
    namespace_manager = rdflib.namespace.NamespaceManager(rdflib.Graph())
    o_graph.namespace_manager = namespace_manager
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
    global bibo_nodes

    from lxml import etree
    parser = etree.XMLParser(strip_cdata=False, remove_comments=True)
    with open(file, "rb") as source:
        tree = etree.parse(source, parser=parser)
        root = tree.getroot()

    ignore_uris = [rdflib.term.URIRef("http://rdfs.org/ns/void#Dataset"),
                   rdflib.term.URIRef("http://www.w3.org/2002/07/owl#Ontology"),
                   rdflib.term.URIRef("http://www.w3.org/1999/02/22-rdf-syntax-ns#Description"),
                   rdflib.term.URIRef("http://www.w3.org/2002/07/owl#DeprecatedClass"),
                   rdflib.term.URIRef("http://www.w3.org/2004/02/skos/core#Concept"),
                   rdflib.term.URIRef("http://www.w3.org/2002/07/owl#DeprecatedProperty")]
    types = sorted(list(set([etreetag_to_uri(x.tag) for x in root if etreetag_to_uri(x.tag) not in ignore_uris])))
    bibo_nodes = [x for x in types if ("purl.org/ontology/bibo/" in str(x))]

    for x in bibo_nodes:
        types.remove(x)

    return types


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
    string = ""
    string += '<div class="global-ref">'

    string += '<table class="table table-hover">'
    string += '<thead>\n\t<tr>'
    string += '    <th scope="col">rdf:type</th>'
    string += '    <th scope="col">Instance</th>'
    string += '  </tr>\n\t</thead>\n<tbody>'
    for x in types:
        string += '<tr>'
        name = '<a href="%s" style="font-weight:bold;">%s:</a>' % (get_link(x), get_prefix(x))
        string += '  <th scope="row">%s</th>' % name
        instances = [get_uri_term(x) for x in o_graph.subjects(None, x)]
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
                    name = '<a href="%s" style="font-weight:bold;">%s:</a>' % (get_link(y), get_prefix(y))
                    instances = [get_uri_term(s) for s, p, o in o_graph.triples(
                        (None, RDF.type, y)) if str(s) not in deprecated_uris]
                    string += '<tr>'
                    string += '  <th scope="row">%s</th>' % name
                    string += create_row(sorted(instances))
                    string += '</tr>'
            string += '</tbody>'
            string += '</table>'
    string += '</div>'

    return string


def all_terms_html(nodes):
    types = [x for x in nodes if spec_url not in x]
    instanceTypes = sorted(list(set(nodes) - set(types)))
    string = ""
    for x in types:
        string += '<div class="type">'
        string += '<h3 id="%s">%s</h3>\n' % (get_prefix(x), get_prefix(x))
        instances = [get_uri_term(x) for x in o_graph.subjects(None, x)]
        string += create_terms_html(sorted(instances), get_prefix(x))
        string += '<div/>'

    for x in types:
        if any((y, RDF.type, x) in o_graph for y in instanceTypes):
            string += '<h3>%s Instances</h3>\n' % get_prefix(x)
            for y in instanceTypes:
                if (y, RDF.type, x) in o_graph:
                    instances = [get_uri_term(s) for s, p, o in o_graph.triples(
                        (None, RDF.type, y)) if str(s) not in deprecated_uris]
                    string += '<hr/>'
                    string += '<h4>%s</h4>\n' % get_prefix(y)
                    string += create_terms_html(sorted(instances), get_prefix(y))
    return string


def specgen(template, language):
    global spec_url
    global spec_ns
    global ns_list
    global namespace_dict

    # getting all namespaces from o_graph
    all_ns = [n for n in o_graph.namespace_manager.namespaces()]

    # creating a dictionary of the names spaces - {identifier:uri}
    namespace_dict = {key: value for (key, value) in all_ns}
    if spec_pre in namespace_dict:
        spec_url = namespace_dict[spec_pre]
    else:
        spec_url = namespace_dict['']

    spec_ns = rdflib.Namespace(spec_url)

    deprecated_html = create_deprecated_html(o_graph)

    global domain_dict
    global range_dict
    domain_dict, range_dict = get_domain_range_dict()
    azlist_html = newAZ(get_high_lvl_nodes())
    terms_html = all_terms_html(get_high_lvl_nodes())
    bibliography_html = all_terms_html(bibo_nodes)

    template = template.replace("{_header_}", get_header_html())
    template = template.replace("{_azlist_}", azlist_html)
    template = template.replace("{_terms_}", terms_html)
    template = template.replace("{_deprecated_}", deprecated_html)
    # template = template.replace("{_bibliography_}", newAZ(bibo_nodes) + bibliography_html)

    return template


def create_term_header(list_type, term, uri):
    html_str = '<p id="top">[<a href="#definition_list">back to top</a>]</p>\n'
    html_str += '<h5>%s:%s</h5>\n' % (spec_pre, term)
    html_str += """<p class="uri">URI: <a href="#%s">%s</a></p>\n""" % (term, uri)
    return html_str


def create_term_main(term, uri):
    label = str(get_label_dict(uri))
    defn = get_definition_list(uri)
    comment = get_comment_list(uri)

    html_str = '<p id="top">[<a href="#definition_list">back to top</a>]</p>\n'
    html_str += '<h5>%s</h5>\n' % (label)
    # html_str += '<h5>%s:%s</h5>\n' % (spec_pre, term)
    # html_str = """<p><em>%s</em></p>""" % (label)
    html_str += """<div class="defn">%s</div>""" % (get_defn_html(defn))
    if comment:
        html_str += get_comment_html(comment)
    return html_str
    # <section id="term-Activity">
    # <h3>Activity</h3>
    # <p>
    #         An activity period, defining when an artist was musically active.
    #     </p>
    # <table class="table table-hover">
    #   <tbody><tr><th>URI:</th> <td><a href="http://purl.org/ontology/mo/Activity">http://purl.org/ontology/mo/Activity</a></td></tr>
    # <tr><th>Label:</th> <td>activity</td></tr>
    # <tr><th>Status:</th> <td>testing</td></tr>
    # <tr><th>Parent Class:</th> <td><a href="http://purl.org/NET/c4dm/event.owl#Event">http://purl.org/NET/c4dm/event.owl#Event</a></td></tr>
    # </tbody></table>
    # </section>


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

    pred_dict.pop("foaf1:subject", None)
    for x in sorted(pred_dict.keys()):
        html_str += "<tr>\n"
        html_str += """<th><a href="%s">%s</a>:</th>\n""" % (pred_dict[x], x)
        pred_uri = pred_dict[x]
        if pred_dict[x][0] == '#':
            pred_uri = get_full_uri(pred_dict[x][1:])

        html_str += "<td>"
        for y in term_dict[pred_uri]:
            if x == "owl:oneOf":
                html_str += 'Contents Currently Unavailable'
            elif type(y) is not rdflib.term.Literal:
                html_str += '<a href="%s">%s</a>' % (
                    get_link(y), get_prefix(y))
            else:
                html_str += '%s' % (y)
            html_str += ' '
        html_str += "</td>"
        html_str += "</tr>\n"
    html_str += create_term_domran(uri)
    instance_list = [get_uri_term(str(s)) for s, p, o in o_graph.triples(
        (None, RDF.type, uri)) if str(s) not in deprecated_uris]
    if instance_list:
        html_str += "<tr>\n"
        html_str += """<th>Concepts:</th>\n"""
        html_str += create_row(sorted(instance_list), listitem=False)
        html_str += "</tr>\n"

    html_str += "</tbody>\n"
    html_str += "</table>\n"
    return html_str


def create_term_domran(uri):
    html_str = ""
    if str(uri) in domain_dict:
        html_str += "<tr>\n"
        html_str += """<th>Within Domain:</th>\n"""
        html_str += """<td>\n"""
        for x in domain_dict[str(uri)]:
            if str(x) not in deprecated_uris:
                html_str += '<a href="%s">%s</a> ' % (get_link(x), get_prefix(x))
        html_str += "</td>\n"
        html_str += "</tr>\n"
    if str(uri) in range_dict:
        html_str += "<tr>\n"
        html_str += """<th>Within Range:</th>\n"""
        html_str += "<td>\n"
        for x in range_dict[str(uri)]:
            if str(x) not in deprecated_uris:
                html_str += '<a href="%s">%s</a> ' % (
                    get_link(x), get_prefix(x))
        html_str += "</td>\n"
        html_str += "</tr>\n"
    return html_str

# def createOneOfCollectionHTML(uri):
#     p
#     # if https://www.w3.org/2002/07/owl#oneOf:
#         # pass


def create_terms_html(term_list, list_type):
    html_str = ""
    for uri in term_list:
        full_uri = get_full_uri(uri)
        html_str += '<section class="specterm" id="%s">\n' % uri
        # html_str += create_term_header(list_type, uri, full_uri)
        html_str += create_term_main(uri, full_uri)

        term_dict = {}
        predicates = sorted(list(set([p for s, p, o in o_graph.triples(
            (full_uri, None, None)) if (p not in term_main_uris) and (p not in term_ignore_uris)])))

        for predicate in predicates:
            objects = [o for o in o_graph.objects(full_uri, predicate) if(type(o) == rdflib.term.Literal and (
                o.language == lang or o.language is None)) or (type(o) is not rdflib.term.Literal)]
            term_dict[predicate] = sorted(objects)

        html_str += create_term_extra(term_dict, full_uri, uri)
        html_str += '</section>\n'

    return html_str


def get_comment_list(uri):
    comment = [o for s, p, o in o_graph.triples(((uri, RDFS.comment, None)))]
    return [str(x) for x in comment if x.language == lang]


def get_label_dict(uri):
    label = [o for s, p, o in o_graph.triples(((uri, RDFS.label, None)))]
    for x in label:
        if x.language == lang:
            return x
    return (None)


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
    defn = [o for s, p, o in o_graph.triples(((uri, SKOS.definition, None)))]
    return [str(x) for x in defn if x.language == lang]


def get_comment_html(comm_list):
    html_str = "<div class=\"comment\">"
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
    defn = str(term_dict["defn"])
    replacement = str(term_dict["replacement"])

    html_str = ""
    html_str += '<div class="specterm" id="%s">\n' % term
    html_str += '<p id="top">[<a href="#deprecated_list">back to top</a>]</p>'
    html_str += '<h5>%s:%s</h5>\n' % (spec_pre, term)
    html_str += """<p class="uri">URI: <a href="%s">%s</a></p>\n""" % (uri, uri)
    if label:
        html_str += "<p><em>%s</em></p>" % label
    if defn:
        html_str += """<p>%s</p>""" % (defn)
    if comment:
        html_str += "<p>Comment: %s</p>" % comment
    if replacement:
        if spec_pre in replacement:
            html_str += """<p class="uri">Replaced by: <a href="#%s">%s</a></p>\n""" % (replacement.split("#")[
                1], replacement)
        else:
            if replacement != "None":
                html_str += """<p class="uri">Replaced by: <a href="%s">%s</a></p>\n""" % (
                    replacement, replacement)

    html_str += "</div>\n"
    return html_str


def get_deprecated_terms(o_graph):
    query_str = """
select * where {
    ?uri vs:term_status ?literal.
}
    """
    global deprecated_uris
    deprecated_uris = [str(row.uri) for row in o_graph.query(query_str) if str(row.literal) == "deprecated"]
    deprecated_uris = sorted(deprecated_uris)
    terms = [get_uri_term(s) for s in deprecated_uris]

    html_str = '<h4 id="deprecated_list" >Global Cross Reference of Deprecated Terms</h4>'
    html_str += '<div class="az_list deprecated_list">'
    html_str += create_link_lists(terms, "Deprecated Terms:<br/>")
    html_str += '</div><h4>Terms and details</h4>'
    html_str += "<div class=\"deprecated_term\">"

    for uri in deprecated_uris:
        query_str = """
        select distinct ?label ?y ?defn ?comment where {
            OPTIONAL { <%s> rdfs:comment ?comment. }.
            OPTIONAL { <%s> rdfs:label ?label. }.
            OPTIONAL { <%s> skos:definition ?defn. }.
            OPTIONAL { <%s> dcterms:isReplacedBy ?y. }.
            filter(
                langMatches(lang(?defn), "%s") && langMatches(lang(?label), "%s")
            )
        }
            """ % (uri, uri, uri, uri, lang, lang)

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
            html_str += '<a href="%s">%s</a>' % (names[x], x)
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
            html_str += '<a href="%s">%s</a>' % (names[x], x)
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
        html_str += """<img src="%s" align="right" width="350"/>\n""" % header["logo"][0]

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
        html_str += """(<a href="%s.owl">owl - rdf/xml</a>, """ % (prior)
        html_str += """<a href="%s.ttl">ttl</a>, <a href="%s.nt">nt</a>)\n""" % (prior, prior)
        html_str += """</dd>\n"""

    html_str += """<dt>%s:</dt>\n""" % (trans_dict["current_ver"][l_index])
    html_str += """<dd><a href="%s.html">%s.html</a>\n""" % (curr_url, curr_url)
    html_str += """(<a href="%s.owl">owl-rdf/xml</a>,\n""" % (curr_url)
    html_str += """<a href="%s.ttl">ttl</a>,\n""" % (curr_url)
    html_str += """<a href="%s.nt">nt</a>)\n""" % (curr_url)
    html_str += """</dd>\n"""

    html_str += """<dt>%s:</dt>\n""" % (trans_dict["latest_ver"][l_index])
    html_str += """<dd><a href="%s.html">%s.html</a>\n""" % (latest_url, latest_url)
    html_str += """(<a href="%s.owl">owl-rdf/xml</a>,\n""" % (latest_url)
    html_str += """<a href="%s.ttl">ttl</a>,\n""" % (latest_url)
    html_str += """<a href="%s.nt">nt</a>)\n""" % (latest_url)
    html_str += """</dd>\n"""
    html_str += """<dt>%s: %s</dt>\n""" % (trans_dict["last_ver"][l_index], header["version"][0])
    html_str += """<dd>Date: %s</dd>\n""" % header["date_str"]
    html_str += get_authors_html()
    html_str += get_contributors()
    html_str += "<dt>%s:</dt>\n" % trans_dict["subjects"][l_index]
    for subj in header["subj"]:
        html_str += "<dd>\n"
        html_str += '<a href="%s">%s</a>' % (subj, get_webpage_title(subj))
        html_str += "</dd>\n"

    html_str += "</dl>\n"
    return(html_str)


def get_header():
    import datetime
    header_info = {}
    ontology_uri = rdflib.URIRef(spec_url[:-1])
    header_info["desc"] = [str(o) for s, p, o in o_graph.triples(
        (ontology_uri, DCTERMS.description, None)) if o.language == lang]
    header_info["title"] = [str(o) for s, p, o in o_graph.triples(
        (ontology_uri, DCTERMS.title, None)) if o.language == lang]
    header_info["version"] = [str(o) for s, p, o in o_graph.triples(
        (ontology_uri, OWL.versionInfo, None))]
    header_info["logo"] = [str(o) for s, p, o in o_graph.triples(
        (ontology_uri, FOAF.logo, None))]
    header_info["prior"] = [str(o) for s, p, o in o_graph.triples(
        (ontology_uri, OWL.priorVersion, None))]
    header_info["rights"] = [str(o) for s, p, o in o_graph.triples(
        (ontology_uri, DCTERMS.rights, None))]
    header_info["subj"] = [str(o) for s, p, o in o_graph.triples(
        (ontology_uri, DCTERMS.subject, None))]
    pre_date = [str(o) for s, p, o in o_graph.triples(
        (ontology_uri, DCTERMS.date, None))][0].split("-")
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
    spec_pre = [str(o) for s, p, o in o_graph.triples(((None, VANN.preferredNamespacePrefix, None)))][0]

    print("\n" * 3)

    template = specgen(template, lang)
    template += "<!-- specification regenerated by DocGen on %s-->" % time.strftime("%A, %B %d at %I:%M:%S %p %Z")
    save(template, dest)


if __name__ == "__main__":
    main()
