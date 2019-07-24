<?xml version="1.0"?>


<!DOCTYPE rdf:RDF [
    <!ENTITY terms "http://purl.org/dc/terms/" >
    <!ENTITY foaf "http://xmlns.com/foaf/0.1/" >
    <!ENTITY vann "http://purl.org/vocab/vann/" >
    <!ENTITY owl "http://www.w3.org/2002/07/owl#" >
    <!ENTITY bibo "http://purl.org/ontology/bibo/" >
    <!ENTITY xsd "http://www.w3.org/2001/XMLSchema#" >
    <!ENTITY event "http://purl.org/NET/c4dm/event.owl#" >
    <!ENTITY skos "http://www.w3.org/2004/02/skos/core#" >
    <!ENTITY status "http://purl.org/ontology/bibo/status/" >
    <!ENTITY rdfs "http://www.w3.org/2000/01/rdf-schema#" >
    <!ENTITY degrees "http://purl.org/ontology/bibo/degrees/" >
    <!ENTITY rdf "http://www.w3.org/1999/02/22-rdf-syntax-ns#" >
    <!ENTITY ns "http://www.w3.org/2003/06/sw-vocab-status/ns#" >
    <!ENTITY schema "http://schemas.talis.com/2005/address/schema#" >
    <!ENTITY prism "http://prismstandard.org/namespaces/1.2/basic/" >
]>


<rdf:RDF xmlns="http://purl.org/ontology/bibo/"
     xml:base="http://purl.org/ontology/bibo/"
     xmlns:schema="http://schemas.talis.com/2005/address/schema#"
     xmlns:ns="http://www.w3.org/2003/06/sw-vocab-status/ns#"
     xmlns:owl="http://www.w3.org/2002/07/owl#"
     xmlns:xsd="http://www.w3.org/2001/XMLSchema#"
     xmlns:skos="http://www.w3.org/2004/02/skos/core#"
     xmlns:rdfs="http://www.w3.org/2000/01/rdf-schema#"
     xmlns:degrees="&bibo;degrees/"
     xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"
     xmlns:terms="http://purl.org/dc/terms/"
     xmlns:bibo="http://purl.org/ontology/bibo/"
     xmlns:event="http://purl.org/NET/c4dm/event.owl#"
     xmlns:vann="http://purl.org/vocab/vann/"
     xmlns:prism="http://prismstandard.org/namespaces/1.2/basic/"
     xmlns:foaf="http://xmlns.com/foaf/0.1/"
     xmlns:status="&bibo;status/">
    <owl:Ontology rdf:about="http://purl.org/ontology/bibo/">
        <owl:versionInfo>http://purl.org/ontology/bibo/1.3/</owl:versionInfo>
        <terms:title>The Bibliographic Ontology</terms:title>
        <terms:description xml:lang="en">The Bibliographic Ontology describes
bibliographic things on the semantic Web in RDF.  This ontology can be
used as a citation ontology, as a document classification ontology, or
simply as a way to describe any kind of document in RDF. It has been
inspired by many existing document description metadata formats, and
can be used as a common ground for converting other bibliographic data
sources.</terms:description>
        <terms:creator rdf:resource="&bibo;bdarcus"/>
        <terms:creator rdf:resource="&bibo;fgiasson"/>
    </owl:Ontology>
    


    <!-- 
    ///////////////////////////////////////////////////////////////////////////////////////
    //
    // Annotation properties
    //
    ///////////////////////////////////////////////////////////////////////////////////////
     -->

    


    <!-- http://purl.org/dc/terms/creator -->

    <owl:AnnotationProperty rdf:about="&terms;creator"/>
    


    <!-- http://purl.org/dc/terms/description -->

    <owl:AnnotationProperty rdf:about="&terms;description">
        <skos:scopeNote xml:lang="en">Used to describe a bibliographic resource.</skos:scopeNote>
    </owl:AnnotationProperty>
    


    <!-- http://purl.org/dc/terms/identifier -->

    <owl:AnnotationProperty rdf:about="&terms;identifier"/>
    


    <!-- http://purl.org/dc/terms/title -->

    <owl:AnnotationProperty rdf:about="&terms;title">
        <skos:scopeNote xml:lang="en">Used to describe the title of a bibliographic resource</skos:scopeNote>
    </owl:AnnotationProperty>
    


    <!-- http://www.w3.org/2002/07/owl#deprecated -->

    <owl:AnnotationProperty rdf:about="&owl;deprecated"/>
    


    <!-- http://www.w3.org/2003/06/sw-vocab-status/ns#term_status -->

    <owl:AnnotationProperty rdf:about="&ns;term_status"/>
    


    <!-- http://www.w3.org/2004/02/skos/core#changeNote -->

    <owl:AnnotationProperty rdf:about="&skos;changeNote"/>
    


    <!-- http://www.w3.org/2004/02/skos/core#editorialNote -->

    <owl:AnnotationProperty rdf:about="&skos;editorialNote"/>
    


    <!-- http://www.w3.org/2004/02/skos/core#example -->

    <owl:AnnotationProperty rdf:about="&skos;example"/>
    


    <!-- http://www.w3.org/2004/02/skos/core#historyNote -->

    <owl:AnnotationProperty rdf:about="&skos;historyNote"/>
    


    <!-- http://www.w3.org/2004/02/skos/core#note -->

    <owl:AnnotationProperty rdf:about="&skos;note"/>
    


    <!-- http://www.w3.org/2004/02/skos/core#scopeNote -->

    <owl:AnnotationProperty rdf:about="&skos;scopeNote"/>
    


    <!-- 
    ///////////////////////////////////////////////////////////////////////////////////////
    //
    // Object Properties
    //
    ///////////////////////////////////////////////////////////////////////////////////////
     -->

    


    <!-- http://purl.org/NET/c4dm/event.owl#agent -->

    <owl:ObjectProperty rdf:about="&event;agent">
        <skos:changeNote xml:lang="en">Used to link an agent (a person) to an event (a conference, an hearing, etc.)</skos:changeNote>
    </owl:ObjectProperty>
    


    <!-- http://purl.org/NET/c4dm/event.owl#place -->

    <owl:ObjectProperty rdf:about="&event;place">
        <skos:scopeNote xml:lang="en">Used to relate an event such as a conference to the geographical place where it happens, for example Paris.</skos:scopeNote>
    </owl:ObjectProperty>
    


    <!-- http://purl.org/NET/c4dm/event.owl#produced_in -->

    <owl:ObjectProperty rdf:about="&event;produced_in"/>
    


    <!-- http://purl.org/NET/c4dm/event.owl#product -->

    <owl:ObjectProperty rdf:about="&event;product">
        <skos:scopeNote xml:lang="en">Used to link an event such as a conference to an outcome (a product) of that event, for example, an article, a proceeding, etc.</skos:scopeNote>
    </owl:ObjectProperty>
    


    <!-- http://purl.org/NET/c4dm/event.owl#sub_event -->

    <owl:ObjectProperty rdf:about="&event;sub_event">
        <skos:scopeNote xml:lang="en">Used to link big events with smaller events such as workshops that happen in the context of a conference.</skos:scopeNote>
    </owl:ObjectProperty>
    


    <!-- http://purl.org/NET/c4dm/event.owl#time -->

    <owl:ObjectProperty rdf:about="&event;time">
        <skos:scopeNote xml:lang="en">Used to describe the timing of an event. For example, when a conference starts and stops.</skos:scopeNote>
    </owl:ObjectProperty>
    


    <!-- http://purl.org/dc/terms/contributor -->

    <owl:ObjectProperty rdf:about="&terms;contributor">
        <skos:scopeNote xml:lang="en">Used to link a bibliographic item to one of its contributor: can be an author, an editor, a publisher, etc.</skos:scopeNote>
    </owl:ObjectProperty>
    


    <!-- http://purl.org/dc/terms/format -->

    <owl:ObjectProperty rdf:about="&terms;format">
        <skos:example xml:lang="en">&lt;dcterms:format&gt;
   &lt;dcterms:MediaTypeOrExtent&gt;
     &lt;rdf:value&gt;text/html&lt;/rdf:value&gt;
     &lt;rdfs:label&gt;HTML&lt;/rdfs:label&gt;
   &lt;/dcterms:MediaTypeOrExtent&gt;
 &lt;/dcterms:format&gt;</skos:example>
        <skos:scopeNote xml:lang="en">Used to describe the format of a bibliographic resource.</skos:scopeNote>
    </owl:ObjectProperty>
    


    <!-- http://purl.org/dc/terms/hasPart -->

    <owl:ObjectProperty rdf:about="&terms;hasPart"/>
    


    <!-- http://purl.org/dc/terms/isPartOf -->

    <owl:ObjectProperty rdf:about="&terms;isPartOf"/>
    


    <!-- http://purl.org/dc/terms/isReferencedBy -->

    <owl:ObjectProperty rdf:about="&terms;isReferencedBy">
        <skos:scopeNote xml:lang="en">Used to relate a reference citation to a bibliographic resource.</skos:scopeNote>
    </owl:ObjectProperty>
    


    <!-- http://purl.org/dc/terms/isVersionOf -->

    <owl:ObjectProperty rdf:about="&terms;isVersionOf"/>
    


    <!-- http://purl.org/dc/terms/language -->

    <owl:ObjectProperty rdf:about="&terms;language">
        <skos:scopeNote xml:lang="en">Used to link a bibliographic resource to the language used to express it.</skos:scopeNote>
    </owl:ObjectProperty>
    


    <!-- http://purl.org/dc/terms/publisher -->

    <owl:ObjectProperty rdf:about="&terms;publisher">
        <skos:scopeNote xml:lang="en">Used to link a bibliographic item to its publisher.</skos:scopeNote>
    </owl:ObjectProperty>
    


    <!-- http://purl.org/dc/terms/references -->

    <owl:ObjectProperty rdf:about="&terms;references"/>
    


    <!-- http://purl.org/dc/terms/relation -->

    <owl:ObjectProperty rdf:about="&terms;relation"/>
    


    <!-- http://purl.org/dc/terms/rights -->

    <owl:ObjectProperty rdf:about="&terms;rights">
        <skos:scopeNote xml:lang="en">Used to describe rights related to a bibliographic resource.</skos:scopeNote>
    </owl:ObjectProperty>
    


    <!-- http://purl.org/dc/terms/subject -->

    <owl:ObjectProperty rdf:about="&terms;subject">
        <skos:scopeNote xml:lang="en">Used to describe the subject of a bibliographic resource.</skos:scopeNote>
    </owl:ObjectProperty>
    


    <!-- http://purl.org/dc/terms/title -->

    <owl:ObjectProperty rdf:about="&terms;title">
        <skos:scopeNote xml:lang="en">Used to describe the title of a bibliographic resource</skos:scopeNote>
    </owl:ObjectProperty>
    


    <!-- http://purl.org/ontology/bibo/affirmedBy -->

    <owl:ObjectProperty rdf:about="&bibo;affirmedBy">
        <rdfs:isDefinedBy rdf:datatype="&xsd;anyURI">http://purl.org/ontology/bibo/</rdfs:isDefinedBy>
        <rdfs:comment xml:lang="en">A legal decision that affirms a ruling.</rdfs:comment>
        <rdfs:range rdf:resource="&bibo;LegalDecision"/>
        <rdfs:domain rdf:resource="&bibo;LegalDecision"/>
        <rdfs:subPropertyOf rdf:resource="&bibo;subsequentLegalDecision"/>
    </owl:ObjectProperty>
    


    <!-- http://purl.org/ontology/bibo/annotates -->

    <owl:ObjectProperty rdf:about="&bibo;annotates">
        <rdfs:label xml:lang="en">annotates</rdfs:label>
        <rdfs:isDefinedBy rdf:datatype="&xsd;anyURI">http://purl.org/ontology/bibo/</rdfs:isDefinedBy>
        <rdfs:comment xml:lang="en">Critical or explanatory note for a Document.</rdfs:comment>
        <ns:term_status>stable</ns:term_status>
        <rdfs:subPropertyOf rdf:resource="&terms;relation"/>
        <rdfs:domain rdf:resource="&bibo;Note"/>
        <rdfs:range rdf:resource="&rdfs;Resource"/>
    </owl:ObjectProperty>
    


    <!-- http://purl.org/ontology/bibo/authorList -->

    <owl:ObjectProperty rdf:about="&bibo;authorList">
        <rdfs:label xml:lang="en">list of authors</rdfs:label>
        <rdfs:isDefinedBy rdf:datatype="&xsd;anyURI">http://purl.org/ontology/bibo/</rdfs:isDefinedBy>
        <ns:term_status>stable</ns:term_status>
        <rdfs:comment xml:lang="en">An ordered list of authors. Normally, this list is seen as a priority list that order authors by importance.</rdfs:comment>
        <rdfs:domain rdf:resource="&bibo;Document"/>
        <rdfs:subPropertyOf rdf:resource="&bibo;contributorList"/>
        <rdfs:range>
            <owl:Class>
                <owl:unionOf rdf:parseType="Collection">
                    <rdf:Description rdf:about="&rdf;List"/>
                    <rdf:Description rdf:about="&rdf;Seq"/>
                </owl:unionOf>
            </owl:Class>
        </rdfs:range>
    </owl:ObjectProperty>
    


    <!-- http://purl.org/ontology/bibo/citedBy -->

    <owl:ObjectProperty rdf:about="&bibo;citedBy">
        <rdfs:label xml:lang="en">cited by</rdfs:label>
        <rdfs:isDefinedBy rdf:datatype="&xsd;anyURI">http://purl.org/ontology/bibo/</rdfs:isDefinedBy>
        <rdfs:comment xml:lang="en">Relates a document to another document that cites the
first document.</rdfs:comment>
        <ns:term_status>unstable</ns:term_status>
        <rdfs:domain rdf:resource="&bibo;Document"/>
        <rdfs:range rdf:resource="&bibo;Document"/>
        <owl:inverseOf rdf:resource="&bibo;cites"/>
    </owl:ObjectProperty>
    


    <!-- http://purl.org/ontology/bibo/cites -->

    <owl:ObjectProperty rdf:about="&bibo;cites">
        <rdfs:label xml:lang="en">cites</rdfs:label>
        <rdfs:isDefinedBy rdf:datatype="&xsd;anyURI">http://purl.org/ontology/bibo/</rdfs:isDefinedBy>
        <ns:term_status>unstable</ns:term_status>
        <rdfs:comment xml:lang="en">Relates a document to another document that is cited
by the first document as reference, comment, review, quotation or for
another purpose.</rdfs:comment>
        <rdfs:subPropertyOf rdf:resource="&terms;references"/>
        <rdfs:domain rdf:resource="&bibo;Document"/>
        <rdfs:range rdf:resource="&bibo;Document"/>
    </owl:ObjectProperty>
    


    <!-- http://purl.org/ontology/bibo/contributorList -->

    <owl:ObjectProperty rdf:about="&bibo;contributorList">
        <rdfs:label xml:lang="en">list of contributors</rdfs:label>
        <rdfs:isDefinedBy rdf:datatype="&xsd;anyURI">http://purl.org/ontology/bibo/</rdfs:isDefinedBy>
        <ns:term_status>stable</ns:term_status>
        <rdfs:comment xml:lang="en">An ordered list of contributors. Normally, this list is seen as a priority list that order contributors by importance.</rdfs:comment>
        <rdfs:domain rdf:resource="&bibo;Document"/>
        <rdfs:range>
            <owl:Class>
                <owl:unionOf rdf:parseType="Collection">
                    <rdf:Description rdf:about="&rdf;List"/>
                    <rdf:Description rdf:about="&rdf;Seq"/>
                </owl:unionOf>
            </owl:Class>
        </rdfs:range>
    </owl:ObjectProperty>
    


    <!-- http://purl.org/ontology/bibo/court -->

    <owl:ObjectProperty rdf:about="&bibo;court">
        <rdfs:label xml:lang="en">court</rdfs:label>
        <rdfs:isDefinedBy rdf:datatype="&xsd;anyURI">http://purl.org/ontology/bibo/</rdfs:isDefinedBy>
        <rdfs:comment xml:lang="en">A court associated with a legal document; for example, that which issues a decision.</rdfs:comment>
        <ns:term_status>unstable</ns:term_status>
        <rdfs:domain rdf:resource="&bibo;LegalDocument"/>
        <rdfs:range rdf:resource="&foaf;Organization"/>
    </owl:ObjectProperty>
    


    <!-- http://purl.org/ontology/bibo/degree -->

    <owl:ObjectProperty rdf:about="&bibo;degree">
        <rdfs:label xml:lang="en">degree</rdfs:label>
        <rdfs:isDefinedBy rdf:datatype="&xsd;anyURI">http://purl.org/ontology/bibo/</rdfs:isDefinedBy>
        <ns:term_status>unstable</ns:term_status>
        <rdfs:comment xml:lang="en">The thesis degree.</rdfs:comment>
        <skos:editorialNote xml:lang="en">We are not defining, using an enumeration, the range of the bibo:degree to the defined list of bibo:ThesisDegree. We won&apos;t do it because we want people to be able to define new degress if needed by some special usecases. Creating such an enumeration would restrict this to happen.</skos:editorialNote>
        <rdfs:domain rdf:resource="&bibo;Thesis"/>
        <rdfs:range rdf:resource="&bibo;ThesisDegree"/>
    </owl:ObjectProperty>
    


    <!-- http://purl.org/ontology/bibo/director -->

    <owl:ObjectProperty rdf:about="&bibo;director">
        <rdfs:label>director</rdfs:label>
        <rdfs:isDefinedBy rdf:datatype="&xsd;anyURI">http://purl.org/ontology/bibo/</rdfs:isDefinedBy>
        <rdfs:comment xml:lang="en">A Film director.</rdfs:comment>
        <ns:term_status>stable</ns:term_status>
        <rdfs:subPropertyOf rdf:resource="&terms;contributor"/>
        <rdfs:domain rdf:resource="&bibo;AudioVisualDocument"/>
        <rdfs:range rdf:resource="&foaf;Agent"/>
    </owl:ObjectProperty>
    


    <!-- http://purl.org/ontology/bibo/distributor -->

    <owl:ObjectProperty rdf:about="&bibo;distributor">
        <rdfs:label xml:lang="en">distributor</rdfs:label>
        <rdfs:isDefinedBy rdf:datatype="&xsd;anyURI">http://purl.org/ontology/bibo/</rdfs:isDefinedBy>
        <rdfs:comment xml:lang="en">Distributor of a document or a collection of documents.</rdfs:comment>
        <ns:term_status>stable</ns:term_status>
        <rdfs:range rdf:resource="&foaf;Agent"/>
        <rdfs:domain>
            <owl:Class>
                <owl:unionOf rdf:parseType="Collection">
                    <rdf:Description rdf:about="&bibo;Collection"/>
                    <rdf:Description rdf:about="&bibo;Document"/>
                </owl:unionOf>
            </owl:Class>
        </rdfs:domain>
    </owl:ObjectProperty>
    


    <!-- http://purl.org/ontology/bibo/editor -->

    <owl:ObjectProperty rdf:about="&bibo;editor">
        <rdfs:label>editor</rdfs:label>
        <rdfs:isDefinedBy rdf:datatype="&xsd;anyURI">http://purl.org/ontology/bibo/</rdfs:isDefinedBy>
        <rdfs:comment xml:lang="en">A person having managerial and sometimes policy-making responsibility for the editorial part of a publishing firm or of a newspaper, magazine, or other publication.</rdfs:comment>
        <ns:term_status>stable</ns:term_status>
        <rdfs:subPropertyOf rdf:resource="&terms;contributor"/>
        <rdfs:range rdf:resource="&foaf;Agent"/>
        <rdfs:domain>
            <owl:Class>
                <owl:unionOf rdf:parseType="Collection">
                    <rdf:Description rdf:about="&bibo;Collection"/>
                    <rdf:Description rdf:about="&bibo;Document"/>
                </owl:unionOf>
            </owl:Class>
        </rdfs:domain>
    </owl:ObjectProperty>
    


    <!-- http://purl.org/ontology/bibo/editorList -->

    <owl:ObjectProperty rdf:about="&bibo;editorList">
        <rdfs:label xml:lang="en">list of editors</rdfs:label>
        <rdfs:isDefinedBy rdf:datatype="&xsd;anyURI">http://purl.org/ontology/bibo/</rdfs:isDefinedBy>
        <rdfs:comment xml:lang="en">An ordered list of editors. Normally, this list is seen as a priority list that order editors by importance.</rdfs:comment>
        <ns:term_status>stable</ns:term_status>
        <rdfs:domain rdf:resource="&bibo;Document"/>
        <rdfs:subPropertyOf rdf:resource="&bibo;contributorList"/>
        <rdfs:range>
            <owl:Class>
                <owl:unionOf rdf:parseType="Collection">
                    <rdf:Description rdf:about="&rdf;List"/>
                    <rdf:Description rdf:about="&rdf;Seq"/>
                </owl:unionOf>
            </owl:Class>
        </rdfs:range>
    </owl:ObjectProperty>
    


    <!-- http://purl.org/ontology/bibo/interviewee -->

    <owl:ObjectProperty rdf:about="&bibo;interviewee">
        <rdfs:label>interviewee</rdfs:label>
        <rdfs:isDefinedBy rdf:datatype="&xsd;anyURI">http://purl.org/ontology/bibo/</rdfs:isDefinedBy>
        <ns:term_status>stable</ns:term_status>
        <rdfs:comment xml:lang="en">An agent that is interviewed by another agent.</rdfs:comment>
        <rdfs:subPropertyOf rdf:resource="&terms;contributor"/>
        <rdfs:domain rdf:resource="&foaf;Agent"/>
        <rdfs:range rdf:resource="&foaf;Agent"/>
    </owl:ObjectProperty>
    


    <!-- http://purl.org/ontology/bibo/interviewer -->

    <owl:ObjectProperty rdf:about="&bibo;interviewer">
        <rdfs:label>interviewer</rdfs:label>
        <rdfs:isDefinedBy rdf:datatype="&xsd;anyURI">http://purl.org/ontology/bibo/</rdfs:isDefinedBy>
        <rdfs:comment xml:lang="en">An agent that interview another agent.</rdfs:comment>
        <ns:term_status>stable</ns:term_status>
        <rdfs:subPropertyOf rdf:resource="&terms;contributor"/>
        <rdfs:range rdf:resource="&foaf;Agent"/>
        <rdfs:domain rdf:resource="&foaf;Agent"/>
    </owl:ObjectProperty>
    


    <!-- http://purl.org/ontology/bibo/issuer -->

    <owl:ObjectProperty rdf:about="&bibo;issuer">
        <rdfs:label>issuer</rdfs:label>
        <rdfs:isDefinedBy rdf:datatype="&xsd;anyURI">http://purl.org/ontology/bibo/</rdfs:isDefinedBy>
        <rdfs:comment>An entity responsible for issuing often informally published documents such as press releases, reports, etc.</rdfs:comment>
        <ns:term_status>unstable</ns:term_status>
        <rdfs:subPropertyOf rdf:resource="&terms;publisher"/>
        <rdfs:range rdf:resource="&foaf;Agent"/>
        <rdfs:domain>
            <owl:Class>
                <owl:unionOf rdf:parseType="Collection">
                    <rdf:Description rdf:about="&bibo;Collection"/>
                    <rdf:Description rdf:about="&bibo;Document"/>
                </owl:unionOf>
            </owl:Class>
        </rdfs:domain>
    </owl:ObjectProperty>
    


    <!-- http://purl.org/ontology/bibo/organizer -->

    <owl:ObjectProperty rdf:about="&bibo;organizer">
        <rdfs:label xml:lang="en">organizer</rdfs:label>
        <rdfs:isDefinedBy rdf:datatype="&xsd;anyURI">http://purl.org/ontology/bibo/</rdfs:isDefinedBy>
        <ns:term_status>unstable</ns:term_status>
        <rdfs:comment xml:lang="en">The organizer of an event; includes conference organizers, but also government agencies or other bodies that are responsible for conducting hearings.</rdfs:comment>
        <rdfs:domain rdf:resource="&event;Event"/>
        <rdfs:range rdf:resource="&foaf;Agent"/>
    </owl:ObjectProperty>
    


    <!-- http://purl.org/ontology/bibo/owner -->

    <owl:ObjectProperty rdf:about="&bibo;owner">
        <rdfs:label xml:lang="en">owner</rdfs:label>
        <rdfs:isDefinedBy rdf:datatype="&xsd;anyURI">http://purl.org/ontology/bibo/</rdfs:isDefinedBy>
        <ns:term_status>unstable</ns:term_status>
        <rdfs:comment xml:lang="en">Owner of a document or a collection of documents.</rdfs:comment>
        <rdfs:range rdf:resource="&foaf;Agent"/>
        <rdfs:domain>
            <owl:Class>
                <owl:unionOf rdf:parseType="Collection">
                    <rdf:Description rdf:about="&bibo;Collection"/>
                    <rdf:Description rdf:about="&bibo;Document"/>
                </owl:unionOf>
            </owl:Class>
        </rdfs:domain>
    </owl:ObjectProperty>
    


    <!-- http://purl.org/ontology/bibo/performer -->

    <owl:ObjectProperty rdf:about="&bibo;performer">
        <rdfs:label>performer</rdfs:label>
        <rdfs:isDefinedBy rdf:datatype="&xsd;anyURI">http://purl.org/ontology/bibo/</rdfs:isDefinedBy>
        <ns:term_status>stable</ns:term_status>
        <rdfs:subPropertyOf rdf:resource="&terms;contributor"/>
        <rdfs:domain rdf:resource="&bibo;Performance"/>
        <rdfs:range rdf:resource="&foaf;Agent"/>
    </owl:ObjectProperty>
    


    <!-- http://purl.org/ontology/bibo/presentedAt -->

    <owl:ObjectProperty rdf:about="&bibo;presentedAt">
        <rdfs:label xml:lang="en">presented at</rdfs:label>
        <rdfs:isDefinedBy rdf:datatype="&xsd;anyURI">http://purl.org/ontology/bibo/</rdfs:isDefinedBy>
        <ns:term_status>unstable</ns:term_status>
        <rdfs:comment xml:lang="en">Relates a document to an event; for example, a paper to a conference.</rdfs:comment>
        <rdfs:subPropertyOf rdf:resource="&event;produced_in"/>
        <rdfs:domain rdf:resource="&bibo;Document"/>
        <rdfs:range rdf:resource="&bibo;Event"/>
    </owl:ObjectProperty>
    


    <!-- http://purl.org/ontology/bibo/presents -->

    <owl:ObjectProperty rdf:about="&bibo;presents">
        <rdfs:label xml:lang="en">presents</rdfs:label>
        <rdfs:isDefinedBy rdf:datatype="&xsd;anyURI">http://purl.org/ontology/bibo/</rdfs:isDefinedBy>
        <rdfs:comment xml:lang="en">Relates an event to associated documents; for example, conference to a paper.</rdfs:comment>
        <ns:term_status>unstable</ns:term_status>
        <rdfs:subPropertyOf rdf:resource="&event;product"/>
        <rdfs:range rdf:resource="&bibo;Document"/>
        <rdfs:domain rdf:resource="&bibo;Event"/>
        <owl:inverseOf rdf:resource="&bibo;presentedAt"/>
    </owl:ObjectProperty>
    


    <!-- http://purl.org/ontology/bibo/producer -->

    <owl:ObjectProperty rdf:about="&bibo;producer">
        <rdfs:label xml:lang="en">producer</rdfs:label>
        <rdfs:isDefinedBy rdf:datatype="&xsd;anyURI">http://purl.org/ontology/bibo/</rdfs:isDefinedBy>
        <rdfs:comment xml:lang="en">Producer of a document or a collection of documents.</rdfs:comment>
        <ns:term_status>stable</ns:term_status>
        <rdfs:range rdf:resource="&foaf;Agent"/>
        <rdfs:domain>
            <owl:Class>
                <owl:unionOf rdf:parseType="Collection">
                    <rdf:Description rdf:about="&bibo;Collection"/>
                    <rdf:Description rdf:about="&bibo;Document"/>
                </owl:unionOf>
            </owl:Class>
        </rdfs:domain>
    </owl:ObjectProperty>
    


    <!-- http://purl.org/ontology/bibo/recipient -->

    <owl:ObjectProperty rdf:about="&bibo;recipient">
        <rdfs:label>recipient</rdfs:label>
        <rdfs:isDefinedBy rdf:datatype="&xsd;anyURI">http://purl.org/ontology/bibo/</rdfs:isDefinedBy>
        <rdfs:comment xml:lang="en">An agent that receives a communication document.</rdfs:comment>
        <ns:term_status>stable</ns:term_status>
        <rdfs:domain rdf:resource="&bibo;PersonalCommunicationDocument"/>
        <rdfs:range rdf:resource="&foaf;Agent"/>
    </owl:ObjectProperty>
    


    <!-- http://purl.org/ontology/bibo/reproducedIn -->

    <owl:ObjectProperty rdf:about="&bibo;reproducedIn">
        <rdfs:isDefinedBy rdf:datatype="&xsd;anyURI">http://purl.org/ontology/bibo/</rdfs:isDefinedBy>
        <rdfs:comment xml:lang="en">The resource in which another resource is reproduced.</rdfs:comment>
        <ns:term_status>unstable</ns:term_status>
        <rdfs:subPropertyOf rdf:resource="&terms;isPartOf"/>
        <rdfs:range rdf:resource="&bibo;Document"/>
        <rdfs:domain rdf:resource="&bibo;Document"/>
    </owl:ObjectProperty>
    


    <!-- http://purl.org/ontology/bibo/reversedBy -->

    <owl:ObjectProperty rdf:about="&bibo;reversedBy">
        <rdfs:isDefinedBy rdf:datatype="&xsd;anyURI">http://purl.org/ontology/bibo/</rdfs:isDefinedBy>
        <rdfs:comment xml:lang="en">A legal decision that reverses a ruling.</rdfs:comment>
        <rdfs:range rdf:resource="&bibo;LegalDecision"/>
        <rdfs:domain rdf:resource="&bibo;LegalDecision"/>
        <rdfs:subPropertyOf rdf:resource="&bibo;subsequentLegalDecision"/>
    </owl:ObjectProperty>
    


    <!-- http://purl.org/ontology/bibo/reviewOf -->

    <owl:ObjectProperty rdf:about="&bibo;reviewOf">
        <rdfs:label xml:lang="en">review of</rdfs:label>
        <rdfs:isDefinedBy rdf:datatype="&xsd;anyURI">http://purl.org/ontology/bibo/</rdfs:isDefinedBy>
        <rdfs:comment xml:lang="en">Relates a review document to a reviewed thing (resource, item, etc.).</rdfs:comment>
        <ns:term_status>stable</ns:term_status>
        <rdfs:subPropertyOf rdf:resource="&terms;relation"/>
        <rdfs:domain rdf:resource="&bibo;Document"/>
        <rdfs:range rdf:resource="&rdfs;Resource"/>
    </owl:ObjectProperty>
    


    <!-- http://purl.org/ontology/bibo/status -->

    <owl:ObjectProperty rdf:about="&bibo;status">
        <rdfs:label xml:lang="en">status</rdfs:label>
        <rdfs:isDefinedBy rdf:datatype="&xsd;anyURI">http://purl.org/ontology/bibo/</rdfs:isDefinedBy>
        <ns:term_status>stable</ns:term_status>
        <rdfs:comment xml:lang="en">The publication status of (typically academic) content.</rdfs:comment>
        <skos:editorialNote xml:lang="en">We are not defining, using an enumeration, the range of the bibo:status to the defined list of bibo:DocumentStatus. We won&apos;t do it because we want people to be able to define new status if needed by some special usecases. Creating such an enumeration would restrict this to happen.</skos:editorialNote>
        <rdfs:domain rdf:resource="&bibo;Document"/>
        <rdfs:range rdf:resource="&bibo;DocumentStatus"/>
    </owl:ObjectProperty>
    


    <!-- http://purl.org/ontology/bibo/subsequentLegalDecision -->

    <owl:ObjectProperty rdf:about="&bibo;subsequentLegalDecision">
        <rdfs:isDefinedBy rdf:datatype="&xsd;anyURI">http://purl.org/ontology/bibo/</rdfs:isDefinedBy>
        <rdfs:comment xml:lang="en">A legal decision on appeal that takes action on a case (affirming it, reversing it, etc.).</rdfs:comment>
        <rdfs:subPropertyOf rdf:resource="&terms;isReferencedBy"/>
        <rdfs:domain rdf:resource="&bibo;LegalDecision"/>
        <rdfs:range rdf:resource="&bibo;LegalDecision"/>
    </owl:ObjectProperty>
    


    <!-- http://purl.org/ontology/bibo/transcriptOf -->

    <owl:ObjectProperty rdf:about="&bibo;transcriptOf">
        <rdfs:label xml:lang="en">transcript of</rdfs:label>
        <rdfs:isDefinedBy rdf:datatype="&xsd;anyURI">http://purl.org/ontology/bibo/</rdfs:isDefinedBy>
        <rdfs:comment xml:lang="en">Relates a document to some transcribed original.</rdfs:comment>
        <ns:term_status>unstable</ns:term_status>
        <rdfs:subPropertyOf rdf:resource="&terms;relation"/>
        <rdfs:domain rdf:resource="&bibo;Document"/>
        <rdfs:range rdf:resource="&rdfs;Resource"/>
    </owl:ObjectProperty>
    


    <!-- http://purl.org/ontology/bibo/translationOf -->

    <owl:ObjectProperty rdf:about="&bibo;translationOf">
        <rdfs:label xml:lang="en">translation of</rdfs:label>
        <rdfs:isDefinedBy rdf:datatype="&xsd;anyURI">http://purl.org/ontology/bibo/</rdfs:isDefinedBy>
        <ns:term_status>stable</ns:term_status>
        <rdfs:comment xml:lang="en">Relates a translated document to the original document.</rdfs:comment>
        <rdfs:subPropertyOf rdf:resource="&terms;isVersionOf"/>
        <rdfs:range rdf:resource="&bibo;Document"/>
        <rdfs:domain rdf:resource="&bibo;Document"/>
    </owl:ObjectProperty>
    


    <!-- http://purl.org/ontology/bibo/translator -->

    <owl:ObjectProperty rdf:about="&bibo;translator">
        <rdfs:label>translator</rdfs:label>
        <rdfs:isDefinedBy rdf:datatype="&xsd;anyURI">http://purl.org/ontology/bibo/</rdfs:isDefinedBy>
        <ns:term_status>stable</ns:term_status>
        <rdfs:comment xml:lang="en">A person who translates written document from one language to another.</rdfs:comment>
        <rdfs:subPropertyOf rdf:resource="&terms;contributor"/>
        <rdfs:range rdf:resource="&foaf;Agent"/>
        <rdfs:domain>
            <owl:Class>
                <owl:unionOf rdf:parseType="Collection">
                    <rdf:Description rdf:about="&bibo;Collection"/>
                    <rdf:Description rdf:about="&bibo;Document"/>
                </owl:unionOf>
            </owl:Class>
        </rdfs:domain>
    </owl:ObjectProperty>
    


    <!-- http://www.w3.org/1999/02/22-rdf-syntax-ns#value -->

    <owl:ObjectProperty rdf:about="&rdf;value">
        <skos:scopeNote xml:lang="en">Used to describe the content of a bibo:Document and othr bibliographic resouces.

We suggest to use this property instead of the deprecated &quot;bibo:content&quot; one.</skos:scopeNote>
    </owl:ObjectProperty>
    


    <!-- http://xmlns.com/foaf/0.1/based_near -->

    <owl:ObjectProperty rdf:about="&foaf;based_near">
        <skos:scopeNote xml:lang="en">Used to link an agent, related to bibliographic things, to a place where it is based near: can be a city, a monument, a building, etc.</skos:scopeNote>
    </owl:ObjectProperty>
    


    <!-- http://xmlns.com/foaf/0.1/depiction -->

    <owl:ObjectProperty rdf:about="&foaf;depiction">
        <skos:scopeNote xml:lang="en">Used to link an agent with an image that depict it.</skos:scopeNote>
    </owl:ObjectProperty>
    


    <!-- http://xmlns.com/foaf/0.1/homepage -->

    <owl:ObjectProperty rdf:about="&foaf;homepage">
        <skos:scopeNote xml:lang="en">Used to link an agent to its homepage (which is a web page accessible using a URL).</skos:scopeNote>
    </owl:ObjectProperty>
    


    <!-- 
    ///////////////////////////////////////////////////////////////////////////////////////
    //
    // Data properties
    //
    ///////////////////////////////////////////////////////////////////////////////////////
     -->

    


    <!-- http://prismstandard.org/namespaces/1.2/basic/doi -->

    <owl:DatatypeProperty rdf:about="&prism;doi">
        <owl:equivalentProperty rdf:resource="&bibo;doi"/>
    </owl:DatatypeProperty>
    


    <!-- http://prismstandard.org/namespaces/1.2/basic/eIssn -->

    <owl:DatatypeProperty rdf:about="&prism;eIssn">
        <owl:equivalentProperty rdf:resource="&bibo;eissn"/>
    </owl:DatatypeProperty>
    


    <!-- http://prismstandard.org/namespaces/1.2/basic/edition -->

    <owl:DatatypeProperty rdf:about="&prism;edition">
        <owl:equivalentProperty rdf:resource="&bibo;edition"/>
    </owl:DatatypeProperty>
    


    <!-- http://prismstandard.org/namespaces/1.2/basic/endingPage -->

    <owl:DatatypeProperty rdf:about="&prism;endingPage">
        <owl:equivalentProperty rdf:resource="&bibo;pageEnd"/>
    </owl:DatatypeProperty>
    


    <!-- http://prismstandard.org/namespaces/1.2/basic/isbn -->

    <owl:DatatypeProperty rdf:about="&prism;isbn">
        <owl:equivalentProperty rdf:resource="&bibo;isbn"/>
    </owl:DatatypeProperty>
    


    <!-- http://prismstandard.org/namespaces/1.2/basic/issn -->

    <owl:DatatypeProperty rdf:about="&prism;issn">
        <owl:equivalentProperty rdf:resource="&bibo;issn"/>
    </owl:DatatypeProperty>
    


    <!-- http://prismstandard.org/namespaces/1.2/basic/issue -->

    <owl:DatatypeProperty rdf:about="&prism;issue">
        <owl:equivalentProperty rdf:resource="&bibo;issue"/>
    </owl:DatatypeProperty>
    


    <!-- http://prismstandard.org/namespaces/1.2/basic/number -->

    <owl:DatatypeProperty rdf:about="&prism;number">
        <owl:equivalentProperty rdf:resource="&bibo;locator"/>
    </owl:DatatypeProperty>
    


    <!-- http://prismstandard.org/namespaces/1.2/basic/startingPage -->

    <owl:DatatypeProperty rdf:about="&prism;startingPage">
        <owl:equivalentProperty rdf:resource="&bibo;pageStart"/>
    </owl:DatatypeProperty>
    


    <!-- http://prismstandard.org/namespaces/1.2/basic/volume -->

    <owl:DatatypeProperty rdf:about="&prism;volume">
        <owl:equivalentProperty rdf:resource="&bibo;volume"/>
    </owl:DatatypeProperty>
    


    <!-- http://purl.org/dc/terms/created -->

    <owl:DatatypeProperty rdf:about="&terms;created">
        <skos:scopeNote xml:lang="en">Used to describe the creation date of a bibliographic item</skos:scopeNote>
        <rdfs:subPropertyOf rdf:resource="&terms;date"/>
    </owl:DatatypeProperty>
    


    <!-- http://purl.org/dc/terms/date -->

    <owl:DatatypeProperty rdf:about="&terms;date">
        <skos:scopeNote xml:lang="en">Use to link a bibliographic item to the date of an event. Check dcterms:created and other for proper specializations for this property</skos:scopeNote>
    </owl:DatatypeProperty>
    


    <!-- http://purl.org/dc/terms/description -->

    <owl:DatatypeProperty rdf:about="&terms;description">
        <skos:scopeNote xml:lang="en">Used to describe a bibliographic resource.</skos:scopeNote>
    </owl:DatatypeProperty>
    


    <!-- http://purl.org/dc/terms/issued -->

    <owl:DatatypeProperty rdf:about="&terms;issued">
        <skos:scopeNote xml:lang="en">Used to describe the issue date of a bibliographic resource</skos:scopeNote>
        <rdfs:subPropertyOf rdf:resource="&terms;date"/>
    </owl:DatatypeProperty>
    


    <!-- http://purl.org/ontology/bibo/abstract -->

    <owl:DatatypeProperty rdf:about="&bibo;abstract">
        <rdfs:label>abstract</rdfs:label>
        <rdfs:isDefinedBy rdf:datatype="&xsd;anyURI">http://purl.org/ontology/bibo/</rdfs:isDefinedBy>
        <ns:term_status>stable</ns:term_status>
        <rdfs:comment>A summary of the resource.</rdfs:comment>
        <rdfs:range rdf:resource="&rdfs;Literal"/>
        <rdfs:domain rdf:resource="&rdfs;Resource"/>
    </owl:DatatypeProperty>
    


    <!-- http://purl.org/ontology/bibo/argued -->

    <owl:DatatypeProperty rdf:about="&bibo;argued">
        <rdfs:label xml:lang="en">date argued</rdfs:label>
        <rdfs:isDefinedBy rdf:datatype="&xsd;anyURI">http://purl.org/ontology/bibo/</rdfs:isDefinedBy>
        <rdfs:comment xml:lang="en">The date on which a legal case is argued before a court. Date is of format xsd:date</rdfs:comment>
        <ns:term_status>unstable</ns:term_status>
        <rdfs:domain rdf:resource="&bibo;LegalDocument"/>
        <rdfs:range rdf:resource="&rdfs;Literal"/>
    </owl:DatatypeProperty>
    


    <!-- http://purl.org/ontology/bibo/asin -->

    <owl:DatatypeProperty rdf:about="&bibo;asin">
        <rdfs:subPropertyOf rdf:resource="&bibo;identifier"/>
        <rdfs:range rdf:resource="&rdfs;Literal"/>
        <rdfs:domain>
            <owl:Class>
                <owl:unionOf rdf:parseType="Collection">
                    <rdf:Description rdf:about="&bibo;Collection"/>
                    <rdf:Description rdf:about="&bibo;Document"/>
                </owl:unionOf>
            </owl:Class>
        </rdfs:domain>
    </owl:DatatypeProperty>
    


    <!-- http://purl.org/ontology/bibo/chapter -->

    <owl:DatatypeProperty rdf:about="&bibo;chapter">
        <rdfs:label xml:lang="en">chapter</rdfs:label>
        <rdfs:isDefinedBy rdf:datatype="&xsd;anyURI">http://purl.org/ontology/bibo/</rdfs:isDefinedBy>
        <rdfs:comment xml:lang="en">An chapter number</rdfs:comment>
        <ns:term_status>unstable</ns:term_status>
        <rdfs:domain rdf:resource="&bibo;BookSection"/>
        <rdfs:subPropertyOf rdf:resource="&bibo;locator"/>
        <rdfs:range rdf:resource="&rdfs;Literal"/>
    </owl:DatatypeProperty>
    


    <!-- http://purl.org/ontology/bibo/coden -->

    <owl:DatatypeProperty rdf:about="&bibo;coden">
        <rdfs:subPropertyOf rdf:resource="&bibo;identifier"/>
        <rdfs:range rdf:resource="&rdfs;Literal"/>
        <rdfs:domain>
            <owl:Class>
                <owl:unionOf rdf:parseType="Collection">
                    <rdf:Description rdf:about="&bibo;Collection"/>
                    <rdf:Description rdf:about="&bibo;Document"/>
                </owl:unionOf>
            </owl:Class>
        </rdfs:domain>
    </owl:DatatypeProperty>
    


    <!-- http://purl.org/ontology/bibo/content -->

    <owl:DatatypeProperty rdf:about="&bibo;content">
        <rdfs:label xml:lang="en">content</rdfs:label>
        <rdfs:isDefinedBy rdf:datatype="&xsd;anyURI">http://purl.org/ontology/bibo/</rdfs:isDefinedBy>
        <owl:deprecated rdf:datatype="&xsd;boolean">true</owl:deprecated>
        <skos:historyNote xml:lang="en">bibo:content has been deprecated; we recommend to use &quot;rdf:value&quot; for this purpose. Here is the rational behind this choice: http://www.w3.org/TR/2004/REC-rdf-primer-20040210/#rdfvalue</skos:historyNote>
        <ns:term_status>unstable</ns:term_status>
        <rdfs:comment xml:lang="en">This property is for a plain-text rendering of the content of a Document. While the plain-text content of an entire document could be described by this property.</rdfs:comment>
        <rdfs:domain rdf:resource="&bibo;Document"/>
        <rdfs:range rdf:resource="&rdfs;Literal"/>
    </owl:DatatypeProperty>
    


    <!-- http://purl.org/ontology/bibo/doi -->

    <owl:DatatypeProperty rdf:about="&bibo;doi">
        <rdfs:subPropertyOf rdf:resource="&bibo;identifier"/>
        <rdfs:range rdf:resource="&rdfs;Literal"/>
        <rdfs:domain>
            <owl:Class>
                <owl:unionOf rdf:parseType="Collection">
                    <rdf:Description rdf:about="&bibo;Collection"/>
                    <rdf:Description rdf:about="&bibo;Document"/>
                </owl:unionOf>
            </owl:Class>
        </rdfs:domain>
    </owl:DatatypeProperty>
    


    <!-- http://purl.org/ontology/bibo/eanucc13 -->

    <owl:DatatypeProperty rdf:about="&bibo;eanucc13">
        <rdfs:subPropertyOf rdf:resource="&bibo;identifier"/>
        <rdfs:range rdf:resource="&rdfs;Literal"/>
        <rdfs:domain>
            <owl:Class>
                <owl:unionOf rdf:parseType="Collection">
                    <rdf:Description rdf:about="&bibo;Collection"/>
                    <rdf:Description rdf:about="&bibo;Document"/>
                </owl:unionOf>
            </owl:Class>
        </rdfs:domain>
    </owl:DatatypeProperty>
    


    <!-- http://purl.org/ontology/bibo/edition -->

    <owl:DatatypeProperty rdf:about="&bibo;edition">
        <rdfs:label xml:lang="en">edition</rdfs:label>
        <rdfs:isDefinedBy rdf:datatype="&xsd;anyURI">http://purl.org/ontology/bibo/</rdfs:isDefinedBy>
        <ns:term_status>stable</ns:term_status>
        <rdfs:comment xml:lang="en">The name defining a special edition of a document. Normally its a literal value composed of a version number and words.</rdfs:comment>
        <rdfs:domain rdf:resource="&bibo;Document"/>
        <rdfs:range rdf:resource="&rdfs;Literal"/>
    </owl:DatatypeProperty>
    


    <!-- http://purl.org/ontology/bibo/eissn -->

    <owl:DatatypeProperty rdf:about="&bibo;eissn">
        <rdfs:domain rdf:resource="&bibo;Collection"/>
        <rdfs:subPropertyOf rdf:resource="&bibo;identifier"/>
        <rdfs:range rdf:resource="&rdfs;Literal"/>
    </owl:DatatypeProperty>
    


    <!-- http://purl.org/ontology/bibo/gtin14 -->

    <owl:DatatypeProperty rdf:about="&bibo;gtin14">
        <rdfs:subPropertyOf rdf:resource="&bibo;identifier"/>
        <rdfs:range rdf:resource="&rdfs;Literal"/>
        <rdfs:domain>
            <owl:Class>
                <owl:unionOf rdf:parseType="Collection">
                    <rdf:Description rdf:about="&bibo;Collection"/>
                    <rdf:Description rdf:about="&bibo;Document"/>
                </owl:unionOf>
            </owl:Class>
        </rdfs:domain>
    </owl:DatatypeProperty>
    


    <!-- http://purl.org/ontology/bibo/handle -->

    <owl:DatatypeProperty rdf:about="&bibo;handle">
        <rdfs:subPropertyOf rdf:resource="&bibo;identifier"/>
        <rdfs:range rdf:resource="&rdfs;Literal"/>
        <rdfs:domain>
            <owl:Class>
                <owl:unionOf rdf:parseType="Collection">
                    <rdf:Description rdf:about="&bibo;Collection"/>
                    <rdf:Description rdf:about="&bibo;Document"/>
                </owl:unionOf>
            </owl:Class>
        </rdfs:domain>
    </owl:DatatypeProperty>
    


    <!-- http://purl.org/ontology/bibo/identifier -->

    <owl:DatatypeProperty rdf:about="&bibo;identifier">
        <rdfs:range rdf:resource="&rdfs;Literal"/>
        <rdfs:domain>
            <owl:Class>
                <owl:unionOf rdf:parseType="Collection">
                    <rdf:Description rdf:about="&bibo;Collection"/>
                    <rdf:Description rdf:about="&bibo;Document"/>
                </owl:unionOf>
            </owl:Class>
        </rdfs:domain>
    </owl:DatatypeProperty>
    


    <!-- http://purl.org/ontology/bibo/isbn -->

    <owl:DatatypeProperty rdf:about="&bibo;isbn">
        <rdfs:subPropertyOf rdf:resource="&bibo;identifier"/>
    </owl:DatatypeProperty>
    


    <!-- http://purl.org/ontology/bibo/isbn10 -->

    <owl:DatatypeProperty rdf:about="&bibo;isbn10">
        <rdfs:subPropertyOf rdf:resource="&bibo;isbn"/>
        <rdfs:range rdf:resource="&rdfs;Literal"/>
        <rdfs:domain>
            <owl:Class>
                <owl:unionOf rdf:parseType="Collection">
                    <rdf:Description rdf:about="&bibo;Collection"/>
                    <rdf:Description rdf:about="&bibo;Document"/>
                </owl:unionOf>
            </owl:Class>
        </rdfs:domain>
    </owl:DatatypeProperty>
    


    <!-- http://purl.org/ontology/bibo/isbn13 -->

    <owl:DatatypeProperty rdf:about="&bibo;isbn13">
        <rdfs:subPropertyOf rdf:resource="&bibo;isbn"/>
        <rdfs:range rdf:resource="&rdfs;Literal"/>
        <rdfs:domain>
            <owl:Class>
                <owl:unionOf rdf:parseType="Collection">
                    <rdf:Description rdf:about="&bibo;Collection"/>
                    <rdf:Description rdf:about="&bibo;Document"/>
                </owl:unionOf>
            </owl:Class>
        </rdfs:domain>
    </owl:DatatypeProperty>
    


    <!-- http://purl.org/ontology/bibo/issn -->

    <owl:DatatypeProperty rdf:about="&bibo;issn">
        <rdfs:domain rdf:resource="&bibo;Collection"/>
        <rdfs:subPropertyOf rdf:resource="&bibo;identifier"/>
        <rdfs:range rdf:resource="&rdfs;Literal"/>
    </owl:DatatypeProperty>
    


    <!-- http://purl.org/ontology/bibo/issue -->

    <owl:DatatypeProperty rdf:about="&bibo;issue">
        <rdfs:label xml:lang="en">issue</rdfs:label>
        <rdfs:isDefinedBy rdf:datatype="&xsd;anyURI">http://purl.org/ontology/bibo/</rdfs:isDefinedBy>
        <rdfs:comment xml:lang="en">An issue number</rdfs:comment>
        <ns:term_status>stable</ns:term_status>
        <rdfs:domain rdf:resource="&bibo;Issue"/>
        <rdfs:subPropertyOf rdf:resource="&bibo;locator"/>
        <rdfs:range rdf:resource="&rdfs;Literal"/>
    </owl:DatatypeProperty>
    


    <!-- http://purl.org/ontology/bibo/lccn -->

    <owl:DatatypeProperty rdf:about="&bibo;lccn">
        <rdfs:subPropertyOf rdf:resource="&bibo;identifier"/>
        <rdfs:range rdf:resource="&rdfs;Literal"/>
        <rdfs:domain>
            <owl:Class>
                <owl:unionOf rdf:parseType="Collection">
                    <rdf:Description rdf:about="&bibo;Collection"/>
                    <rdf:Description rdf:about="&bibo;Document"/>
                </owl:unionOf>
            </owl:Class>
        </rdfs:domain>
    </owl:DatatypeProperty>
    


    <!-- http://purl.org/ontology/bibo/locator -->

    <owl:DatatypeProperty rdf:about="&bibo;locator">
        <rdfs:label xml:lang="en">locator</rdfs:label>
        <rdfs:isDefinedBy rdf:datatype="&xsd;anyURI">http://purl.org/ontology/bibo/</rdfs:isDefinedBy>
        <rdfs:comment xml:lang="en">A description (often numeric) that locates an item within a containing document or collection.</rdfs:comment>
        <ns:term_status>stable</ns:term_status>
        <rdfs:domain rdf:resource="&bibo;Document"/>
        <rdfs:range rdf:resource="&rdfs;Literal"/>
    </owl:DatatypeProperty>
    


    <!-- http://purl.org/ontology/bibo/numPages -->

    <owl:DatatypeProperty rdf:about="&bibo;numPages">
        <rdfs:label xml:lang="en">number of pages</rdfs:label>
        <rdfs:isDefinedBy rdf:datatype="&xsd;anyURI">http://purl.org/ontology/bibo/</rdfs:isDefinedBy>
        <ns:term_status>stable</ns:term_status>
        <rdfs:comment xml:lang="en">The number of pages contained in a document</rdfs:comment>
        <rdfs:domain rdf:resource="&bibo;Document"/>
        <rdfs:range rdf:resource="&rdfs;Literal"/>
    </owl:DatatypeProperty>
    


    <!-- http://purl.org/ontology/bibo/numVolumes -->

    <owl:DatatypeProperty rdf:about="&bibo;numVolumes">
        <rdfs:label xml:lang="en">number of volumes</rdfs:label>
        <rdfs:isDefinedBy rdf:datatype="&xsd;anyURI">http://purl.org/ontology/bibo/</rdfs:isDefinedBy>
        <rdfs:comment xml:lang="en">The number of volumes contained in a collection of documents (usually a series, periodical, etc.).</rdfs:comment>
        <ns:term_status>stable</ns:term_status>
        <rdfs:domain rdf:resource="&bibo;Collection"/>
        <rdfs:range rdf:resource="&rdfs;Literal"/>
    </owl:DatatypeProperty>
    


    <!-- http://purl.org/ontology/bibo/number -->

    <owl:DatatypeProperty rdf:about="&bibo;number">
        <rdfs:label xml:lang="en">number</rdfs:label>
        <rdfs:isDefinedBy rdf:datatype="&xsd;anyURI">http://purl.org/ontology/bibo/</rdfs:isDefinedBy>
        <ns:term_status>stable</ns:term_status>
        <rdfs:comment xml:lang="en">A generic item or document number. Not to be confused with issue number.</rdfs:comment>
        <rdfs:domain rdf:resource="&bibo;Document"/>
        <rdfs:range rdf:resource="&rdfs;Literal"/>
    </owl:DatatypeProperty>
    


    <!-- http://purl.org/ontology/bibo/oclcnum -->

    <owl:DatatypeProperty rdf:about="&bibo;oclcnum">
        <rdfs:subPropertyOf rdf:resource="&bibo;identifier"/>
        <rdfs:range rdf:resource="&rdfs;Literal"/>
        <rdfs:domain>
            <owl:Class>
                <owl:unionOf rdf:parseType="Collection">
                    <rdf:Description rdf:about="&bibo;Collection"/>
                    <rdf:Description rdf:about="&bibo;Document"/>
                </owl:unionOf>
            </owl:Class>
        </rdfs:domain>
    </owl:DatatypeProperty>
    


    <!-- http://purl.org/ontology/bibo/pageEnd -->

    <owl:DatatypeProperty rdf:about="&bibo;pageEnd">
        <rdfs:label xml:lang="en">page end</rdfs:label>
        <rdfs:isDefinedBy rdf:datatype="&xsd;anyURI">http://purl.org/ontology/bibo/</rdfs:isDefinedBy>
        <ns:term_status>stable</ns:term_status>
        <rdfs:comment xml:lang="en">Ending page number within a continuous page range.</rdfs:comment>
        <rdfs:domain rdf:resource="&bibo;Document"/>
        <rdfs:subPropertyOf rdf:resource="&bibo;locator"/>
        <rdfs:range rdf:resource="&rdfs;Literal"/>
    </owl:DatatypeProperty>
    


    <!-- http://purl.org/ontology/bibo/pageStart -->

    <owl:DatatypeProperty rdf:about="&bibo;pageStart">
        <rdfs:label xml:lang="en">page start</rdfs:label>
        <rdfs:isDefinedBy rdf:datatype="&xsd;anyURI">http://purl.org/ontology/bibo/</rdfs:isDefinedBy>
        <ns:term_status>stable</ns:term_status>
        <rdfs:comment xml:lang="en">Starting page number within a continuous page range.</rdfs:comment>
        <rdfs:domain rdf:resource="&bibo;Document"/>
        <rdfs:subPropertyOf rdf:resource="&bibo;locator"/>
        <rdfs:range rdf:resource="&rdfs;Literal"/>
    </owl:DatatypeProperty>
    


    <!-- http://purl.org/ontology/bibo/pages -->

    <owl:DatatypeProperty rdf:about="&bibo;pages">
        <rdfs:label xml:lang="en">pages</rdfs:label>
        <rdfs:isDefinedBy rdf:datatype="&xsd;anyURI">http://purl.org/ontology/bibo/</rdfs:isDefinedBy>
        <ns:term_status>stable</ns:term_status>
        <rdfs:comment xml:lang="en">A string of non-contiguous page spans that locate a Document within a Collection. Example: 23-25, 34, 54-56. For continuous page ranges, use the pageStart and pageEnd properties.</rdfs:comment>
        <rdfs:domain rdf:resource="&bibo;Document"/>
        <rdfs:subPropertyOf rdf:resource="&bibo;locator"/>
        <rdfs:range rdf:resource="&rdfs;Literal"/>
    </owl:DatatypeProperty>
    


    <!-- http://purl.org/ontology/bibo/pmid -->

    <owl:DatatypeProperty rdf:about="&bibo;pmid">
        <rdfs:subPropertyOf rdf:resource="&bibo;identifier"/>
        <rdfs:range rdf:resource="&rdfs;Literal"/>
        <rdfs:domain>
            <owl:Class>
                <owl:unionOf rdf:parseType="Collection">
                    <rdf:Description rdf:about="&bibo;Collection"/>
                    <rdf:Description rdf:about="&bibo;Document"/>
                </owl:unionOf>
            </owl:Class>
        </rdfs:domain>
    </owl:DatatypeProperty>
    


    <!-- http://purl.org/ontology/bibo/prefixName -->

    <owl:DatatypeProperty rdf:about="&bibo;prefixName">
        <rdfs:label xml:lang="en">prefix name</rdfs:label>
        <rdfs:isDefinedBy rdf:datatype="&xsd;anyURI">http://purl.org/ontology/bibo/</rdfs:isDefinedBy>
        <rdfs:comment xml:lang="en">The prefix of a name</rdfs:comment>
        <ns:term_status>stable</ns:term_status>
        <rdfs:range rdf:resource="&rdfs;Literal"/>
        <rdfs:domain rdf:resource="&foaf;Agent"/>
    </owl:DatatypeProperty>
    


    <!-- http://purl.org/ontology/bibo/section -->

    <owl:DatatypeProperty rdf:about="&bibo;section">
        <rdfs:label xml:lang="en">section</rdfs:label>
        <rdfs:isDefinedBy rdf:datatype="&xsd;anyURI">http://purl.org/ontology/bibo/</rdfs:isDefinedBy>
        <ns:term_status>unstable</ns:term_status>
        <rdfs:comment xml:lang="en">A section number</rdfs:comment>
        <skos:example xml:lang="en">Di Rado, Alicia. 1995. Trekking through college: Classes explore
modern society using the world of Star trek. Los Angeles Times, March
15, sec. A, p. 3.</skos:example>
        <rdfs:domain rdf:resource="&bibo;Document"/>
        <rdfs:subPropertyOf rdf:resource="&bibo;locator"/>
        <rdfs:range rdf:resource="&rdfs;Literal"/>
    </owl:DatatypeProperty>
    


    <!-- http://purl.org/ontology/bibo/shortDescription -->

    <owl:DatatypeProperty rdf:about="&bibo;shortDescription">
        <rdfs:domain rdf:resource="&bibo;Document"/>
        <rdfs:range rdf:resource="&rdfs;Literal"/>
    </owl:DatatypeProperty>
    


    <!-- http://purl.org/ontology/bibo/shortTitle -->

    <owl:DatatypeProperty rdf:about="&bibo;shortTitle">
        <rdfs:label xml:lang="en">short title</rdfs:label>
        <rdfs:isDefinedBy rdf:datatype="&xsd;anyURI">http://purl.org/ontology/bibo/</rdfs:isDefinedBy>
        <ns:term_status>stable</ns:term_status>
        <rdfs:comment xml:lang="en">The abbreviation of a title.</rdfs:comment>
        <rdfs:domain rdf:resource="&bibo;Document"/>
        <rdfs:range rdf:resource="&rdfs;Literal"/>
    </owl:DatatypeProperty>
    


    <!-- http://purl.org/ontology/bibo/sici -->

    <owl:DatatypeProperty rdf:about="&bibo;sici">
        <rdfs:subPropertyOf rdf:resource="&bibo;identifier"/>
        <rdfs:range rdf:resource="&rdfs;Literal"/>
        <rdfs:domain>
            <owl:Class>
                <owl:unionOf rdf:parseType="Collection">
                    <rdf:Description rdf:about="&bibo;Collection"/>
                    <rdf:Description rdf:about="&bibo;Document"/>
                </owl:unionOf>
            </owl:Class>
        </rdfs:domain>
    </owl:DatatypeProperty>
    


    <!-- http://purl.org/ontology/bibo/suffixName -->

    <owl:DatatypeProperty rdf:about="&bibo;suffixName">
        <rdfs:label xml:lang="en">suffix name</rdfs:label>
        <rdfs:isDefinedBy rdf:datatype="&xsd;anyURI">http://purl.org/ontology/bibo/</rdfs:isDefinedBy>
        <ns:term_status>stable</ns:term_status>
        <rdfs:comment xml:lang="en">The suffix of a name</rdfs:comment>
        <rdfs:range rdf:resource="&rdfs;Literal"/>
        <rdfs:domain rdf:resource="&foaf;Agent"/>
    </owl:DatatypeProperty>
    


    <!-- http://purl.org/ontology/bibo/upc -->

    <owl:DatatypeProperty rdf:about="&bibo;upc">
        <rdfs:subPropertyOf rdf:resource="&bibo;identifier"/>
        <rdfs:range rdf:resource="&rdfs;Literal"/>
        <rdfs:domain>
            <owl:Class>
                <owl:unionOf rdf:parseType="Collection">
                    <rdf:Description rdf:about="&bibo;Collection"/>
                    <rdf:Description rdf:about="&bibo;Document"/>
                </owl:unionOf>
            </owl:Class>
        </rdfs:domain>
    </owl:DatatypeProperty>
    


    <!-- http://purl.org/ontology/bibo/uri -->

    <owl:DatatypeProperty rdf:about="&bibo;uri">
        <rdfs:label xml:lang="en">uri</rdfs:label>
        <rdfs:isDefinedBy rdf:datatype="&xsd;anyURI">http://purl.org/ontology/bibo/</rdfs:isDefinedBy>
        <rdfs:comment xml:lang="en">Universal Resource Identifier of a document</rdfs:comment>
        <ns:term_status>stable</ns:term_status>
        <rdfs:subPropertyOf rdf:resource="&bibo;identifier"/>
        <rdfs:range rdf:resource="&rdfs;Literal"/>
        <rdfs:domain>
            <owl:Class>
                <owl:unionOf rdf:parseType="Collection">
                    <rdf:Description rdf:about="&bibo;Collection"/>
                    <rdf:Description rdf:about="&bibo;Document"/>
                </owl:unionOf>
            </owl:Class>
        </rdfs:domain>
    </owl:DatatypeProperty>
    


    <!-- http://purl.org/ontology/bibo/volume -->

    <owl:DatatypeProperty rdf:about="&bibo;volume">
        <rdfs:label xml:lang="en">volume</rdfs:label>
        <rdfs:isDefinedBy rdf:datatype="&xsd;anyURI">http://purl.org/ontology/bibo/</rdfs:isDefinedBy>
        <ns:term_status>stable</ns:term_status>
        <rdfs:comment xml:lang="en">A volume number</rdfs:comment>
        <rdfs:domain rdf:resource="&bibo;Document"/>
        <rdfs:subPropertyOf rdf:resource="&bibo;locator"/>
        <rdfs:range rdf:resource="&rdfs;Literal"/>
    </owl:DatatypeProperty>
    


    <!-- http://schemas.talis.com/2005/address/schema#localityName -->

    <owl:DatatypeProperty rdf:about="&schema;localityName">
        <skos:scopeNote xml:lang="en">Used to name the locality of a publisher, an author, etc.</skos:scopeNote>
    </owl:DatatypeProperty>
    


    <!-- http://xmlns.com/foaf/0.1/family_name -->

    <owl:DatatypeProperty rdf:about="&foaf;family_name">
        <skos:scopeNote xml:lang="en">This is the property we choose to use to describe the family name of a person related to a bibliographic resource.</skos:scopeNote>
    </owl:DatatypeProperty>
    


    <!-- http://xmlns.com/foaf/0.1/givenname -->

    <owl:DatatypeProperty rdf:about="&foaf;givenname">
        <skos:scopeNote xml:lang="en">This is the property we choose to describe the given name of a Person related to a bibliographic resource. This is the first name of a person.</skos:scopeNote>
    </owl:DatatypeProperty>
    


    <!-- http://xmlns.com/foaf/0.1/name -->

    <owl:DatatypeProperty rdf:about="&foaf;name"/>
    


    <!-- 
    ///////////////////////////////////////////////////////////////////////////////////////
    //
    // Classes
    //
    ///////////////////////////////////////////////////////////////////////////////////////
     -->

    


    <!-- http://purl.org/NET/c4dm/event.owl#Event -->

    <owl:Class rdf:about="&event;Event">
        <skos:scopeNote xml:lang="en">Used to describe bibliographic related events such as conferences, hearing, etc.</skos:scopeNote>
    </owl:Class>
    


    <!-- http://purl.org/dc/terms/Agent -->

    <owl:Class rdf:about="&terms;Agent">
        <owl:equivalentClass rdf:resource="&foaf;Agent"/>
        <skos:editorialNote xml:lang="en">BIBO assert that a dcterms:Agent is an equivalent class to foaf:Agent.
This means that all the individuals belonging to the foaf:Agent class
also belongs to the dcterms:Agent class. This way, dcterms:contributor
can be used on foaf:Person, foaf:Organization, foaf:Agent and foaf:Group.
Even if this link is not done in neither the FOAF nor the DCTERMS ontologies this is a wide spread fact that is asserted by BIBO.</skos:editorialNote>
    </owl:Class>
    


    <!-- http://purl.org/ontology/bibo/AcademicArticle -->

    <owl:Class rdf:about="&bibo;AcademicArticle">
        <rdfs:label xml:lang="en">Academic Article</rdfs:label>
        <rdfs:subClassOf rdf:resource="&bibo;Article"/>
        <rdfs:isDefinedBy rdf:datatype="&xsd;anyURI">http://purl.org/ontology/bibo/</rdfs:isDefinedBy>
        <ns:term_status>stable</ns:term_status>
        <rdfs:comment xml:lang="en">A scholarly academic article, typically published in a journal.</rdfs:comment>
    </owl:Class>
    


    <!-- http://purl.org/ontology/bibo/Article -->

    <owl:Class rdf:about="&bibo;Article">
        <rdfs:label xml:lang="en">Article</rdfs:label>
        <rdfs:subClassOf rdf:resource="&bibo;Document"/>
        <rdfs:isDefinedBy rdf:datatype="&xsd;anyURI">http://purl.org/ontology/bibo/</rdfs:isDefinedBy>
        <ns:term_status>stable</ns:term_status>
        <rdfs:comment xml:lang="en">A written composition in prose, usually nonfiction, on a specific topic, forming an independent part of a book or other publication, as a newspaper or magazine.</rdfs:comment>
    </owl:Class>
    


    <!-- http://purl.org/ontology/bibo/AudioDocument -->

    <owl:Class rdf:about="&bibo;AudioDocument">
        <rdfs:label xml:lang="en">audio document</rdfs:label>
        <rdfs:subClassOf rdf:resource="&bibo;Document"/>
        <rdfs:isDefinedBy rdf:datatype="&xsd;anyURI">http://purl.org/ontology/bibo/</rdfs:isDefinedBy>
        <ns:term_status>stable</ns:term_status>
        <rdfs:comment xml:lang="en">An audio document; aka record.</rdfs:comment>
    </owl:Class>
    


    <!-- http://purl.org/ontology/bibo/AudioVisualDocument -->

    <owl:Class rdf:about="&bibo;AudioVisualDocument">
        <rdfs:label xml:lang="en">audio-visual document</rdfs:label>
        <rdfs:subClassOf rdf:resource="&bibo;Document"/>
        <rdfs:isDefinedBy rdf:datatype="&xsd;anyURI">http://purl.org/ontology/bibo/</rdfs:isDefinedBy>
        <rdfs:comment xml:lang="en">An audio-visual document; film, video, and so forth.</rdfs:comment>
        <ns:term_status>stable</ns:term_status>
    </owl:Class>
    


    <!-- http://purl.org/ontology/bibo/Bill -->

    <owl:Class rdf:about="&bibo;Bill">
        <rdfs:label xml:lang="en">Bill</rdfs:label>
        <rdfs:subClassOf rdf:resource="&bibo;Legislation"/>
        <rdfs:isDefinedBy rdf:datatype="&xsd;anyURI">http://purl.org/ontology/bibo/</rdfs:isDefinedBy>
        <rdfs:comment xml:lang="en">Draft legislation presented for discussion to a legal body.</rdfs:comment>
        <ns:term_status>stable</ns:term_status>
    </owl:Class>
    


    <!-- http://purl.org/ontology/bibo/Book -->

    <owl:Class rdf:about="&bibo;Book">
        <rdfs:label xml:lang="en">Book</rdfs:label>
        <rdfs:subClassOf rdf:resource="&bibo;Document"/>
        <rdfs:isDefinedBy rdf:datatype="&xsd;anyURI">http://purl.org/ontology/bibo/</rdfs:isDefinedBy>
        <ns:term_status>stable</ns:term_status>
        <rdfs:comment xml:lang="en">A written or printed work of fiction or nonfiction, usually on sheets of paper fastened or bound together within covers.</rdfs:comment>
    </owl:Class>
    


    <!-- http://purl.org/ontology/bibo/BookSection -->

    <owl:Class rdf:about="&bibo;BookSection">
        <rdfs:label xml:lang="en">Book Section</rdfs:label>
        <rdfs:subClassOf rdf:resource="&bibo;DocumentPart"/>
        <rdfs:isDefinedBy rdf:datatype="&xsd;anyURI">http://purl.org/ontology/bibo/</rdfs:isDefinedBy>
        <ns:term_status>unstable</ns:term_status>
        <rdfs:comment xml:lang="en">A section of a book.</rdfs:comment>
    </owl:Class>
    


    <!-- http://purl.org/ontology/bibo/Brief -->

    <owl:Class rdf:about="&bibo;Brief">
        <rdfs:label xml:lang="en">Brief</rdfs:label>
        <rdfs:subClassOf rdf:resource="&bibo;LegalCaseDocument"/>
        <rdfs:isDefinedBy rdf:datatype="&xsd;anyURI">http://purl.org/ontology/bibo/</rdfs:isDefinedBy>
        <rdfs:comment xml:lang="en">A written argument submitted to a court.</rdfs:comment>
        <ns:term_status>unstable</ns:term_status>
    </owl:Class>
    


    <!-- http://purl.org/ontology/bibo/Chapter -->

    <owl:Class rdf:about="&bibo;Chapter">
        <rdfs:label xml:lang="en">Chapter</rdfs:label>
        <rdfs:subClassOf rdf:resource="&bibo;BookSection"/>
        <rdfs:isDefinedBy rdf:datatype="&xsd;anyURI">http://purl.org/ontology/bibo/</rdfs:isDefinedBy>
        <rdfs:comment xml:lang="en">A chapter of a book.</rdfs:comment>
        <ns:term_status>unstable</ns:term_status>
    </owl:Class>
    


    <!-- http://purl.org/ontology/bibo/Code -->

    <owl:Class rdf:about="&bibo;Code">
        <rdfs:label xml:lang="en">Code</rdfs:label>
        <rdfs:subClassOf rdf:resource="&bibo;Periodical"/>
        <rdfs:subClassOf>
            <owl:Restriction>
                <owl:onProperty rdf:resource="&terms;hasPart"/>
                <owl:minCardinality rdf:datatype="&xsd;nonNegativeInteger">1</owl:minCardinality>
            </owl:Restriction>
        </rdfs:subClassOf>
        <rdfs:subClassOf>
            <owl:Restriction>
                <owl:onProperty rdf:resource="&terms;hasPart"/>
                <owl:allValuesFrom rdf:resource="&bibo;Legislation"/>
            </owl:Restriction>
        </rdfs:subClassOf>
        <rdfs:isDefinedBy rdf:datatype="&xsd;anyURI">http://purl.org/ontology/bibo/</rdfs:isDefinedBy>
        <ns:term_status>stable</ns:term_status>
        <rdfs:comment xml:lang="en">A collection of statutes.</rdfs:comment>
    </owl:Class>
    


    <!-- http://purl.org/ontology/bibo/CollectedDocument -->

    <owl:Class rdf:about="&bibo;CollectedDocument">
        <rdfs:label xml:lang="en">Collected Document</rdfs:label>
        <rdfs:subClassOf rdf:resource="&bibo;Document"/>
        <rdfs:subClassOf>
            <owl:Restriction>
                <owl:onProperty rdf:resource="&terms;hasPart"/>
                <owl:allValuesFrom rdf:resource="&bibo;Document"/>
            </owl:Restriction>
        </rdfs:subClassOf>
        <rdfs:subClassOf>
            <owl:Restriction>
                <owl:onProperty rdf:resource="&terms;hasPart"/>
                <owl:minCardinality rdf:datatype="&xsd;nonNegativeInteger">1</owl:minCardinality>
            </owl:Restriction>
        </rdfs:subClassOf>
        <rdfs:isDefinedBy rdf:datatype="&xsd;anyURI">http://purl.org/ontology/bibo/</rdfs:isDefinedBy>
        <ns:term_status>stable</ns:term_status>
        <rdfs:comment xml:lang="en">A document that simultaneously contains other documents.</rdfs:comment>
    </owl:Class>
    


    <!-- http://purl.org/ontology/bibo/Collection -->

    <owl:Class rdf:about="&bibo;Collection">
        <rdfs:label xml:lang="en">Collection</rdfs:label>
        <rdfs:subClassOf>
            <owl:Restriction>
                <owl:onProperty rdf:resource="&terms;hasPart"/>
                <owl:allValuesFrom>
                    <owl:Class>
                        <owl:unionOf rdf:parseType="Collection">
                            <rdf:Description rdf:about="&bibo;Collection"/>
                            <rdf:Description rdf:about="&bibo;Document"/>
                        </owl:unionOf>
                    </owl:Class>
                </owl:allValuesFrom>
            </owl:Restriction>
        </rdfs:subClassOf>
        <rdfs:isDefinedBy rdf:datatype="&xsd;anyURI">http://purl.org/ontology/bibo/</rdfs:isDefinedBy>
        <rdfs:comment xml:lang="en">A collection of Documents or Collections</rdfs:comment>
        <ns:term_status>stable</ns:term_status>
    </owl:Class>
    


    <!-- http://purl.org/ontology/bibo/Conference -->

    <owl:Class rdf:about="&bibo;Conference">
        <rdfs:label xml:lang="en">Conference</rdfs:label>
        <rdfs:subClassOf rdf:resource="&event;Event"/>
        <rdfs:isDefinedBy rdf:datatype="&xsd;anyURI">http://purl.org/ontology/bibo/</rdfs:isDefinedBy>
        <ns:term_status>stable</ns:term_status>
        <rdfs:comment xml:lang="en">A meeting for consultation or discussion.</rdfs:comment>
    </owl:Class>
    


    <!-- http://purl.org/ontology/bibo/CourtReporter -->

    <owl:Class rdf:about="&bibo;CourtReporter">
        <rdfs:label xml:lang="en">Court Reporter</rdfs:label>
        <rdfs:subClassOf rdf:resource="&bibo;Periodical"/>
        <rdfs:subClassOf>
            <owl:Restriction>
                <owl:onProperty rdf:resource="&terms;hasPart"/>
                <owl:minCardinality rdf:datatype="&xsd;nonNegativeInteger">1</owl:minCardinality>
            </owl:Restriction>
        </rdfs:subClassOf>
        <rdfs:subClassOf>
            <owl:Restriction>
                <owl:onProperty rdf:resource="&terms;hasPart"/>
                <owl:allValuesFrom rdf:resource="&bibo;LegalDocument"/>
            </owl:Restriction>
        </rdfs:subClassOf>
        <rdfs:isDefinedBy rdf:datatype="&xsd;anyURI">http://purl.org/ontology/bibo/</rdfs:isDefinedBy>
        <rdfs:comment xml:lang="en">A collection of legal cases.</rdfs:comment>
        <ns:term_status>stable</ns:term_status>
    </owl:Class>
    


    <!-- http://purl.org/ontology/bibo/Document -->

    <owl:Class rdf:about="&bibo;Document">
        <rdfs:label xml:lang="en">Document</rdfs:label>
        <owl:equivalentClass rdf:resource="&foaf;Document"/>
        <rdfs:isDefinedBy rdf:datatype="&xsd;anyURI">http://purl.org/ontology/bibo/</rdfs:isDefinedBy>
        <rdfs:comment xml:lang="en">A document (noun) is a bounded physical representation of body of information designed with the capacity (and usually intent) to communicate. A document may manifest symbolic, diagrammatic or sensory-representational information.</rdfs:comment>
        <ns:term_status>stable</ns:term_status>
    </owl:Class>
    


    <!-- http://purl.org/ontology/bibo/DocumentPart -->

    <owl:Class rdf:about="&bibo;DocumentPart">
        <rdfs:label xml:lang="en">document part</rdfs:label>
        <rdfs:subClassOf rdf:resource="&bibo;Document"/>
        <rdfs:subClassOf>
            <owl:Restriction>
                <owl:onProperty rdf:resource="&terms;isPartOf"/>
                <owl:maxCardinality rdf:datatype="&xsd;nonNegativeInteger">1</owl:maxCardinality>
            </owl:Restriction>
        </rdfs:subClassOf>
        <rdfs:isDefinedBy rdf:datatype="&xsd;anyURI">http://purl.org/ontology/bibo/</rdfs:isDefinedBy>
        <rdfs:comment xml:lang="en">a distinct part of a larger document or collected document.</rdfs:comment>
        <ns:term_status>unstable</ns:term_status>
    </owl:Class>
    


    <!-- http://purl.org/ontology/bibo/DocumentStatus -->

    <owl:Class rdf:about="&bibo;DocumentStatus">
        <rdfs:label xml:lang="en">Document Status</rdfs:label>
        <rdfs:isDefinedBy rdf:datatype="&xsd;anyURI">http://purl.org/ontology/bibo/</rdfs:isDefinedBy>
        <rdfs:comment xml:lang="en">The status of the publication of a document.</rdfs:comment>
        <ns:term_status>stable</ns:term_status>
    </owl:Class>
    


    <!-- http://purl.org/ontology/bibo/EditedBook -->

    <owl:Class rdf:about="&bibo;EditedBook">
        <rdfs:label xml:lang="en">Edited Book</rdfs:label>
        <rdfs:subClassOf rdf:resource="&bibo;CollectedDocument"/>
        <rdfs:isDefinedBy rdf:datatype="&xsd;anyURI">http://purl.org/ontology/bibo/</rdfs:isDefinedBy>
        <rdfs:comment xml:lang="en">An edited book.</rdfs:comment>
        <ns:term_status>stable</ns:term_status>
    </owl:Class>
    


    <!-- http://purl.org/ontology/bibo/Email -->

    <owl:Class rdf:about="&bibo;Email">
        <rdfs:label xml:lang="en">EMail</rdfs:label>
        <rdfs:subClassOf rdf:resource="&bibo;PersonalCommunicationDocument"/>
        <rdfs:isDefinedBy rdf:datatype="&xsd;anyURI">http://purl.org/ontology/bibo/</rdfs:isDefinedBy>
        <ns:term_status>stable</ns:term_status>
        <rdfs:comment xml:lang="en">A written communication addressed to a person or organization and transmitted electronically.</rdfs:comment>
    </owl:Class>
    


    <!-- http://purl.org/ontology/bibo/Event -->

    <owl:Class rdf:about="&bibo;Event"/>
    


    <!-- http://purl.org/ontology/bibo/Excerpt -->

    <owl:Class rdf:about="&bibo;Excerpt">
        <rdfs:label xml:lang="en">Excerpt</rdfs:label>
        <rdfs:subClassOf rdf:resource="&bibo;DocumentPart"/>
        <rdfs:isDefinedBy rdf:datatype="&xsd;anyURI">http://purl.org/ontology/bibo/</rdfs:isDefinedBy>
        <rdfs:comment xml:lang="en">A passage selected from a larger work.</rdfs:comment>
        <ns:term_status>stable</ns:term_status>
    </owl:Class>
    


    <!-- http://purl.org/ontology/bibo/Film -->

    <owl:Class rdf:about="&bibo;Film">
        <rdfs:label xml:lang="en">Film</rdfs:label>
        <rdfs:subClassOf rdf:resource="&bibo;AudioVisualDocument"/>
        <rdfs:isDefinedBy rdf:datatype="&xsd;anyURI">http://purl.org/ontology/bibo/</rdfs:isDefinedBy>
        <rdfs:comment xml:lang="en">aka movie.</rdfs:comment>
        <ns:term_status>stable</ns:term_status>
    </owl:Class>
    


    <!-- http://purl.org/ontology/bibo/Hearing -->

    <owl:Class rdf:about="&bibo;Hearing">
        <rdfs:label xml:lang="en">Hearing</rdfs:label>
        <rdfs:subClassOf rdf:resource="&event;Event"/>
        <rdfs:isDefinedBy rdf:datatype="&xsd;anyURI">http://purl.org/ontology/bibo/</rdfs:isDefinedBy>
        <rdfs:comment xml:lang="en">An instance or a session in which testimony and arguments are presented, esp. before an official, as a judge in a lawsuit.</rdfs:comment>
        <ns:term_status>stable</ns:term_status>
    </owl:Class>
    


    <!-- http://purl.org/ontology/bibo/Image -->

    <owl:Class rdf:about="&bibo;Image">
        <rdfs:label xml:lang="en">Image</rdfs:label>
        <owl:equivalentClass rdf:resource="&foaf;Image"/>
        <rdfs:subClassOf rdf:resource="&bibo;Document"/>
        <rdfs:isDefinedBy rdf:datatype="&xsd;anyURI">http://purl.org/ontology/bibo/</rdfs:isDefinedBy>
        <ns:term_status>stable</ns:term_status>
        <rdfs:comment xml:lang="en">A document that presents visual or diagrammatic information.</rdfs:comment>
    </owl:Class>
    


    <!-- http://purl.org/ontology/bibo/Interview -->

    <owl:Class rdf:about="&bibo;Interview">
        <rdfs:label xml:lang="en">Interview</rdfs:label>
        <rdfs:subClassOf rdf:resource="&event;Event"/>
        <rdfs:isDefinedBy rdf:datatype="&xsd;anyURI">http://purl.org/ontology/bibo/</rdfs:isDefinedBy>
        <ns:term_status>stable</ns:term_status>
        <rdfs:comment xml:lang="en">A formalized discussion between two or more people.</rdfs:comment>
    </owl:Class>
    


    <!-- http://purl.org/ontology/bibo/Issue -->

    <owl:Class rdf:about="&bibo;Issue">
        <rdfs:label xml:lang="en">Issue</rdfs:label>
        <rdfs:subClassOf rdf:resource="&bibo;CollectedDocument"/>
        <rdfs:subClassOf>
            <owl:Restriction>
                <owl:onProperty rdf:resource="&terms;hasPart"/>
                <owl:minCardinality rdf:datatype="&xsd;nonNegativeInteger">1</owl:minCardinality>
            </owl:Restriction>
        </rdfs:subClassOf>
        <rdfs:subClassOf>
            <owl:Restriction>
                <owl:onProperty rdf:resource="&terms;hasPart"/>
                <owl:allValuesFrom rdf:resource="&bibo;Article"/>
            </owl:Restriction>
        </rdfs:subClassOf>
        <rdfs:isDefinedBy rdf:datatype="&xsd;anyURI">http://purl.org/ontology/bibo/</rdfs:isDefinedBy>
        <rdfs:comment xml:lang="en">something that is printed or published and distributed, esp. a given number of a periodical</rdfs:comment>
        <ns:term_status>stable</ns:term_status>
    </owl:Class>
    


    <!-- http://purl.org/ontology/bibo/Journal -->

    <owl:Class rdf:about="&bibo;Journal">
        <rdfs:label xml:lang="en">Journal</rdfs:label>
        <rdfs:subClassOf rdf:resource="&bibo;Periodical"/>
        <rdfs:subClassOf>
            <owl:Restriction>
                <owl:onProperty rdf:resource="&terms;hasPart"/>
                <owl:minCardinality rdf:datatype="&xsd;nonNegativeInteger">1</owl:minCardinality>
            </owl:Restriction>
        </rdfs:subClassOf>
        <rdfs:subClassOf>
            <owl:Restriction>
                <owl:onProperty rdf:resource="&terms;hasPart"/>
                <owl:allValuesFrom rdf:resource="&bibo;Issue"/>
            </owl:Restriction>
        </rdfs:subClassOf>
        <rdfs:isDefinedBy rdf:datatype="&xsd;anyURI">http://purl.org/ontology/bibo/</rdfs:isDefinedBy>
        <ns:term_status>stable</ns:term_status>
        <rdfs:comment xml:lang="en">A periodical of scholarly journal Articles.</rdfs:comment>
    </owl:Class>
    


    <!-- http://purl.org/ontology/bibo/LegalCaseDocument -->

    <owl:Class rdf:about="&bibo;LegalCaseDocument">
        <rdfs:label xml:lang="en">Legal Case Document</rdfs:label>
        <rdfs:subClassOf rdf:resource="&bibo;LegalDocument"/>
        <rdfs:isDefinedBy rdf:datatype="&xsd;anyURI">http://purl.org/ontology/bibo/</rdfs:isDefinedBy>
        <ns:term_status>unstable</ns:term_status>
        <rdfs:comment xml:lang="en">A document accompanying a legal case.</rdfs:comment>
    </owl:Class>
    


    <!-- http://purl.org/ontology/bibo/LegalDecision -->

    <owl:Class rdf:about="&bibo;LegalDecision">
        <rdfs:label xml:lang="en">Decision</rdfs:label>
        <rdfs:subClassOf rdf:resource="&bibo;LegalCaseDocument"/>
        <rdfs:isDefinedBy rdf:datatype="&xsd;anyURI">http://purl.org/ontology/bibo/</rdfs:isDefinedBy>
        <ns:term_status>unstable</ns:term_status>
        <rdfs:comment xml:lang="en">A document containing an authoritative determination (as a decree or judgment) made after consideration of facts or law.</rdfs:comment>
    </owl:Class>
    


    <!-- http://purl.org/ontology/bibo/LegalDocument -->

    <owl:Class rdf:about="&bibo;LegalDocument">
        <rdfs:label xml:lang="en">Legal Document</rdfs:label>
        <rdfs:subClassOf rdf:resource="&bibo;Document"/>
        <rdfs:isDefinedBy rdf:datatype="&xsd;anyURI">http://purl.org/ontology/bibo/</rdfs:isDefinedBy>
        <ns:term_status>stable</ns:term_status>
        <rdfs:comment xml:lang="en">A legal document; for example, a court decision, a brief, and so forth.</rdfs:comment>
    </owl:Class>
    


    <!-- http://purl.org/ontology/bibo/Legislation -->

    <owl:Class rdf:about="&bibo;Legislation">
        <rdfs:label xml:lang="en">Legislation</rdfs:label>
        <rdfs:subClassOf rdf:resource="&bibo;LegalDocument"/>
        <rdfs:isDefinedBy rdf:datatype="&xsd;anyURI">http://purl.org/ontology/bibo/</rdfs:isDefinedBy>
        <ns:term_status>unstable</ns:term_status>
        <rdfs:comment xml:lang="en">A legal document proposing or enacting a law or a group of laws.</rdfs:comment>
    </owl:Class>
    


    <!-- http://purl.org/ontology/bibo/Letter -->

    <owl:Class rdf:about="&bibo;Letter">
        <rdfs:label xml:lang="en">Letter</rdfs:label>
        <rdfs:subClassOf rdf:resource="&bibo;PersonalCommunicationDocument"/>
        <rdfs:isDefinedBy rdf:datatype="&xsd;anyURI">http://purl.org/ontology/bibo/</rdfs:isDefinedBy>
        <ns:term_status>stable</ns:term_status>
        <rdfs:comment xml:lang="en">A written or printed communication addressed to a person or organization and usually transmitted by mail.</rdfs:comment>
    </owl:Class>
    


    <!-- http://purl.org/ontology/bibo/Magazine -->

    <owl:Class rdf:about="&bibo;Magazine">
        <rdfs:label xml:lang="en">Magazine</rdfs:label>
        <rdfs:subClassOf rdf:resource="&bibo;Periodical"/>
        <rdfs:subClassOf>
            <owl:Restriction>
                <owl:onProperty rdf:resource="&terms;hasPart"/>
                <owl:minCardinality rdf:datatype="&xsd;nonNegativeInteger">1</owl:minCardinality>
            </owl:Restriction>
        </rdfs:subClassOf>
        <rdfs:subClassOf>
            <owl:Restriction>
                <owl:onProperty rdf:resource="&terms;hasPart"/>
                <owl:allValuesFrom rdf:resource="&bibo;Issue"/>
            </owl:Restriction>
        </rdfs:subClassOf>
        <rdfs:isDefinedBy rdf:datatype="&xsd;anyURI">http://purl.org/ontology/bibo/</rdfs:isDefinedBy>
        <rdfs:comment xml:lang="en">A periodical of magazine Articles. A magazine is a publication that is issued periodically, usually bound in a paper cover, and typically contains essays, stories, poems, etc., by many writers, and often photographs and drawings, frequently specializing in a particular subject or area, as hobbies, news, or sports.</rdfs:comment>
        <ns:term_status>stable</ns:term_status>
    </owl:Class>
    


    <!-- http://purl.org/ontology/bibo/Manual -->

    <owl:Class rdf:about="&bibo;Manual">
        <rdfs:label xml:lang="en">Manual</rdfs:label>
        <rdfs:subClassOf rdf:resource="&bibo;Document"/>
        <rdfs:isDefinedBy rdf:datatype="&xsd;anyURI">http://purl.org/ontology/bibo/</rdfs:isDefinedBy>
        <rdfs:comment xml:lang="en">A small reference book, especially one giving instructions.</rdfs:comment>
        <ns:term_status>unstable</ns:term_status>
    </owl:Class>
    


    <!-- http://purl.org/ontology/bibo/Manuscript -->

    <owl:Class rdf:about="&bibo;Manuscript">
        <rdfs:label xml:lang="en">Manuscript</rdfs:label>
        <rdfs:subClassOf rdf:resource="&bibo;Document"/>
        <rdfs:isDefinedBy rdf:datatype="&xsd;anyURI">http://purl.org/ontology/bibo/</rdfs:isDefinedBy>
        <rdfs:comment xml:lang="en">An unpublished Document, which may also be submitted to a publisher for publication.</rdfs:comment>
        <ns:term_status>stable</ns:term_status>
    </owl:Class>
    


    <!-- http://purl.org/ontology/bibo/Map -->

    <owl:Class rdf:about="&bibo;Map">
        <rdfs:label xml:lang="en">Map</rdfs:label>
        <rdfs:subClassOf rdf:resource="&bibo;Image"/>
        <rdfs:isDefinedBy rdf:datatype="&xsd;anyURI">http://purl.org/ontology/bibo/</rdfs:isDefinedBy>
        <rdfs:comment xml:lang="en">A graphical depiction of geographic features.</rdfs:comment>
        <ns:term_status>unstable</ns:term_status>
    </owl:Class>
    


    <!-- http://purl.org/ontology/bibo/MultiVolumeBook -->

    <owl:Class rdf:about="&bibo;MultiVolumeBook">
        <rdfs:label xml:lang="en">Multivolume Book</rdfs:label>
        <rdfs:subClassOf rdf:resource="&bibo;Collection"/>
        <rdfs:subClassOf>
            <owl:Restriction>
                <owl:onProperty rdf:resource="&terms;hasPart"/>
                <owl:allValuesFrom rdf:resource="&bibo;Book"/>
            </owl:Restriction>
        </rdfs:subClassOf>
        <rdfs:isDefinedBy rdf:datatype="&xsd;anyURI">http://purl.org/ontology/bibo/</rdfs:isDefinedBy>
        <rdfs:comment xml:lang="en">A loose, thematic, collection of Documents, often Books.</rdfs:comment>
        <ns:term_status>stable</ns:term_status>
    </owl:Class>
    


    <!-- http://purl.org/ontology/bibo/Newspaper -->

    <owl:Class rdf:about="&bibo;Newspaper">
        <rdfs:label xml:lang="en">Newspaper</rdfs:label>
        <rdfs:subClassOf rdf:resource="&bibo;Periodical"/>
        <rdfs:subClassOf>
            <owl:Restriction>
                <owl:onProperty rdf:resource="&terms;hasPart"/>
                <owl:minCardinality rdf:datatype="&xsd;nonNegativeInteger">1</owl:minCardinality>
            </owl:Restriction>
        </rdfs:subClassOf>
        <rdfs:subClassOf>
            <owl:Restriction>
                <owl:onProperty rdf:resource="&terms;hasPart"/>
                <owl:allValuesFrom rdf:resource="&bibo;Issue"/>
            </owl:Restriction>
        </rdfs:subClassOf>
        <rdfs:isDefinedBy rdf:datatype="&xsd;anyURI">http://purl.org/ontology/bibo/</rdfs:isDefinedBy>
        <ns:term_status>stable</ns:term_status>
        <rdfs:comment xml:lang="en">A periodical of documents, usually issued daily or weekly, containing current news, editorials, feature articles, and usually advertising.</rdfs:comment>
    </owl:Class>
    


    <!-- http://purl.org/ontology/bibo/Note -->

    <owl:Class rdf:about="&bibo;Note">
        <rdfs:label xml:lang="en">Note</rdfs:label>
        <rdfs:subClassOf rdf:resource="&bibo;Document"/>
        <rdfs:isDefinedBy rdf:datatype="&xsd;anyURI">http://purl.org/ontology/bibo/</rdfs:isDefinedBy>
        <ns:term_status>stable</ns:term_status>
        <rdfs:comment xml:lang="en">Notes or annotations about a resource.</rdfs:comment>
    </owl:Class>
    


    <!-- http://purl.org/ontology/bibo/Patent -->

    <owl:Class rdf:about="&bibo;Patent">
        <rdfs:label xml:lang="en">Patent</rdfs:label>
        <rdfs:subClassOf rdf:resource="&bibo;Document"/>
        <rdfs:isDefinedBy rdf:datatype="&xsd;anyURI">http://purl.org/ontology/bibo/</rdfs:isDefinedBy>
        <rdfs:comment xml:lang="en">A document describing the exclusive right granted by a government to an inventor to manufacture, use, or sell an invention for a certain number of years.</rdfs:comment>
        <ns:term_status>stable</ns:term_status>
    </owl:Class>
    


    <!-- http://purl.org/ontology/bibo/Performance -->

    <owl:Class rdf:about="&bibo;Performance">
        <rdfs:label xml:lang="en">Performance</rdfs:label>
        <rdfs:subClassOf rdf:resource="&event;Event"/>
        <rdfs:isDefinedBy rdf:datatype="&xsd;anyURI">http://purl.org/ontology/bibo/</rdfs:isDefinedBy>
        <ns:term_status>unstable</ns:term_status>
        <rdfs:comment xml:lang="en">A public performance.</rdfs:comment>
    </owl:Class>
    


    <!-- http://purl.org/ontology/bibo/Periodical -->

    <owl:Class rdf:about="&bibo;Periodical">
        <rdfs:label xml:lang="en">Periodical</rdfs:label>
        <rdfs:subClassOf rdf:resource="&bibo;Collection"/>
        <rdfs:subClassOf>
            <owl:Restriction>
                <owl:onProperty rdf:resource="&terms;hasPart"/>
                <owl:minCardinality rdf:datatype="&xsd;nonNegativeInteger">1</owl:minCardinality>
            </owl:Restriction>
        </rdfs:subClassOf>
        <rdfs:subClassOf>
            <owl:Restriction>
                <owl:onProperty rdf:resource="&terms;hasPart"/>
                <owl:allValuesFrom rdf:resource="&bibo;Issue"/>
            </owl:Restriction>
        </rdfs:subClassOf>
        <rdfs:isDefinedBy rdf:datatype="&xsd;anyURI">http://purl.org/ontology/bibo/</rdfs:isDefinedBy>
        <ns:term_status>stable</ns:term_status>
        <rdfs:comment xml:lang="en">A group of related documents issued at regular intervals.</rdfs:comment>
    </owl:Class>
    


    <!-- http://purl.org/ontology/bibo/PersonalCommunication -->

    <owl:Class rdf:about="&bibo;PersonalCommunication">
        <rdfs:label xml:lang="en">Personal Communication</rdfs:label>
        <rdfs:subClassOf rdf:resource="&event;Event"/>
        <rdfs:isDefinedBy rdf:datatype="&xsd;anyURI">http://purl.org/ontology/bibo/</rdfs:isDefinedBy>
        <ns:term_status>stable</ns:term_status>
        <rdfs:comment xml:lang="en">A communication between an agent and one or more specific recipients.</rdfs:comment>
    </owl:Class>
    


    <!-- http://purl.org/ontology/bibo/PersonalCommunicationDocument -->

    <owl:Class rdf:about="&bibo;PersonalCommunicationDocument">
        <rdfs:label xml:lang="en">Personal Communication Document</rdfs:label>
        <rdfs:subClassOf rdf:resource="&bibo;Document"/>
        <rdfs:isDefinedBy rdf:datatype="&xsd;anyURI">http://purl.org/ontology/bibo/</rdfs:isDefinedBy>
        <rdfs:comment xml:lang="en">A personal communication manifested in some document.</rdfs:comment>
        <ns:term_status>stable</ns:term_status>
    </owl:Class>
    


    <!-- http://purl.org/ontology/bibo/Proceedings -->

    <owl:Class rdf:about="&bibo;Proceedings">
        <rdfs:label xml:lang="en">Proceedings</rdfs:label>
        <rdfs:subClassOf rdf:resource="&bibo;Book"/>
        <rdfs:isDefinedBy rdf:datatype="&xsd;anyURI">http://purl.org/ontology/bibo/</rdfs:isDefinedBy>
        <ns:term_status>unstable</ns:term_status>
        <rdfs:comment xml:lang="en">A compilation of documents published from an event, such as a conference.</rdfs:comment>
    </owl:Class>
    


    <!-- http://purl.org/ontology/bibo/Quote -->

    <owl:Class rdf:about="&bibo;Quote">
        <rdfs:label xml:lang="en">Quote</rdfs:label>
        <rdfs:subClassOf rdf:resource="&bibo;Excerpt"/>
        <rdfs:isDefinedBy rdf:datatype="&xsd;anyURI">http://purl.org/ontology/bibo/</rdfs:isDefinedBy>
        <rdfs:comment xml:lang="en">An excerpted collection of words.</rdfs:comment>
        <ns:term_status>stable</ns:term_status>
    </owl:Class>
    


    <!-- http://purl.org/ontology/bibo/ReferenceSource -->

    <owl:Class rdf:about="&bibo;ReferenceSource">
        <rdfs:label xml:lang="en">Reference Source</rdfs:label>
        <rdfs:subClassOf rdf:resource="&bibo;Document"/>
        <rdfs:isDefinedBy rdf:datatype="&xsd;anyURI">http://purl.org/ontology/bibo/</rdfs:isDefinedBy>
        <ns:term_status>unstable</ns:term_status>
        <rdfs:comment xml:lang="en">A document that presents authoritative reference information, such as a dictionary or encylopedia .</rdfs:comment>
    </owl:Class>
    


    <!-- http://purl.org/ontology/bibo/Report -->

    <owl:Class rdf:about="&bibo;Report">
        <rdfs:label xml:lang="en">Report</rdfs:label>
        <rdfs:subClassOf rdf:resource="&bibo;Document"/>
        <rdfs:isDefinedBy rdf:datatype="&xsd;anyURI">http://purl.org/ontology/bibo/</rdfs:isDefinedBy>
        <rdfs:comment xml:lang="en">A document describing an account or statement describing in detail an event, situation, or the like, usually as the result of observation, inquiry, etc..</rdfs:comment>
        <ns:term_status>stable</ns:term_status>
    </owl:Class>
    


    <!-- http://purl.org/ontology/bibo/Series -->

    <owl:Class rdf:about="&bibo;Series">
        <rdfs:label xml:lang="en">Series</rdfs:label>
        <rdfs:subClassOf rdf:resource="&bibo;Collection"/>
        <rdfs:subClassOf>
            <owl:Restriction>
                <owl:onProperty rdf:resource="&terms;hasPart"/>
                <owl:allValuesFrom rdf:resource="&bibo;Document"/>
            </owl:Restriction>
        </rdfs:subClassOf>
        <rdfs:isDefinedBy rdf:datatype="&xsd;anyURI">http://purl.org/ontology/bibo/</rdfs:isDefinedBy>
        <rdfs:comment xml:lang="en">A loose, thematic, collection of Documents, often Books.</rdfs:comment>
        <ns:term_status>stable</ns:term_status>
    </owl:Class>
    


    <!-- http://purl.org/ontology/bibo/Slide -->

    <owl:Class rdf:about="&bibo;Slide">
        <rdfs:label xml:lang="en">Slide</rdfs:label>
        <rdfs:subClassOf rdf:resource="&bibo;DocumentPart"/>
        <rdfs:isDefinedBy rdf:datatype="&xsd;anyURI">http://purl.org/ontology/bibo/</rdfs:isDefinedBy>
        <rdfs:comment xml:lang="en">A slide in a slideshow</rdfs:comment>
        <ns:term_status>unstable</ns:term_status>
    </owl:Class>
    


    <!-- http://purl.org/ontology/bibo/Slideshow -->

    <owl:Class rdf:about="&bibo;Slideshow">
        <rdfs:label xml:lang="en">Slideshow</rdfs:label>
        <rdfs:subClassOf rdf:resource="&bibo;Document"/>
        <rdfs:subClassOf>
            <owl:Restriction>
                <owl:onProperty rdf:resource="&terms;hasPart"/>
                <owl:allValuesFrom rdf:resource="&bibo;Slide"/>
            </owl:Restriction>
        </rdfs:subClassOf>
        <rdfs:isDefinedBy rdf:datatype="&xsd;anyURI">http://purl.org/ontology/bibo/</rdfs:isDefinedBy>
        <rdfs:comment xml:lang="en">A presentation of a series of slides, usually presented in front of an audience with written text and images.</rdfs:comment>
        <ns:term_status>stable</ns:term_status>
    </owl:Class>
    

    <!-- http://purl.org/ontology/bibo/Specification -->

    <owl:Class rdf:about="&bibo;Specification">
        <rdfs:label xml:lang="en">Specification</rdfs:label>
        <rdfs:subClassOf rdf:resource="&bibo;Document"/>
        <rdfs:isDefinedBy rdf:datatype="&xsd;anyURI">http://purl.org/ontology/bibo/</rdfs:isDefinedBy>
        <ns:term_status>testing</ns:term_status>
        <rdfs:comment xml:lang="en">A document describing a specification.</rdfs:comment>
    </owl:Class>

    <!-- http://purl.org/ontology/bibo/Standard -->

    <owl:Class rdf:about="&bibo;Standard">
        <rdfs:label xml:lang="en">Standard</rdfs:label>
        <rdfs:subClassOf rdf:resource="&bibo;Specification"/>
        <rdfs:isDefinedBy rdf:datatype="&xsd;anyURI">http://purl.org/ontology/bibo/</rdfs:isDefinedBy>
        <ns:term_status>stable</ns:term_status>
        <rdfs:comment xml:lang="en">A document describing a standard: a specification organized through a standards body.</rdfs:comment>
    </owl:Class>

    <!-- http://purl.org/ontology/bibo/Statute -->

    <owl:Class rdf:about="&bibo;Statute">
        <rdfs:label xml:lang="en">Statute</rdfs:label>
        <rdfs:subClassOf rdf:resource="&bibo;Legislation"/>
        <rdfs:isDefinedBy rdf:datatype="&xsd;anyURI">http://purl.org/ontology/bibo/</rdfs:isDefinedBy>
        <rdfs:comment xml:lang="en">A bill enacted into law.</rdfs:comment>
        <ns:term_status>stable</ns:term_status>
    </owl:Class>
    


    <!-- http://purl.org/ontology/bibo/Thesis -->

    <owl:Class rdf:about="&bibo;Thesis">
        <rdfs:label xml:lang="en">Thesis</rdfs:label>
        <rdfs:subClassOf rdf:resource="&bibo;Document"/>
        <rdfs:isDefinedBy rdf:datatype="&xsd;anyURI">http://purl.org/ontology/bibo/</rdfs:isDefinedBy>
        <rdfs:comment xml:lang="en">A document created to summarize research findings associated with the completion of an academic degree.</rdfs:comment>
        <ns:term_status>stable</ns:term_status>
    </owl:Class>
    


    <!-- http://purl.org/ontology/bibo/ThesisDegree -->

    <owl:Class rdf:about="&bibo;ThesisDegree">
        <rdfs:label xml:lang="en">Thesis degree</rdfs:label>
        <rdfs:isDefinedBy rdf:datatype="&xsd;anyURI">http://purl.org/ontology/bibo/</rdfs:isDefinedBy>
        <ns:term_status>stable</ns:term_status>
        <rdfs:comment xml:lang="en">The academic degree of a Thesis</rdfs:comment>
    </owl:Class>
    


    <!-- http://purl.org/ontology/bibo/Webpage -->

    <owl:Class rdf:about="&bibo;Webpage">
        <rdfs:label xml:lang="en">Webpage</rdfs:label>
        <rdfs:subClassOf rdf:resource="&bibo;Document"/>
        <rdfs:isDefinedBy rdf:datatype="&xsd;anyURI">http://purl.org/ontology/bibo/</rdfs:isDefinedBy>
        <ns:term_status>unstable</ns:term_status>
        <rdfs:comment xml:lang="en">A web page is an online document available (at least initially) on the world wide web. A web page is written first and foremost to appear on the web, as distinct from other online resources such as books, manuscripts or audio documents which use the web primarily as a distribution mechanism alongside other more traditional methods such as print.</rdfs:comment>
    </owl:Class>
    


    <!-- http://purl.org/ontology/bibo/Website -->

    <owl:Class rdf:about="&bibo;Website">
        <rdfs:label xml:lang="en">Website</rdfs:label>
        <rdfs:subClassOf rdf:resource="&bibo;Collection"/>
        <rdfs:subClassOf>
            <owl:Restriction>
                <owl:onProperty rdf:resource="&terms;hasPart"/>
                <owl:minCardinality rdf:datatype="&xsd;nonNegativeInteger">1</owl:minCardinality>
            </owl:Restriction>
        </rdfs:subClassOf>
        <rdfs:subClassOf>
            <owl:Restriction>
                <owl:onProperty rdf:resource="&terms;hasPart"/>
                <owl:allValuesFrom rdf:resource="&bibo;Webpage"/>
            </owl:Restriction>
        </rdfs:subClassOf>
        <rdfs:isDefinedBy rdf:datatype="&xsd;anyURI">http://purl.org/ontology/bibo/</rdfs:isDefinedBy>
        <ns:term_status>unstable</ns:term_status>
        <rdfs:comment xml:lang="en">A group of Webpages accessible on the Web.</rdfs:comment>
    </owl:Class>
    


    <!-- http://purl.org/ontology/bibo/Workshop -->

    <owl:Class rdf:about="&bibo;Workshop">
        <rdfs:label xml:lang="en">Workshop</rdfs:label>
        <rdfs:subClassOf rdf:resource="&event;Event"/>
        <rdfs:isDefinedBy rdf:datatype="&xsd;anyURI">http://purl.org/ontology/bibo/</rdfs:isDefinedBy>
        <rdfs:comment xml:lang="en">A seminar, discussion group, or the like, that emphasizes zxchange of ideas and the demonstration and application of techniques, skills, etc.</rdfs:comment>
        <ns:term_status>stable</ns:term_status>
    </owl:Class>
    


    <!-- http://www.w3.org/1999/02/22-rdf-syntax-ns#List -->

    <owl:Class rdf:about="&rdf;List"/>
    


    <!-- http://www.w3.org/1999/02/22-rdf-syntax-ns#Seq -->

    <owl:Class rdf:about="&rdf;Seq"/>
    


    <!-- http://www.w3.org/2000/01/rdf-schema#Resource -->

    <owl:Class rdf:about="&rdfs;Resource"/>
    


    <!-- http://www.w3.org/2002/07/owl#Thing -->

    <owl:Class rdf:about="&owl;Thing"/>
    


    <!-- http://xmlns.com/foaf/0.1/Agent -->

    <owl:Class rdf:about="&foaf;Agent">
        <skos:scopeNote xml:lang="en">Used to describe any &quot;agent&quot; related to bibliographic items. Such agents can be persons, organizations or groups of any kind.</skos:scopeNote>
    </owl:Class>
    


    <!-- http://xmlns.com/foaf/0.1/Document -->

    <owl:Class rdf:about="&foaf;Document"/>
    


    <!-- http://xmlns.com/foaf/0.1/Image -->

    <owl:Class rdf:about="&foaf;Image"/>
    


    <!-- http://xmlns.com/foaf/0.1/Organization -->

    <owl:Class rdf:about="&foaf;Organization">
        <skos:scopeNote xml:lang="en">Ued to describe an organization related to bibliographic items such as a publishing company, etc.</skos:scopeNote>
    </owl:Class>
    


    <!-- http://xmlns.com/foaf/0.1/Person -->

    <owl:Class rdf:about="&foaf;Person">
        <skos:scopeNote xml:lang="en">Used to describe a Person related to a bibliographic ite such as an author, an editor, etc.</skos:scopeNote>
    </owl:Class>
    


    <!-- 
    ///////////////////////////////////////////////////////////////////////////////////////
    //
    // Individuals
    //
    ///////////////////////////////////////////////////////////////////////////////////////
     -->

    


    <!-- http://purl.org/ontology/bibo/bdarcus -->

    <owl:Thing rdf:about="&bibo;bdarcus">
        <rdf:type rdf:resource="&owl;NamedIndividual"/>
        <rdf:type rdf:resource="&foaf;Person"/>
        <rdfs:seeAlso rdf:datatype="&xsd;anyURI">http://purl.org/net/darcusb/info#me</rdfs:seeAlso>
        <rdfs:isDefinedBy rdf:datatype="&xsd;anyURI">http://purl.org/ontology/bibo/</rdfs:isDefinedBy>
        <foaf:name>Bruce D&apos;Arcus</foaf:name>
    </owl:Thing>
    


    <!-- http://purl.org/ontology/bibo/fgiasson -->

    <owl:Thing rdf:about="&bibo;fgiasson">
        <rdf:type rdf:resource="&owl;NamedIndividual"/>
        <rdf:type rdf:resource="&foaf;Person"/>
        <rdfs:seeAlso rdf:datatype="&xsd;anyURI">http://fgiasson.com/me/</rdfs:seeAlso>
        <rdfs:isDefinedBy rdf:datatype="&xsd;anyURI">http://purl.org/ontology/bibo/</rdfs:isDefinedBy>
        <foaf:name>Frederick Giasson</foaf:name>
    </owl:Thing>
    


    <!-- http://purl.org/ontology/bibo/degrees/ma -->

    <owl:Thing rdf:about="&bibo;degrees/ma">
        <rdf:type rdf:resource="&bibo;ThesisDegree"/>
        <rdf:type rdf:resource="&owl;NamedIndividual"/>
        <rdfs:label xml:lang="en">M.A.</rdfs:label>
        <ns:term_status>stable</ns:term_status>
        <rdfs:comment xml:lang="en">masters degree in arts</rdfs:comment>
    </owl:Thing>
    


    <!-- http://purl.org/ontology/bibo/degrees/ms -->

    <owl:Thing rdf:about="&bibo;degrees/ms">
        <rdf:type rdf:resource="&bibo;ThesisDegree"/>
        <rdf:type rdf:resource="&owl;NamedIndividual"/>
        <rdfs:label xml:lang="en">M.S.</rdfs:label>
        <ns:term_status>stable</ns:term_status>
        <rdfs:comment xml:lang="en">masters degree in science</rdfs:comment>
    </owl:Thing>
    


    <!-- http://purl.org/ontology/bibo/degrees/phd -->

    <owl:Thing rdf:about="&bibo;degrees/phd">
        <rdf:type rdf:resource="&bibo;ThesisDegree"/>
        <rdf:type rdf:resource="&owl;NamedIndividual"/>
        <rdfs:label xml:lang="en">PhD degree</rdfs:label>
        <rdfs:comment xml:lang="en">PhD degree</rdfs:comment>
        <ns:term_status>stable</ns:term_status>
    </owl:Thing>
    


    <!-- http://purl.org/ontology/bibo/status/accepted -->

    <owl:Thing rdf:about="&bibo;status/accepted">
        <rdf:type rdf:resource="&bibo;DocumentStatus"/>
        <rdf:type rdf:resource="&owl;NamedIndividual"/>
        <rdfs:label xml:lang="en">accepted</rdfs:label>
        <rdfs:comment xml:lang="en">Accepted for publication after peer reviewing.</rdfs:comment>
        <ns:term_status>stable</ns:term_status>
    </owl:Thing>
    


    <!-- http://purl.org/ontology/bibo/status/draft -->

    <owl:Thing rdf:about="&bibo;status/draft">
        <rdf:type rdf:resource="&bibo;DocumentStatus"/>
        <rdf:type rdf:resource="&owl;NamedIndividual"/>
        <rdfs:label xml:lang="en">draft</rdfs:label>
        <ns:term_status>stable</ns:term_status>
        <rdfs:comment xml:lang="en">Document drafted</rdfs:comment>
    </owl:Thing>
    


    <!-- http://purl.org/ontology/bibo/status/forthcoming -->

    <owl:Thing rdf:about="&bibo;status/forthcoming">
        <rdf:type rdf:resource="&bibo;DocumentStatus"/>
        <rdf:type rdf:resource="&owl;NamedIndividual"/>
        <rdfs:label xml:lang="en">forthcoming</rdfs:label>
        <rdfs:comment xml:lang="en">Document to be published</rdfs:comment>
        <ns:term_status>stable</ns:term_status>
    </owl:Thing>
    


    <!-- http://purl.org/ontology/bibo/status/legal -->

    <owl:Thing rdf:about="&bibo;status/legal">
        <rdf:type rdf:resource="&bibo;DocumentStatus"/>
        <rdf:type rdf:resource="&owl;NamedIndividual"/>
        <rdfs:label xml:lang="en">legal</rdfs:label>
        <ns:term_status>stable</ns:term_status>
        <rdfs:comment xml:lang="en">Legal document</rdfs:comment>
    </owl:Thing>
    


    <!-- http://purl.org/ontology/bibo/status/nonPeerReviewed -->

    <owl:Thing rdf:about="&bibo;status/nonPeerReviewed">
        <rdf:type rdf:resource="&bibo;DocumentStatus"/>
        <rdf:type rdf:resource="&owl;NamedIndividual"/>
        <rdfs:label xml:lang="en">non peer reviewed</rdfs:label>
        <ns:term_status>stable</ns:term_status>
        <rdfs:comment xml:lang="en">A document that is not peer reviewed</rdfs:comment>
    </owl:Thing>
    


    <!-- http://purl.org/ontology/bibo/status/peerReviewed -->

    <owl:Thing rdf:about="&bibo;status/peerReviewed">
        <rdf:type rdf:resource="&bibo;DocumentStatus"/>
        <rdf:type rdf:resource="&owl;NamedIndividual"/>
        <rdfs:label xml:lang="en">peer reviewed</rdfs:label>
        <rdfs:comment xml:lang="en">The process by which articles are chosen to be included in a refereed journal. An editorial board consisting of experts in the same field as the author review the article and decide if it is authoritative enough for publication.</rdfs:comment>
        <ns:term_status>stable</ns:term_status>
    </owl:Thing>
    


    <!-- http://purl.org/ontology/bibo/status/published -->

    <owl:Thing rdf:about="&bibo;status/published">
        <rdf:type rdf:resource="&bibo;DocumentStatus"/>
        <rdf:type rdf:resource="&owl;NamedIndividual"/>
        <rdfs:label xml:lang="en">published</rdfs:label>
        <rdfs:comment xml:lang="en">Published document</rdfs:comment>
        <ns:term_status>stable</ns:term_status>
    </owl:Thing>
    


    <!-- http://purl.org/ontology/bibo/status/rejected -->

    <owl:Thing rdf:about="&bibo;status/rejected">
        <rdf:type rdf:resource="&bibo;DocumentStatus"/>
        <rdf:type rdf:resource="&owl;NamedIndividual"/>
        <rdfs:label xml:lang="en">rejected</rdfs:label>
        <rdfs:comment xml:lang="en">Rejected for publication after peer reviewing.</rdfs:comment>
        <ns:term_status>stable</ns:term_status>
    </owl:Thing>
    


    <!-- http://purl.org/ontology/bibo/status/unpublished -->

    <owl:Thing rdf:about="&bibo;status/unpublished">
        <rdf:type rdf:resource="&bibo;DocumentStatus"/>
        <rdf:type rdf:resource="&owl;NamedIndividual"/>
        <rdfs:label xml:lang="en">unpublished</rdfs:label>
        <ns:term_status>stable</ns:term_status>
        <rdfs:comment xml:lang="en">Unpublished document</rdfs:comment>
    </owl:Thing>
</rdf:RDF>



<!-- Generated by the OWL API (version 3.5.0) http://owlapi.sourceforge.net -->

