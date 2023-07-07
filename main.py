import requests, time, random
from bs4 import BeautifulSoup
from selenium import webdriver  
import streamlit as st
import csv


st.set_page_config(page_title = 'LinkedIn Manager')
st.title('Get mutual LinkedIn Connections')
st.subheader('Feed your credentials')

username = st.text_input('Enter your Email ID: ')
password = st.text_input('Enter your Password: ', type='password')

links = []
l = st.text_input('Enter LinkedIn Profile to scrape: ')
links.append(l)

if username and password and l:
    browser = webdriver.Chrome()
    browser.get('https://www.linkedin.com/login')

    elementID = browser.find_element('id','username')
    elementID.send_keys(username)

    elementID = browser.find_element('id','password')
    elementID.send_keys(password)

    elementID.submit()
    all_mutual=[["Name", "Degree", "Link", "Mutual Contact", "Profile"]]
    for link in links:
        browser.get(link) 

        src = browser.page_source
        soup = BeautifulSoup(src, 'lxml')

        nameDiv = soup.find('div', {'class': 'mt2 relative'})

        name_loc = nameDiv.find('h1')
        name = name_loc.get_text().strip()
        # print(name)

        degree_span = soup.find('span', {'class':'distance-badge'})
        degree_loc = degree_span.find('span', {'class': 'dist-value'})
        degree = degree_loc.get_text().strip()

        # print(degree)

        details = soup.find('div',{'class':'ph5'})
        mutual_connection = details.find('a', {'class':'link-without-hover-visited'})
        # print(mutual_connections)
        # print('<<<<<<<<<<<<<<------------------------------------------------------------------>>>>>>>')
        if mutual_connection:
            mutual_connections = mutual_connection['href'].strip()
            browser.get(mutual_connections)
            src = browser.page_source
            soup = BeautifulSoup(src, 'lxml')

            connections_list = soup.find('div', {'class':'artdeco-card'})
            connections_links = connections_list.find('ul')
            connections = connections_links.find_all('li')
            # print(connections)
            # print('<<<<<<<<<<<<<<------------------------------------------------------------------>>>>>>>')
            for connection in connections:
                current_mutual = [] 
                current_mutual.append(name)
                current_mutual.append(degree)
                current_mutual.append(link)
                profile = connection.find('div', {'class':'entity-result__item'})
                profile_detail = profile.find('span',{'class':'entity-result__title-text'})
                mutual_name_link = profile_detail.find('a', {'class':'app-aware-link'})
                # print(mutual_name_link)
                # print('<<<<<<<<<<<<<<------------------------------------------------------------------>>>>>>>')
                name_span = mutual_name_link.find('span',{'aria-hidden':'true'})
                # print(name_span)
                # print('<<<<<<<<<<<<<<------------------------------------------------------------------>>>>>>>')
                mutual_name = name_span.get_text().strip()
                current_mutual.append(mutual_name)
                current_mutual.append(mutual_name_link['href'].strip())

                # print(mutual_name)
                # print('<<<<<<<<<<<<<<------------------------------------------------------------------>>>>>>>')
                all_mutual.append(current_mutual)

    print(all_mutual)
    with open('mutual_contacts.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(all_mutual)

    st.subheader('Download csv file:')
    with open('mutual_contacts.csv', 'rb') as f:
        st.download_button('Download CSV', f, file_name='contacts.csv')
    username = ''
    password = ''
    links = []
