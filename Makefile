MAKEFLAGS += -J2
ONTOLOGY?=cwrc
O_LANG?=EN
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
	touch $(ONTOLOGY)-template-$(O_LANG).html	
	rm -f $(ONTOLOGY)-ref.bib

all: $(ONTOLOGY)-$(ONTOLOGY_DATE).owl $(ONTOLOGY)-$(ONTOLOGY_DATE).tmp $(ONTOLOGY)-$(ONTOLOGY_DATE)-$(O_LANG).html $(ONTOLOGY).html $(ONTOLOGY)-$(ONTOLOGY_DATE).ttl $(ONTOLOGY)-$(ONTOLOGY_DATE).nt $(ONTOLOGY)-$(ONTOLOGY_DATE).bibli


$(ONTOLOGY)-$(ONTOLOGY_DATE).tmp: $(ONTOLOGY).owl $(ONTOLOGY)-$(ONTOLOGY_DATE).bibli
	echo $(ONTOLOGY_LOGO)
	xpath $(ONTOLOGY).owl "/rdf:RDF" 1> /dev/null 2> /dev/null
	sed 's/DATE_TODAY/$(DATE_CLEAN)/g' < $(ONTOLOGY).owl  | grep -v "</rdf:RDF>" > $(ONTOLOGY)-$(ONTOLOGY_DATE).tmp	
	cat $(ONTOLOGY)-$(ONTOLOGY_DATE).bibli >> $(ONTOLOGY)-$(ONTOLOGY_DATE).tmp 
	echo "</rdf:RDF>" >> $(ONTOLOGY)-$(ONTOLOGY_DATE).tmp 


$(ONTOLOGY)-$(ONTOLOGY_DATE).counts: $(ONTOLOGY)-$(ONTOLOGY_DATE).tmp
	rapper $(ONTOLOGY)-$(ONTOLOGY_DATE).tmp | wc -l > $(ONTOLOGY)-$(ONTOLOGY_DATE).counts
$(ONTOLOGY)-$(ONTOLOGY_DATE).unique: $(ONTOLOGY)-$(ONTOLOGY_DATE).tmp
	rapper $(ONTOLOGY)-$(ONTOLOGY_DATE).tmp | cut -d " " -f 1 | sort | sort -u | wc -l > $(ONTOLOGY)-$(ONTOLOGY_DATE).unique
$(ONTOLOGY)-$(ONTOLOGY_DATE).owl: $(ONTOLOGY)-$(ONTOLOGY_DATE).unique $(ONTOLOGY)-$(ONTOLOGY_DATE).counts $(ONTOLOGY)-$(ONTOLOGY_DATE).tmp
	./scripts/crossRef.py $(ONTOLOGY)-$(ONTOLOGY_DATE).tmp > $(ONTOLOGY)-$(ONTOLOGY_DATE).tmp2
	cat $(ONTOLOGY)-$(ONTOLOGY_DATE).tmp2 | sed 's/ONTOLOGY_DATE/$(ONTOLOGY_DATE)/g' | sed 's/TOTAL_TRIPLES_CWRC_ONTOLOGY/$(TOTAL_TRIPLES_CWRC_ONTOLOGY)/g' | sed 's/TOTAL_ENTITIES_CWRC_ONTOLOGY/$(TOTAL_ENTITIES_CWRC_ONTOLOGY)/g' > $(ONTOLOGY)-$(ONTOLOGY_DATE).owl	
$(ONTOLOGY)-$(ONTOLOGY_DATE).nt: $(ONTOLOGY)-$(ONTOLOGY_DATE).owl
	rapper $(ONTOLOGY)-$(ONTOLOGY_DATE).owl > $(ONTOLOGY)-$(ONTOLOGY_DATE).nt
$(ONTOLOGY)-$(ONTOLOGY_DATE).ttl: $(ONTOLOGY)-$(ONTOLOGY_DATE).owl
	rapper -o turtle $(ONTOLOGY)-$(ONTOLOGY_DATE).owl > $(ONTOLOGY)-$(ONTOLOGY_DATE).ttl	
$(ONTOLOGY)-$(ONTOLOGY_DATE).bibli:
	./scripts/getFedoraCollection.sh $(ONTOLOGY) $(ONTOLOGY)-$(ONTOLOGY_DATE).bibli
$(DOCS_TEMPLATES): $(DOCS) $(ONTOLOGY).owl
	./generateTermDocumentation.sh doc $(ONTOLOGY)-docs/
$(ONTOLOGY)-$(ONTOLOGY_DATE).dot: $(ONTOLOGY).owl
	grep -v "rdfs:label" $(ONTOLOGY).owl  | grep -v "rdfs:comment"| grep -v "foaf:name" | grep -v "rdf:type" | rapper -o dot - "http://rdf.muninn-project.org/ontologies/"$(ONTOLOGY)"#" | grep -v "owl:Class" | grep -v "owl:ObjectProperty" > $(ONTOLOGY)-$(ONTOLOGY_DATE).dot

$(ONTOLOGY)-template-$(ONTOLOGY_DATE)-$(O_LANG).html: $(ONTOLOGY)-template-$(O_LANG).html figures/religionTaxonomy-$(ONTOLOGY_DATE)-$(O_LANG).svg figures/politicalAffiliationTaxonomy-$(ONTOLOGY_DATE)-$(O_LANG).svg #figures/genreTaxonomy-$(ONTOLOGY_DATE)-$(O_LANG).svg
	sed "s/PREVIOUS_ONTOLOGY/$(PREVIOUS_ONTOLOGY)/g"  < $(ONTOLOGY)-template-$(O_LANG).html | sed "s/ONTOLOGY_LOGO/$(ONTOLOGY_LOGO)/g" | sed "s/ONTOLOGY_NAME/$(ONTOLOGY)/g"  | sed "s/ONTOLOGY_DATE/$(ONTOLOGY_DATE)/g" |  sed "s/ONTOLOGY_LONGDATE/$(ONTOLOGY_LONGDATE)/g"  | sed "s/ONTOLOGY_VERSION/$(ONTOLOGY_VERSION)/g"  | sed 's/ONTOLOGY_LOGO/$(ONTOLOGY_LOGO)/g'  > $(ONTOLOGY)-template-$(ONTOLOGY_DATE)-$(O_LANG).html
$(ONTOLOGY)-template2-$(ONTOLOGY_DATE)-$(O_LANG).html: $(ONTOLOGY)-template-$(ONTOLOGY_DATE)-$(O_LANG).html $(ONTOLOGY)-citations.html
	 m4 -P $(ONTOLOGY)-template-$(ONTOLOGY_DATE)-$(O_LANG).html > $(ONTOLOGY)-template2-$(ONTOLOGY_DATE)-$(O_LANG).html
$(ONTOLOGY)-$(ONTOLOGY_DATE)-$(O_LANG).html: $(ONTOLOGY)-$(ONTOLOGY_DATE).owl $(ONTOLOGY)-template2-$(ONTOLOGY_DATE)-$(O_LANG).html
	./scripts/docgen.py $(ONTOLOGY)-$(ONTOLOGY_DATE).owl $(ONTOLOGY)-template2-$(ONTOLOGY_DATE)-$(O_LANG).html  $(ONTOLOGY)-$(ONTOLOGY_DATE)-$(O_LANG).html  $(O_LANG)

$(ONTOLOGY)-citations.html:     cwrc-ref.bib
	bibtex2html --use-keys -nodoc -nobibsource -unicode --quiet -o - cwrc-ref.bib  | sed "s/<\/table><hr><p><em>This file was generated by/<\/table>/" | head -n -1 > $(ONTOLOGY)-citations.html
cwrc-ref.bib:
	curl  "https://api.zotero.org/groups/1018142/items/top?start=0&limit=100&format=bibtex&v=1" | grep -v "abstract = {" | grep -v "keywords = {" > cwrc-ref.bib
figures/religionTaxonomy-$(ONTOLOGY_DATE)-$(O_LANG).svg: cwrc.owl scripts/createTaxonomy.pl
	./scripts/createTaxonomy.pl cwrc.owl Religion $(O_LANG) | unflatten -l 5 -c 10 | dot -ofigures/religionTaxonomy-$(ONTOLOGY_DATE)-$(O_LANG).svg -Tsvg 
figures/politicalAffiliationTaxonomy-$(ONTOLOGY_DATE)-$(O_LANG).svg: cwrc.owl scripts/createTaxonomy.pl
	./scripts/createTaxonomy.pl cwrc.owl PoliticalAffiliation $(O_LANG) | unflatten -l 5 -c 10 | dot -ofigures/politicalAffiliationTaxonomy-$(ONTOLOGY_DATE)-$(O_LANG).svg -Tsvg 
figures/genreTaxonomy-$(ONTOLOGY_DATE)-$(O_LANG).svg: genre.owl scripts/createTaxonomy.pl
	./scripts/createTaxonomy.pl genre.owl Genre $(O_LANG) | unflatten -l 5 -c 10 | dot -ofigures/genreTaxonomy-$(ONTOLOGY_DATE)-$(O_LANG).svg -Tsvg 


$(ONTOLOGY).html: $(ONTOLOGY)-$(ONTOLOGY_DATE)-EN.html
	cp -f $(ONTOLOGY)-$(ONTOLOGY_DATE)-EN.html $(ONTOLOGY).html
	rm $(ONTOLOGY)-template-$(ONTOLOGY_DATE)-$(O_LANG).html
	rm $(ONTOLOGY)-template2-$(ONTOLOGY_DATE)-$(O_LANG).html
	rm $(ONTOLOGY)-$(ONTOLOGY_DATE).tmp2
	rm $(ONTOLOGY)-$(ONTOLOGY_DATE).tmp

testing-deploy: force all
testing: all
	cat $(ONTOLOGY)-$(ONTOLOGY_DATE)-EN.html | sed 's/cwrc.ca\/ontologies\//cwrc.ca\/testing\//g' > /var/www/html/testing/$(ONTOLOGY)-$(ONTOLOGY_DATE)-EN.html
	cat $(ONTOLOGY)-$(ONTOLOGY_DATE)-FR-.html  | sed 's/cwrc.ca\/ontologies\//cwrc.ca\/testing\//g' > /var/www/html/testing/$(ONTOLOGY)-FR-$(ONTOLOGY_DATE).html
	cp -f $(ONTOLOGY)-$(ONTOLOGY_DATE).owl /var/www/html/testing/.
	cp -f $(ONTOLOGY)-$(ONTOLOGY_DATE).nt /var/www/html/testing/.
	cp -f $(ONTOLOGY)-$(ONTOLOGY_DATE).ttl /var/www/html/testing/.	
	ln -sf /var/www/html/testing/$(ONTOLOGY)-$(ONTOLOGY_DATE)-EN.html /var/www/html/testing/$(ONTOLOGY).html
	ln -sf /var/www/html/testing/$(ONTOLOGY)-$(ONTOLOGY_DATE)-EN.html /var/www/html/testing/$(ONTOLOGY)-$(ONTOLOGY_DATE).html
	ln -sf /var/www/html/testing/$(ONTOLOGY)-$(ONTOLOGY_DATE)-FR.html /var/www/html/testing/$(ONTOLOGY)-FR.html
	ln -sf /var/www/html/testing/$(ONTOLOGY)-$(ONTOLOGY_DATE).owl /var/www/html/testing/$(ONTOLOGY).owl
	ln -sf /var/www/html/testing/$(ONTOLOGY)-$(ONTOLOGY_DATE).nt /var/www/html/testing/$(ONTOLOGY).nt
	ln -sf /var/www/html/testing/$(ONTOLOGY)-$(ONTOLOGY_DATE).ttl /var/www/html/testing/$(ONTOLOGY).ttl
	cp -f figures/* /var/www/html/testing/figures/.	
	cp -f -R css /var/www/html/testing/.

push: cwrc.owl genre.owl
	rapper cwrc.owl -c
	rapper genre.owl -c
clean:
	rm -f $(ONTOLOGY)-citations.html
	rm -f *$(ONTOLOGY_DATE).* 
clean-all:
	@ls -R | grep '[0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9].*'
	@echo "Are you sure you'd like to remove the following files(y/n)"
	@ls -R | grep '[0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9].*'| xargs -p rm -v

doc: scripts/docgen.py
	./scripts/docgen.py $(ONTOLOGY)-$(ONTOLOGY_DATE).owl $(ONTOLOGY)-template-FR.html  $(ONTOLOGY)-FR-$(ONTOLOGY_DATE).html fr
	./scripts/docgen.py $(ONTOLOGY)-$(ONTOLOGY_DATE).owl $(ONTOLOGY)-template2-$(ONTOLOGY_DATE).html  $(ONTOLOGY)-$(ONTOLOGY_DATE)-EN.html  en
	./scripts/docgen.py genre.owl genre genre-template-FR.html  genre-FR-$(ONTOLOGY_DATE).html  fr
	./scripts/docgen.py genre.owl genre genre-template-EN.html  genre-EN-$(ONTOLOGY_DATE).html  en
doctest: scripts/docgen.py
	./scripts/docgen.py $(ONTOLOGY)-$(ONTOLOGY_DATE).owl $(ONTOLOGY)-template2-$(ONTOLOGY_DATE).html  $(ONTOLOGY)-$(ONTOLOGY_DATE)-EN.html  en > ./scripts/test.html
