import pandas as pd
import altair as alt
import streamlit as st
import numpy as np

from utils.database import DatabaseClient
from utils.config import DB_HOST, DB_USER, DB_PASS, DB_NAME

pd.set_option('display.max_columns', None)

db_client = DatabaseClient(database=DB_NAME, username=DB_USER, password=DB_PASS, host=DB_HOST)

st.set_page_config(page_title="Server Inventory", layout="wide")

st.title("Server Inventory")

tabs = ["Disk Space", "Installed Software", "Services", "System Info", "Scheduled Tasks", "Share Access Info", "Personal Certificates"]
disk_tab, installed_software_tab, services_tab, system_info_tab, scheduled_tasks_tab, share_access_info, personal_certificates = st.tabs(tabs)

with disk_tab:
    diskspace_df = pd.read_sql("SELECT * FROM DiskSpace", db_client.get_connection())
    diskspace_df['TotalSize_GB'] = pd.to_numeric(diskspace_df['TotalSize_GB'])
    diskspace_df['FreeSpace_GB'] = pd.to_numeric(diskspace_df['FreeSpace_GB'])
    diskspace_df['UsedSpace_GB'] = diskspace_df['TotalSize_GB'] - diskspace_df['FreeSpace_GB']
    diskspace_df['PercentageUsed'] = diskspace_df['UsedSpace_GB'] / diskspace_df['TotalSize_GB'] * 100

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
            table_df = computer_df[['Drive', 'UsedSpace_GB', 'FreeSpace_GB', 'TotalSize_GB', 'PercentageUsed']]
            formatdict = {col: "{:,.2f} GB" for col in ['UsedSpace_GB', 'FreeSpace_GB', 'TotalSize_GB']}
            formatdict['PercentageUsed'] = "{:.2%}"
            st.markdown(table_df.style.format(formatdict).hide(axis="index").to_html(), unsafe_allow_html=True)

with installed_software_tab:
    installed_software_df = pd.read_sql("SELECT * FROM InstalledSoftware", db_client.get_connection())
    installed_software_df['InstallDate'] = pd.to_datetime(installed_software_df['InstallDate'], errors='coerce')
    installed_software_df = installed_software_df[['ComputerName', 'DisplayVersion', 'DisplayName', 'InstallDate', 'Publisher', 'UpdateTimeStamp']]

    for computer in installed_software_df['ComputerName'].unique():
        computer_df = installed_software_df[installed_software_df['ComputerName'] == computer]
        update_time = computer_df.UpdateTimeStamp.mean().round('1s').strftime('%d/%m-%Y %H:%M:%S')

        chart_col, table_col = st.columns(2)

        with chart_col:
            st.write(f"**Installed Software for {computer} - {update_time}**")

        with table_col:
            st.markdown(computer_df.drop(columns=['ComputerName', 'UpdateTimeStamp']).to_html(index=False), unsafe_allow_html=True)

with services_tab:
    services_df = pd.read_sql("SELECT * FROM Services", db_client.get_connection())
    services_df = services_df[['ComputerName', 'DisplayName', 'Name', 'State', 'StartMode', 'StartName', 'Description', 'UpdateTimeStamp']]

    for computer in services_df['ComputerName'].unique():
        computer_df = services_df[services_df['ComputerName'] == computer]
        update_time = computer_df.UpdateTimeStamp.mean().round('1s').strftime('%d/%m-%Y %H:%M:%S')

        chart_col, table_col = st.columns(2)

        with chart_col:
            st.write(f"**Services for {computer} - {update_time}**")

        with table_col:
            st.markdown(computer_df.drop(columns=['ComputerName', 'UpdateTimeStamp']).to_html(index=False), unsafe_allow_html=True)

with system_info_tab:
    system_info_df = pd.read_sql("SELECT * FROM SystemInfo", db_client.get_connection())
    system_info_df = system_info_df[['ComputerName', 'lastbootuptime', 'OSVersion', 'CPU', 'TotalRAM_GB', 'UpdateTimeStamp']]
    system_info_df = system_info_df.rename(columns={'lastbootuptime': 'LastBootUpTime'})

    for computer in system_info_df['ComputerName'].unique():
        computer_df = system_info_df[system_info_df['ComputerName'] == computer]
        update_time = computer_df.UpdateTimeStamp.mean().round('1s').strftime('%d/%m-%Y %H:%M:%S')

        chart_col, table_col = st.columns(2)

        with chart_col:
            st.write(f"**System Info for {computer} - {update_time}**")

        with table_col:
            st.markdown(computer_df.drop(columns=['ComputerName', 'UpdateTimeStamp']).to_html(index=False), unsafe_allow_html=True)

with scheduled_tasks_tab:
    scheduled_tasks_df = pd.read_sql("SELECT * FROM ScheduledTasks", db_client.get_connection())
    scheduled_tasks_df = scheduled_tasks_df[['ComputerName', 'LastRunTime', 'NextRunTime', 'Schedule', 'UpdateTimeStamp']]

    for computer in scheduled_tasks_df['ComputerName'].unique():
        computer_df = scheduled_tasks_df[scheduled_tasks_df['ComputerName'] == computer]
        update_time = scheduled_tasks_df.UpdateTimeStamp.mean().round('1s').strftime('%d/%m-%Y %H:%M:%S')

        chart_col, table_col = st.columns(2)

        with chart_col:
            st.write(f"**Scheduled Tasks for {computer} - {update_time}**")

        with table_col:
            st.markdown(computer_df.drop(columns=['ComputerName', 'UpdateTimeStamp']).to_html(index=False), unsafe_allow_html=True)

with share_access_info:
    share_access_df = pd.read_sql("SELECT * FROM ShareAccessInfo", db_client.get_connection())
    share_access_df = share_access_df[['ComputerName', 'ShareName', 'SharePath', 'UpdateTimeStamp']]

    for computer in share_access_df['ComputerName'].unique():
        computer_df = share_access_df[share_access_df['ComputerName'] == computer]
        update_time = share_access_df.UpdateTimeStamp.mean().round('1s').strftime('%d/%m-%Y %H:%M:%S')

        chart_col, table_col = st.columns(2)

        with chart_col:
            st.write(f"**Share Access Info for {computer} - {update_time}**")

        with table_col:
            st.markdown(computer_df.drop(columns=['ComputerName', 'UpdateTimeStamp']).to_html(index=False), unsafe_allow_html=True)

with personal_certificates:
    personal_certificates_df = pd.read_sql("SELECT * FROM PersonalCertificates", db_client.get_connection())
    personal_certificates_df = personal_certificates_df[['ComputerName', 'Subject', 'NotBefore', 'NotAfter', 'Issuer', 'UpdateTimeStamp']]

    for computer in personal_certificates_df['ComputerName'].unique():
        computer_df = personal_certificates_df[personal_certificates_df['ComputerName'] == computer]
        update_time = personal_certificates_df.UpdateTimeStamp.mean().round('1s').strftime('%d/%m-%Y %H:%M:%S')

        chart_col, table_col = st.columns(2)

        with chart_col:
            st.write(f"**Personal Certificates for {computer} - {update_time}**")

        with table_col:
            st.markdown(computer_df.drop(columns=['ComputerName', 'UpdateTimeStamp']).to_html(index=False), unsafe_allow_html=True)