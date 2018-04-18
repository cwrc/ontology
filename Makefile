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
TOTAL_TRIPLES_CWRC_ONTOLOGY = $(shell cat $(ONTOLOGY_W_DATE).counts)
TOTAL_ENTITIES_CWRC_ONTOLOGY = $(shell cat $(ONTOLOGY_W_DATE).unique)

force:	$(ONTOLOGY).rdf
	touch $(ONTOLOGY).rdf
	touch $(ONTOLOGY)-template-$(O_LANG).html	
	rm -f cwrc-ref.bib

all: $(ONTOLOGY_W_DATE).rdf $(ONTOLOGY_W_DATE)-$(O_LANG).html $(ONTOLOGY).html $(ONTOLOGY)-preamble-$(O_LANG).html

$(ONTOLOGY_W_DATE).tmp: $(ONTOLOGY).rdf $(ONTOLOGY_W_DATE).bibli
	echo $(ONTOLOGY_LOGO)
	xpath $(ONTOLOGY).rdf "/rdf:RDF" 1> /dev/null 2> /dev/null
	sed 's/DATE_TODAY/$(DATE_CLEAN)/g' < $(ONTOLOGY).rdf  | grep -v "</rdf:RDF>" > $@	
	cat $(ONTOLOGY_W_DATE).bibli >> $@ 
	echo "</rdf:RDF>" >> $@ 
# Metadata to complete rdf file/html pages
$(ONTOLOGY_W_DATE).counts: $(ONTOLOGY_W_DATE).tmp
	rapper $(ONTOLOGY_W_DATE).tmp | wc -l > $@
$(ONTOLOGY_W_DATE).unique: $(ONTOLOGY_W_DATE).tmp
	rapper $(ONTOLOGY_W_DATE).tmp | cut -d " " -f 1 | sort | sort -u | wc -l > $@

# Final rdf file
$(ONTOLOGY_W_DATE).rdf: $(ONTOLOGY_W_DATE).unique $(ONTOLOGY_W_DATE).counts $(ONTOLOGY_W_DATE).tmp scripts/crossRef.py
	python3 scripts/crossRef.py $(ONTOLOGY_W_DATE).tmp > $(ONTOLOGY_W_DATE).tmp2
	cat $(ONTOLOGY_W_DATE).tmp2 | sed 's/ONTOLOGY_DATE/$(ONTOLOGY_DATE)/g' | sed 's/TOTAL_TRIPLES_CWRC_ONTOLOGY/$(TOTAL_TRIPLES_CWRC_ONTOLOGY)/g' | sed 's/TOTAL_ENTITIES_CWRC_ONTOLOGY/$(TOTAL_ENTITIES_CWRC_ONTOLOGY)/g' > $@	
	rapper $@ > $(ONTOLOGY_W_DATE).nt
	rapper -o turtle $@ > $(ONTOLOGY_W_DATE).ttl

# Gathering of bibliographic data/citations from cwrc 
$(ONTOLOGY_W_DATE).bibli:
	./scripts/getFedoraCollection.sh $(ONTOLOGY) $@
$(ONTOLOGY)-citations.html: $(ONTOLOGY_W_DATE).bibli scripts/cwrcCitations.py
	python3 scripts/cwrcCitations.py $(ONTOLOGY_W_DATE).rdf > $@
	# bibtex2html --use-keys -nodoc -nobibsource -a -dl -unicode --quiet -o - $(ONTOLOGY)-ref.bib  | sed "s/<\/table><hr><p><em>This file was generated by/<\/table>/" | head -n -1 > $@
# genre-ref.bib:
# 	curl  "https://api.zotero.org/groups/2089026/items/top?start=0&limit=100&format=bibtex&v=1" | grep -v "abstract = {" | grep -v "keywords = {" > $@
# cwrc-ref.bib:
# 	curl  "https://api.zotero.org/groups/1018142/items/top?start=0&limit=100&format=bibtex&v=1" | grep -v "abstract = {" | grep -v "keywords = {" > $@

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


# Generating svgs of taxonomies for preamble
figures/religionTaxonomy-$(DATE_W_LANG).svg: cwrc.rdf scripts/createTaxonomy.py
	python3 scripts/createTaxonomy.py cwrc.rdf Religion $(O_LANG) | unflatten -l 5 -c 10 | dot -o$@ -Tsvg 
figures/politicalAffiliationTaxonomy-$(DATE_W_LANG).svg: cwrc.rdf scripts/createTaxonomy.py
	python3 scripts/createTaxonomy.py cwrc.rdf PoliticalAffiliation $(O_LANG) -hide | unflatten -l 20 -c 30 | dot -o$@ -Tsvg 
	python3 scripts/createTaxonomy.py cwrc.rdf PoliticalAffiliation $(O_LANG) -disconnected | unflatten -l 20 -c 30 | dot -ofigures/d_politicalAffiliationTaxonomy-$(DATE_W_LANG).svg -Tsvg 
figures/genreTaxonomy-$(DATE_W_LANG).svg: genre.rdf scripts/createTaxonomy.py
	python3 scripts/createTaxonomy.py genre.rdf LiteraryGenre $(O_LANG) | unflatten -l 20 -c 30 | dot -o$@ -Tsvg 

# generating spec
$(ONTOLOGY_W_DATE)-$(O_LANG).html: $(ONTOLOGY_W_DATE).rdf $(ONTOLOGY)-template2-$(DATE_W_LANG).html python3 scripts/docgen.py
	python3 scripts/docgen.py $(ONTOLOGY_W_DATE).rdf $(ONTOLOGY)-template2-$(DATE_W_LANG).html  $@  $(O_LANG)
$(ONTOLOGY).html: $(ONTOLOGY_W_DATE)-EN.html
	cp -f $(ONTOLOGY_W_DATE)-EN.html $@

testing-deploy: force all


# deploy to testing server--> called automatically with every change on git 
testing: all
	cat $(ONTOLOGY_W_DATE)-EN.html | sed 's/cwrc.ca\/ontologies\//cwrc.ca\/testing\//g' > /var/www/html/testing/$(ONTOLOGY_W_DATE)-EN.html
	cat $(ONTOLOGY_W_DATE)-FR.html  | sed 's/cwrc.ca\/ontologies\//cwrc.ca\/testing\//g' > /var/www/html/testing/$(ONTOLOGY_W_DATE)-FR.html
	cat $(ONTOLOGY)-preamble-EN.html | sed 's/cwrc.ca\/ontologies\//cwrc.ca\/testing\//g' > /var/www/html/testing/$(ONTOLOGY)-preamble-EN.html
	cat $(ONTOLOGY)-preamble-FR.html | sed 's/cwrc.ca\/ontologies\//cwrc.ca\/testing\//g' > /var/www/html/testing/$(ONTOLOGY)-preamble-FR.html
	cat our-team-EN.html | sed 's/cwrc.ca\/ontologies\//cwrc.ca\/testing\//g' > /var/www/html/testing/our-team-EN.html
	cat our-team-FR.html | sed 's/cwrc.ca\/ontologies\//cwrc.ca\/testing\//g' > /var/www/html/testing/our-team-FR.html
	
	cp -f $(ONTOLOGY_W_DATE).rdf /var/www/html/testing/.
	cp -f $(ONTOLOGY_W_DATE).nt /var/www/html/testing/.
	cp -f $(ONTOLOGY_W_DATE).ttl /var/www/html/testing/.	
	
	ln -sf /var/www/html/testing/$(ONTOLOGY_W_DATE)-EN.html /var/www/html/testing/$(ONTOLOGY).html
	ln -sf /var/www/html/testing/$(ONTOLOGY_W_DATE)-EN.html /var/www/html/testing/$(ONTOLOGY_W_DATE).html
	ln -sf /var/www/html/testing/$(ONTOLOGY_W_DATE)-FR.html /var/www/html/testing/$(ONTOLOGY)-FR.html
	ln -sf /var/www/html/testing/$(ONTOLOGY_W_DATE).rdf /var/www/html/testing/$(ONTOLOGY).rdf
	ln -sf /var/www/html/testing/$(ONTOLOGY_W_DATE).nt /var/www/html/testing/$(ONTOLOGY).nt
	ln -sf /var/www/html/testing/$(ONTOLOGY_W_DATE).ttl /var/www/html/testing/$(ONTOLOGY).ttl
	
	cp -f figures/* /var/www/html/testing/figures/.	
	cp -f -R css /var/www/html/testing/.
	cp -f -R js /var/www/html/testing/.

# deploy to production
deploy: all
	cp $(ONTOLOGY_W_DATE)-EN.html /var/www/html/ontology/$(ONTOLOGY_W_DATE)-EN.html
	cp $(ONTOLOGY_W_DATE)-FR.html /var/www/html/ontology/$(ONTOLOGY_W_DATE)-FR.html
	cp $(ONTOLOGY)-preamble-EN.html /var/www/html/ontology/$(ONTOLOGY)-preamble-EN.html
	cp $(ONTOLOGY)-preamble-FR.html /var/www/html/ontology/$(ONTOLOGY)-preamble-FR.html
	
	cp -f $(ONTOLOGY_W_DATE).rdf /var/www/html/ontology/.
	cp -f $(ONTOLOGY_W_DATE).nt /var/www/html/ontology/.
	cp -f $(ONTOLOGY_W_DATE).ttl /var/www/html/ontology/.	
	
	ln -sf /var/www/html/ontology/$(ONTOLOGY_W_DATE)-EN.html /var/www/html/ontology/$(ONTOLOGY).html
	ln -sf /var/www/html/ontology/$(ONTOLOGY_W_DATE)-EN.html /var/www/html/ontology/$(ONTOLOGY_W_DATE).html
	ln -sf /var/www/html/ontology/$(ONTOLOGY_W_DATE)-FR.html /var/www/html/ontology/$(ONTOLOGY)-FR.html
	ln -sf /var/www/html/ontology/$(ONTOLOGY_W_DATE).rdf /var/www/html/ontology/$(ONTOLOGY).rdf
	ln -sf /var/www/html/ontology/$(ONTOLOGY_W_DATE).nt /var/www/html/ontology/$(ONTOLOGY).nt
	ln -sf /var/www/html/ontology/$(ONTOLOGY_W_DATE).ttl /var/www/html/ontology/$(ONTOLOGY).ttl
	
	cp -f figures/* /var/www/html/ontology/figures/.	
	cp -f -R css /var/www/html/ontology/.
	cp -f -R js /var/www/html/testing/.

# tests rdf files aren't broken before push, make push --> then commit
push: cwrc.rdf genre.rdf
	rapper cwrc.rdf -c
	rapper genre.rdf -c

# soft clean
clean:
	rm -f $(ONTOLOGY)-citations.html
	rm -f *$(ONTOLOGY_DATE).* 
# Hard clean of all generated files minus figure files (DO NOT RUN ON SERVER) 
clean-all:
	@ls | grep '[0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9].*'
	@echo "Are you sure you'd like to remove the following files(y/n)"
	@ls | grep '[0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9].*'| xargs -p rm -v

# Testing of scripts 
doc: scripts/docgen.py
	python3 scripts/docgen.py $(ONTOLOGY_W_DATE).rdf $(ONTOLOGY)-template-EN.html  $(ONTOLOGY_W_DATE)-EN.html  en
	python3 scripts/docgen.py $(ONTOLOGY_W_DATE).rdf $(ONTOLOGY)-template-FR.html  $(ONTOLOGY_W_DATE)-FR.html fr
doctest: scripts/docgen.py
	python3 scripts/docgen.py $(ONTOLOGY).rdf $(ONTOLOGY)-template2-$(DATE_W_LANG).html  $(ONTOLOGY_W_DATE)-EN.html  en
cross:
	python3 scripts/crossRef.py cwrc.rdf
