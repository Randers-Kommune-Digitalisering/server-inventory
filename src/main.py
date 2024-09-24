import pandas as pd
import altair as alt
import streamlit as st
import numpy as np


from utils.database import DatabaseClient
from utils.config import DB_HOST, DB_USER, DB_PASS, DB_NAME

pd.set_option('display.max_columns', None)

db_client = DatabaseClient(database=DB_NAME, username=DB_USER, password=DB_PASS, host=DB_HOST)
# # print(db_client.execute_sql("SELECT * FROM DiskSpace"))
# df = pd.read_sql("SELECT * FROM DiskSpace", db_client.get_connection())
# print(df.loc[df['ComputerName'] == 'CALIBRA'])
# df = pd.read_sql("SELECT * FROM DiskSpace", db_client.get_connection())
# print(df)

st.set_page_config(page_title="Server Inventory", layout="wide")

st.title("Server Inventory")

disk_tab, other_tab = st.tabs(["Disk Space", "Other"])

with disk_tab:
    diskspace_df = pd.read_sql("SELECT * FROM DiskSpace", db_client.get_connection())
    diskspace_df['TotalSize_GB'] = pd.to_numeric(diskspace_df['TotalSize_GB'])
    diskspace_df['FreeSpace_GB'] = pd.to_numeric(diskspace_df['FreeSpace_GB'])
    diskspace_df['UsedSpace_GB'] = diskspace_df['TotalSize_GB'] - diskspace_df['FreeSpace_GB']
    diskspace_df['ProcentageUsed'] = diskspace_df['UsedSpace_GB'] / diskspace_df['TotalSize_GB'] #* 100

    for computer in diskspace_df['ComputerName'].unique():
        computer_df = diskspace_df[diskspace_df['ComputerName'] == computer]

        update_time = computer_df.UpdateTimeStamp.mean().round('1s').strftime('%d/%m-%Y %H:%M:%S')

        chart_col, table_col = st.columns(2)

        with chart_col:
            melted_df = computer_df.melt(id_vars=['ComputerName', 'Drive'], value_vars=['UsedSpace_GB', 'FreeSpace_GB'], var_name='SpaceType', value_name='Space_GB')

            chart = alt.Chart(melted_df).mark_bar().encode(
                    x=alt.X('Drive:N', title='Drive'),
                    y=alt.Y('sum(Space_GB):Q', title='Space (GB)'),
                    color=alt.Color('SpaceType:N',
                                    scale=alt.Scale(domain=['UsedSpace_GB', 'FreeSpace_GB'], range=['orange', 'green']),
                                    legend=alt.Legend(title="Space Type"))
                ).properties(
                    title=f'{computer} - {update_time}',
                    width=600,
                    height=400
                )
            st.altair_chart(chart, use_container_width=True)

        with table_col:
            table_df = computer_df[['Drive', 'UsedSpace_GB', 'FreeSpace_GB', 'TotalSize_GB', 'ProcentageUsed']]
            formatdict = {}
            all_cols = ['UsedSpace_GB', 'FreeSpace_GB', 'TotalSize_GB']
            for gb_col in all_cols:
                formatdict[gb_col] = "{:,.2f} GB"
            formatdict['ProcentageUsed'] = "{:.2%}"
            st.markdown(table_df.style.format(formatdict).hide(axis="index").to_html(), unsafe_allow_html=True)
