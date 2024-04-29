# Translating Natural Language into SQL Queries

## [SQL in LangChain](https://python.langchain.com/docs/use_cases/sql/)

Connecting your Q&A bot to a SQL database is the best way to allow the model to return data accurate response. LangChain comes with a multitude of built-in chains that are compatible with any SQLAlchemy. This enables use-cases such as:
* Generating queries that will be run based on natural language
* Creating chatbots that can answer questions based on database data
* Building custom dashboards based on insights a user wants to analyse

This method can escalate out of control if the model is provided with more database access than neccesary.

## [Translating Text to SQL with T5](https://www.kaggle.com/code/balraj98/translating-text-to-sql-with-t5-wikisql-torch)

### T5 Basics
T5 is an encoder-decoder model pre-trained on a multitask mixture of unsupervised task and supervised tasks and for which each task is converted into a text-to-text format.

Converts all NLP into text-to-text format. Trained using teacher forcing.

### Notes from Article

There is already T5 model fine-tuned to translate natural language into SQL.

Little information about the actually steps to fine-tune the model to translate into SQL.

[WikiSQL](https://huggingface.co/datasets/wikisql) was used to train the model.

Dataset contains:
* English question
* Table in *dict*(?) format
* SQL query that should be intrepreted from the English

As we have our own tables, we can design the queries and answers ourselves. Using our own tables.

## [Natural Language to SQL using an Open Source LLM](https://medium.com/brillio-data-science/natural-language-to-sql-using-an-open-source-llm-3702e1db56b5)

Article only introduce deploying the model with langchain and showcasing it. Now indication on how it can possibly be achieved.

Article asked the question of how the model will be able to accomadate more than one table (complex queries).