#!/bin/bash

# Function to prompt the user for their choice
prompt_user() {
    echo "Do you want to run app:"
    echo "1. Yes"
    echo "2. No"
    read -p "Enter your choice (1/2): " choice
}

run_app() {
    echo "MYSQL_ROOT_PASSWORD=mysqlpassword" > .env
    echo "MYSQL_USER=root" >> .env
    echo "MYSQL_DB=ticket" >> .env
    echo "MYSQL_HOST=localhost" >> .env
    echo "MYSQL_PORT=3306" >> .env
    echo "MYSQL_PASSWORD=mysqlpassword" >> .env
    echo "DB_URI=mysql+pymysql://root:HelloWorld123@localhost:3306/ticket" >> .env
    echo "APP_PORT=8080" >> .env
    echo "DEBUG_PORT=8081" >> .env
    echo "The .env file has been created with API_KEY set to your provided key."

    docker compose build && docker compose up -d



    echo "The application will run on http://localhost:8080"
}

# Prompt the user for their choice
prompt_user

# Handle the user's choice
case $choice in
    1)
        run_app
        ;;
    2)
        exist
        ;;
    *)
        echo "Invalid choice. Please choose either 1 or 2."
        ;;
esac