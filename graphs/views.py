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
            graph_labels1 = []
            graph_data1 = []
            for row in cur.fetchall():
                graph_data1.append(row[0])
                graph_labels1.append(row[1])
            context["graph_labels1"] = graph_labels1
            context["graph_data1"] = graph_data1
            con.close()
            print(context)
            print(json.dumps(context))
        
        
    else:
        return render(request, "dash.html")
    return render(request, "graphs.html", {"json_data":json.dumps(context)})