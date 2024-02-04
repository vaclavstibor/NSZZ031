#!/bin/sh

# Extract API key from config.json
API_KEY=$(jq -r '.sources["New York Times"]["api key"]' config.json)

# Create the archive directory if it does not exist
mkdir -p archive

# Download all data in 2022 from the New York Times Business section archive
for month in {1..1}
do
  curl "https://api.nytimes.com/svc/archive/v1/2022/${month}.json?api-key=${API_KEY}" | jq '[.response.docs[]]' > "archive/2022/2022-${month}.json"
  sleep 12
done

echo "Data downloaded!"

# Install library: bew install jq
# Make the script executable by: chmod +x nyt-all-business-archive-2022.sh
# Then run the script by: ./nyt-all-business-archive-2022.sh