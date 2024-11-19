# Keycloak Client API and utility scripts

### Installation
```bash
poetry install

# Activate virtual environment
poetry shell
```

### Env variables
```bash
# For py scripts
export ACCESS_TOKEN=<keycloak_access_token>
```
### .env dotfile (for Makefile examples)
```bash
# .example.env
# KC_HOST=https://<keycloak-host>
# KC_REALM=<realm>
# KC_CLIENT_ID=<clientID>
# KC_CLIENT_SECRET=<clientSecret>
# KC_GRANT_TYPE=client_credentials

```

# Usage
### Create keycloak users from a users.json file
```python
python ./scripts/add_users_to_keycloak.py --users example.users.json
```

### Parse user + group membership files from Microsoft entra AD into a user.json
file
```python
python ./scripts/parse_entra_users.py -i entra_users_export.csv --groups ./groups
```
