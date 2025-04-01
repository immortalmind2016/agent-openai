<!-- Write a good readme to describe my project -->

# Agent for executing sql commands in a database

## Description

This project is an agent that can execute SQL commands in a database. It uses the LangChain library to create a custom agent that can interact with a database and execute SQL commands.

## Features

- Execute SQL commands in a database
- Use LangChain library to create a custom agent

## Requirements

- Python 3.8 or higher
- LangChain library

## Database tables

- The database should have the following tables:
  - `users`: A table to store user information.
  - `orders`: A table to store order information.
  - `products`: A table to store product information.
  - `order_products`: A table to store the relationship between orders and products.
  - `addresses`: A table to store address information.
  - `carts`: A table to store cart information.

## Installation

1. Clone the repository:

```bash
python -m venv venv
source venv/bin/activate # On Windows use `venv\Scripts\activate`
pip install -r requirements.txt
```
