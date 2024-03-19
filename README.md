# Simple-Caching
Using Python Fast API &amp; Redis

Run main.py of inventory in cmd with 'uvicorn main:app --reload'
Run consumer.py of inventory
Run main.py of payment in cmd with 'uvicorn main:app --reload --port=8001'
Run consumer.py of payment
Run App.js of inventory-frontend with 'npm start'

After run 'npm start' access 'localhost/create' to create products or access 'localhost/orders' to create orders
