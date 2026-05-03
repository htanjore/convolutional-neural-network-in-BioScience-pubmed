## Convolutional Neural Network (CNN) in BioSciences: PubMed Analysis & Topic Modeling

This project analyzes the application and trends of Convolutional Neural Networks (CNNs) in biomedical research using PubMed publications. We retrieve, analyze, and model research abstracts to understand how CNNs are being applied across different biomedical domains.

Convolutional Neural Networks (CNNs) are deep learning architectures primarily known for image analysis but increasingly used in biomedical text classification, medical image analysis, and computational biology applications.




## Data Collection

Data is acquired from [PubMed](https://www.ncbi.nlm.nih.gov/pubmed/) using the NCBI E-utilities API. The `fetch_pubmed.py` script retrieves comprehensive publication metadata including:
- Article abstracts and titles
- Publication year and date
- Journal information (title, country, impact factor)
- Author affiliations
- Publication types and keywords

### Usage

The PubMed fetcher supports flexible date ranges and batch processing. Run these commands from the project root after setting your API key in `.env`.

CNN search example:
```bash
source notebooks/.env && python3 notebooks/fetch_pubmed.py "Convolutional Neural Network (CNN or ConvNet)" \
   --email your.email@example.com \
   --start-year 1990 --end-year 2026 \
   --batch-size 10000 \
     --api-key $NCBI_API_KEY \
     --csv-name cnn_abstract.csv
- Leading countries and journals
- Publication type distribution
- Impact factor analysis

![Publication Trends](data/cnn_publications_per_year.png 'CNN Publications Per Year')
![Journal Distribution](data/cnn_journals.png 'Top Journals')
![Country Analysis](data/cnn_top_countries.png 'Top Countries')

## Topic Modeling (Latent Dirichlet Allocation)

Latent Dirichlet Allocation (LDA) is used to discover hidden semantic topics within CNN-related biomedical research abstracts. This unsupervised learning approach automatically identifies key research themes and their relationships.

### Interactive LDA Visualization

**[View the CNN Topic Model Visualization](https://htmlpreview.github.io/?https://github.com/htanjore/convolutional-neural-network-in-BioScience-pubmed/blob/master/data/ldacnn.html)**

The interactive visualization shows topic distributions, key terms per topic, and term relevance metrics.

### Topic Word Clouds

Word clouds derived from LDA topics highlight the most relevant terms in each topic:

![CNN Topic Word Clouds](data/topic_words_cnn.png 'Topic Word Clouds')
![CNN Bigrams](data/wordcloud_cnn.png 'CNN Research Bigrams')

## Project Structure

- `notebooks/` — Jupyter notebooks for data fetching, EDA, and LDA analysis
  - `fetch_pubmed.py` — PubMed API data retrieval script
  - `cnn_version_EDA.ipynb` — Exploratory data analysis
  - `LDA_Topic_model.ipynb` — Topic modeling with LDA
- `data/` — Processed outputs and visualizations
- `requirements.txt` — Python dependencies

## Results

Analysis reveals that CNNs have diverse applications in biomedical research, including medical image analysis, genomics, drug discovery, and text mining. The topic model identifies key research clusters and emerging trends in CNN applications.

