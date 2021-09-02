# test-assignment

## About

<p>This Docker-based app populates the Postgres database with the data from the Reuters news feed located at https://news.google.com/rss/search?q=when:24h+allinurl:reuters.com&ceid=US:en&hl=en-US&gl=US.</p>
<p>The URL from the original task is not availale.</p>

## Prequisites

1. Install Docker

<https://docs.docker.com/desktop/#download-and-install>

2. Install Git

<https://github.com/git-guides/install-git>

3. Clone this repo to your machine

`git clone https://github.com/kozzy911/test-assignment.git`

4. Build the image and send it to the background

`docker-compose up -d`

5. Create the main table

`docker-compose run backend python3 reuters2.py create`

## Usage

#### Update the database with the most recent info

`docker-compose run backend python3 reuters2.py update`

#### Get the data from the database

`docker-compose run backend python3 reuters2.py fetch`

#### Delete specific items or delete the data from the whole table

`docker-compose run backend python3 reuters2.py delete 1`

`docker-compose run backend python3 reuters2.py delete all`
