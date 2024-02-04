#!/bin/sh

# This script is used to fetch list from the New York Times API for a specific section.

# Prerequisites:
# - Install the jq library using the command: brew install jq
# - Make the script executable using the command: chmod +x nyt-field-list.sh

# Extract the API key from the config.json file.
# The jq command is used to parse the JSON file and extract the value of the API key.
API_KEY=$(jq -r '.sources["New York Times"]["api key"]' config.json)

# Define the field variable.
# This variable will be used in the URL to fetch the specific section from the New York Times API.
field="section"

# Construct the request URL using the field variable and the API key.
request="https://api.nytimes.com/svc/news/v3/content/${field}-list.json?api-key=${API_KEY}"

# Print the field and request URL for debugging purposes.
echo "[INFO] Looking for field: ${field}"
echo "[INFO] Sending request: $request"

# Use the curl command to send a GET request to the New York Times API.
# If the request is successful, the response is saved to a variable.
response=$(curl --silent --fail $request)

# If the curl command was successful, pipe the response into the jq command to format the JSON.
# The formatted JSON is then redirected into a file named after the section.
if [ $? -eq 0 ]; then
    echo "$response" | jq . > "${field}-list.json"
    # Print a completion message.
    echo "[INFO] Data downloaded!"
else
    echo "[ERROR] Failed to download data!"
fi

# To run the script, use the command: ./nyt-field-list.sh