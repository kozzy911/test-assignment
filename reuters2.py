from bs4 import BeautifulSoup
import requests
import psycopg2
from psycopg2 import Error
import os
import sys
import json

print ('Argument List:', str(sys.argv))
# Argument List: ['reuters2.py', 'test', 'test2']
args = sys.argv
command = sys.argv[1]

url = "https://news.google.com/rss/search?q=when:24h+allinurl:reuters.com&ceid=US:en&hl=en-US&gl=US"

headers = {
            'User-Agent': 'your-user-agent-here'
        }

class ReadRss:

    def __init__(self, rss_url, headers):

        self.url = rss_url
        self.headers = headers
        try:
            self.r = requests.get(rss_url, headers=self.headers)
            self.status_code = self.r.status_code
        except Exception as e:
            print('Error fetching the URL: ', rss_url)
            print(e)
        try:
            self.soup = BeautifulSoup(self.r.text, 'lxml')
        except Exception as e:
            print('Could not parse the xml: ', self.url)
            print(e)
        self.articles = self.soup.findAll('item')
        self.articles_dicts = [{'title':a.find('title').text,'link':a.link.next_sibling.replace('\n','').replace('\t',''),'description':str(a.find('description').text),'pubdate':a.find('pubdate').text} for a in self.articles]

class ConnectPG:

    def __init__(self, values, command):

        self.values = values
        self.command = command
        try:
            self.connection = psycopg2.connect(user="burger", password="new_password", host="postgres", port="5432", database="reuters")
            self.cursor = self.connection.cursor()

            if (self.command == "update"):
                title = json.dumps(self.values[0])
                print(title)
                check_query = """SELECT id, title from news where title = '"""+title+"';"
                self.cursor.execute(check_query)
                self.connection.commit()
                check_result = self.cursor.fetchall()
                print(check_result)
                # Executing a SQL query to update table
                # check_query = """SELECT id, title from news;"""
                # self.cursor.execute(check_query)
                # self.connection.commit()
                # check_result = self.cursor.fetchall()
                # # print(check_result)
                # if check_result:
                #     for item in check_result:
                #         # print("Item: "+item[1])
                #         # print("Values: "+self.values[0])
                #         if (self.values[0] != item[1]):
                #             # print("Item: "+item[1])
                #             insert_query = """ INSERT INTO news (title, url, description, date) VALUES """+str(self.values)+""";"""
                #             self.cursor.execute(insert_query)
                #             self.connection.commit()
                #             # print("1 Record inserted successfully")
                #             # count = self.cursor.rowcount
                #             # print(count, "Record inserted successfully ")
                #             # Fetch result
                #             # self.cursor.execute("SELECT * from news")
                #             # record = self.cursor.fetchall()
                #             # print("Result ", record)
                #         else:
                #             print("item already exists with id "+item[0])
                # else:
                #     insert_query = """ INSERT INTO news (title, url, description, date) VALUES """+str(self.values)+""";"""
                #     self.cursor.execute(insert_query)
                #     self.connection.commit()
                #     # print("1 Record inserted successfully")
                #     count = self.cursor.rowcount
                #     # print(count, "Record inserted successfully ")
                #     # Fetch result
                #     # self.cursor.execute("SELECT * from news")
                #     # record = self.cursor.fetchall()
                #     # print("Result ", record)


            elif (self.command == "change"):
                # TODO
                update_query = """Update news set x where id = y"""

            elif (self.command == "delete"):
                if (self.values == "all"):
                    delete_query = """TRUNCATE news RESTART IDENTITY;"""
                    self.cursor.execute(delete_query)
                    self.connection.commit()
                    rowcount = self.cursor.rowcount
                    print("rows left: ", rowcount)
                else:
                    delete_query = """Delete from news where id = """+values
                    self.cursor.execute(delete_query)
                    self.connection.commit()
                    rowcount = self.cursor.rowcount
                    print("rows left: ", rowcount)

            elif (self.command == "fetch"):
                # Executing a SQL query to get the full table
                fetch_query = """SELECT id, title from news;"""
                self.cursor.execute(fetch_query)
                self.connection.commit()
                rowcount = self.cursor.rowcount
                print("rowcount ", rowcount)
                record = self.cursor.fetchall()
                print(record)

            elif (self.command == "create"):
                # Executing a SQL query to create table
                create_query = """CREATE TABLE news(id int GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY,title varchar(250),url varchar(250),description varchar(1250),date varchar(250));"""
                self.cursor.execute(create_query)
                self.connection.commit()
                rowcount = self.cursor.rowcount
                print("rowcount ", rowcount)
                record = self.cursor.fetchall()
                print("Result ", record)
            else:
                print("No command passed for execution in DB")
        except (Exception, Error) as error:
            print("Error while connecting to PostgreSQL", error)
        finally:
            if (self.connection):
                self.cursor.close()
                self.connection.close()
                print("PostgreSQL connection is closed")

if __name__ == '__main__':

    if (command == "create"):
        values = ''
        ConnectPG(values, command)
    elif (command == "delete"):
        try:
            values = sys.argv[2]
            ConnectPG(values, command)
        except Exception as e:
            print("Did you enter the row value or all? "+e)
    elif (command == "fetch"):
        values = ''
        ConnectPG(values, command)
    elif (command == "update"):
        feed = ReadRss(url, headers)
        i=1
        for item in feed.articles_dicts:
            i=i+1

            values = (item["title"], item["link"], item["description"], item["pubdate"])
            ConnectPG(values, command)

            # if i>3: break
        ConnectPG("", "fetch")
    else:
        print("please run the command:")
        print("docker-compose run backend python3 reuters2.py create/delete/fetch/insert")
