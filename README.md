Takes a list of return delimited email addresses and ensures that a paired google group matches this membership file.

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
# Clone project
git clone https://github.com/TheSageColleges/GoogleGroupFeeder.git
cd GoogleGroupFeeder
# Checkout to the latest tag
git checkout $(git describe --tags $(git rev-list --tags --max-count=1))
# Install python requirements
sudo pip install -r requirements.txt
# Create a new configuration
cp config.example.yml config.yml
# edit the config
vi config.yml
```

The following options must be configured in the YAML config file.

* `super_admin_email` - An email address that is a super administrator on your Google Apps domain.
* `key_file_path` - The private key file supplied to you from Google when you create your service account.
* `group_source_map` - Yaml 2D array containing member files paired with a target group.

Make the script executable:

```shell
chmod +x feedme.py
```

## Usage

```
./feedme.py
```