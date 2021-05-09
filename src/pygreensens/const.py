"""GreenSens Constants"""

# API
BASE_URL = "https://api.greensens.de/api"

# USER
USER_URL = BASE_URL + "/users"
AUTH_URL = USER_URL + "/authenticate"
NOTIFICATIONS_URL = USER_URL + "/notifications"

# PLANT
PLANT_URL = BASE_URL + "/plants"

# POST - /api/users/authenticate
# GET - /api/users
# Get user data.
# GET - /api/users/notifications
# Get user notifications.
# POST - /api/users/forgot-password
# Forgot user password.
# POST - /api/users/change-username
# Change user login=mail.
# POST - /api/users/change-password
# Change user password.
