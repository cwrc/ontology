MAKEFLAGS += -J2
ONTOLOGY?=cwrc
O_LANG?=EN
ONTOLOGY_DATE = $(shell date -u +"%Y-%m-%d")
ONTOLOGY_W_DATE = $(ONTOLOGY)-$(ONTOLOGY_DATE)
DATE_W_LANG = $(ONTOLOGY_DATE)-$(O_LANG)
DATE_CLEAN = $(shell date -u +"%Y%m%d")
ONTOLOGY_LONGDATE = $(shell date -d '$(ONTOLOGY_DATE)'  +'%d %B %Y')
ONTOLOGY_VERSION = $(shell xpath -e '/rdf:RDF/owl:Ontology/owl:versionInfo/text()' $(ONTOLOGY).rdf  2> /dev/null)
ONTOLOGY_LOGO = $(shell xpath -e '/rdf:RDF/owl:Ontology/foaf:logo/@rdf:resource' $(ONTOLOGY).rdf  2> /dev/null | sed 's/\//\\\//g' | cut -d "\"" -f 2)
PREVIOUS_ONTOLOGY = $(shell xpath -e '/rdf:RDF/owl:Ontology/owl:priorVersion/@rdf:resource' $(ONTOLOGY).rdf  2> /dev/null | sed 's/\//\\\//g' | cut -d "\"" -f 2)
TOTAL_TRIPLES = $(shell cat $(ONTOLOGY_W_DATE).counts)
TOTAL_ENTITIES = $(shell cat $(ONTOLOGY_W_DATE).unique)

force:	$(ONTOLOGY).rdf
	touch $(ONTOLOGY).rdf
	touch $(ONTOLOGY)-template-$(O_LANG).html	
	rm -f cwrc-ref.bib

all: $(ONTOLOGY_W_DATE).rdf $(ONTOLOGY_W_DATE)-$(O_LANG).html $(ONTOLOGY).html $(ONTOLOGY)-preamble-$(O_LANG).html

$(ONTOLOGY_W_DATE)-temp.rdf: $(ONTOLOGY).rdf
	python3 scripts/crossRef.py $(ONTOLOGY).rdf $@

# Metadata to complete rdf file/html pages
$(ONTOLOGY_W_DATE).counts: $(ONTOLOGY_W_DATE)-temp.rdf
	rapper $(ONTOLOGY_W_DATE)-temp.rdf | wc -l > $@
$(ONTOLOGY_W_DATE).unique: $(ONTOLOGY_W_DATE)-temp.rdf
	rapper $(ONTOLOGY_W_DATE)-temp.rdf | cut -d " " -f 1 | sort | sort -u | wc -l > $@

# Filling in metadata for template of spec
$(ONTOLOGY)-template-$(DATE_W_LANG).html: $(ONTOLOGY)-template-$(O_LANG).html 
	sed "s/PREVIOUS_ONTOLOGY/$(PREVIOUS_ONTOLOGY)/g"  < $(ONTOLOGY)-template-$(O_LANG).html | sed "s/ONTOLOGY_LOGO/$(ONTOLOGY_LOGO)/g" | sed "s/ONTOLOGY_NAME/$(ONTOLOGY)/g"  | sed "s/ONTOLOGY_DATE/$(ONTOLOGY_DATE)/g" |  sed "s/ONTOLOGY_LONGDATE/$(ONTOLOGY_LONGDATE)/g"  | sed "s/ONTOLOGY_VERSION/$(ONTOLOGY_VERSION)/g"  | sed 's/ONTOLOGY_LOGO/$(ONTOLOGY_LOGO)/g'  > $@
$(ONTOLOGY)-template2-$(DATE_W_LANG).html: $(ONTOLOGY)-template-$(DATE_W_LANG).html $(ONTOLOGY)-citations.html
	 m4 -P $(ONTOLOGY)-template-$(DATE_W_LANG).html > $@

# Filling in metadata for preamble 
$(ONTOLOGY)-preamble-template2-$(O_LANG).html: $(ONTOLOGY)-preamble-template-$(O_LANG).html figures/religionTaxonomy-$(DATE_W_LANG).svg figures/politicalAffiliationTaxonomy-$(DATE_W_LANG).svg figures/genreTaxonomy-$(DATE_W_LANG).svg
	sed "s/PREVIOUS_ONTOLOGY/$(PREVIOUS_ONTOLOGY)/g"  < $(ONTOLOGY)-preamble-template-$(O_LANG).html | sed "s/ONTOLOGY_LOGO/$(ONTOLOGY_LOGO)/g" | sed "s/ONTOLOGY_NAME/$(ONTOLOGY)/g"  | sed "s/ONTOLOGY_DATE/$(ONTOLOGY_DATE)/g" |  sed "s/ONTOLOGY_LONGDATE/$(ONTOLOGY_LONGDATE)/g"  | sed "s/ONTOLOGY_VERSION/$(ONTOLOGY_VERSION)/g"  | sed 's/ONTOLOGY_LOGO/$(ONTOLOGY_LOGO)/g'  > $@
$(ONTOLOGY)-preamble-$(O_LANG).html: $(ONTOLOGY)-preamble-template2-$(O_LANG).html $(ONTOLOGY)-citations.html
	 m4 -P $(ONTOLOGY)-preamble-template2-$(O_LANG).html > $@

# generating spec
$(ONTOLOGY_W_DATE)-$(O_LANG).html: $(ONTOLOGY_W_DATE)-temp.rdf $(ONTOLOGY)-template2-$(DATE_W_LANG).html scripts/docgen.py scripts/relations.json
	python3 scripts/docgen.py $(ONTOLOGY_W_DATE)-temp.rdf $(ONTOLOGY)-template2-$(DATE_W_LANG).html  $@  $(O_LANG)
	cp -f $(ONTOLOGY_W_DATE)-$(O_LANG).html $(ONTOLOGY)-$(O_LANG).html
$(ONTOLOGY).html: $(ONTOLOGY_W_DATE)-EN.html
	cp -f $(ONTOLOGY_W_DATE)-EN.html $@


# creating precursor to final rdf including bibliography and dates
$(ONTOLOGY_W_DATE)-temp2.rdf: $(ONTOLOGY_W_DATE)-temp.rdf $(ONTOLOGY_W_DATE).bibli
	xpath $(ONTOLOGY_W_DATE)-temp.rdf "/rdf:RDF" 1> /dev/null 2> /dev/null
	sed 's/DATE_TODAY/$(DATE_CLEAN)/g' < $(ONTOLOGY_W_DATE)-temp.rdf  | grep -v "</rdf:RDF>" > $@	
	cat $(ONTOLOGY_W_DATE).bibli >> $@ 
	echo "</rdf:RDF>" >> $@

# # Gathering of bibliographic data/citations from cwrc 
$(ONTOLOGY_W_DATE).bibli:
	./scripts/getFedoraCollection.sh $(ONTOLOGY) $@
$(ONTOLOGY)-citations.html: $(ONTOLOGY_W_DATE).bibli scripts/cwrcCitations.py
	python3 scripts/cwrcCitations.py $(ONTOLOGY_W_DATE).rdf > $@
	# bibtex2html --use-keys -nodoc -nobibsource -a -dl -unicode --quiet -o - $(ONTOLOGY)-ref.bib  | sed "s/<\/table><hr><p><em>This file was generated by/<\/table>/" | head -n -1 > $@

# # Final rdf file
$(ONTOLOGY_W_DATE).rdf: $(ONTOLOGY_W_DATE).unique $(ONTOLOGY_W_DATE).counts $(ONTOLOGY_W_DATE)-temp2.rdf
	cat $(ONTOLOGY_W_DATE)-temp2.rdf | sed 's/ONTOLOGY_DATE/$(ONTOLOGY_DATE)/g' | sed 's/TOTAL_TRIPLES/$(TOTAL_TRIPLES)/g' | sed 's/TOTAL_ENTITIES/$(TOTAL_ENTITIES)/g' > $@	
	rapper $@ > $(ONTOLOGY_W_DATE).nt
	rapper -o turtle $@ > $(ONTOLOGY_W_DATE).ttl



# # Doesn't matter when
# # Generating svgs of taxonomies for preamble
figures/religionTaxonomy-$(DATE_W_LANG).svg: cwrc.rdf scripts/createTaxonomy.py
	python3 scripts/createTaxonomy.py cwrc.rdf Religion $(O_LANG) | unflatten -l 5 -c 10 | dot -o$@ -Tsvg 
figures/politicalAffiliationTaxonomy-$(DATE_W_LANG).svg: cwrc.rdf scripts/createTaxonomy.py
	python3 scripts/createTaxonomy.py cwrc.rdf PoliticalAffiliation $(O_LANG) | unflatten -l 20 -c 30 | dot -o$@ -Tsvg 
	# python3 scripts/createTaxonomy.py cwrc.rdf PoliticalAffiliation $(O_LANG) -hide | unflatten -l 20 -c 30 | dot -o$@ -Tsvg 
	# python3 scripts/createTaxonomy.py cwrc.rdf PoliticalAffiliation $(O_LANG) -disconnected | unflatten -l 20 -c 30 | dot -ofigures/d_politicalAffiliationTaxonomy-$(DATE_W_LANG).svg -Tsvg 
figures/genreTaxonomy-$(DATE_W_LANG).svg: genre.rdf scripts/createTaxonomy.py
	python3 scripts/createTaxonomy.py genre.rdf LiteraryGenre $(O_LANG) | unflatten -l 20 -c 30 | dot -o$@ -Tsvg 


testing-deploy: force all


# deploy to testing server--> called automatically with every change on git 
testing: all
	cat $(ONTOLOGY_W_DATE)-EN.html | sed 's/cwrc.ca\/ontologies\//cwrc.ca\/testing\//g' > ~/data/www/testing/$(ONTOLOGY_W_DATE)-EN.html
	cat $(ONTOLOGY_W_DATE)-FR.html  | sed 's/cwrc.ca\/ontologies\//cwrc.ca\/testing\//g' > ~/data/www/testing/$(ONTOLOGY_W_DATE)-FR.html
	cat $(ONTOLOGY)-preamble-EN.html | sed 's/cwrc.ca\/ontologies\//cwrc.ca\/testing\//g' > ~/data/www/testing/$(ONTOLOGY)-preamble-EN.html
	cat $(ONTOLOGY)-preamble-FR.html | sed 's/cwrc.ca\/ontologies\//cwrc.ca\/testing\//g' > ~/data/www/testing/$(ONTOLOGY)-preamble-FR.html
	
	cat our-team-EN.html | sed 's/cwrc.ca\/ontologies\//cwrc.ca\/testing\//g' > ~/data/www/testing/our-team-EN.html
	cat our-team-FR.html | sed 's/cwrc.ca\/ontologies\//cwrc.ca\/testing\//g' > ~/data/www/testing/our-team-FR.html

	cat $(ONTOLOGY_W_DATE).rdf | sed 's/cwrc.ca\/ontologies\//cwrc.ca\/testing\//g' > ~/data/www/testing/$(ONTOLOGY_W_DATE).rdf
	cat $(ONTOLOGY_W_DATE).nt | sed 's/cwrc.ca\/ontologies\//cwrc.ca\/testing\//g' > ~/data/www/testing/$(ONTOLOGY_W_DATE).nt
	cat $(ONTOLOGY_W_DATE).ttl | sed 's/cwrc.ca\/ontologies\//cwrc.ca\/testing\//g' > ~/data/www/testing/$(ONTOLOGY_W_DATE).ttl
	
	ln -sf ~/data/www/testing/$(ONTOLOGY_W_DATE)-EN.html ~/data/www/testing/$(ONTOLOGY).html
	ln -sf ~/data/www/testing/$(ONTOLOGY_W_DATE)-EN.html ~/data/www/testing/$(ONTOLOGY_W_DATE).html
	ln -sf ~/data/www/testing/$(ONTOLOGY_W_DATE)-FR.html ~/data/www/testing/$(ONTOLOGY)-FR.html
	ln -sf ~/data/www/testing/$(ONTOLOGY_W_DATE).rdf ~/data/www/testing/$(ONTOLOGY).rdf
	ln -sf ~/data/www/testing/$(ONTOLOGY_W_DATE).nt ~/data/www/testing/$(ONTOLOGY).nt
	ln -sf ~/data/www/testing/$(ONTOLOGY_W_DATE).ttl ~/data/www/testing/$(ONTOLOGY).ttl
	
	cp -f figures/* ~/data/www/testing/figures/.	
	cp -f -R css ~/data/www/testing/.
	cp -f -R js ~/data/www/testing/.
	cp -f -R documentation ~/data/www/testing/.

# curl -X POST -H 'Content-Type:application/sparql-update' -d 'CLEAR GRAPH <http://sparql.cwrc.ca/testing/$(ONTOLOGY)>' http://localhost:9999/blazegraph/sparql
# curl -X POST -H 'Content-Type:application/rdf+xml' --data-binary @~/data/www/testing/$(ONTOLOGY).rdf http://localhost:9999/blazegraph/sparql?context-uri=http://sparql.cwrc.ca/testing/$(ONTOLOGY)

documentation-test:	
	cp -f -R documentation ~/data/www/testing/.
	cp -f -R css ~/data/www/testing/.

documentation-prod:	
	cp -f -R documentation ~/data/www/ontologies/.
	cp -f -R css ~/data/www/ontologies/.

# deploy to production
deploy: all
	cp $(ONTOLOGY_W_DATE)-EN.html ~/data/www/ontologies/$(ONTOLOGY_W_DATE)-EN.html
	cp $(ONTOLOGY_W_DATE)-FR.html ~/data/www/ontologies/$(ONTOLOGY_W_DATE)-FR.html
	cp $(ONTOLOGY)-preamble-EN.html ~/data/www/ontologies/$(ONTOLOGY)-preamble-EN.html
	cp $(ONTOLOGY)-preamble-FR.html ~/data/www/ontologies/$(ONTOLOGY)-preamble-FR.html
	
	cp our-team-EN.html ~/data/www/ontologies/our-team-EN.html
	cp our-team-FR.html ~/data/www/ontologies/our-team-FR.html

	cp -f $(ONTOLOGY_W_DATE).rdf ~/data/www/ontologies/.
	cp -f $(ONTOLOGY_W_DATE).nt ~/data/www/ontologies/.
	cp -f $(ONTOLOGY_W_DATE).ttl ~/data/www/ontologies/.	
	
	ln -sf ~/data/www/ontologies/$(ONTOLOGY_W_DATE)-EN.html ~/data/www/ontologies/$(ONTOLOGY).html
	ln -sf ~/data/www/ontologies/$(ONTOLOGY_W_DATE)-EN.html ~/data/www/ontologies/$(ONTOLOGY_W_DATE).html
	ln -sf ~/data/www/ontologies/$(ONTOLOGY_W_DATE)-FR.html ~/data/www/ontologies/$(ONTOLOGY)-FR.html
	ln -sf ~/data/www/ontologies/$(ONTOLOGY_W_DATE).rdf ~/data/www/ontologies/$(ONTOLOGY).rdf
	ln -sf ~/data/www/ontologies/$(ONTOLOGY_W_DATE).nt ~/data/www/ontologies/$(ONTOLOGY).nt
	ln -sf ~/data/www/ontologies/$(ONTOLOGY_W_DATE).ttl ~/data/www/ontologies/$(ONTOLOGY).ttl
	
	cp -f figures/* ~/data/www/ontologies/figures/.	
	cp -f -R css ~/data/www/ontologies/.
	cp -f -R js ~/data/www/ontologies/.
	cp -f -R documentation ~/data/www/ontologies/.

# curl -X POST -H 'Content-Type:application/sparql-update' -d 'CLEAR GRAPH <http://sparql.cwrc.ca/ontologies/$(ONTOLOGY)>' http://localhost:9999/blazegraph/sparql
# curl -X POST -H 'Content-Type:application/rdf+xml' --data-binary @/var/www/public/ontologies/$(ONTOLOGY).rdf http://localhost:9999/blazegraph/sparql?context-uri=http://sparql.cwrc.ca/ontologies/$(ONTOLOGY)


# tests rdf files aren't broken before push, make push --> then commit
push: cwrc.rdf genre.rdf ii.rdf
	rapper cwrc.rdf -c
	rapper genre.rdf -c
	rapper ii.rdf -c

# soft clean
clean:
	rm -f *-citations.html
	rm -f *.bib
	rm -f *-template2*
	rm -f *$(ONTOLOGY_DATE).* 

# Hard clean of all generated files minus figure files (DO NOT RUN ON SERVER) 
clean-all:
	@ls | grep '[0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9].*'
	@echo "Are you sure you'd like to remove the following files(y/n)"
	@ls | grep '[0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9].*'| xargs -p rm -v

extraction:
	python3 scripts/cf_label_extraction.py cwrc.rdf scripts/CF_external_mapping.csv mapTest.csv 
	cat mapTest.csv | python3 scripts/fixcsv.py 40 > cf_master_mapping.csv 
	python3 scripts/occupation_label_extraction.py cwrc.rdf occupations.csv 
# 	cp cf_master_mapping.csv ~
#	cp occupations.csv /home/alliyya/stuff/work/cwrc/RDF-extraction/data/occupation_mapping.csv