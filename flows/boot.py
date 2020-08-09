import yaml, requests
import os
from tabulate import tabulate
import time

class Boot:

    def __init__(self):
        self.account_read_token = None
        self.project_read_access_token = None
        self.projects = {}

    def print_bootup(self):
        os.system('clear')
        print (""" 

             `.-/os`   ohhhhhhys/`             .hh+ .hh+ -hh+                                 
        `.:+shhddmm-   ymm+::/smmy`     `      -mms -mmo :mmo                                 
    `-+shddhyso/omm-   ymm-   `dmd` `:syyyyo-  -mms -mmo :mms+yyyo-   -oyyyys:  -ss:+yy.      
   -yddyo/:--/+:+mm-   ymmo//+ydy: `ymd+-:smd+ -mms -mmo :mmd+::ymd/ -yho-.+md/ /mmdy++`      
  :dmy::`--.-++:+mm-   ymmhyyhmdo` +mm+   `hmd.-mms -mmo :mmo   `mmd `-/++osmms /mms          
 `dmh.:/`--.-++:+mm-   ymm-  `smmo +mm+   `hmd.-mms -mmo :mmo   `dmd +dmo:-:mms /mm+          
 omm:://`--.-++:+mm-   ymm-   `hmd:`ydd+-:smd+ -mms -mmo :mmd+::ymd/ ymm/-:sdms /mm+          
`sso`--- ..`.::-:ss.   +ss.    -sso `:syhhyo-  .ss/ .ss/ -ss/+yyyo-  .+yyys:+so -ss:  


Welcome to Rollbar's CLI tool!
""")

    def load_auth_tokens(self):
        with open("rollbar-tokens.yaml", 'r') as stream:
            try:
                self.account_read_token = yaml.safe_load(stream).get('account-read-access-token')
            except yaml.YAMLError as exc:
                print(exc)


    def get_project_monitoring_input(self):
        return self.projects.get(input("""> """))['id']


    def load_all_projects(self):
        headers = {'X-Rollbar-Access-Token': self.account_read_token}
        projects = requests.get('https://api.rollbar.com/api/1/projects',
                                headers=headers)

        table_rows = []
        num = 1
        for project in projects.json()['result']:
            self.projects[num] = {'id': project['id'], 'name': project['name'], 'status': project['status']}
            table_rows.append(
                ['(' + str(num) + ')', str(project['id']), project['name'], project['status']])
            num += 1

        print(tabulate(table_rows,
                       headers=['', 'id', 'project name', 'status']))

    def set_project_read_token(self, project_id):
        headers = {'X-Rollbar-Access-Token': self.account_read_token}
        tokens = requests.get('https://api.rollbar.com/api/1/project/%s/access_tokens' % project_id, headers=headers)
        tokens = [token for token in tokens.json()['result'] if 'read' in token['scopes']]
        self.project_read_access_token = tokens[0]['access_token']

    def get_items_api(self):
        headers = {'X-Rollbar-Access-Token': self.project_read_access_token}
        items = requests.get('https://api.rollbar.com/api/1/items', headers=headers)

        table_rows = []
        for item in items.json()['result']['items']:
            table_rows.append([str(item['id']), 'mox', (item['title'][:75] + '..') if len(item['title']) > 75 else item['title'], item['framework'], item['environment'], str(item['total_occurrences'])])

        print(chr(27) + "[2J")
        print(tabulate(table_rows,
                       headers=['id', 'project', 'title', 'framework', 'environment', 'total_occurrences']))


    def start(self):
        self.print_bootup()
        self.load_auth_tokens()
        self.load_all_projects()
        project_id = self.get_project_monitoring_input()
        self.set_project_read_token(project_id)

        while True:
            self.get_items_api()
            time.sleep(3)
