# AdStream Revenue Optimization API

## Project Overview

This project implements an AI-powered Ad Tech revenue optimization backend.

The system analyzes user scroll behavior and recommends an optimal advertisement placement.

It uses:

- FastAPI for the backend API
- Pydantic for input validation
- Redis for caching
- Docker for running Redis
- Gemini LLM for generating contextual explanations
- Python for the optimization logic

## Objective

The objective is to improve ad viewability and RPM by dynamically selecting advertisement positions based on user behavior.

## System Flow

User Scroll Data  
↓  
FastAPI  
↓  
Redis Cache Check  
↓  
Ad Placement Optimization  
↓  
Gemini LLM  
↓  
Recommended Ad Placement  
↓  
Redis Cache  
↓  
API Response

## Features

- Scroll-based ad placement optimization
- Dynamic ad format recommendation
- Predicted ad viewability
- Estimated RPM
- Gemini LLM integration
- Redis caching
- FastAPI Swagger documentation
- Input validation using Pydantic
- Health check endpoint

## Project Structure

```text
Cherwin_project/
├── main.py
├── models.py
├── optimizer.py
├── redis_service.py
├── llm_service.py
├── requirements.txt
├── API_DOCUMENTATION.md
├── README.md
├── .env
└── .gitignore