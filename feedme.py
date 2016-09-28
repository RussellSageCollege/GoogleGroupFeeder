#! /usr/bin/env python

from __future__ import print_function
from httplib2 import Http
import yaml
from io import open
from apiclient import discovery
from oauth2client.service_account import ServiceAccountCredentials


class Feed:
    SCOPES = [
        'https://www.googleapis.com/auth/admin.directory.group',
        'https://www.googleapis.com/auth/admin.directory.group.member'
    ]
    SERVICE = []
    CONFIG = []
    CURRENT_MEMBERS = []
    DESIRED_MEMBERS = []
    MEMBERS_TO_ADD = []
    MEMBERS_TO_DEL = []

    # Reads our config file
    def get_config(self):
        with open('config.yml', 'r') as stream:
            try:
                return yaml.load(stream)
            except yaml.YAMLError as exc:
                print(exc)

    # Gets credentials from OAuth provider and impersonates the designated super admin.
    def get_credentials(self):
        credentials = ServiceAccountCredentials.from_json_keyfile_name(self.CONFIG['key_file_path'], self.SCOPES)
        return credentials.create_delegated(self.CONFIG['super_admin_email'])

    # Builds a google directory service
    def build_service(self):
        credentials = self.get_credentials()
        http = credentials.authorize(Http())
        return discovery.build('admin', 'directory_v1', http=http)

    # Gets all member emails from the service and dumps them into an array
    def get_members_from_google(self):
        members = self.SERVICE.members()
        request = members.list(groupKey=self.CONFIG['group_email'])
        while request is not None:
            members_doc = request.execute()
            for m in members_doc['members']:
                self.CURRENT_MEMBERS.append(m['email'])
            request = members.list_next(request, members_doc)

    # Get users from local file
    def get_members_from_local(self):
        self.DESIRED_MEMBERS = [line.rstrip('\n') for line in open(self.CONFIG['feed_file_path'])]

    # Builds two lists based on a comparision of each. One list is users that need to be made members
    # and the other is a list of users that should have their membership revoked.
    def reconcile_lists(self):
        self.MEMBERS_TO_ADD = set(self.DESIRED_MEMBERS).difference(self.CURRENT_MEMBERS)
        self.MEMBERS_TO_DEL = set(self.CURRENT_MEMBERS).difference(self.DESIRED_MEMBERS)

    # Removes user's membership from group
    def remove_members(self):
        members = self.SERVICE.members()
        for member in self.MEMBERS_TO_DEL:
            try:
                members.delete(groupKey=self.CONFIG['group_email'], memberKey=member).execute()
                print(' - ' + member + '... OK')
            except:
                print(' - ' + member + '... Fail')
        return None

    # Creates user's membership within group
    def add_members(self):
        members = self.SERVICE.members()
        for member in self.MEMBERS_TO_ADD:
            try:
                members.insert(groupKey=self.CONFIG['group_email'], body={'email': member}).execute()
                print(' - ' + member + '... OK')
            except:
                print(' - ' + member + '... Fail')
        return None

    # Main function
    def main(self):
        print('Reading config...')
        self.CONFIG = self.get_config()
        print('Building service...')
        self.SERVICE = self.build_service()
        print('Gathering current members of group: \n - ' + self.CONFIG['group_email'] + '...')
        self.get_members_from_google()
        print('Gathering list of desired members from: \n - ' + self.CONFIG['key_file_path'] + '...')
        self.get_members_from_local()
        print('Building operations list...')
        self.reconcile_lists()
        print('Removing user memberships...')
        self.remove_members()
        print('Assigning new memberships...')
        self.add_members()


Feed().main()
