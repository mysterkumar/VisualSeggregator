# Image Similarity Clustering Application

## Project Overview

This web application enables users to upload and cluster images based on their visual similarities using K-Nearest Neighbors (KNN) algorithm. The project provides an intuitive interface for analyzing and grouping images across different product categories and styles.  

## 🌟 Features

- Image Upload Interface  
- Similarity-based Clustering  
- Interactive Graph Visualization  
- Customizable Clustering Parameters  
- Support for Multiple Product Categories  

## 🛠 Tech Stack

### Frontend

- React.js  
- Formik (Form Management)  
- Tailwind CSS (Styling)  
- Yup (Form Validation)  

### Backend

- Django  
- Python  
- OpenCV  
- scikit-learn (KNN Implementation)  
- NumPy  
- Pillow  

### Visualization

- Network Graph Visualization Library  

## 🔍 Key Algorithms

- K-Nearest Neighbors (KNN) for Image Similarity  
- Feature Extraction Techniques  
- Clustering Algorithm  

## 📦 Installation

### Prerequisites

- Python 3.8+  
- Node.js 14+  
- pip  
- npm  

### Backend Setup

```bash  

# Clone the repository

git clone 

# Create virtual environment

python -m venv venv  
source venv/bin/activate  # On Windows use `venv\Scripts\activate`  

# Install dependencies

pip install -r requirements.txt  

# Run migrations

python manage.py migrate  

# Start Django server

python manage.py runserver
