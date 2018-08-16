
import os
import argparse
import ConfigParser
import xml.etree.ElementTree as ET
from random import randint
import httplib, urllib
import codecs
parser=argparse.ArgumentParser()
parser.add_argument('-p', help='Path Parameters')
args=parser.parse_args()
parameters={}
if __name__ == '__main__':
    import pubmed_random_retrieval
    parameters = pubmed_random_retrieval.ReadParameters(args)     
    pubmed_random_retrieval.Main(parameters)
    
def ReadParameters(args):
    if(args.p!=None):
        Config = ConfigParser.ConfigParser()
        Config.read(args.p)
        parameters['quantity']=Config.get('MAIN', 'quantity')
        parameters['start']=Config.get('MAIN', 'start')
        parameters['end']=Config.get('MAIN', 'end')
        parameters['output_directory']=Config.get('MAIN', 'output')
    return parameters
 
def Main(parameters):
    retrieval_output=parameters['output_directory']
    if not os.path.exists(retrieval_output):
        os.makedirs(retrieval_output)
    quantity=int(parameters['quantity'])
    start=int(parameters['start'])
    final=int(parameters['end'])
    if not os.path.exists(retrieval_output):
        os.makedirs(retrieval_output)
    download_random(retrieval_output, quantity, start, final)
            
def download_random(source, quantity, start, final):
    print "Downloading " + str(quantity) + " pubmed random abstract, into " + source + " beginning from pmid"+str(start) + "pmid"+str(final)
    conn = httplib.HTTPSConnection("eutils.ncbi.nlm.nih.gov")
    i=0
    articles_ids=[]
    while (i<quantity):
        try:
            randomId=randint(start, final)
            randomId=str(randomId)
            params = urllib.urlencode({'db':'pubmed','retmode':'xml','id':'PMID'+randomId})
            conn.request("POST", "/entrez/eutils/efetch.fcgi", params )
            rf = conn.getresponse()
            if not rf.status == 200 :
                print "Error en la conexion: " + rf.status + " " + rf.reason 
                exit()
            response_efetch = rf.read()
            doc_xml = ET.fromstring(response_efetch) 
            article = doc_xml.find("PubmedArticle")
            if(article!=None):
                medline = article.find("MedlineCitation")
                article_xml = medline.find("Article")
                abstract_xml = article_xml.find("Abstract")
                if(abstract_xml!=None):
                    #abstract_text = abstract_xml.find("AbstractText").text
                    i=i+1
                    #print abstract_text
                    print str(i) + " from " +  str(quantity)
                    xml_file=codecs.open(source+"/PMID"+randomId+".xml",'w')
                    xml_file.write(response_efetch)
                    xml_file.flush()
                    xml_file.close()
                    articles_ids.append(randomId)
            rf.close()
            conn.close()
        except Exception as inst:
            print "Error Downloading " + randomId
            print inst
    thefile = open(source+'pmids.txt', 'w')
    for item in articles_ids:
        thefile.write("%s\n" % item)   
        
    