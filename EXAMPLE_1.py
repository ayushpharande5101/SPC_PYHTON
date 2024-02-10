import numpy as np
import pandas as pd
import streamlit as st
from PIL import Image
import pyodbc
import matplotlib.pyplot as plt

# creating a Dashboard
st.set_page_config(page_title="SPC chart", layout='wide')

# inserting an image as a logo
dash_logo = "CTPL2.png"  # need changes
l_width = 200
l_height = 200
img = Image.open(dash_logo)
img.thumbnail((l_width, l_height))


# for an example inserting random values into the chart

def connection():  # sql server connection changes needed
    conn = pyodbc.connect('Driver={ODBC Driver 17 for SQL Server};'
                          'Server= AYUSHP-DELL\\SQLEXPRESS03;'
                          'Trusted_Connection=yes;')

    cursor = conn.cursor()
    return cursor


# creating a chart on the dashboard
chart_placeholder = st.empty()

l_w = 3
left_width = 2
right_width = 2
batch_w = 2
valu_w = 2
m_w = 2
r_w = 1
l_side, left, right, batch, valu, m_side, r_side = st.columns([l_w, left_width, right_width, batch_w, valu_w, m_w, r_w])
with l_side:
    st.image(img, use_column_width=False)
with left:
    From_date = st.date_input(label='From')
with right:
    To_date = st.date_input(label='To:')
with batch:
    Batch = ['1', '2', '3']
    s_option = st.selectbox('Batch:', Batch)
with valu:
    pass
with m_side:
    f_date = From_date
    t_date = To_date
    batch_n = s_option
    batch = int(batch_n.replace('Batch ', ''))
    chart_types = ['R Chart', 'X Chart', 'Histogram']
    selected_chart_type = st.selectbox('Select Chart Type:', chart_types)
    if selected_chart_type == 'R Chart':
        sql = ("SELECT SR_NO,DATETIME,BATCH,1,2,3,4,5,X_MAX,X_MIN,RANGE,OVERALL_RANGE,UCL_R,LCL_R"
               " FROM Control_chart1.dbo.R_CHART_1 WHERE DATETIME BETWEEN ? AND ? AND BATCH = ?")
        curs = connection().execute(sql, (f_date, t_date, batch))
        # Fetch all rows and create a DataFrame
        rows = curs.fetchall()
        columns = [column[0] for column in curs.description]
        ds = pd.DataFrame.from_records(rows, columns=columns)
        # Close cursor and connection
        curs.close()

        if not ds.empty:
            UCL_R = ds['UCL_R'].iloc[0]
            LCL_R = ds['LCL_R'].iloc[0]
            USL_R = ds['USL_R'].iloc[0]
            LSL_R = ds['LSL_R'].iloc[0]
            x_bar = 250
            chart_types = ['R Chart', 'X Chart', 'Histogram']
            selected_chart_type = st.selectbox('Select Chart Type:', chart_types)
            plt.plot(ds['SR_NO'], ds['RANGE'], marker='o', linestyle='-')
            for index, row in ds.iterrows():
                plt.text(row['SR_NO'], row['RANGE'], f'{row["RANGE"]:.2f}', fontsize=8, ha='center',
                         va='bottom')
            X_bar = 20
            usl = 70
            lsl = -2
            plt.axhline(y=X_bar, color='g', linestyle='-', label='X-bar')
            plt.axhline(y=UCL_R, color='r', linestyle='--', label='UCL')
            plt.axhline(y=LCL_R, color='r', linestyle='--', label='LCL')
            plt.axhline(y=USL_R, color='b', linestyle='-', label='USL')
            plt.axhline(y=LSL_R, color='b', linestyle='-', label='LSL')
            for label, value in [('UCL', UCL_R), ('LCL', LCL_R), ('X-bar', X_bar), ('USL', USL_R), ('LSL', LSL_R)]:
                plt.annotate(label, xy=(ds['SR_NO'].iloc[-1], value), xytext=(ds['SR_NO'].iloc[-1] + 0.2, value),
                             color='black', fontsize=10, ha='left', va='center')
            plt.xticks(ds['SR_NO'], ha='right')
            for index, row in ds.iterrows():
                if selected_chart_type == 'R Chart' and (row['RANGE'] > UCL_R or row['RANGE'] < LCL_R):
                    plt.scatter(row['SR_NO'], row['RANGE'], color='red', zorder=5)
        else:
            st.warning("No data available for the selected date range and batch.")
        plt.title('SPC-bar Chart')
        plt.xlabel('Part Id In Integer')
        plt.ylabel('Coating Difference In Real Format')

    # plot the X chart
    elif selected_chart_type == 'X Chart':
        # sql server query to fetch data from sql
        sql = ("SELECT SR_NO,DATETIME,BATCH_NO,PART_ID,DOSING_WEIGHT,AVERAGE,RANGE,UCL_X,LCL_X,USL_X,LSL_X,CpK_X,Cp_X"
               " FROM Control_chart1.dbo.X_CHART_1 WHERE DATETIME BETWEEN ? AND ? AND BATCH_NO = ?")
        curs = connection().execute(sql, (f_date, t_date, batch))
        # Fetch all rows and create a DataFrame
        rows = curs.fetchall()
        columns = [column[0] for column in curs.description]
        ds = pd.DataFrame.from_records(rows, columns=columns)
        # Close cursor and connection
        curs.close()

        UCL_X = ds['UCL_X'].iloc[0]
        LCL_X = ds['LCL_X'].iloc[0]
        USL_X = ds['USL_X'].iloc[0]
        LSL_X = ds['LSL_X'].iloc[0]
        x_bar = 250
        plt.plot(ds['SR_NO'], ds['AVERAGE'], marker='o', linestyle='-')
        for index, row in ds.iterrows():
            plt.text(row['SR_NO'], row['AVERAGE'], f'{row["AVERAGE"]:.2f}', fontsize=8, ha='center', va='bottom')
        plt.axhline(y=x_bar, color='g', linestyle='-', label='X-bar')
        plt.axhline(y=UCL_X, color='r', linestyle='--', label='UCL')
        plt.axhline(y=LCL_X, color='r', linestyle='--', label='LCL')
        plt.axhline(y=USL_X, color='b', linestyle='-', label='USL')
        plt.axhline(y=LSL_X, color='b', linestyle='-', label='LSL')
        for label, value in [('UCL', UCL_X), ('LCL', LCL_X), ('X-bar', x_bar), ('USL', USL_X), ('LSL', LSL_X)]:
            plt.annotate(label, xy=(ds['SR_NO'].iloc[-1], value), xytext=(ds['SR_NO'].iloc[-1] + 0.5, value),
                         color='black', fontsize=10, ha='left', va='center')

        plt.xticks(ds['SR_NO'], ha='right')
        for index, row in ds.iterrows():
            if selected_chart_type == 'X Chart' and (row['AVERAGE'] > UCL_X or row['AVERAGE'] < LCL_X):
                plt.scatter(row['SR_NO'], row['AVERAGE'], color='red', zorder=5)
        plt.title('SPC-bar Chart')
        plt.xlabel('Part Id In Integer')
        plt.ylabel('Coating Difference In Real Format')
        cpk_cp_table = pd.DataFrame({'Parameter': ['CpK_X', 'Cp_X'],
                                     'Value': [ds['CpK_X'].iloc[0], ds['Cp_X'].iloc[0]]})

    # Plot the histogram
    elif selected_chart_type == 'Histogram':
        # sql server query to fetch data from sql
        sql = ("SELECT SR_NO,DATETIME,BATCH_NO,PART_ID,DOSING_WEIGHT,AVERAGE,RANGE,UCL,LCL,USL,LSL,CpK,Cp"
               " FROM Control_chart.dbo.SPC")
        curs = connection().execute(sql)
        # Fetch all rows and create a DataFrame
        rows = curs.fetchall()
        columns = [column[0] for column in curs.description]
        ds = pd.DataFrame.from_records(rows, columns=columns)
        # Close cursor and connection
        curs.close()
        data = np.random.randn(100)
        plt.hist(data, bins=30, edgecolor='black')  # Adjust the number of bins as needed

        # Add labels and title
        plt.xlabel('Interval')
        plt.ylabel('Frequency')
        plt.title('Histogram Example')
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    # Plot the R chart
    plt.figure(figsize=(10, 5))
with r_side:
    if st.button('Clear Chart', help='Click to clear the chart'):
        # Clear the chart by updating the placeholder with an empty figure
        fig, ax = plt.subplots(figsize=(10, 5))
left_w = 7
m = 1
right_w = 2
left_s, mm, right_s = st.columns([left_w, m, right_w])
with left_s:
    with st.container(border=True):
        st.pyplot(plt)
with mm:
    pass
with right_s:
    with st.container(border=True):
        cpk_cp_table = pd.DataFrame({'Parameter': ['CpK', 'Cp'],
                                     'Value': [ds['CpK'].iloc[0], ds['Cp'].iloc[0]]})
        st.table(cpk_cp_table)



