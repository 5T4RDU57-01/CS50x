# VibeVault
#### Video Demo:  https://youtu.be/_CoetKB12WE
#### Description:

Ever wanted to have a journal that tells you the vibe of your entries? VibeVault is a web application written in python using the Flask web framework
that allows you to see the general tone of your everyday journal entries using a natural language processing library. 

You can add new entries, remove old entries, track the time they were created and if they had a positive, negative, or neutral tone.
You can also see entries from the previous week, month, six months and year so that you can tracck the tone of your journals more effectively.


### Functions:

## index():

Description: This function renders the homepage of the journal app. It displays all journal entries belonging to the logged-in user, along with their titles, timestamps, and tone analysis. Users can also remove entries from this page.

Parameters: None.

Returns: Renders the index.html template with the entries data.

## add():

Description: This function allows users to add new journal entries. It handles both GET and POST requests. For GET requests, it renders the add.html template for users to input their new entry details. For POST requests, it retrieves the entry title and content, performs tone analysis, inserts the entry into the database, and redirects the user to the homepage.

Parameters: None.

Returns: Renders the add.html template for GET requests. Redirects to the homepage for POST requests.

## remove(entry_id):

Description: This function allows users to remove a specific journal entry identified by its entry ID. It deletes the entry from the database and redirects the user to the homepage.

Parameters: entry_id (string) - The unique identifier of the entry to be removed.

Returns: Redirects the user to the homepage.

## login():

Description: Manages user login functionality. For GET requests, it renders the login.html template. For POST requests, it verifies the submitted username and password against the database. If the credentials are valid, it logs the user in and redirects to the homepage.

Parameters: None.

Returns: Renders the login.html template for GET requests. Redirects to the homepage for successful logins.

## logout():

Description: Logs the user out of their current session by clearing the session data. After logging out, the user is redirected to the homepage.

Parameters: None.

Returns: Redirects the user to the homepage.

## register():

Description: Handles user registration. For GET requests, it renders the register.html template. For POST requests, it validates the submitted username and password, checks for duplicate usernames, inserts the new user into the database, and redirects to the login page.

Parameters: None.

Returns: Renders the register.html template for GET requests. Redirects to the login page for successful registrations.

## change():

Description: Allows users to change their passwords. For GET requests, it renders the change_pass.html template. For POST requests, it verifies the old password, validates the new password, updates the password hash in the database, and redirects to the homepage.

Parameters: None.

Returns: Renders the change_pass.html template for GET requests. Redirects to the homepage for successful password changes.

## percentages(timeframe):

Description: Displays the percentage breakdown of different tones in journal entries over a specified timeframe. It retrieves tone data from the database, calculates the percentages, and renders the percentages.html template with the data.

Parameters: timeframe (string) - Specifies the timeframe for which tone percentages are calculated.

Returns: Renders the percentages.html template with the tone percentage data.

### Templates:

## layout.html:

Purpose: This is the layout template that serves as the base for other HTML pages in the app.

Features:
Includes Bootstrap CSS and JavaScript for styling and interactivity.
Displays a navigation bar with links to different sections of the app based on user authentication status.
Provides a container for displaying flash messages.
Defines the structure of the main content area.

HTML Elements:
Navigation bar with links to home, new entry, percentages, registration, and login/logout.
Container for displaying flash messages.
Main content area where page-specific content is displayed using Jinja2 templating.

## index.html:

Purpose: This template displays all journal entries belonging to the logged-in user.

Features:
Iterates through the list of entries and displays each entry's title, tone, timestamp, and content.
Provides a "Delete" button for each entry to allow users to remove entries.

HTML Elements:
Container for displaying entries, iterating through each entry and displaying its details.
Card layout to display entry information.
"Delete" button for removing entries.

## add.html:

Purpose: This template allows users to add a new journal entry.

Features:
Users can input a title and the content of their journal entry.
The form submits data to the /add route using the POST method.

HTML Elements:
Input field for the title (id="title")
Text area for the entry content
"Add" button to submit the form


## percentages.html:

Purpose: This template displays the percentage breakdown of different tones in journal entries over various timeframes.

Features:
Users can select a timeframe from the dropdown menu to view tone percentages for that specific period.
Displays tone percentages along with the total number of entries analyzed.

HTML Elements:
Dropdown menu for selecting timeframes.
Container for displaying tone percentages and entry counts.

## login.html:

Purpose: This template provides a form for users to log in to their accounts.

Features:
Users input their username and password to log in.
Includes a link to register for a new account if the user doesn't have one.

HTML Elements:
Input fields for username and password.
"Log In" button to submit the login form.

## register.html:

Purpose: This template allows users to register for a new account.

Features:
Users input a username, password, and confirmation password to register.
Includes a link to log in if the user already has an account.

HTML Elements:
Input fields for username, password, and confirmation password.
"Register" button to submit the registration form.

## change_pass.html:

Purpose: This template enables users to change their passwords.

Features:
Users input their username, old password, new password, and confirmation password to change their password.
Includes a link to register for a new account if the user forgot their old password.

HTML Elements:
Input fields for username, old password, new password, and confirmation password.
"Change Password" button to submit the password change request.


### Static files:


## script.js:

Function: confirmDelete(entry_id)

input: entry_id (The unique ID for each entry)

Purpose:

Upon pressing the delete button for an entry, this function confirms that the user meant to delete the entry.
If the user confirms it, the function changes the app route to "/remove/" + {the entry ID} and the deletion is
done by the backend


## styles.css:

Contains the styling for the app