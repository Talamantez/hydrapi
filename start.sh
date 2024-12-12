#!/bin/bash
if [ -z "${PORT}" ]; then
    export PORT=8000
fi
eval "uvicorn app.main:app --host 0.0.0.0 --port ${PORT}"