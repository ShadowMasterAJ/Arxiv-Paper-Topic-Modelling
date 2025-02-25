# Arxiv Paper Topic Analysis

This project is focused on analyzing and clustering research papers from Arxiv based on their abstracts. The analysis spans multiple years and involves various machine learning techniques to extract meaningful insights from the data.

## Project Structure

- **unsup_topicator.ipynb**: The main Jupyter notebook containing the code for data fetching, preprocessing, clustering, and topic modeling.
- **arxiv_papers.csv**: CSV file containing the fetched papers' data for the first time period.
- **arxiv_papers2.csv**: CSV file containing the fetched papers' data for the second time period.

## Dependencies

- Python 3.11.9
- Jupyter Notebook
- pandas
- matplotlib
- seaborn
- tqdm
- arxiv
- nltk
- gensim
- scikit-learn
- pyLDAvis

## Setup

1. Clone the repository.
2. Install the required dependencies using `pip install -r requirements.txt`.
3. Open `unsup_topicator.ipynb` in Jupyter Notebook.

## Data Fetching

The notebook fetches papers from Arxiv using the `arxiv` library. The data is fetched for specific categories and time periods, and saved into CSV files.

## Data Preprocessing

The abstracts are cleaned, stemmed, and lemmatized. Stop words are removed, and bigrams and trigrams are formed using Gensim's Phrases.

## Clustering

The cleaned abstracts are vectorized using TF-IDF and clustered using KMeans. The optimal number of clusters is determined using the Elbow method.

## Topic Modeling

LDA (Latent Dirichlet Allocation) is used to extract topics from the clustered abstracts. The coherence score is calculated to evaluate the quality of the topics.

## Visualization

The results are visualized using matplotlib, seaborn, and pyLDAvis for interactive topic exploration.

## Usage

1. Run the data fetching cells to download the papers.
2. Preprocess the data by running the preprocessing cells.
3. Perform clustering and topic modeling by running the respective cells.
4. Visualize the results using the provided visualization cells.

## Results

The notebook provides insights into the distribution of categories, time-based trends, and the top keywords and topics for each time period.

## Conclusion

This project demonstrates the use of various machine learning techniques to analyze and cluster research papers based on their abstracts, providing valuable insights into the research trends over time.

## License

This project is licensed under the MIT License.

## Contact

For any questions or issues, please contact Arnav at arnav@example.com.
