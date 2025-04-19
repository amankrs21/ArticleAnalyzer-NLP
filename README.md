# 📰 ArticleAnalyzer-NLP

**ArticleAnalyzer-NLP** is a Python-based Natural Language Processing (NLP) tool designed to extract, analyze, and report insights from online articles. It scrapes content from a list of URLs, processes each article for sentiment and readability metrics, and generates a detailed Excel report summarizing the analysis.

---

## 📌 Features

- 🔗 **Scrapes Articles**: Fetches article content from provided URLs and saves it to local text files.
- 🧠 **NLP Analysis**:
  - **Sentiment Analysis**: Calculates positive, negative, polarity, and subjectivity scores.
  - **Readability Metrics**: Includes fog index, average sentence length, complex word ratio, etc.
  - **Linguistic Features**: Computes word count, average word/syllable length, and personal pronoun usage.
- 📤 **Excel Export**: Outputs the final analysis in a well-structured Excel (`Output.xlsx`) file.
- 📁 **Modular Structure**: Easily understandable functions for scraping, text processing, and reporting.

---


## 📥 Input Format

Your `Input.xlsx` file should contain two columns:

| URL_ID | URL                            |
|--------|--------------------------------|
| 101    | https://example.com/article-1  |
| 102    | https://example.com/article-2  |

---

## 🛠 Setup Instructions

```bash
git clone https://github.com/your-username/ArticleAnalyzer-NLP.git
cd ArticleAnalyzer-NLP
pip install -r requirements.txt
python text_analysis.py
```
---


## 📃 License
- This project is licensed under the MIT License.

---

## 🙋‍♂️ Author

**Aman** – Python NLP Enthusiast  
Feel free to connect or follow:

- 🔗 [LinkedIn](https://www.linkedin.com/in/amankrs21)
- 💻 [GitHub](https://github.com/amankrs21)

---
