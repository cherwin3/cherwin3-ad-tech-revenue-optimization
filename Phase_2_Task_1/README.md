# Phase 2 – Task 1: Requirements Analysis and Architecture Design

## Project Title

Ad Tech and Revenue Optimization Platform

## Project Overview

This task focuses on analysing the business and technical requirements of the AdStream Revenue Optimization Platform and designing an initial production-ready architecture.

AdStream Analytics serves approximately 500 digital publishers and processes nearly two billion advertisement impressions every month. The platform manages programmatic advertising, real-time bidding, direct advertising deals, sponsored content, and multiple advertisement formats such as display, video, and native advertisements.

The proposed platform uses user engagement information, contextual data, advertisement performance metrics, machine-learning predictions, and LLM-generated explanations to recommend the most suitable advertisement position and format.

## Business Problem

Publisher Revenue Per Mille (RPM) has declined by approximately 25% during the last two years because of cookie deprecation, privacy regulations, poor advertisement placement, and reduced targeting effectiveness.

The current advertisement viewability rate is approximately 55%, which is below the industry benchmark of 70%. Header bidding also introduces nearly 800 milliseconds of latency, increasing page-load time and contributing to a 12% increase in bounce rate.

## Task Objective

The objective of this task is to:

- Analyse the business and technical requirements of the platform.
- Identify functional and non-functional requirements.
- Document privacy, security, performance, and integration constraints.
- Design an initial architecture for real-time advertisement optimization.
- Explain important architectural decisions and assumptions.
- Incorporate reliable LLM integration with structured and validated output.

## Proposed Solution

The platform collects privacy-compliant user engagement signals such as scroll depth, time spent on the page, device type, page category, and advertisement interaction.

FastAPI receives this information and sends it to the optimization service. The optimization engine predicts advertisement viewability and estimated RPM before recommending an advertisement position and format.

Redis is used as a context cache to provide low-latency access to recent optimization results. LangChain Agents coordinate the optimization tools and LLM explanation service. Structured Output ensures that the generated response follows a predefined JSON schema, while Guardrails AI validates the safety and correctness of the LLM output.

Temporal manages durable workflows, retries, timeouts, and failure recovery. Kafka carries impression and engagement events, while ClickHouse stores high-volume analytical data. The processed information can be displayed through a React-based publisher dashboard.

## Required Toolkit

- LangChain Agents: Coordinate the optimization engine, cache, analytics services, and LLM.
- Redis Context Cache: Stores frequently requested context and recent optimization results.
- Structured Output: Ensures predictable, machine-readable JSON responses.
- Guardrails AI: Validates the format, safety, and business constraints of LLM output.
- Temporal: Manages durable workflows, automatic retries, timeouts, and recovery.

## Supporting Technologies

- FastAPI
- Python
- Gemini or another supported LLM
- Redis
- Apache Kafka
- ClickHouse
- PostgreSQL
- React
- Docker
- OpenTelemetry
- Grafana

## Expected Deliverables

This folder contains:

1. requirements.md – Business, functional, non-functional, technical, privacy, and security requirements.
2. architecture.md – Description of the proposed system architecture and data flow.
3. architecture-diagram.png – Visual representation of the initial architecture.
4. design-decisions.md – Architectural decisions, assumptions, risks, limitations, and future improvements.
5. README.md – Task overview and deliverable summary.

## Expected Outcome
 The expected outcome is a production-oriented LLM integration design for an Ad Tech and Revenue Optimization Platform. The design addresses performance, scalability, security, privacy, compliance, output validation, workflow reliability, and integration with the existing advertising infrastructure.