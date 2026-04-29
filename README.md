# 📰 Visualising the news
## How the New York Times covered the US election, Gaza and Trump’s return to the White House through machine learning and sentiment analysis

## 📱 Summary
Analysing thousands of NY Times headlines for 2024 and 2025 provides insight into how one of the world’s leading news organisations is framing global events for public consumption. 

This project analyses 96,510 headlines using unsupervised machine learning and natural language processing to uncover hidden patterns in coverage and tone. 

K-means clustering identifies seven thematic groups, such as Trump & Politics, while VADER sentiment analysis tracks whether coverage skews positive, negative or neutral and when these tones shift over time. 

The project's findings reveal that World News & Conflict are by far the most negatively framed cluster, with sentiment deteriorating consistently throughout 2025. Trump & Politics is the most volatile cluster, shifting noticeably more negatively during the US election and inauguration. 

By contrast, Lifestyle & Culture and Breaking News & Disasters remain flat throughout 2024 and 2025, appearing to be unaffected by the negative clusters. 

A further finding suggests that headlines understate the negativity of articles compared to when article abstracts are added to the analysis. 

All findings are presented through an interactive Streamlit app, making the analysis accessible to a non-technical audience.

## 🔗 Live interactive Streamlit app
https://nyt-headlines-analysis-6gsazhjdqry2xs9n2hcaam.streamlit.app/

- K-Means clustering to identify seven thematic groups
- VADER sentiment analysis on headlines and abstracts
- Interactive timeline showing sentiment shifts around the US election and Trump's inauguration
- Filterable headline browser of all 96,510 headlines
- Built with: Python, Pandas, Scikit-learn, VADER, Streamlit, Matplotlib

## 📉 Data collection and preprocessing
Data for this project was collected using a NY Times API from the newspaper’s developer’s portal, resulting in 96,510 rows and eight columns scraped for headline, date, month, section, author, URL, abstract and year for 2024 and 2025. 

Cleaning of data consisted of removing rows with null values and duplicate entries. 

Text preprocessing was applied to the headline column using the Natural Language Processing (NLP) library, removing stop words (words such as “and”, “the” and “was”), punctuation and special characters. 

All headlines were converted to lowercase to allow for more consistency across the dataset. 

Sections of the newspaper were also removed: Crosswords & Games, News Briefings, Corrections, Summaries and Word of the Day, which were identified as not relevant to the analysis.

## 📁 Data
- Source: New York Times API
- 96,510 rows, 8 columns
- Date range: January 2024 — December 2025
