Python Script that takes a list of accounts and adds them to a Google Group. It will also prune out removed accounts.


## Google Setup

1. Create a new "Super Admin" account in google.
2. Create new project in the API console.
3. Create a new service account with `Enable Google Apps Damian-wide Delegation` and `Furnish a new private key` enabled.
4. Open the JSON key file and copy the `client_id`.
5. Return to the Admin Console and navigate to "Security" > "Show More" > "Advanced Settings" > "Manage API client access"
6. Paste the `client_id` that you copied in the "Client Name" box.
7. Paste the following "API Scopes" `https://www.googleapis.com/auth/admin.directory.group, https://www.googleapis.com/auth/admin.directory.user` in the box labeled "One or More API Scopes".
8. Click Authorize.

## Installation

```shell
sudo pip install -r requirements.txt
cp config.example.yml config.yml
# edit the config
vi config.yml
```