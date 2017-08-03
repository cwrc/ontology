MAKEFLAGS += -J2
ONTOLOGY?=cwrc
ONTOLOGY_DATE = $(shell date -u +"%Y-%m-%d")
DATE_CLEAN = $(shell date -u +"%Y%m%d")
ONTOLOGY_LONGDATE = $(shell date -d '$(ONTOLOGY_DATE)'  +'%d %B %Y')
ONTOLOGY_VERSION = $(shell xpath -e '/rdf:RDF/owl:Ontology/owl:versionInfo/text()' $(ONTOLOGY).owl  2> /dev/null)
ONTOLOGY_LOGO = $(shell xpath -e '/rdf:RDF/owl:Ontology/foaf:logo/@rdf:resource' $(ONTOLOGY).owl  2> /dev/null | sed 's/\//\\\//g' | cut -d "\"" -f 2)
PREVIOUS_ONTOLOGY = $(shell xpath -e '/rdf:RDF/owl:Ontology/owl:priorVersion/@rdf:resource' $(ONTOLOGY).owl  2> /dev/null | sed 's/\//\\\//g' | cut -d "\"" -f 2)
TOTAL_TRIPLES_CWRC_ONTOLOGY = $(shell cat $(ONTOLOGY)-$(ONTOLOGY_DATE).counts)
TOTAL_ENTITIES_CWRC_ONTOLOGY = $(shell cat $(ONTOLOGY)-$(ONTOLOGY_DATE).unique)

force:	$(ONTOLOGY).owl
	touch $(ONTOLOGY).owl
	touch $(ONTOLOGY)-template-EN.html	
	touch $(ONTOLOGY)-template-FR.html	
	rm -f $(ONTOLOGY)-ref.bib

all: $(ONTOLOGY)-$(ONTOLOGY_DATE).owl $(ONTOLOGY)-$(ONTOLOGY_DATE).tmp $(ONTOLOGY)-FR-$(ONTOLOGY_DATE).html $(ONTOLOGY)-$(ONTOLOGY_DATE)-EN.html $(ONTOLOGY).html

$(ONTOLOGY)-$(ONTOLOGY_DATE).tmp: $(ONTOLOGY).owl
	echo $(ONTOLOGY_LOGO)
	xpath $(ONTOLOGY).owl "/rdf:RDF" 1> /dev/null 2> /dev/null
	sed 's/DATE_TODAY/$(DATE_CLEAN)/g' < $(ONTOLOGY).owl > $(ONTOLOGY)-$(ONTOLOGY_DATE).tmp	
$(ONTOLOGY)-$(ONTOLOGY_DATE).counts: $(ONTOLOGY)-$(ONTOLOGY_DATE).tmp
	rapper $(ONTOLOGY)-$(ONTOLOGY_DATE).tmp | wc -l > $(ONTOLOGY)-$(ONTOLOGY_DATE).counts
$(ONTOLOGY)-$(ONTOLOGY_DATE).unique: $(ONTOLOGY)-$(ONTOLOGY_DATE).tmp
	rapper $(ONTOLOGY)-$(ONTOLOGY_DATE).tmp | cut -d " " -f 1 | sort | sort -u | wc -l > $(ONTOLOGY)-$(ONTOLOGY_DATE).unique
$(ONTOLOGY)-$(ONTOLOGY_DATE).owl: $(ONTOLOGY)-$(ONTOLOGY_DATE).unique $(ONTOLOGY)-$(ONTOLOGY_DATE).counts $(ONTOLOGY)-$(ONTOLOGY_DATE).tmp
	cat $(ONTOLOGY)-$(ONTOLOGY_DATE).tmp | sed 's/ONTOLOGY_DATE/$(ONTOLOGY_DATE)/g' | sed 's/TOTAL_TRIPLES_CWRC_ONTOLOGY/$(TOTAL_TRIPLES_CWRC_ONTOLOGY)/g' | sed 's/TOTAL_ENTITIES_CWRC_ONTOLOGY/$(TOTAL_ENTITIES_CWRC_ONTOLOGY)/g' > $(ONTOLOGY)-$(ONTOLOGY_DATE).owl	
$(ONTOLOGY)-$(ONTOLOGY_DATE).nt: $(ONTOLOGY)-$(ONTOLOGY_DATE).owl
	rapper $(ONTOLOGY)-$(ONTOLOGY_DATE).owl > $(ONTOLOGY)-$(ONTOLOGY_DATE).nt
$(ONTOLOGY)-$(ONTOLOGY_DATE).ttl: $(ONTOLOGY)-$(ONTOLOGY_DATE).owl
	rapper -o turtle $(ONTOLOGY)-$(ONTOLOGY_DATE).owl > $(ONTOLOGY)-$(ONTOLOGY_DATE).ttl	

$(ONTOLOGY).html: $(ONTOLOGY)-$(ONTOLOGY_DATE)-EN.html
	cp -f $(ONTOLOGY)-$(ONTOLOGY_DATE)-EN.html $(ONTOLOGY).html
testing: all
	cat $(ONTOLOGY)-$(ONTOLOGY_DATE)-EN.html | sed 's/cwrc.ca\/ontologies\//cwrc.ca\/testing\//g' > /var/www/html/testing/$(ONTOLOGY)-$(ONTOLOGY_DATE)-EN.html
	cat $(ONTOLOGY)-FR-$(ONTOLOGY_DATE).html  | sed 's/cwrc.ca\/ontologies\//cwrc.ca\/testing\//g' > /var/www/html/testing/$(ONTOLOGY)-FR-$(ONTOLOGY_DATE).html
	ln -sf /var/www/html/testing/$(ONTOLOGY)-$(ONTOLOGY_DATE)-EN.html /var/www/html/testing/$(ONTOLOGY).html
	ln -sf /var/www/html/testing/$(ONTOLOGY)-FR-$(ONTOLOGY_DATE).html /var/www/html/testing/$(ONTOLOGY)-FR.html
	cp -f $(ONTOLOGY)-$(ONTOLOGY_DATE).owl /var/www/html/testing/$(ONTOLOGY).owl
	cp -f $(ONTOLOGY)-$(ONTOLOGY_DATE).nt /var/www/html/testing/$(ONTOLOGY).nt
	cp -f $(ONTOLOGY)-$(ONTOLOGY_DATE).ttl /var/www/html/testing/$(ONTOLOGY).ttl	
	cp -f figures/* /var/www/html/testing/figures/.	
	cp -f -R css /var/www/html/testing/.

$(DOCS_TEMPLATES): $(DOCS) $(ONTOLOGY).owl
	./generateTermDocumentation.sh doc $(ONTOLOGY)-docs/
$(ONTOLOGY)-$(ONTOLOGY_DATE).dot: $(ONTOLOGY).owl
	grep -v "rdfs:label" $(ONTOLOGY).owl  | grep -v "rdfs:comment"| grep -v "foaf:name" | grep -v "rdf:type" | rapper -o dot - "http://rdf.muninn-project.org/ontologies/"$(ONTOLOGY)"#" | grep -v "owl:Class" | grep -v "owl:ObjectProperty" > $(ONTOLOGY)-$(ONTOLOGY_DATE).dot
$(ONTOLOGY)-template-$(ONTOLOGY_DATE)-EN.html: $(ONTOLOGY)-template-EN.html figures/religionTaxonomy-$(ONTOLOGY_DATE).svg figures/genreTaxonomy-$(ONTOLOGY_DATE).svg
	sed "s/PREVIOUS_ONTOLOGY/$(PREVIOUS_ONTOLOGY)/g"  < $(ONTOLOGY)-template-EN.html | sed "s/ONTOLOGY_LOGO/$(ONTOLOGY_LOGO)/g" | sed "s/ONTOLOGY_NAME/$(ONTOLOGY)/g"  | sed "s/ONTOLOGY_DATE/$(ONTOLOGY_DATE)/g" |  sed "s/ONTOLOGY_LONGDATE/$(ONTOLOGY_LONGDATE)/g"  | sed "s/ONTOLOGY_VERSION/$(ONTOLOGY_VERSION)/g"  | sed 's/ONTOLOGY_LOGO/$(ONTOLOGY_LOGO)/g'  > $(ONTOLOGY)-template-$(ONTOLOGY_DATE)-EN.html
$(ONTOLOGY)-template2-$(ONTOLOGY_DATE).html: $(ONTOLOGY)-template-$(ONTOLOGY_DATE)-EN.html $(ONTOLOGY)-citations.html
	 m4 -P $(ONTOLOGY)-template-$(ONTOLOGY_DATE)-EN.html > $(ONTOLOGY)-template2-$(ONTOLOGY_DATE).html
$(ONTOLOGY)-$(ONTOLOGY_DATE)-EN.html: $(ONTOLOGY)-$(ONTOLOGY_DATE).owl $(ONTOLOGY)-template2-$(ONTOLOGY_DATE).html # $(ONTOLOGY)-overall-$(ONTOLOGY_DATE).jpg
	./scripts/docgen.py $(ONTOLOGY)-$(ONTOLOGY_DATE).owl $(ONTOLOGY) $(ONTOLOGY)-template2-$(ONTOLOGY_DATE).html  $(ONTOLOGY)-$(ONTOLOGY_DATE)-EN.html  en
$(ONTOLOGY)-FR-template-$(ONTOLOGY_DATE).html: $(ONTOLOGY)-template-FR.html figures/religionTaxonomy-$(ONTOLOGY_DATE).svg figures/genreTaxonomy-$(ONTOLOGY_DATE).svg
	sed "s/PREVIOUS_ONTOLOGY/$(PREVIOUS_ONTOLOGY)/g"  < $(ONTOLOGY)-template-FR.html | sed "s/ONTOLOGY_LOGO/$(ONTOLOGY_LOGO)/g" | sed "s/ONTOLOGY_NAME/$(ONTOLOGY)/g"  | sed "s/ONTOLOGY_DATE/$(ONTOLOGY_DATE)/g" |  sed "s/ONTOLOGY_LONGDATE/$(ONTOLOGY_LONGDATE)/g"  | sed "s/ONTOLOGY_VERSION/$(ONTOLOGY_VERSION)/g"  | sed 's/ONTOLOGY_LOGO/$(ONTOLOGY_LOGO)/g'  > $(ONTOLOGY)-FR-template-$(ONTOLOGY_DATE).html
$(ONTOLOGY)-FR-template2-$(ONTOLOGY_DATE).html: $(ONTOLOGY)-FR-template-$(ONTOLOGY_DATE).html $(ONTOLOGY)-citations.html
	 m4 -P $(ONTOLOGY)-FR-template-$(ONTOLOGY_DATE).html > $(ONTOLOGY)-FR-template2-$(ONTOLOGY_DATE).html
$(ONTOLOGY)-FR-$(ONTOLOGY_DATE).html: $(ONTOLOGY)-$(ONTOLOGY_DATE).owl $(ONTOLOGY)-FR-template2-$(ONTOLOGY_DATE).html # $(ONTOLOGY)-overall-$(ONTOLOGY_DATE).jpg
	./scripts/docgen.py $(ONTOLOGY)-$(ONTOLOGY_DATE).owl $(ONTOLOGY) $(ONTOLOGY)-FR-template2-$(ONTOLOGY_DATE).html  $(ONTOLOGY)-FR-$(ONTOLOGY_DATE).html fr
$(ONTOLOGY)-citations.html:     cwrc-ref.bib
	bibtex2html --use-keys -nodoc -nobibsource -unicode --quiet -o - cwrc-ref.bib  | sed "s/<\/table><hr><p><em>This file was generated by/<\/table>/" | head -n -1 > $(ONTOLOGY)-citations.html
cwrc-ref.bib:
	wget -O cwrc-ref.bib "https://api.zotero.org/groups/1018142/items/top?start=0&limit=100&format=bibtex&v=1"
figures/religionTaxonomy-$(ONTOLOGY_DATE).svg: cwrc-$(ONTOLOGY_DATE).owl
	./scripts/createReligionTaxonomy.pl cwrc-$(ONTOLOGY_DATE).owl | unflatten -l 5 -c 10 | dot -ofigures/religionTaxonomy-$(ONTOLOGY_DATE).svg -Tsvg 
figures/genreTaxonomy-$(ONTOLOGY_DATE).svg: genre.owl
	./scripts/createGenreTaxonomy.pl genre.owl | unflatten -l 5 -c 24 | dot -ofigures/genreTaxonomy-$(ONTOLOGY_DATE).svg -Tsvg
clean:
	rm -f $(ONTOLOGY)-citations.html
	rm -f *$(ONTOLOGY_DATE).* 
testing-deploy: force all

clean-all:
	@ls -R | grep '[0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9].*'
	@echo "Are you sure you'd like to remove the following files(y/n)"
	@ls -R | grep '[0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9].*'| xargs -p rm -v

doc: scripts/docgen.py
	# french 
	./scripts/docgen.py $(ONTOLOGY)-$(ONTOLOGY_DATE).owl $(ONTOLOGY) $(ONTOLOGY)-template-FR.html  $(ONTOLOGY)-FR-$(ONTOLOGY_DATE).html fr
	@echo "\n\n\n\n\n"
	# anglais 
	./scripts/docgen.py $(ONTOLOGY)-$(ONTOLOGY_DATE).owl $(ONTOLOGY) $(ONTOLOGY)-template2-$(ONTOLOGY_DATE).html  $(ONTOLOGY)-$(ONTOLOGY_DATE)-EN.html  en
	./scripts/docgen.py genre.owl genre genre-template-FR.html  genre-FR-$(ONTOLOGY_DATE).html  fr
	./scripts/docgen.py genre.owl genre genre-template-EN.html  genre-EN-$(ONTOLOGY_DATE).html  en

doctest: scripts/docgen.py
	./scripts/docgen.py $(ONTOLOGY)-$(ONTOLOGY_DATE).owl $(ONTOLOGY) $(ONTOLOGY)-template2-$(ONTOLOGY_DATE).html  $(ONTOLOGY)-$(ONTOLOGY_DATE)-EN.html  en > ./scripts/test.html
