#!/bin/bash

# Run the gunicorn command
gunicorn main_routing:app

# Check if the command was successful
if [ $? -eq 0 ]; then
    echo "Gunicorn server started successfully."
else
    echo "Failed to start Gunicorn server."
fi
