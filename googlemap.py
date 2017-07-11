from flask import *
from flask_googlemaps import GoogleMaps
from flask_googlemaps import  Map, icons
import pandas as pd
import logging
from pandas import DataFrame, read_excel
import socket
import sys
import re
import json

app = Flask(__name__, template_folder="templates")

# you can set key as config
app.config['GOOGLEMAPS_KEY'] = "AIzaSyA2DrGtd4DK_tjmIdVtRwBU5rqW_OnuqeA"

# you can also pass the key here if you prefer
GoogleMaps(app, key="AIzaSyA2DrGtd4DK_tjmIdVtRwBU5rqW_OnuqeA")


@app.route('/')
# def hello_world():
#     return 'Hello World!'

def mapview():
    data = pd.read_excel('/home/superstar/workspace/flask/googlemap/SampleCSV.xlsx')
    data['Index'] = data.index + 1
    data.set_index(['Index'], inplace=True)
    data.index.name = None

    for idx, val in enumerate(data['Name']):
        cell = data['Name'][idx + 1]
        param = idx + 1
        html_cell = '<a href="/item/' + str(param) + '">' + cell + '</a>'
        data['Name'][idx + 1] = html_cell

    data_table = data

    green_markers = []
    red_markers = []
    yellow_markers = []

    green_geo = []
    yellow_geo = []
    red_geo = []



    for idx, color in enumerate(data['O']):
        lat = data['Lat'][idx+1]
        lon = data['Lon'][idx+1]


        if color == 'Green':
            green_geo.append([lat, lon])
            green_markers.append({
                    'icon': 'http://maps.google.com/mapfiles/ms/icons/green-dot.png',
                    'lat':  lat,
                    'lng':  lon
                })

        elif color == 'Yellow':
            yellow_geo.append([lat, lon])
            yellow_markers.append({
                    'icon': 'http://maps.google.com/mapfiles/ms/icons/yellow-dot.png',
                    'lat': lat,
                    'lng': lon
                })

        else:
            red_geo.append([lat, lon])
            red_markers.append({
                    'icon': 'http://maps.google.com/mapfiles/ms/icons/red-dot.png',
                    'lat': lat,
                    'lng': lon
                })

    greenmap = Map(
        identifier="greenmap",
        varname="greenmap",
        lat=green_geo[0][0],
        lng=green_geo[0][1],
        zoom=15,
        markers=green_markers
    )

    yellowmap = Map(
        identifier="yellomap",
        varname="yellowmap",
        lat=yellow_geo[0][0],
        lng=yellow_geo[0][1],
        zoom=15,
        markers=yellow_markers
    )

    redmap = Map(
        identifier="redmap",
        varname="redmap",
        lat=red_geo[0][0],
        lng=red_geo[0][1],
        zoom=15,
        markers=red_markers
    )

    return render_template('categoriedmap.html', greenmap=greenmap, yellowmap=yellowmap, redmap=redmap, tables=[data_table.to_html(classes='data_table').replace('&lt;', '<').replace('&gt;', '>')], titles=['Table'])

@app.route('/item/<idx>')
def itemdetail(idx):
    df = pd.read_excel('/home/superstar/workspace/flask/googlemap/SampleCSV.xlsx')
    df['Index'] = df.index + 1
    df.set_index(['Index'], inplace=True)
    df.index.name = None
    namefield = df['Name'].unique()
    levelfield = df['Level'].unique()
    prob1 = df['Prob 1']
    prob2 = df['Prob 2']
    prob3 = df['Prob 3']
    prob4 = df['Prob 4']
    probnames = ['Prob1', 'Prob2', 'Prob3', 'Prob4']
    lat = df['Lat'][int(idx)]
    lng = df['Lon'][int(idx)]
    color = df['O'][int(idx)].lower()
    l1 = df['L1'][int(idx)]
    l2 = df['L2'][int(idx)]
    l3 = df['L3'][int(idx)]
    l4 = df['L4'][int(idx)]
    m1 = df['M1'][int(idx)]
    m2 = df['M2'][int(idx)]
    m3 = df['M3'][int(idx)]
    m4 = df['M4'][int(idx)]
    h1 = df['H1'][int(idx)]
    h2 = df['H2'][int(idx)]
    h3 = df['H3'][int(idx)]
    h4 = df['H4'][int(idx)]
    lmh1 = [l1, m1, h1]
    lmh2 = [l2, m2, h2]
    lmh3 = [l3, m3, h3]
    lmh4 = [l4, m4, h4]
    lmhs = [lmh1, lmh2, lmh3, lmh4]
    a = df['A'][int(idx)]
    b = df['B'][int(idx)]
    c = df['C'][int(idx)]
    d = df['D'][int(idx)]
    e = df['E'][int(idx)]
    a1 = df['A1'][int(idx)]
    a2 = df['A2'][int(idx)]
    a3 = df['A3'][int(idx)]
    f1 = df['F1'][int(idx)]
    f2 = df['F2'][int(idx)]
    f3 = df['F3'][int(idx)]
    f4 = df['F4'][int(idx)]
    r1 = df['R1'][int(idx)]
    r2 = df['R2'][int(idx)]
    o = df['O'][int(idx)]
    p5 = df['P5'][int(idx)]
    i1 = df['I1'][int(idx)]
    elements = [a, b, c, d, e, a1, a2, a3, f1, f2, f3, f4]
    ros = [r1, r2, o]
    pis = [p5, i1]
    fnames = ['F1', 'F2', 'F3', 'F4']
    fvalues = [f1, f2, f3, f4]
    current_name = df['Name'][int(idx)]
    current_level= df['Level'][int(idx)]
    name_json_array = json.dumps(list(df['Name']))
    level_json_array = json.dumps(list(df['Level']))
    mymap = Map(
        identifier="mymap",
        varname="mymap",
        lat=lat,
        lng=lng,
        zoom=15,
        markers=[{
                    'icon': 'http://maps.google.com/mapfiles/ms/icons/' + color + '-dot.png',
                    'lat':  lat,
                    'lng':  lng
                }]
    )


    if request.method == 'GET':
        return render_template('itemdetail.html', name_json_array=name_json_array, level_json_array=level_json_array, current_name=current_name, current_level=current_level,
                               namefield=namefield, levelfield=levelfield, idx=idx, prob1=prob1, prob2=prob2,
                               prob3=prob3, prob4=prob4, probnames=probnames, mymap=mymap, lmh1=lmh1,
                               lmh2=lmh2, lmh3=lmh3, lmh4=lmh4, elements=elements, ros=ros, pis=pis, fnames=fnames,
                               fvalues=fvalues)
def _clean_text(self, text):
    text = text.replace("\n", " ").replace("\t", " ").replace("\r", " ")
    text = re.sub("&nbsp;", " ", text).strip()

    return re.sub(r'\s+', ' ', text)

if __name__ == '__main__':
    app.run()

