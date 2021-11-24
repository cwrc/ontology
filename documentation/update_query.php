<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="utf-8" />
    <!-- Bootstrap core CSS -->
    <link href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm" crossorigin="anonymous" />
    <link href="../css/cwrc.css" rel="stylesheet" type="text/css" />
    <link rel="shortcut icon" href="../css/favicon.ico" type="image/x-icon" />
    <link rel="icon" href="../css/favicon.ico" type="image/x-icon" />
    <title>Sample Orlando Queries</title>
</head>


<body>
    <nav class="navbar navbar-expand-lg navbar-dark fixed-top bg-dark">
      <a class="navbar-brand" href="/">
        <img src="http://sparql.cwrc.ca/images/cwrclogo-vert-white.png" height="30" class="align-top" alt="CWRC Logo"/> CWRC Ontologies</a>
      <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarCollapse" aria-controls="navbarCollapse" aria-expanded="false" aria-label="Toggle navigation">
        <span class="navbar-toggler-icon"></span>
      </button>
      <div class="collapse navbar-collapse" id="navbarCollapse">
        <ul class="navbar-nav mr-auto">
          <li class="nav-item"><a class="nav-link" href="/">Home</a></li>
          <li class="nav-item"><a class="nav-link" href="/sparql">SPARQL</a></li>
          <li class="nav-item dropdown">
            <a class="nav-link dropdown-toggle" href="#" id="navbarDropdown" role="button" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
              Preamble
            </a>
            <div class="dropdown-menu" aria-labelledby="navbarDropdown">
              <a class="dropdown-item" href="../cwrc-preamble-EN.html">CWRC Ontology</a>
              <a class="dropdown-item" href="../genre-preamble-EN.html">Genre Ontology</a>
              <a class="dropdown-item" href="../ii-preamble-EN.html">II Ontology</a>
            </div>
          </li>
          <li class="nav-item dropdown">
            <a class="nav-link dropdown-toggle" href="#" id="navbarDropdown" role="button" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
              Specification
            </a>
            <div class="dropdown-menu" aria-labelledby="navbarDropdown">
              <a class="dropdown-item" href="../cwrc.html">CWRC Ontology</a>
              <a class="dropdown-item" href="../genre.html">Genre Ontology</a>
              <a class="dropdown-item" href="../ii.html">II Ontology</a>
            </div>
          </li>
          <li class="nav-item dropdown">
            <a class="nav-link dropdown-toggle" href="#" id="navbarDropdown" role="button" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
              Guide to Our Dataset
            </a>
            <div class="dropdown-menu" aria-labelledby="navbarDropdown">
              <a class="dropdown-item" href="../releasenotes-EN.html">Release Notes</a>
              <div class="dropdown-divider"></div>
              <a class="dropdown-item" href="page_ONE.html">Intro to SPARQL</a>
              <a class="dropdown-item" href="page_TWO.html">Query Modifiers</a>
              <a class="dropdown-item" href="#">Sample Queries<span class="sr-only">(current)</span></a>
            </div>
          </li>
          <li class="nav-item"><a class="nav-link" href="../our-team-EN.html">Our Team</a></li>
          <li class="nav-item"><a class="nav-link" href="https://github.com/cwrc/ontology">Github</a></li>
        </ul>
        <span class="navbar-text">The Ontology of the Canadian Writing Research Collaboratory</span>
      </div>
    </nav>
    <div class="container-fluid">
        <div class="row">
            <nav class="col-xl-2 col-lg-3 col-md-12 d-none d-lg-block bg-light sidebar">
                <div class="sidebar-sticky">
                    <div class="sidebar-heading justify-content-between align-items-center px-3 mt-4 mb-1 text-muted">
                        <span>Table of Contents</span>
                        <a class="d-flex align-items-center text-muted" href="#"></a>
                        <div id="toc">
                            <!-- Table of Contents -->
                        </div>
                    </div>
                </div>
            </nav>
            <main role="main" class="col-xl-10 col-lg-9 col-md-12 ml-sm-auto pt-3 px-4" data-spy="scroll" data-target="#toc">
                <h1>Sample Queries to get started</h1>
                

            <?php
             $names = array("Abdy, Maria","Abergavenny, Frances Neville, Baroness","Ackland, Valentine","Adams, Abigail","Adams, Henry Brooks","Adams, Sarah Flower","Adcock, Fleur","Addison, Joseph","Aguilar, Grace","Aiken, Joan","Aikin, Lucy","Ainsworth, William Harrison","Akhmatova, Anna","Alcott, Louisa May","Alderman, Naomi","Alexander, Cecil Frances","Alexander, Mrs","Alison, Archibald, 1792 - 1867","Allatini, Rose","Allen, Grant","Allen, Hannah","Allingham, Margery","Allingham, William","Allnutt, Gillian","Alma-Tadema, Laurence","Amiel, Henri-Fr&eacute;d&eacute;ric","Andersen, Hans Christian","Angelou, Maya","Anger, Jane","Anna Livia","Anspach, Elizabeth, Margravine of","Arendt, Hannah","Ariadne","Arnold, Matthew","Arrowsmith, Pat","Ashbridge, Elizabeth","Ashford, Daisy","Askew, Anne","Asquith, Lady Cynthia","Astell, Mary","Athill, Diana","Atkins, Anna","Atwood, Margaret","Aubin, Penelope","Auden, W. H.","Audland, Anne","Aulnoy, Marie-Catherine d'","Austen, Jane","Austin, Sarah","Avery, Elizabeth","Ayres, Ruby M.","Aytoun, William Edmonstoune","Bacon, Anne","Bagehot, Walter","Bagnold, Enid","Bailey, Mary","Baillie, Joanna","Bainbridge, Beryl","Baker, Elizabeth","Baker, Ella","Baldwin, Louisa","Balfour, Clara","Ballantyne, R. M.","Balzac, Honor&eacute; de","Banks, Isabella","Bannerman, Anne","Bannerman, Helen","Barbauld, Anna Letitia","Barber, Mary","Barcynska, H&eacute;l&egrave;ne","Barham, Richard Harris","Barker, Jane","Barker, Mary Anne","Barker, Pat","Barnard, Charlotte","Barnard, Lady Anne","Barnes, Djuna","Barney, Natalie Clifford","Barrell, Maria","Barrie, Sir J. M.","Barrington, Emilie","Basset, Mary","Bathurst, Elizabeth","Battier, Henrietta","Baudelaire, Charles","Bawden, Nina","Beach, Sylvia","Beauclerc, Amelia","Beaumont, Agnes","Beauvoir, Simone de","Becker, Lydia","Beckett, Samuel","Beckford, William","Bedford, Sybille","Beer, Patricia","Beeton, Isabella","Behn, Aphra","Bellerby, Frances","Bell, Eva Mary","Bell, Gertrude","Belli, Giuseppe Gioachino","Benger, Elizabeth Ogilvy","Bennett, Anna Maria","Bennett, Arnold","Benson, Stella","Benson, Theodora","Bensusan, Inez","Bentley, Elizabeth","Bentley, Phyllis","Besant, Annie","Besant, Sir Walter","Betham-Edwards, Matilda","Betham, Mary Matilda","Betjeman, John","Beverley, Elizabeth","Bevington, L. S.","Biddle, Hester","Billington, Mary Frances","Bird, Isabella","Bishop, Elizabeth","Blackburne, E. Owens","Blackburn, Helen","Black, Clementina");
            (isset($_POST["stdname"])) ? $stdname = $_POST["stdname"] : $stdname="Abdy, Maria";
             
            ?>
<h2>Retrieving the simple triples for a particular author</h2>
<p>In the following query you can replace '<strong><?php echo $stdname; ?>'</strong> with the standard name of another author</p>
            <form action="update_query.php" method="post">
              Name:
              <select name="stdname">
                <?php 
                  foreach($names as $fname){
                    echo "<option "; 
                    if ($stdname == $fname ) echo 'selected ' ;  
                    echo 'value="'.$fname.'">'.$fname.'</option>';
                  }
                ?>
              </select>
              <input type="submit" name="submit" value="Update SPARQL Query">  
            </form>




<p>
  <?php $query_url = "https://yasgui.lincsproject.ca/#query=+PREFIX+cwrc%3A+%3Chttp%3A%2F%2Fsparql.cwrc.ca%2Fontologies%2Fcwrc%23%3E%0A++PREFIX+rdf%3A+%3Chttp%3A%2F%2Fwww.w3.org%2F1999%2F02%2F22-rdf-syntax-ns%23%3E%0A++PREFIX+rdfs%3A+%3Chttp%3A%2F%2Fwww.w3.org%2F2000%2F01%2Frdf-schema%23%3E%0A++PREFIX+data%3A+%3Chttp%3A%2F%2Fcwrc.ca%2Fcwrcdata%2F%3E%0A++PREFIX+skos%3A+%3Chttp%3A%2F%2Fwww.w3.org%2F2004%2F02%2Fskos%2Fcore%23%3E%0A++CONSTRUCT+%7B%0A++++%3FcontextFocus+%3FsubjectCentricPredicate+%3Fo+.%0A++++%3FcontextFocus+rdfs%3Alabel+%3Flabel.%0A++++%3FcontextFocus+skos%3AaltLabel+%3Fname.%0A++%7D+WHERE+%7B%0A++++GRAPH+%3Chttp%3A%2F%2Fsparql.cwrc.ca%2Fdb%2FBiographyV2Beta%3E+%7B%0A++++++%3Fperson+rdfs%3Alabel+%22".urlencode($stdname)."%22.%0A++++++BIND(%3Fperson+AS+%3FcontextFocus)%0A+++++++++%3Fcontext+cwrc%3AcontextFocus+%3FcontextFocus+%3B%0A++++++++++++++++++%3Fp+%3Fo+%3B%0A++++++%7D++++++++++++++++++++++.%0A++++++%23+Grab+the+correct+relationship+for+the+predicate+we+are+looking+for%0A++++++%3Fp+cwrc%3AsubjectCentricPredicate+%3FsubjectCentricPredicate+.+++%0A++++%3FcontextFocus+rdfs%3Alabel+%3Flabel.%0A++++%3FcontextFocus+skos%4AaltLabel+%3Fname.%0A++%7D+&contentTypeConstruct=text%2Fturtle&contentTypeSelect=application%2Fsparql-results%2Bjson&endpoint=https://fuseki.lincsproject.ca/cwrc/sparql&requestMethod=POST&tabTitle=Query+2&headers=%7B%7D&outputFormat=rawResponse"
  ?>
  <a href="<?php echo $query_url; ?>">Link to query</a></p>
<pre><code>
  PREFIX cwrc: &lt;http://sparql.cwrc.ca/ontologies/cwrc#&gt;
  PREFIX rdf: &lt;http://www.w3.org/1999/02/22-rdf-syntax-ns#&gt;
  PREFIX rdfs: &lt;http://www.w3.org/2000/01/rdf-schema#&gt;
  PREFIX data: &lt;http://cwrc.ca/cwrcdata/&gt;
  PREFIX skos: &lt;http://www.w3.org/2004/02/skos/core#&gt;
  CONSTRUCT {
    ?contextFocus ?subjectCentricPredicate ?o .
    ?contextFocus rdfs:label ?label.
    ?contextFocus skos:altLabel ?name.
  } WHERE {
    GRAPH &lt;http://sparql.cwrc.ca/db/BiographyV2Beta&gt; {
      ?person rdfs:label <strong>"<?php echo $stdname; ?>"</strong>.
      BIND(?person AS ?contextFocus)
         ?context cwrc:contextFocus ?contextFocus ;
                  ?p ?o ;
      }                      .
      # Grab the correct relationship for the predicate we are looking for
      ?p cwrc:subjectCentricPredicate ?subjectCentricPredicate .   
    ?contextFocus rdfs:label ?label.
    ?contextFocus skos:altLabel ?name.
  } 
</code></pre>

                <pre id="query1">
                    <code>PREFIX cwrc: &lt;http://sparql.cwrc.ca/ontologies/cwrc#&gt;
PREFIX rdf: &lt;http://www.w3.org/1999/02/22-rdf-syntax-ns#&gt;
PREFIX rdfs: &lt;http://www.w3.org/2000/01/rdf-schema#&gt;
PREFIX data: &lt;http://cwrc.ca/cwrcdata/&gt;
PREFIX skos: &lt;http://www.w3.org/2004/02/skos/core#&gt;
PREFIX oa: &lt;http://www.w3.org/ns/oa#&gt;

SELECT ?obj ?snippet WHERE { 
    GRAPH &lt;http://sparql.cwrc.ca/db/BiographyV2Beta&gt; {
        ?context ?pred ?obj;
            cwrc:contextFocus ?person;
            oa:hasTarget ?target;
            rdf:type cwrc:FamilyContext.
        ?person rdfs:label <strong>"<?php echo $stdname; ?>"</strong>.
    }
    
    ?target oa:hasSelector ?xpath_selector.
    ?xpath_selector oa:refinedBy ?text_selector.
    ?text_selector oa:exact ?snippet.
    ?pred cwrc:subjectCentricPredicate <strong>cwrc:hasFather</strong>.
}                   </code>
                </pre>

              
                    <ul>
                        <li><a href="http://sparql.cwrc.ca/ontologies/cwrc.html#hasAunt">hasAunt</a></li>
                        <li><a href="http://sparql.cwrc.ca/ontologies/cwrc.html#hasUncle">hasUncle</a></li>
                        <li><a href="http://sparql.cwrc.ca/ontologies/cwrc.html#hasGrandFather">hasGrandFather</a></li>
                        <li><a href="http://sparql.cwrc.ca/ontologies/cwrc.html#hasGrandMother">hasGrandMother</a></li>
                        <li><a href="http://sparql.cwrc.ca/ontologies/cwrc.html#hasGrandDaughter">hasGrandDaughter</a></li>
                        <li><a href="http://sparql.cwrc.ca/ontologies/cwrc.html#hasGrandSon">hasGrandSon</a></li>
                        <li><a href="http://sparql.cwrc.ca/ontologies/cwrc.html#hasNephew">hasNephew</a></li>
                        <li><a href="http://sparql.cwrc.ca/ontologies/cwrc.html#hasStepSister">hasStepSister</a></li>
                        <li><a href="http://sparql.cwrc.ca/ontologies/cwrc.html#hasStepBrother">hasStepBrother</a></li>
                    </ul>
                    
                        
                    
            </main>
        </div>
    </div>
    <!-- Bootstrap core JavaScript
      ================================================== -->
    <!-- Placed at the end of the document so the pages load faster -->
    <script src="https://code.jquery.com/jquery-3.2.1.slim.min.js" integrity="sha384-KJ3o2DKtIkvYIK3UENzmM7KCkRr/rE9/Qpg6aAZGJwFDMVNA/GpGFF93hXpG5KkN" crossorigin="anonymous"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.11.0/umd/popper.min.js" integrity="sha384-b/U6ypiBEHpOf/4+1nzFpr53nxSS+GLCkfwBdFNTxtclqqenISfwAzpKaMNFNmj4" crossorigin="anonymous"></script>
    <script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/js/bootstrap.min.js" integrity="sha384-JZR6Spejh3U02d8jOt6vLEHfe/JQGiRRSQQxSfFWpi1MquVdAyjUar5+76PVCmYl" crossorigin="anonymous"></script>
    <script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/js/bootstrap.bundle.min.js" integrity="sha384-feJI7QwhOS+hwpX2zkaeJQjeiwlhOP+SdQDqhgvvo1DsjtiSQByFdThsxO669S2D" crossorigin="anonymous"></script>
    <script src="../js/toc.js"></script>
    <script src="../js/svg-pan-zoom.min.js"></script>
    <script>
    window.onload = function() {
        var options = {
            selector: 'h2, h3, h4, h5',
            scope: 'main'
        };

        var container = document.querySelector('#toc');
        var toc = initTOC(options);
        container.appendChild(toc);
    };
    </script>
</body>

</html>