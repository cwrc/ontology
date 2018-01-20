#!/usr/bin/perl
#Usage:
# ./createTaxonomy ontology.owl Class lang
# Class that you're interested in building a taxonomy for ex.
# ./createTaxonomy cwrc.owl Religion en
# ./createTaxonomy cwrc.owl PoliticalAffiliation en
use strict;
use RDF::Trine;
use RDF::Query;
use XML::LibXML;
use Digest::MD5 qw(md5 md5_hex);
 
my $xml_parser = XML::LibXML->new();
$xml_parser->clean_namespaces(1);
my $store = RDF::Trine::Store::Memory->new();
my $model = RDF::Trine::Model->new($store);
if (scalar(@ARGV) != 3) {
    print "Insufficent Arguments Provided\n";
    print "Expected Usage:\n";
    print "\t./createTaxonomy ontology.owl Class lang\n";
    print "\t./createTaxonomy cwrc.owl Religion en\n";
    print "Will output a diagraph with instance nodes of that class linking to their uri's\n";
    exit(0);
}
my $raw_file = 'file:'. $ARGV[0];
my $taxonomy = $ARGV[1];
my $lang = $ARGV[2];

RDF::Trine::Parser->parse_url_into_model( $raw_file, $model );

# gets base xml uri for use in other ontologies
my $query = RDF::Query->new('SELECT * WHERE { ?uri <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://www.w3.org/2002/07/owl#Ontology>.
}');
my $iterator = $query->execute( $model );
my $namespaceUri = "";
while (my $row = $iterator->next) {
    $row =~ s/{ uri=//;
    $row =~ s/> }/#/;
    $namespaceUri = $row;
}

my @allmaps;

# Gets all instances of the chosen class
my $query_str = 'SELECT * WHERE { ?uri <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> 
    '.$namespaceUri.$taxonomy.'> .
    ?uri <http://www.w3.org/2000/01/rdf-schema#label> ?label .
    FILTER(LANG(?label) = "" || LANGMATCHES(LANG(?label), "'.$lang.'"))
}';
my $query = RDF::Query->new($query_str);
my $iterator = $query->execute( $model );

unless ($iterator->next) {
    print "Query has failed, unable to generate diagraph!\n";
    print "Here was the provided query based on the class provided: ".$taxonomy."\n\n" ;
    print $query_str."\n";
    exit 0;
}

print "digraph ".$taxonomy."Graph {\n
 size=\"30,30\";
 margin=0;\n";

while (my $row = $iterator->next) {
    my $astring = $row->{"uri"}->as_string();
    my $innerquery =  RDF::Query->new('SELECT * WHERE { ' . $astring . '  <http://www.w3.org/2004/02/skos/core#broaderTransitive> ?upper . }');
    my $inneriterator = $innerquery->execute( $model );
    my $lhs = "X" . substr(md5_hex($astring),1,5);
    while (my $tworow = $inneriterator->next) {
        my $rhs = "X" . substr(md5_hex($tworow->{"upper"}->as_string()),1,5);
        print " " .$lhs . " -> " . $rhs . "\n";
    }
    my $uri = $astring;
    $uri =~ s/</"/;
    $uri =~ s/>/"/;
    print " $lhs [label=\"" . $row->{"label"}->value()."\" URL=".$uri."target=\"_parent\"]\n";
}
print "}";
exit();
