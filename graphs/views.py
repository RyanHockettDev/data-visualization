from django.shortcuts import render
import sqlite3
import json
from django.http import HttpRequest

def graphs(request):
    

    if request.method == "POST":
        con = sqlite3.connect("db.sqlite3")
        con.row_factory = sqlite3.Row
        cur = con.cursor()

        data = request.POST.__getitem__("dataset")
        
        context={}
        if data == "book":
            cur.execute("SELECT count(authors), authors FROM graphs_book group by authors order by count() desc limit 10")
            graph_labels0 = []
            graph_data0 = []
            #Declaring empty list to place row data in
            
            for row in cur.fetchall():
                graph_data0.append(row[0])
                graph_labels0.append(row[1])

            #Reformat lists of rows as values in a dictionary    
            context["graph_labels0"] = graph_labels0
            context["graph_data0"] = graph_data0

            #line graph, generating avgs for ratings per range of 100 books, increments of 25
            graph_labels1 = []
            graph_data1 = []
            low = 0
            high = low + 100
            for i in range(39):
                cur.execute("SELECT avg(average_rating), avg(num_pages) FROM graphs_book where num_pages > " + str(low) + " AND num_pages < " + str(high))
                fetch = cur.fetchone()
                graph_data1.append(fetch[0])
                graph_labels1.append(round(fetch[1], 0))
                low = low + 25
                high = high + 25
            context["graph_labels1"] = graph_labels1
            context["graph_data1"] = graph_data1

            #Setup for radial graph, data_list is a helper to load two lists into graph_data
            graph_labels2 = []
            graph_data2 = []
            
            
            #Function to build helper list and append it to graph_data
            def builder():
                data_list = []
                fetch = cur.fetchone()
                for i in range(len(fetch)):
                    match i:
                        case 0:
                            graph_labels2.append(fetch[0])
                        case 1:
                            data_list.append(round((fetch[1]) / 10, 1))
                        case 2:
                            data_list.append(round(fetch[2], 2))
                        case 3:
                            data_list.append(round((fetch[3] / 100), 2))
                        case 4:
                            data_list.append(round((fetch[4] / 1000000), 2))
                        case 5:
                            data_list.append(round((fetch[5] / 10000), 1))
                graph_data2.append(data_list)
            
            cur.execute('SELECT authors, count(authors), avg(average_rating), avg(num_pages), sum(ratings_count), sum(text_review_count) FROM graphs_book where authors = "J.R.R. Tolkien"')
            builder()
            cur.execute('SELECT authors, count(authors), avg(average_rating), avg(num_pages), sum(ratings_count), sum(text_review_count) FROM graphs_book where authors = "Stephen King"')
            builder()
            context["graph_labels2"] = graph_labels2
            context["graph_data2"] = graph_data2

            con.close()
            #Render template, passing context dict with row data through context arg
            return render(request, "books.html", {"json_data":json.dumps(context)})
        
    else:
        return render(request, "dash.html")
 