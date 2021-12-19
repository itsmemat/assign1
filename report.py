from jinja2 import Environment, FileSystemLoader
import pandas as pd

def access_report_gen():

    print("Starting to write the report")
    
    # Load data from th csv
    
    df = pd.read_csv('ftp_report.csv')

    # 2. Create a template Environment
    env = Environment(loader=FileSystemLoader('templates'))
    

    # 3. Load the template from the Environment
    template = env.get_template('access_report.html')
    print("template loaded")

    # 4. Render the template with variables
    html = template.render(page_title_text='Honey Pot Access Report',
                           title_text='Honey Pot Access Report',
                           ftp_access_text='FTP Access Report',
                           ftp_access_report=df)
   #5. Write the template to an HTML file
    with open('honeypot_access_report.html', 'w') as f:
        f.write(html)
