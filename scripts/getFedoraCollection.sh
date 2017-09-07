#!/bin/sh
#
#
if [ -z "$1" ] || [ -z "$2" ]
then
 echo "getFedoraCollection.sh [ontology] [outputfile]"
 exit 255;
fi
WORKFILE=/tmp/wo.$$
DOWNLOAD=/tmp/down.$$
BIBFILE=$2
if [ "$1" == "cwrc" ]
then
 STOPNOW="islandora/object/cwrc%3Aontologysources"
elif [ "$1" == "genre" ]
then
 STOPNOW="islandora/object/cwrc%3Agenreontologysources"
else
 echo "Unknown ontology $1"
 exit 255;
fi
#cwrc%3Agenreontologysources
#STOPNOW="islandora/object/cwrc%3Aontologysources"
if [ ! -f "scripts/mods2rdf.pl" ]
then
 wget -O "scripts/mods2rdf.pl" "https://raw.githubusercontent.com/muninn/ontology-tools/master/mods2rdf.pl"
 chmod 700 scripts/mods2rdf.pl
fi
rm -f ${WORKFILE}
while [ ! -z "$STOPNOW" ]
do
 curl "http://beta.cwrc.ca/${STOPNOW}" > ${DOWNLOAD}
 grep "islandora/object" ${DOWNLOAD} | grep title | grep "no-image" | cut -d "\"" -f 2 >> ${WORKFILE}
 STOPNOW=`grep "Go to next page" ${DOWNLOAD} | tr " " "\n" | grep href | cut -d "\"" -f 2`
done
rm -f ${DOWNLOAD}
rm -f ${BIBFILE}
echo "<!-- This is autogenerated from the beta.cwrc.ca bibliographic source. Do not edit. -->" >> ${BIBFILE}
for WORK in `cat ${WORKFILE}`
do
 echo ${WORK} 
 FILE=`echo ${WORK} | rev | cut -d "/" -f 1 | rev`
 RealURI=`echo ${FILE} | cut -d "%" -f 2 | cut -c 3-`
 curl "http://beta.cwrc.ca/${WORK}/datastream/MODS" > /tmp/myfile.$$
 ./scripts/mods2rdf.pl /tmp/myfile.$$ "${RealURI}" | ./scripts/xpath-unicode  -e "/rdf:RDF/node()" >> ${BIBFILE} 
done
rm -f ${WORKFILE}
echo ${BIBFILE}
