#!/usr/bin/env python
# coding: utf-8

# In[11]:


import pandas as pd
from bs4 import BeautifulSoup
import os.path
import requests
import re
pd.options.display.max_rows = 1500
pd.options.display.max_columns = 1500
pd.__version__


def get_data(search_for, filename):
  
    """ 1. This function takes two arguments a) search item, b)filename to be saved
        2. Searches the pubmed that gives keys a) query key and b) webenv key
        3. Fetches files from the server using the keys and saves it as a txt file of the xml output 
        and prints the number of records in total"""
    url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&usehistory=y&retmax=99999&term="+search_for
    response = requests.get(url)
    search = BeautifulSoup(response.content, 'xml')
    total_ids_search = int(search.find('Count').text)
    webenv = search.find('WebEnv').text
    query_key = search.find('QueryKey').text
    get_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pubmed&retmode=xml&query_key=1&webenv="+webenv
    for item in range(0, total_ids_search, 100000):
        get = get_url+"&retstart="+str(item)
        #get = get_url+"&retmax="+number+"&retstart="+str(item)
        get_response = requests.post(get)
        file = open("../data/"+filename+'.txt', 'w') # location of text file
        file.write(get_response.text) # saves the results into a txt file from get_response
        file.close()
 
        
        print("Total Number of records found :"+str(total_ids_search))
        
search_item = input("Search For:-")
filename =input("File name to xml output:-")
get_data(search_item,filename)



def get_dataframe(name, tocsv):
   
    """ 1.This function reads filename, that the user provided with an extension .txt generated from pubmed after get_data(search_for, filename) function.
        2.Then parses the xml file and creates a lists of PMID, Article_title, ISOAbbreviation, Journal_title,
         Abstract, Journal_Country,Published_year, Keyword_list,publication_type,Medlinecitation,pubmed_year,Affiliation
        3.Take the above list and creates a dataframe and returns a dataframe
        4.Finally the datafrane is saved into a csv file"""
    pubmed_results = open('../data/'+name+'.txt','r')
    contents = pubmed_results.read()
    soup = BeautifulSoup(contents, 'xml')
    root = soup.find_all('PubmedArticle')

    notuseful_list = ['Research Support', "U.S. Gov't","Non-U.S. Gov't","Research Support, Non-U.S. Gov't",
           "Research Support, N.I.H., Extramural", "Research Support, U.S. Gov't, Non-P.H.S.",
           "Research Support, N.I.H., Extramural,Research Support, U.S. Gov't, Non-P.H.S." ,
           "Research Support, N.I.H., Intramural", "Research Support, U.S. Gov't, P.H.S." ] 


    PMID = []
    year=[]
    ISO = []
    Article_title = []
    Journal_Country=[]
    Journal_title=[]
    abstract = []
    keywords=[]
    Medlinecitation = []
    pubmed_year =[]

    for item in root:
        pmid =  item.find('PMID')
        pmid_text= pmid.text
        PMID.append(pmid_text)
        iso_abbreviation = item.find('ISOAbbreviation')
        iso_abbreviation_text = iso_abbreviation.text
        ISO.append(iso_abbreviation_text)
        title = item.find('ArticleTitle')
        title_text = title.text
        Article_title.append(title_text)

    for item in root:
        if item is not None:
            journal = item.find('Journal')
            journal_name = journal.find_all('Title')
            for item in journal_name:
                journal_name_list = item.string
                Journal_title.append(journal_name_list)
        else:
             Journal_title.append(None)  

    all_Year_info =[]    
    for item in root:
        year_pub =  item.find_all('PubDate')
        year_pub_text = year_pub[0].text
        all_Year_info.append(year_pub_text)
        s = ''.join(all_Year_info)
    for item in re.findall('(\d{4})', s):
        year.append(item.strip())

    for item in root:
        year_pub =  item.find(PubStatus="pubmed")
        if year_pub is not None:
            year1 =  year_pub.find_all('Year')
            for i in year1:
                pubmed_year.append(i.text)

    pubtype=[]
    for item in root:
        pub = item.find('PublicationTypeList')
        if pub is not None:
            pub_lst=[]
            pubtype_list = pub.find_all('PublicationType')
            for item in pubtype_list:
                pubtype_text = item.text
                pub_lst.append(pubtype_text)
            pub_lst = [x for x in pub_lst if x.strip() not in notuseful_list]
            pubs_join= ','.join(pub_lst)
            pubtype.append(pubs_join)
        else:
            pubtype.append(None)      

    for item in root:
        journal_country = item.find('MedlineJournalInfo')
        if journal_country is not None:
            country_list = journal_country.find_all('Country')
            for item in country_list:
                country_list=item.text
                Journal_Country.append(country_list)
        else:
            Journal_Country.append(None)

    for item in root:
        abstract_text = item.find('Abstract')
        if abstract_text is not None:
            text = abstract_text.find_all('AbstractText')
            lst = []
            for item in text:
                lst.append(item.text)
            lst_join='\n'.join(lst)
            abstract.append(lst_join)
        else:
             abstract.append(None) 

    for item in root:
        keyword_text=item.find('KeywordList')
        if keyword_text is not None:
            key=[]
            keyword_text_list=keyword_text.find_all('Keyword')
            for item in keyword_text_list:
                keyword_text=item.text
                key.append(keyword_text)
            keys_join=','.join(key)
            keywords.append(keys_join)
        else:
            keywords.append(None)

    for item in soup.find_all('MedlineCitation'):
        status = item.get('Status')
        Medlinecitation.append(status)    

    affiliation=[] 
    for item in root:
        abstract_text = item.find('AuthorList')
        if abstract_text is not None:
            text = abstract_text.find_all('Affiliation')
            lst = []
            for item in text:
                lst.append(item.text)
            lst_join='\n'.join(lst).replace("\n","")
            affiliation.append(lst_join)
        else:
            affiliation.append(None)
            
    dict_columns = {'PMID': PMID,
       'Title': Article_title,
         'ISOAbbreviation': ISO,
       'journal_title':Journal_title,
         'Abstract':abstract,
         'Journalinfo_country': Journal_Country,
          'Published_year':year,
           'Keyword_list':keywords,
          'publication_type':pubtype,
          'medline_citation':Medlinecitation,
          "pubmed_year":pubmed_year,
          "Affiliation":affiliation}

    df =pd.DataFrame.from_dict(dict_columns, orient='index').transpose()
    df.to_csv('../data/'+tocsv+'.csv',index=False)
    print("Number of articles :"+str(len(root)))
    #return df

get_dataframe(filename, input("file name to save as csv:"))



