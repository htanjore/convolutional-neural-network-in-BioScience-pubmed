## Convolutional Neural Network(CNN) in BioSciences from Pubmed and Topic Model
Convolutional Neural Network (CNN) is a deep learning algorithm used in image analysis and text classification. For my capstone project at Nashville Software School, I used text analysis on customer reviews using Natural Language Processing (NLP) and Machine learning algorithm to predict ratings from Drugs.com. I tested Logistic Regression, Support Vector Machines (SVM) and Keras/CNN machine learning algorithms to predict ratings. Of the three models tested, CNN model performed better compared to Logistic regression and SVM based on AOC and accuracy scores. 

Following this project, I was curious to understand how the CNN is used in Biomedical Research. Pubmed, is a freely available search engine for Biomedical Literature from National Library of Medicine (NLM). In this project, I took advantage of Pubmed API/Eutilities and Pandas/BeautifulSoup libraries to get the data from XML output. Text from the Abstracts were analyzed using NLP and LDA Topic Model to determine How researchers are using CNN in Biomedical Research?. Majority of studies used CNN for Image analysis and fewer studies used the algorithm for Text analysis. Overall, the code has general applicability to search for any topic or author in Biomedical Literature from Pubmed for visualize the publication per year, Impact factor of journals and topic model. 



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

