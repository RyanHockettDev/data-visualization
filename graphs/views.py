from django.shortcuts import render
import sqlite3
import json
from django.http import HttpRequest


#helper function to build chart based on type kwarg
#kwarg skip used for data compression, skips number of rows = skip
def chart(cur, context, query, i,  **kwargs):
    type = kwargs.get("type", None)
    skip = kwargs.get("skip", None)
    if type and (type == "bar" or type == "line" or type == "pie" or type == "doughtnut"):
        cur.execute(query)
        graph_labels = []
        graph_data = []
        #Declaring empty list to place row data in
        
        if skip == None:
            for row in cur.fetchall():
                graph_labels.append(row[0])
                graph_data.append(row[1])
                
        else:
            for i in range(len(cur.fetchall())):
                graph_labels.append(cur.fetchall()[i][0])
                graph_data.append(cur.fetchall()[i][1])
                i =+ skip

        #Reformat lists of rows as values in a dictionary
        context_type = "type" + str(i)
        context_label = "graph_labels" + str(i)
        context_data = "graph_data" + str(i)
        context[context_type] = type    
        context[context_label] = graph_labels
        context[context_data] = graph_data
        return context


def graphs(request):
    

    if request.method == "POST":
        con = sqlite3.connect("db.sqlite3")
        con.row_factory = sqlite3.Row
        cur = con.cursor()

        data = request.POST.__getitem__("dataset")
        
        context={}

        if data == "book":
            query = "SELECT authors, count(authors) FROM graphs_book group by authors order by count() desc limit 10"
            i = 0
            context = chart(cur, context, query, i, type="bar")
            i = 1
            #context = chart(cur,context,query,i,type="line",skip="")

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
            def author_radial_builder():
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
            author_radial_builder()
            cur.execute('SELECT authors, count(authors), avg(average_rating), avg(num_pages), sum(ratings_count), sum(text_review_count) FROM graphs_book where authors = "Stephen King"')
            author_radial_builder()
            context["graph_labels2"] = graph_labels2
            context["graph_data2"] = graph_data2

            con.close()
            #Render template, passing context dict with row data through context arg
            return render(request, "books.html", {"json_data":json.dumps(context)})
        
        
        elif data == "sale":
            i = 0
            query = "SELECT strftime('%m', date) as month, sum(total) as total from graphs_sale group by month order by month"
            context = chart(cur, context, query, i, type="line")
            i = 1
            query = "select category, sum(total) as total from graphs_sale group by category order by total"
            context = chart(cur, context, query, i, type="pie")
            i = 2
            query = "SELECT strftime('%m', date) as month, sum(total) as total, gender from graphs_sale group by month, gender order by month"
            
            #custom multi-line graph
            cur.execute(query)
            fetch = cur.fetchall()
            data_list1 = []
            data_list2 = []
            j = 0
            for row in fetch:
                if j % 2 != 0:
                    data_list1.append(row[1])
                else:
                    data_list2.append(row[1])
                j += 1
            graph_data2 = []
            graph_data2.append(data_list1)
            graph_data2.append(data_list2)
            context["graph_data2"] = graph_data2
            con.close()
            return render(request, "sales.html", {"json_data":json.dumps(context)})
        else:
            return render(request, "dash.html")
        
    else:
        return render(request, "dash.html")
 