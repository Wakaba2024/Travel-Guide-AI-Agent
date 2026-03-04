# Kenya Tourism Intelligence Assistant

## Overview

The **Kenya Tourism Intelligence Assistant** is an AI-powered travel
recommendation system that helps users discover tourism experiences
across Kenya based on their preferences.
The platform combines **data engineering, web scraping, vector
databases, and Retrieval-Augmented Generation (RAG)** to deliver
intelligent recommendations for travel packages and destinations.

Users can search for travel options based on:

-   Budget
-   Travel duration
-   Travel style (luxury, budget, family, adventure, relaxing)
-   Preferred destination

The system retrieves relevant travel packages from a database and
enhances the results using AI-powered contextual reasoning.

The application is delivered through a **Streamlit web interface** and
is deployed on **Streamlit Cloud**, making it accessible from anywhere.

------------------------------------------------------------------------

## Problem Statement

Tourists planning trips to Kenya face several challenges:

-   Information about travel packages is scattered across many websites
-   Most travel platforms offer static listings instead of personalized
    recommendations
-   It is difficult to quickly compare destinations based on budget and
    travel style
-   Travelers often lack insight into the best destinations for their
    preferences

This project addresses these problems by building an **AI-powered
tourism assistant** that:

-   Understands user travel preferences
-   Retrieves relevant travel packages using intelligent search
-   Generates personalized recommendations
-   Provides contextual insights about destinations

------------------------------------------------------------------------

## Tools, Frameworks, and Technologies

### Programming Language

Python

### Data Engineering

PostgreSQL\
pgvector (vector database extension)

### Artificial Intelligence

Mistral AI (embeddings and language model)\
Retrieval-Augmented Generation (RAG)

### Data Collection

Playwright (web scraping)\
BeautifulSoup

### Backend Framework

SQLAlchemy

### Frontend

Streamlit

### Deployment

Streamlit Cloud\
Neon PostgreSQL

### Version Control

Git\
GitHub

------------------------------------------------------------------------

## Project Architecture

The system architecture consists of five main layers:

1.  Data Collection Layer
2.  Data Storage Layer
3.  Vector Embedding Layer
4.  Retrieval and Recommendation Layer
5.  User Interface Layer

### Architecture Diagram

                     +------------------------+
                     |   Tourism Websites     |
                     | (Travel Packages Data) |
                     +-----------+------------+
                                 |
                                 v
                     +------------------------+
                     |   Web Scraping Layer   |
                     |  Playwright / BS4      |
                     +-----------+------------+
                                 |
                                 v
                     +------------------------+
                     |    PostgreSQL Database |
                     |  Travel Packages Table |
                     +-----------+------------+
                                 |
                                 v
                     +------------------------+
                     |   Embedding Generator  |
                     |     Mistral AI         |
                     +-----------+------------+
                                 |
                                 v
                     +------------------------+
                     |  Vector Database Layer |
                     |       pgvector         |
                     +-----------+------------+
                                 |
                                 v
                     +------------------------+
                     |  Recommendation Engine |
                     |  RAG + SQL Filtering   |
                     +-----------+------------+
                                 |
                                 v
                     +------------------------+
                     |   Streamlit Web App    |
                     |  User Travel Queries   |
                     +------------------------+

------------------------------------------------------------------------

## RAG Pipeline Workflow

The system uses **Retrieval-Augmented Generation (RAG)** to produce
intelligent responses.

### RAG Pipeline

    User Query
         |
         v
    Convert Query to Embedding
         |
         v
    Vector Similarity Search (pgvector)
         |
         v
    Retrieve Relevant Travel Packages
         |
         v
    Provide Context to Language Model
         |
         v
    Generate Personalized Recommendation

------------------------------------------------------------------------

## Project Methodology

### 1. Data Collection

Travel package information was collected from tourism websites using
automated scraping tools.

Collected fields included:

-   Package name
-   Destination
-   Duration
-   Price
-   Tour operator

### 2. Data Storage

The extracted data was stored in a **PostgreSQL database** with
structured tables including:

-   travel_packages
-   destinations

### 3. Embedding Generation

Each travel package description was converted into vector embeddings
using **Mistral AI embeddings**.

These embeddings allow the system to perform **semantic similarity
searches**.

### 4. Vector Database Integration

Embeddings were stored using the **pgvector extension** within
PostgreSQL.

This enables fast similarity search between user queries and stored
travel information.

### 5. Retrieval-Augmented Generation

When a user submits a query:

1.  The query is converted into an embedding
2.  Similar travel packages are retrieved from the vector database
3.  Relevant context is sent to the language model
4.  The model generates a personalized travel recommendation

### 6. Recommendation Engine

The system filters travel packages using structured queries based on:

-   Budget
-   Destination
-   Travel style
-   Duration

Results are ranked to show the most relevant travel options.

### 7. Frontend Application

A **Streamlit web application** was developed to provide a simple
interface where users can:

-   Input travel preferences
-   Explore recommended travel packages
-   Receive AI-generated insights

### 8. Deployment

The application was deployed using:

-   **Streamlit Cloud** for hosting
-   **Neon PostgreSQL** for database infrastructure

------------------------------------------------------------------------

## Results and Key Insights

The project produced a fully functioning **AI-powered tourism
assistant** capable of:

-   Retrieving travel packages using semantic search
-   Generating personalized travel recommendations
-   Providing contextual destination insights
-   Delivering a user-friendly web interface

Key insights:

-   Vector search significantly improves recommendation relevance.
-   Combining SQL filtering with AI retrieval produces more accurate
    results.
-   Streamlit enables rapid development of AI-powered data applications.

------------------------------------------------------------------------

## Key Challenges Experienced

### 1. Web Scraping Limitations

Some tourism websites load content dynamically, requiring advanced
scraping tools such as Playwright.

### 2. Data Inconsistencies

Scraped data contained issues such as:

-   Missing prices
-   Duplicate packages
-   Inconsistent destination naming

Data cleaning and validation processes were required.

### 3. Embedding Rate Limits

AI embedding APIs occasionally triggered rate limits during bulk
embedding generation.

Retry logic and delays were implemented to handle this.

### 4. Vector Database Integration

Integrating **pgvector** with PostgreSQL required careful handling of
vector formats and similarity queries.

### 5. Deployment Configuration

Deploying the application required proper configuration of:

-   Environment variables
-   Database connection strings
-   Streamlit secrets

Incorrect configurations initially caused connection errors.

------------------------------------------------------------------------

## Usage

### Accessing the Application

Open the deployed Streamlit application link. https://master-8egi5pluohnqk46bkd4ary.streamlit.app/

### How to Use

1.  Enter your travel preferences:

    -   Budget
    -   Travel duration
    -   Travel style
    -   Preferred destination

2.  Click **Explore Packages**

3.  The AI assistant returns personalized travel recommendations.

### Example Queries

-   Budget safari in Maasai Mara
-   Beach holiday in Diani under \$2000
-   Luxury safari in Kenya
-   3-day wildlife trip to Nakuru

------------------------------------------------------------------------


