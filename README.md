# Kenya Tourism Intelligence Assistant

## Overview

The **Kenya Tourism Intelligence Assistant** is an AI-powered travel
recommendation platform designed to help users discover the best tourism
experiences across Kenya.\
The system combines **data engineering, web scraping, vector databases,
and Retrieval-Augmented Generation (RAG)** to provide intelligent
recommendations based on user preferences such as budget, travel style,
duration, and destination.

The application is deployed as an interactive **Streamlit web app** and
integrates AI models to provide smart travel insights and itinerary
suggestions.

------------------------------------------------------------------------

## Problem Statement

Tourists planning trips to Kenya often struggle to find: - Reliable
travel packages - Personalized travel recommendations - Up‑to‑date
tourism insights - Efficient tools to compare destinations and budgets

Most travel websites provide **static listings** instead of
**personalized recommendations**.

This project solves that problem by building an **AI-driven tourism
assistant** that: - Understands traveler preferences - Retrieves
relevant travel packages - Generates personalized travel
recommendations - Provides intelligent destination insights

------------------------------------------------------------------------

## Tools, Frameworks, and Technologies

### Programming

-   Python

### Data Engineering

-   PostgreSQL
-   pgvector (vector database extension)

### AI / Machine Learning

-   Mistral AI (embeddings and language model)
-   Retrieval-Augmented Generation (RAG)

### Data Collection

-   Playwright (web scraping)
-   BeautifulSoup (HTML parsing)

### Backend

-   SQLAlchemy

### Frontend

-   Streamlit

### Deployment

-   Streamlit Cloud
-   Neon PostgreSQL (hosted database)

### Version Control

-   Git
-   GitHub

------------------------------------------------------------------------

## Project Methodology

### 1. Data Collection

Travel package data and destination information were collected from
tourism websites using automated web scraping tools.

The collected data included: - Package names - Destinations - Duration -
Prices - Tour operators

### 2. Data Storage

The scraped data was stored in a **PostgreSQL database**.\
The schema included tables such as: - travel_packages - destinations

### 3. Embedding Generation

Text data was converted into vector embeddings using **Mistral AI
embeddings**.\
These embeddings were stored in PostgreSQL using the **pgvector
extension** to enable similarity search.

### 4. Retrieval-Augmented Generation (RAG)

The RAG pipeline works as follows:

1.  User submits a travel query
2.  Query is converted into an embedding
3.  Similar travel packages and destinations are retrieved using vector
    similarity search
4.  Retrieved context is passed to the language model
5.  The model generates a personalized travel recommendation

### 5. Recommendation Engine

A recommendation engine was built to filter travel packages based on: -
Budget - Destination - Travel style - Duration

Results are ranked to provide the most relevant travel options.

### 6. Frontend Interface

A **Streamlit web application** was developed to allow users to: - Enter
travel preferences - Search for packages - Receive AI-generated
recommendations

### 7. Deployment

The application was deployed using: - **Streamlit Cloud** for hosting -
**Neon PostgreSQL** for the database

------------------------------------------------------------------------

## Results and Key Insights

The project successfully delivered:

-   An **AI-powered tourism assistant**
-   A **vector search system for travel packages**
-   A **personalized recommendation engine**
-   A **fully deployed web application**

Key insights include:

-   AI-powered retrieval significantly improves the relevance of travel
    recommendations.
-   Vector databases allow efficient semantic search across travel data.
-   Combining structured SQL filtering with vector search produces
    better results than either approach alone.

------------------------------------------------------------------------

## Key Challenges Experienced

During development several challenges were encountered:

### 1. Web Scraping Complexity

Many tourism websites use dynamic content loading, which required tools
like **Playwright** to scrape data effectively.

### 2. Data Quality Issues

Some scraped data contained: - Missing prices - Inconsistent destination
names - Duplicate records

These issues required data cleaning and validation.

### 3. Vector Database Integration

Integrating **pgvector with PostgreSQL** required careful handling of
embeddings and similarity queries.

### 4. Rate Limits from AI APIs

Generating embeddings using external APIs occasionally triggered rate
limits.

### 5. Deployment Configuration

Deploying the application required careful configuration of: -
Environment variables - Database connection strings - Streamlit secrets

Incorrect configuration initially caused connection errors.

------------------------------------------------------------------------

## Usage

### Access the Live Application

The application can be accessed via the deployed Streamlit link.

### How to Use

1.  Enter your travel preferences:

    -   Budget
    -   Travel duration
    -   Travel style
    -   Preferred destination

2.  Click **Explore Packages**

3.  The AI assistant will return recommended travel packages based on
    your preferences.

### Example Queries

-   Budget safari in Maasai Mara
-   Beach holiday in Diani under \$2000
-   Luxury safari in Kenya
-   3-day Nakuru wildlife trip

------------------------------------------------------------------------




