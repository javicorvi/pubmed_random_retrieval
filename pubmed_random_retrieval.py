import os
import sys
import argparse
import ConfigParser
import xml.etree.ElementTree as ET
from random import randint
import httplib, urllib
import codecs
import logging
import time

logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)

'''
Parameters configuration
'''

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
        parameters['random_file']=Config.get('MAIN', 'random_file')
        parameters['random_folder']=Config.get('MAIN', 'random_folder')
        parameters['useLabel']=Config.get('MAIN', 'useLabel')
        parameters['label']=Config.get('MAIN', 'label')
        parameters['pubmed_api_key']=Config.get('MAIN', 'pubmed_api_key')
    else:
        logging.error("Please send the correct parameters config.properties --help ")
        sys.exit(1)
    return parameters
 
def Main(parameters):
    random_folder=parameters['random_folder']
    random_file=parameters['random_file']
    quantity=int(parameters['quantity'])
    start=int(parameters['start'])
    final=int(parameters['end'])
    useLabel=parameters['useLabel']
    label=parameters['label']
    pubmed_api_key=parameters['pubmed_api_key']
    if not os.path.exists(random_folder):
        os.makedirs(random_folder)
    download_random(random_file, quantity, start, final, useLabel, label, pubmed_api_key)
            
def download_random(random_file, quantity, start, final, useLabel, label, pubmed_api_key):
    logging.info("Downloading " + str(quantity) + " pubmed random abstract, into " + random_file + " beginning from pmid: "+str(start) + " to pmid: "+str(final))
    conn = httplib.HTTPSConnection("eutils.ncbi.nlm.nih.gov")
    i=0
    with open(random_file+"_id_list.txt",'w') as pmid_list_file:
        with codecs.open(random_file,'w',encoding='utf8') as txt_file:
            while (i<quantity):
                try:
                    #time.sleep(0.1)
                    randomId=randint(start, final)
                    randomId=str(randomId)
                    params = urllib.urlencode({'db':'pubmed','retmode':'xml','id':'PMID'+randomId,'api_key':pubmed_api_key})
                    conn.request("POST", "/entrez/eutils/efetch.fcgi", params )
                    rf = conn.getresponse()
                    if not rf.status == 200 :
                        logging.error("Error en la conexion:   "  + rf.status + " " + rf.reason)
                        exit()
                    response_efetch = rf.read()
                    doc_xml = ET.fromstring(response_efetch) 
                    article = doc_xml.find("PubmedArticle")
                    if(article!=None):
                        pmid = article.find("MedlineCitation").find("PMID").text
                        art_txt = label + "\t" + pmid + "\t"    
                        article_xml = article.find("MedlineCitation").find("Article")
                        abstract_xml = article_xml.find("Abstract")
                        if(abstract_xml!=None):
                            title_xml=article_xml.find("ArticleTitle")
                            if(title_xml!=None):
                                title = title_xml.text
                                if(title!=None):
                                    art_txt = art_txt + title.replace("\n"," ").replace("\t"," ").replace("\r"," ") + "\t" 
                                else:
                                    art_txt = art_txt + " " + "\t"     
                                abstract_xml = article_xml.find("Abstract")
                                if(abstract_xml!=None):
                                    abstract_text = abstract_xml.find("AbstractText")
                                    if(abstract_text!=None):
                                        abstract=abstract_text.text
                                        if(abstract!=None):
                                            art_txt = art_txt + abstract.replace("\n"," ").replace("\t"," ").replace("\r"," ") + "\n" 
                                            txt_file.write(art_txt)
                                            txt_file.flush()
                                            i=i+1
                                            pmid_list_file.write(pmid+"\n")
                                            pmid_list_file.flush()
                    rf.close()
                    conn.close()
                except Exception as inst:
                    logging.error("Error Downloading  " + randomId)
                    logging.error("Error Downloading  " + inst)
        txt_file.close()
    pmid_list_file.close()
    logging.info("Download End ")
        
    