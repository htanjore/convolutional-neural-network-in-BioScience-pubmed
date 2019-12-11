## Convolutional Neural Network(CNN) in BioSciences from Pubmed and Topic Model
Convolutional Neural Network(CNN) is a deep learning algorithm used in image analysis. Past few years, CNN has been applied in text classification with great success. During my capstone project at Nashville Software School, I was adviced to try CNN on text classification. I used Logistic Regression, Support Vector Machines and Keras/CNN machine learning algorithms to Predict customer ratings from drugs.com customer reviews. I found that CNN improved prediction accuracy of drug ratings based AOC and accuracy score compared to Logistic regressionm and Support vector machines. Following this and as a Biomedical Scientist, I wanted to Analyse how the CNN is used in Biomeical research. For this I used Pubmed, which is a freely available search engine for Biomedical Literature from National Library of Medicine(NLM). I used BeautifulSoup and Pubmed API/Eutilities to get the data and analyze XML files and used NLP and LDA Topic Model on Abstracts to understand How CNN is used in Biomedical Literature. In summary, CNN is used mostly for Image analysis and few studies have used it for Text analysis. 
Overallm the code has general applicability to search any topic or author in Biomedical Literature from Pubmed. 



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

