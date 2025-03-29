from flask import Flask , render_template
import pygal
import nasdaqdatalink
import pandas as pd
import os

app = Flask(__name__)

nasdaqdatalink.ApiConfig.api_key = os.environ.get('NASDAQ_API_KEY') #setting up os environ for securing api_key

def get_metric_data(m_code): #created function to fetch different metric data

    data = nasdaqdatalink.get_table('QDL/BCHAIN' , code = m_code) #fetching the data from nasdaqdatalink
    return (
        data['code'].iloc[0], #Extract metric code
        pd.to_datetime(data['date']).dt.strftime('%Y-%m'), #Format dates to 'YYYY-MM
        data['value'].tolist() #converts values to list 
    )

def create_chart(title , dates , values): #function to create a chart with parameters title , dates and values
    chart = pygal.Line(
        height = 400,
        x_label_rotation = 20,
        show_x_guides = True, #Show vertical guideliens
        show_minor_x_labels = False #Simplify x-axis labels
    )
    chart.title = title
    chart.x_labels = dates[::60] #shows every 60th date (5 year)
    chart.add('value', values) 
    return chart.render_data_uri()



@app.route('/')
def index():

    codes1 , dates1 , values1 = get_metric_data('TVTVR') #get trade vs transaction volume ratio data
    chart1 = create_chart(
        f"{codes1} : Trade Volume vs Transaction Volume Ratio",
        dates1,
        values1
    )

    codes2 , dates2 , values2 = get_metric_data('HRATE') #get network hash rate data
    chart2 = create_chart(
        f"{codes2} : Network Hash Rate",
        dates2,
        values2
    )
    return render_template( #render template with chart 
        'index.html',
        chart1 = chart1,
        chart2 = chart2
    )
app.run(host='0.0.0.0' , port=8080)