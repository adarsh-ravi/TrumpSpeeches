from bs4 import BeautifulSoup
import requests
import pyodbc

speechList = {'National Emergency Remarks': 'https://transcripts.factcheck.org/382-2/',
              'State of Union Address': 'https://transcripts.factcheck.org/state-of-the-union-address/',
              'UN Press Conference': 'https://transcripts.factcheck.org/president-trumps-u-n-press-conference/',
              'World Economic Forum': 'https://transcripts.factcheck.org/remarks-president-trump-world-economic-forum/',
              'Tax Reform Event': 'https://transcripts.factcheck.org/remarks-president-trump-tax-reform-event/',
              'Tax Reform': 'https://transcripts.factcheck.org/remarks-president-trump-tax-reform/',
              'Infrastructure, Charlottesville': 'https://transcripts.factcheck.org/remarks-president-trump-infrastructure-charlottesville/',
              'Paris Climate Accord': 'https://transcripts.factcheck.org/president-trump-paris-climate-accord/',
              'NRCC Dinner': 'https://transcripts.factcheck.org/remarks-president-nrcc-dinner/',
              'Nashville, Tennessee': 'https://transcripts.factcheck.org/remarks-president-nashville-tennessee/',
              'Joint session of Congress': 'https://transcripts.factcheck.org/president-trumps-address-joint-session-congress/',
              'Press Conference': 'https://transcripts.factcheck.org/president-trump-press-conference/',
              'African American History Month': 'https://transcripts.factcheck.org/president-trump-remarks-african-american-history-month/',
              'Statement on Immigration': 'https://transcripts.factcheck.org/president-trump-statement-immigration/',
              'Pence at CIA Headquarters': 'https://transcripts.factcheck.org/remarks-president-trump-vice-president-pence-cia-headquarters/',
              'Inaugural Address': 'https://transcripts.factcheck.org/president-donald-j-trump-inaugural-address/',
              'Speech in Miami': 'https://transcripts.factcheck.org/donald-trump-speech-in-miami-sept-16/'
              }

for title, url in speechList.items():
    result = requests.get(url)
    c = result.content
    soup = BeautifulSoup(c, 'html5lib')
    summary = soup.find('div', attrs={"class": "post-entry"})
    p = summary.find_all('p')
    strReport = ''
    for x in p:
        if not x.text.startswith("Q    ") and not x.text.startswith("THE PRESIDENT:"):
            strReport += x.text

    conn = pyodbc.connect('Driver={SQL Server};'
                          'Server=ADARSH;'
                          'Database=TrumpSpeeches;'
                          'Trusted_Connection=yes;')

    # print(strReport)
    # nstrReport = strReport.replace("'", "")
    # print(nstrReport)
    cursor = conn.cursor()
    cursor.execute("Insert into Speeches(SContent, STitle) VALUES (? , ?)", (strReport, title))
    conn.commit()
print("Scraping Complete!!")
