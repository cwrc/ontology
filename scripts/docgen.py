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
o_graph = None
ns_list = {
    "content": "http://purl.org/rss/1.0/modules/content/",
    "dbpedia": "http://dbpedia.org/resource/",
    "dc": "http://purl.org/dc/elements/1.1/",
    "dcterms": "http://purl.org/dc/terms/",
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
    "xsd": "http://www.w3.org/2001/XMLSchema#",
    "cwrc": "http://sparql.cwrc.ca/ontologies/cwrc#",
    "vann": "http://purl.org/vocab/vann/"

}

# Important nspaces
RDF = rdflib.Namespace(ns_list["rdf"])
RDFS = rdflib.Namespace(ns_list["rdfs"])
SKOS = rdflib.Namespace(ns_list["skos"])
OWL = rdflib.Namespace(ns_list["owl"])
FOAF = rdflib.Namespace(ns_list["foaf"])
VS = rdflib.Namespace(ns_list["vs"])
VANN = rdflib.Namespace(ns_list["vann"])
PROV = rdflib.Namespace(ns_list["prov"])
CWRC = rdflib.Namespace(ns_list["cwrc"])
DCTERMS = rdflib.Namespace(ns_list["dcterms"])

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
    "listterm": ["Detailed references for all terms, classes and properties", "Références détaillées pour tous les termes, classes et propriétés"],
    "classes": ["Classes", "Classes"],
    "props": ["Properties", "Propriétés"],
    "dicts": ["Dictionaries", "Dictionnaires"]
}


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


def insert_dictionary(where, key, value):
    if key not in where:
        where[key] = []
    if value not in where[key]:
        where[key].append(value)


def get_domain_range_dict():
    range_list = set(sorted(o_graph.objects(None, RDFS.range)))
    domain_list = set(sorted(o_graph.objects(None, RDFS.domain)))

    domain_dict = {}
    for domain_class in domain_list:
        query_str = "select ?x where {?x rdfs:domain <" + str(domain_class) + ">}"
        dom_props = []
        for row in o_graph.query(query_str):
            dom_props.append(str(row.x))
        domain_dict[str(domain_class)] = dom_props

    range_dict = {}
    for range_class in range_list:
        query_str = "select ?x where {?x rdfs:range <" + str(range_class) + ">}"
        rang_props = []
        for row in o_graph.query(query_str):
            rang_props.append(str(row.x))
        range_dict[str(range_class)] = rang_props

    return domain_dict, range_dict


def get_uri_term(uri):
    string = str(uri)
    index = max(uri.rfind('#'), uri.rfind('/')) + 1
    substring = string[index:]
    return (substring)


def get_instances(class_list):
    instances = []
    for owl_class in class_list:
        class_uri = spec_ns[owl_class]
        for s, p, o in o_graph.triples((None, RDF.type, class_uri)):
            instances.append(get_uri_term(s))

    instances = sorted(list(set(instances)))
    return instances


def create_link_lists(list, name):
    string = "<p>%s" % name
    for x in list:
        title = str(get_label_dict(get_full_uri(x)))
        string += '<span class="list-item"><a href="#%s" title="%s">%s</a>,</span>' % (x, title, x)
    string += "</p>"
    ' '.join(string.split())
    return(string)


def get_azlist_html(az_dict, list):
    string = '<div class="az_list">'
    for key in list:
        string += create_link_lists(az_dict[key], key)
    string += '</div>'
    return string


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


def specgen(template, language):
    global spec_url
    global spec_ns
    global ns_list

    # getting all namespaces from o_graph
    all_ns = [n for n in o_graph.namespace_manager.namespaces()]

    # creating a dictionary of the names spaces - {identifier:uri}
    global namespace_dict
    namespace_dict = {key: value for (key, value) in all_ns}

    spec_url = namespace_dict['']
    spec_ns = rdflib.Namespace(spec_url)
    ns_list[spec_pre] = spec_url

    # Gets sorted classes & property labels

    class_list = [get_uri_term((x)) for x in sorted(o_graph.subjects(None, OWL.Class))]

    prop_list = [get_uri_term((x)) for x in sorted(o_graph.subjects(None, OWL.ObjectProperty))]

    global domain_dict
    global range_dict
    domain_dict, range_dict = get_domain_range_dict()

    # Dict_list in specgen
    skos_concepts = [get_uri_term(s) for s, p, o in sorted(
        o_graph.triples((None, RDF.type, SKOS.ConceptScheme)))]
    instance_list = get_instances(class_list)

    # Build HTML list of terms.
    dict_str = trans_dict["dicts"][l_index] + ":"
    props_str = trans_dict["props"][l_index] + ":"
    az_dict = {
        "Classes:": class_list,
        props_str: prop_list,
        "Instances:": instance_list,
        dict_str: skos_concepts,
    }
    temp_list = [dict_str, "Classes:", props_str, "Instances:"]

    # create global cross reference
    azlist_html = get_azlist_html(az_dict, temp_list)

    # Creating rest of html
    dict_html = create_dictionary_html(skos_concepts)
    classes_html = "<h3 id='classes'>Classes</h3>" + create_term_html(class_list, "Class")
    prop_html = "<h3 id='properties'>%s</h3>" % props_str[:-1] + create_term_html(prop_list, "Property")
    instance_html = "<h3 id='instances'>Instances</h3>" + create_term_html(instance_list, "Instance")
    deprecated_html = create_deprecated_html(o_graph)

    terms_html = dict_html + classes_html + prop_html + instance_html

    template = template.format(_header_=get_header_html(), _azlist_=azlist_html,
                               _terms_=terms_html, _deprecated_=deprecated_html)
    return template


def create_term_html(list, list_type):
    html_str = ""
    for x in list:
        uri = get_full_uri(x)
        term_dict = {
            "uri": uri,
            "label": get_label_dict(uri),
            "defn": get_definition_list(uri),
            "comment": get_comment_list(uri),
            "derived": get_ns_obj(uri, PROV.derivedFrom)
        }
        term_dict["contraryTo"] = cwrc_specific_properties(uri)
        term_dict["broader"] = get_ns_obj(uri, SKOS.broader)
        term_dict["narrower"] = get_ns_obj(uri, SKOS.narrower)
        term_dict["broader-trans"] = get_ns_obj(uri, SKOS.broaderTransitive)
        term_dict["narrower-trans"] = get_ns_obj(uri, SKOS.narrowerTransitive)

        if list_type == "Instance":
            term_dict["rdf-type"] = get_ns_obj(uri, RDF.type)
        elif list_type == "Class":
            term_dict["same-as"] = get_ns_obj(uri, OWL.sameAs)
            term_dict["subclass"] = get_ns_obj(uri, RDFS.subClassOf)

            if str(uri) in domain_dict:
                temp = domain_dict[str(uri)]
                temp_dict = {}
                for y in temp:
                    temp_dict.update(get_prefix_ns_with_link(y))
                term_dict["in-domain"] = temp_dict
            if str(uri) in range_dict:
                temp = range_dict[str(uri)]
                temp_dict = {}
                for y in temp:
                    temp_dict.update(get_prefix_ns_with_link(y))
                term_dict["in-range"] = temp_dict

        elif list_type == "Property":
            term_dict["range"] = get_ns_obj(uri, RDFS.range)
            term_dict["domain"] = get_ns_obj(uri, RDFS.domain)
            term_dict["subproperty"] = get_ns_obj(uri, RDFS.subPropertyOf)

        html_str += get_term_html(term_dict, list_type)
    return html_str


def cwrc_specific_properties(uri):
    if spec_pre in ["cwrc", "genre"]:
        return get_ns_obj(uri, CWRC.contraryTo)


def get_comment_list(uri):
    comment = [o for s, p, o in o_graph.triples(((uri, RDFS.comment, None)))]
    comment_list = []
    for x in comment:
        if x.language == lang:
            comment_list.append(str(x))

    return comment_list


def get_label_dict(uri):
    label = [o for s, p, o in o_graph.triples(((uri, RDFS.label, None)))]
    for x in label:
        if x.language == lang:
            return x
    return (None)


def get_prefix_ns_with_link(uri):
    uri_list = []
    if "#" in uri:
        uri_list.append(uri.split("#")[0] + "#")
        uri_list.append(uri.split("#")[1])
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


def get_ns_obj(uri, ns_uri):
    uris = [str(o) for s, p, o in o_graph.triples(((uri, ns_uri, None)))]
    ns_dict = {}
    for uri in uris:
        ns_dict.update(get_prefix_ns_with_link(uri))
    if ns_dict:
        return ns_dict


def get_definition_list(uri):
    defn = [o for s, p, o in o_graph.triples(((uri, SKOS.definition, None)))]
    defn_list = []
    for x in defn:
        if x.language == lang:
            tempstr = str(x)
            defn_list.append(tempstr)
    return defn_list


def create_dictionary_html(dictionary):
    html_str = "<h3 id= 'dictionaries'>%s</h3>" % trans_dict["dicts"][l_index]

    for term in dictionary:
        uri = spec_url + term
        label = get_label_dict(uri)
        comment = get_comment_list(uri)

        html_str += '<div class="specterm" id="%s">\n' % term
        html_str += '<p id="top">[<a href="#definition_list">back to top</a>]</p>'
        html_str += '<h3>Dictionary: %s:%s</h3>\n' % (spec_pre, term)
        html_str += """<p class="uri">URI: <a href="#%s">%s</a></p>\n""" % (term, uri)
        html_str += """<p><em>%s</em></p>""" % (label)
        html_str += """<div class="defn">%s</div>""" % (get_defn_html(get_definition_list(uri)))
        html_str += """<div class = "conceptlist">"""
        instance_list = [str(s).split("#")[1] for s, p, o in o_graph.triples((None, SKOS.inScheme, uri))]
        html_str += create_link_lists(instance_list, "Concepts:")
        html_str += "</div>\n"

        if comment:
            html_str += get_comment_html(comment)
        html_str += "</div>\n"
    return html_str


def get_comment_html(comm_list):
    html_str = "<div class=\"comment\">"
    html_str += "<p>Comment:</p>\n<p>"
    for x in comm_list:
        if x:
            html_str += "%s<br>" % x
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


def get_term_html(term_dict, term_type):
    label = str(term_dict["label"])
    uri = str(term_dict["uri"])
    term = get_uri_term(uri)
    comment = term_dict["comment"]
    defn = term_dict["defn"]

    html_str = ""
    html_str += '<div class="specterm" id="%s">\n' % term
    html_str += '<p id="top">[<a href="#definition_list">back to top</a>]</p>'
    html_str += '<h3>%s: %s:%s</h3>\n' % (term_type, spec_pre, term)
    html_str += """<p class="uri">URI: <a href="#%s">%s</a></p>\n""" % (term, uri)
    html_str += """<p><em>%s</em></p>""" % (label)
    html_str += """<div class="defn">%s</div>""" % (get_defn_html(defn))
    if comment:
        html_str += get_comment_html(comment)

    prefix_list = [
        "derived", "rdf-type", "same-as", "subclass", "in-domain", "in-range", "range", "domain",
        "subproperty", "broader-trans", "narrower-trans", "contraryTo"
    ]
    prefix_dict = {
        "derived": "PROV Derived From",
        "rdf-type": "RDF Type",
        "same-as": "Same As",
        "subclass": "Sub Class of",
        "in-domain": "In Domain of",
        "in-range": "In Range of",
        "range": "Range",
        "domain": "Domain",
        "subproperty": "Subproperty",
        "contraryTo": "Contrary to",
        "broader": "Broader",
        "narrower": "Narrower",
        "broader-trans": "Broader Transitive",
        "narrower-trans": "Narrower Transitive"
    }

    for prefix in prefix_list:
        html_str += get_dl_html(prefix_dict[prefix], term_dict, prefix)
    html_str += "\n</div>\n"

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
    html_str += '<h3>Term: %s:%s</h3>\n' % (spec_pre, term)
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
            html_str += """<p class="uri">Replaced by: <a href="%s">%s</a></p>\n""" % (replacement, replacement)

    html_str += "</div>\n"
    return html_str


def get_deprecated_terms(o_graph):
    query_str = """
select * where {
    ?uri vs:term_status ?literal.
}
    """
    deprecated_uris = []
    for row in o_graph.query(query_str):
        if str(row.literal) == "deprecated":
            deprecated_uris.append(str(row.uri))

    deprecated_uris = sorted(deprecated_uris)
    terms = [get_uri_term(s) for s in deprecated_uris]

    html_str = '<h3 id="deprecated_list" >Global Cross Reference of Deprecated Terms</h3>'
    html_str += '<div class="az_list deprecated_list">'
    html_str += create_link_lists(terms, "Deprecated Terms:<br>")
    html_str += '</div><h3>Detailed references for all terms, classes and properties</h3>'
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
    # filter(
    #     langMatches(lang(?name), "%s"))
    # )
    # % lang
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
    html_str = """<h1 id="title">%s %s %s</h1>\n""" % (header["title"]
                                                       [0], trans_dict["specification"][l_index], header["version"][0])
    if header["logo"]:
        html_str += """<img src="%s" align="right" width="350">\n""" % header["logo"][0]

    html_str += """<h2 id="subtitle">%s</h2>\n""" % header["desc"][0]
    html_str += """<h3 id="mymw-doctype">%s &mdash; %s""" % (trans_dict["draft"][l_index], header["date_str"])
    url = "/".join(spec_url.split("/")[:-1]) + "/" + spec_pre + "-"
    curr_url = url + header["date"]
    latest_url = url[:-1]
    version_type = "English"
    if lang == "en":
        version_type = "Française"
    url += header["date"] + "-FR.html"
    html_str += """(<a href="%s">Version %s</a>)</h3>\n""" % (url, version_type)
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

    template = specgen(template, lang)
    template += "<!-- specification regenerated by DocGen on %s-->" % time.strftime("%A, %B %d at %I:%M:%S %p %Z")
    save(template, dest)


if __name__ == "__main__":
    main()
