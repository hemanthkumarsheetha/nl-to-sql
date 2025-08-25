#!/bin/bash

# Run the FastAPI application with uvicorn in reload mode
uvicorn src.app:app --reload --host 0.0.0.0 --port 8004