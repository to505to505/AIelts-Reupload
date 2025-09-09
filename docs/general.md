# Project Name: aiEILTS

## Description

An application that allows you to prepare for the speaking part of IELTS (English language exam) through recording answers to questions (part1 speaking, part2 speaking, part3 speaking) => transcribing => assessment and feedback through LLM providers

## TechStack

- UI & Frontend - Web PWA App with Ionic capacitor into android & ios:
  /web directory

  This module is responsible for the product site as well as client functionality. SSG/SPA (hydration) strategy is used, i.e. all front end logic is on the client, web module has no runtime on the server, static is distributed via nginx

  - tailwind v4
  - svelte 5
  - sveltekit
  - zod
  - bits.ui
  - capacitor
  - pocketbase (client for acess to Pocketbase SQLIte service)

- API (backend AI module):
  /api directory

  This module is responsible for custom server routers if they are needed (payment webhook and so on), as well as for interacting with external LLM and transcription providers. In general, this is the main backend, which does not belong to the generic functionality of pocketbase

  - langchain
  - FastAPI
  - pydantic
  - pocketbase (client for acess to Pocketbase SQLIte service)

## Main Features

1. Record speaking part of IELTS english exam and get ai-generated feedback
2. Navigate IELTs parts, tasks & topics with topic essentials in order to know IELTS better and improve vocabulary
3. Aggregate previous attempt results and track progress in time

## Support Features

1. Create personal profile and manage it
2. Pay for subscription online

## Project Structure

/api - Python FastAPI backend with langchain
/web - Frontend Sveltekit web-app
/utils - some useful python scripts for refresh db-content with .csv files
/research - python scripts for experimenting with ai and working with data
