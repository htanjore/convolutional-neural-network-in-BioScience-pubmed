## Convolutional Neural Network(CNN) in BioSciences from Pubmed and Topic Model
Convolutional Neural Network(CNN) is a deep learning algorithm successufully used in image analysis. CNN algorithm is also used in text classification with great success. For my capstone project at Nashville Software School I used drugs.com customer reviews to predict drug ratings and identify key words from text. Logistic Regression, Support Vector Machines and Keras/CNN machine learning algorithms were tested for text classification and predict ratings. CNN improved prediction accuracy in predicting customer ratings on AOC and accuracy score when compared to Logistic regressionm and Support vector machines. 

I continued to work on understanding more about CNN. I was curious to know how CNN is used in Biomeical research. Pubmed, is a freely available search engine for Biomedical Literature from National Library of Medicine(NLM). For this project, I took advantage of Pubmed API/Eutilities and Python/BeautifulSoup to get the data and analyze XML files. Text from Abstracts were analyzed using NLP and LDA Topic Model to determine How CNN is used in Biomedical Research?. In summary, CNN is widely for Image analysis and fewer studies were used for Text analysis. Overall the code has general applicability to search any topic or author in Biomedical Literature from Pubmed. 



### Data: Data was acquired using Pubmed API and Eutilities with BeautifulSoup.

#### The code can be used to search for specific key words. The source for the articles is from Pubmed https://www.ncbi.nlm.nih.gov/pubmed/ . The code can be used to retrieve Abstract, Article Title, Years Published, Country of Journal, Journal Title, Affiliation etc. 

 
### Topic model(LDA):


### click here [CNN TOPIC Model](http://htmlpreview.github.com/?https://github.com/htanjore/convolutional-neural-network-in-BioScience-pubmed/blob/master/data/lda.html)



Word Cloud of Bigrams Where CNN is used in Biosciences:
![ScreenShot](data/word_cloud_cnn.png 'CNN')


### Topic model(LDA) with text:



### click here [CNN TOPIC Model TEXT](http://htmlpreview.github.com/?https://github.com/htanjore/convolutional-neural-network-in-BioScience-pubmed/blob/master/data/lda_text.html)

Word Cloud of Bigrams Where CNN is used for Text Analysis in BioSciences:
![ScreenShot](data/word_cloud_cnn_text.png 'CNN Text')

