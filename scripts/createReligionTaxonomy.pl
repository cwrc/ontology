#!/usr/bin/env perl
#
use RDF::Trine;
use RDF::Query;
use XML::LibXML;
use Digest::MD5 qw(md5 md5_hex);
my $xml_parser = XML::LibXML->new();
$xml_parser->clean_namespaces(1);
use strict;
my $store = RDF::Trine::Store::Memory->new();
my $model = RDF::Trine::Model->new($store);
# parse some web data into the model, and print the count of resulting RDF statements
my $raw_file = 'file:'. $ARGV[0];
#print $raw_file ."\n\n\n";
RDF::Trine::Parser->parse_url_into_model( $raw_file, $model );
#my $xmldocument = $xml_parser->load_xml(location => 'military.owl');
#print $model->size . " RDF statements parsed\n";
my @allmaps ;
my $query = RDF::Query->new('SELECT * WHERE { ?uri <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://sparql.cwrc.ca/ontologies/cwrc#Religion> . 
?uri <http://www.w3.org/2000/01/rdf-schema#label> ?label .
FILTER(LANG(?label) = "" || LANGMATCHES(LANG(?label), "en"))
}');
my $iterator = $query->execute( $model );
print "digraph ReligionGraph {\n
 size=\"30,30\";
 margin=0;\n";
#ratio=\"fill\";

while (my $row = $iterator->next) {
 my $astring = $row->{"uri"}->as_string();
# print $astring ."\n";
 my $innerquery =  RDF::Query->new('SELECT * WHERE { ' . $astring . '  <http://www.w3.org/2004/02/skos/core#broaderTransitive> ?upper . }');
 #
 #
 my $inneriterator = $innerquery->execute( $model );
 my $lhs = "X" . substr(md5_hex($astring),1,5);
 while (my $tworow = $inneriterator->next) {
  my $rhs = "X" . substr(md5_hex($tworow->{"upper"}->as_string()),1,5);
  print " " .$lhs . " -> " . $rhs . "\n";
 }#while
 my $uri = $astring;
 $uri =~ s/</"/;
 $uri =~ s/>/"/;
 # print $uri."\n";
 print " $lhs [label=\"" . $row->{"label"}->value()."\" URL=".$uri."target=\"_parent\"]\n";
}       #while        
print "}";
 exit 0;        