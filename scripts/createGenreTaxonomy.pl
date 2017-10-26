#!/usr/bin/env perl

use RDF::Trine;
use RDF::Query;
use XML::LibXML;
use Digest::MD5 qw(md5 md5_hex);
use strict;
use utf8;
binmode(STDOUT, ":utf8");
my $xml_parser = XML::LibXML->new();
$xml_parser->clean_namespaces(1);
use strict;
my $store = RDF::Trine::Store::Memory->new();
my $model = RDF::Trine::Model->new($store);
my $raw_file = 'file:'. $ARGV[0];
RDF::Trine::Parser->parse_url_into_model( $raw_file, $model );
my @allmaps;

my $query = RDF::Query->new('SELECT * WHERE { ?uri <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://sparql.cwrc.ca/ontologies/genre#Genre> . 
?uri <http://www.w3.org/2000/01/rdf-schema#label> ?label .
FILTER(LANG(?label) = "" || LANGMATCHES(LANG(?label), "en"))
}');
my $iterator = $query->execute( $model );
#if (length($query->error) > 1) {
#  print $query->error . "\n";
 # }
print "digraph GenreGraph {\n
 margin=0;\n";

while (my $row = $iterator->next) {
	my $astring = $row->{"uri"}->as_string();
	 # print $astring ."\n";
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
	print " $lhs [label=\"" . $row->{"label"}->value()."\" URL=".$uri." target=\"_parent\"]\n";

}
print "}";
exit 0;