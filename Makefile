MAKEFLAGS += -J2
# "2010-01-01"^^xsd:date
ONTOLOGY=cwrc
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
	touch $(ONTOLOGY)-template.html	
	rm -f $(ONTOLOGY)-ref.bib
all:	$(ONTOLOGY)-$(ONTOLOGY_DATE).owl $(ONTOLOGY)-FR-$(ONTOLOGY_DATE).html $(ONTOLOGY)-$(ONTOLOGY_DATE).html

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
all:	$(ONTOLOGY)-$(ONTOLOGY_DATE).html $(ONTOLOGY)-$(ONTOLOGY_DATE).ttl $(ONTOLOGY)-$(ONTOLOGY_DATE).nt  $(ONTOLOGY)-$(ONTOLOGY_DATE).owl #$(ONTOLOGY)-overall-$(ONTOLOGY_DATE).jpg		
	cp -f $(ONTOLOGY)-$(ONTOLOGY_DATE).html cwrc.html
testing:	all	
	cat $(ONTOLOGY)-$(ONTOLOGY_DATE).html | sed 's/\/ontology\//\/testing\//g' > /var/www/html/testing/$(ONTOLOGY)-$(ONTOLOGY_DATE).html
	cat $(ONTOLOGY)-FR-$(ONTOLOGY_DATE).html  | sed 's/\/ontology\//\/testing\//g' > /var/www/html/testing/$(ONTOLOGY)-FR-$(ONTOLOGY_DATE).html
	ln -sf /var/www/html/testing/$(ONTOLOGY)-$(ONTOLOGY_DATE).html /var/www/html/testing/$(ONTOLOGY).html
	ln -sf /var/www/html/testing/$(ONTOLOGY)-FR-$(ONTOLOGY_DATE).html /var/www/html/testing/$(ONTOLOGY)-FR.html
	cp -f $(ONTOLOGY)-$(ONTOLOGY_DATE).owl /var/www/html/testing/cwrc.owl
	cp -f $(ONTOLOGY)-$(ONTOLOGY_DATE).nt /var/www/html/testing/cwrc.nt
	cp -f $(ONTOLOGY)-$(ONTOLOGY_DATE).ttl /var/www/html/testing/cwrc.ttl	
	cp -f figures/* /var/www/html/testing/figures/.	
	cp -f -R css /var/www/html/testing/.
#	cp -f $(ONTOLOGY)-$(ONTOLOGY_DATE).owl  ~/public_html/.
#	cp -f $(ONTOLOGY)-overall-$(ONTOLOGY_DATE).jpg ~/public_html/images/.
#	cp -f $(ONTOLOGY)-overall-small-$(ONTOLOGY_DATE).jpg ~/public_html/images/.
$(DOCS_TEMPLATES): $(DOCS) $(ONTOLOGY).owl
	./generateTermDocumentation.sh doc $(ONTOLOGY)-docs/
$(ONTOLOGY)-$(ONTOLOGY_DATE).dot: $(ONTOLOGY).owl
	grep -v "rdfs:label" $(ONTOLOGY).owl  | grep -v "rdfs:comment"| grep -v "foaf:name" | grep -v "rdf:type" | rapper -o dot - "http://rdf.muninn-project.org/ontologies/"$(ONTOLOGY)"#" | grep -v "owl:Class" | grep -v "owl:ObjectProperty" > $(ONTOLOGY)-$(ONTOLOGY_DATE).dot
$(ONTOLOGY)-template-$(ONTOLOGY_DATE).html: $(ONTOLOGY)-template.html figures/religionTaxonomy-$(ONTOLOGY_DATE).svg figures/genreTaxonomy-$(ONTOLOGY_DATE).svg
	sed "s/PREVIOUS_ONTOLOGY/$(PREVIOUS_ONTOLOGY)/g"  < $(ONTOLOGY)-template.html | sed "s/ONTOLOGY_LOGO/$(ONTOLOGY_LOGO)/g" | sed "s/ONTOLOGY_NAME/$(ONTOLOGY)/g"  | sed "s/ONTOLOGY_DATE/$(ONTOLOGY_DATE)/g" |  sed "s/ONTOLOGY_LONGDATE/$(ONTOLOGY_LONGDATE)/g"  | sed "s/ONTOLOGY_VERSION/$(ONTOLOGY_VERSION)/g"  | sed 's/ONTOLOGY_LOGO/$(ONTOLOGY_LOGO)/g'  > $(ONTOLOGY)-template-$(ONTOLOGY_DATE).html
$(ONTOLOGY)-template2-$(ONTOLOGY_DATE).html: $(ONTOLOGY)-template-$(ONTOLOGY_DATE).html $(ONTOLOGY)-citations.html
	 m4 -P $(ONTOLOGY)-template-$(ONTOLOGY_DATE).html > $(ONTOLOGY)-template2-$(ONTOLOGY_DATE).html
$(ONTOLOGY)-$(ONTOLOGY_DATE).html: $(ONTOLOGY)-$(ONTOLOGY_DATE).owl $(ONTOLOGY)-template2-$(ONTOLOGY_DATE).html # $(ONTOLOGY)-overall-$(ONTOLOGY_DATE).jpg
	./scripts/docgen.py $(ONTOLOGY)-$(ONTOLOGY_DATE).owl $(ONTOLOGY) $(ONTOLOGY)-template2-$(ONTOLOGY_DATE).html  $(ONTOLOGY)-$(ONTOLOGY_DATE).html  en
$(ONTOLOGY)-FR-template-$(ONTOLOGY_DATE).html: $(ONTOLOGY)-template-fr.html figures/religionTaxonomy-$(ONTOLOGY_DATE).svg figures/genreTaxonomy-$(ONTOLOGY_DATE).svg
	sed "s/PREVIOUS_ONTOLOGY/$(PREVIOUS_ONTOLOGY)/g"  < $(ONTOLOGY)-template-fr.html | sed "s/ONTOLOGY_LOGO/$(ONTOLOGY_LOGO)/g" | sed "s/ONTOLOGY_NAME/$(ONTOLOGY)/g"  | sed "s/ONTOLOGY_DATE/$(ONTOLOGY_DATE)/g" |  sed "s/ONTOLOGY_LONGDATE/$(ONTOLOGY_LONGDATE)/g"  | sed "s/ONTOLOGY_VERSION/$(ONTOLOGY_VERSION)/g"  | sed 's/ONTOLOGY_LOGO/$(ONTOLOGY_LOGO)/g'  > $(ONTOLOGY)-FR-template-$(ONTOLOGY_DATE).html
$(ONTOLOGY)-FR-template2-$(ONTOLOGY_DATE).html: $(ONTOLOGY)-FR-template-$(ONTOLOGY_DATE).html $(ONTOLOGY)-citations.html
	 m4 -P $(ONTOLOGY)-FR-template-$(ONTOLOGY_DATE).html > $(ONTOLOGY)-FR-template2-$(ONTOLOGY_DATE).html
$(ONTOLOGY)-FR-$(ONTOLOGY_DATE).html: $(ONTOLOGY)-$(ONTOLOGY_DATE).owl $(ONTOLOGY)-FR-template2-$(ONTOLOGY_DATE).html # $(ONTOLOGY)-overall-$(ONTOLOGY_DATE).jpg
	./scripts/docgen.py $(ONTOLOGY)-$(ONTOLOGY_DATE).owl $(ONTOLOGY) $(ONTOLOGY)-template2-$(ONTOLOGY_DATE).html  $(ONTOLOGY)-$(ONTOLOGY_DATE).html  en
#$(ONTOLOGY)-overall-$(ONTOLOGY_DATE).jpg: $(ONTOLOGY)-$(ONTOLOGY_DATE).dot
#	dot -o $(ONTOLOGY)-overall-$(ONTOLOGY_DATE).jpg -Tpng $(ONTOLOGY)-$(ONTOLOGY_DATE).dot
#$(ONTOLOGY)-overall-small-$(ONTOLOGY_DATE).jpg:  $(ONTOLOGY)-overall-$(ONTOLOGY_DATE).jpg
#	convert -resize 320x200 $(ONTOLOGY)-overall-$(ONTOLOGY_DATE).jpg -resize 320x200 $(ONTOLOGY)-overall-small-$(ONTOLOGY_DATE).jpg
$(ONTOLOGY)-citations.html:     $(ONTOLOGY)-ref.bib
	bibtex2html --use-keys -nodoc -nobibsource -unicode --quiet -o - $(ONTOLOGY)-ref.bib  | sed "s/<\/table><hr><p><em>This file was generated by/<\/table>/" | head -n -1 > $(ONTOLOGY)-citations.html
$(ONTOLOGY)-ref.bib:
	wget -O $(ONTOLOGY)-ref.bib "https://api.zotero.org/groups/1018142/items/top?start=0&limit=100&format=bibtex&v=1"
figures/religionTaxonomy-$(ONTOLOGY_DATE).svg: $(ONTOLOGY)-$(ONTOLOGY_DATE).owl
	./scripts/createReligionTaxonomy.pl $(ONTOLOGY)-$(ONTOLOGY_DATE).owl | unflatten -l 5 -c 10 | dot -ofigures/religionTaxonomy-$(ONTOLOGY_DATE).svg -Tsvg 
figures/genreTaxonomy-$(ONTOLOGY_DATE).svg: genre.owl
	./scripts/createGenreTaxonomy.pl genre.owl | unflatten -l 5 -c 24 | dot -ofigures/genreTaxonomy-$(ONTOLOGY_DATE).svg -Tsvg
clean:
	rm -f $(ONTOLOGY)-$(ONTOLOGY_DATE).dot $(ONTOLOGY)-$(ONTOLOGY_DATE).owl $(ONTOLOGY)-template-$(ONTOLOGY_DATE).html $(ONTOLOGY)-template2-$(ONTOLOGY_DATE).html $(ONTOLOGY)-$(ONTOLOGY_DATE).html $(ONTOLOGY)-citations.html $(ONTOLOGY)-$(ONTOLOGY_DATE).tmp $(ONTOLOGY)-$(ONTOLOGY_DATE).counts $(ONTOLOGY)-$(ONTOLOGY_DATE).unique
testing-deploy: force all

clean-all:
	@ls -R | grep '[0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9].*'
	@echo "Are you sure you'd like to remove the following files(y/n)"
	@ls -R | grep '[0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9].*'| xargs -p rm -v

doc: scripts/docgen.py
	# french 
	./scripts/docgen.py $(ONTOLOGY)-$(ONTOLOGY_DATE).owl $(ONTOLOGY) $(ONTOLOGY)-template-fr.html  $(ONTOLOGY)-FR-$(ONTOLOGY_DATE).html fr
	@echo "\n\n\n\n\n"
	# anglais 
	./scripts/docgen.py $(ONTOLOGY)-$(ONTOLOGY_DATE).owl $(ONTOLOGY) $(ONTOLOGY)-template2-$(ONTOLOGY_DATE).html  $(ONTOLOGY)-$(ONTOLOGY_DATE).html  en
	./scripts/docgen.py genre.owl genre genre-template-fr.html  genre-fr-$(ONTOLOGY_DATE).html  fr
	./scripts/docgen.py genre.owl genre genre-template-en.html  genre-en-$(ONTOLOGY_DATE).html  en

doctest: scripts/docgen.py
	./scripts/docgen.py $(ONTOLOGY)-$(ONTOLOGY_DATE).owl $(ONTOLOGY) $(ONTOLOGY)-template2-$(ONTOLOGY_DATE).html  $(ONTOLOGY)-$(ONTOLOGY_DATE).html  en > ./scripts/test.html
