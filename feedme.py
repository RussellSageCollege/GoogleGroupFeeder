#! /usr/bin/env python

from __future__ import print_function
import httplib2
import json
import yaml
from io import open
from apiclient import discovery
from oauth2client.service_account import ServiceAccountCredentials


class Feed:
    SCOPES = [
        'https://www.googleapis.com/auth/admin.directory.group',
        'https://www.googleapis.com/auth/admin.directory.group.member'
    ]
    CONFIG = []

    def get_config(self):
        with open('config.yml', 'r') as stream:
            try:
                return yaml.load(stream)
            except yaml.YAMLError as exc:
                print(exc)

    def get_credentials(self):
        credentials = ServiceAccountCredentials.from_json_keyfile_name(self.CONFIG['key_file'], self.SCOPES)
        return credentials.create_delegated(self.CONFIG['super_admin_email'])

    def main(self):
        self.CONFIG = self.get_config()
        credentials = self.get_credentials()
        http = credentials.authorize(httplib2.Http())
        service = discovery.build('admin', 'directory_v1', http=http)
        groups = service.groups()
        results = groups.get(groupKey=self.CONFIG['group_email']).execute()
        print(json.dumps(results))



Feed().main()