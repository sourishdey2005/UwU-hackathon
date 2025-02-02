#!/bin/bash

# Update package list
sudo apt-get update 

# Install Tesseract OCR
sudo apt-get install -y tesseract-ocr

# Install additional dependencies if needed (Optional)
sudo apt-get install -y libglib2.0-0
