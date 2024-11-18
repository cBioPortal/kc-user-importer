-include .env
export 

MAX_USERS=3000

# Set these in a .env dotfile
# .env
HOST=$(KC_HOST)
# KC_REALM=<realm: str>
# KC_CLIENT_ID=<client_id: str>
# KC_CLIENT_SECRET=<client_secret: str>
# KC_GRANT_TYPE=<grant_type: 'password' | 'client_credentials'>

hello:
	@echo "Hello World"
	@echo $(HOST)

get_access_token:
	curl -X POST $(HOST)/auth/realms/$(KC_REALM)/protocol/openid-connect/token \
		-H 'Content-type: application/x-www-form-urlencoded' \
		-d "client_id=$(KC_CLIENT_ID)" \
		-d "client_secret=$(KC_CLIENT_SECRET)" \
		-d "grant_type=$(KC_GRANT_TYPE)" | jq '.access_token'

get_user_count:
	curl -X GET $(HOST)/auth/admin/realms/$(KC_REALM)/users/count \
		-H "Authorization: Bearer $(ACCESS_TOKEN)" \
		-H 'cache-control: no-cache'

get_users:
	curl -X GET $(HOST)/auth/admin/realms/$(KC_REALM)/users?max=$(MAX_USERS) \
		-H "Authorization: Bearer $(ACCESS_TOKEN)" \
		-H 'cache-control: no-cache'


