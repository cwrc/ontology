#!/usr/bin/perl
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
RDF::Trine::Parser->parse_url_into_model( 'file:../cwrc.owl', $model );
#my $xmldocument = $xml_parser->load_xml(location => 'military.owl');
print $model->size . " RDF statements parsed\n";
my @allmaps ;
my $query = RDF::Query->new('SELECT * WHERE { ?uri <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://www.cwrc.ca/ontologies/cwrc#Religion> . }');
my $iterator = $query->execute( $model );
print "graph ReligionGraph {\n";
while (my $row = $iterator->next) {
 my $astring = $row->{"uri"}->as_string();
 print $astring ."\n";
 my $innerquery =  RDF::Query->new('SELECT * WHERE { <' .$astring . '>  <http://www.w3.org/2004/02/skos/core#broaderTransitive> ?upper . }');
 my $inneriterator = $innerquery->execute( $model );
 my $lhs = substr(md5_hex($astring),1,5);
 while (my $tworow = $inneriterator->next) {
  my $rhs = substr(md5_hex($tworow->{"upper"}->as_string()),1,5);
  print $lhs . " -> " . $rhs . ";";
 }#while
}       #while        
print "}";
 exit 0;        