# Educa E-learning Platform

## Project Overview 

Doc link at **doc link here**

## Installation Instructions 

### Pre-requisites

Before setting up the project locally, ensure you have the following prerequisites installed:

- [Python](https://www.python.org/downloads/) (>=3.10.4)
- [Django](https://www.djangoproject.com/download/)
- A Database System (e.g., PostgreSQL, MySQL, SQLite) - [Django Database Installation](https://www.djangoproject.com/download/#database-installation)

### Installation Steps

1. Clone the repository:

        git clone https://github.com/Femi-ID/E-Learning-platform.git


2. Change into the parent directory:

        cd educa


3. Create a virtual environment:

        python3 -m venv venv


4. Activate your virtual environment:

        source venv/bin/activate


5. Install the Python dependencies:

        pip install -r requirements.txt


6. Apply migrations to create the database schema:

        python3 manage.py migrate


7. Start the development server: 
 ```
 python3 manage.py runserver
 ```

The application should now be running locally at [http://localhost:8000/](http://localhost:8000/).


## Contribution Guidelines

Educa E-learning Platform is open to contributions, but I recommend creating an issue or replying in a comment to let me know what you are working on first.

1. Clone the repo `git clone https://github.com/hngx-org/Team_Romulus_Zuri_MarketPlace.git`.
2. Open your terminal & set the origin branch: `git remote add origin https://github.com/Femi-ID/E-Learning-platform.git`
3. Pull origin `git pull origin master`
4. Create a new branch for the task you were assigned to, e.g `TicketNumber/(Feat/Bug/Fix/Chore)/Ticket-title` : `git checkout -b ID-001/Feat/Course-Detail-View`
5. After making changes, do `git add .`
6. Commit your changes with a descriptive commit message : `git commit -m "your commit message"`.
7. To make sure there are no conflicts, run `git pull origin dev`.
8. **Push** changes to your **new branch**, run `git push -u origin feat-csv-parser`.
9. Create a pull request to the `dev` branch not `master`.
10. Ensure to describe your pull request.
11. > If you've added code that should be tested, add some test examples.


# Merging
Under any circumstances should you merge a pull request on a specific branch to the `dev` not the `main` branch!!

### _Commit CheatSheet_

| Type     |                          | Description                                                                                                 |
| -------- | ------------------------ | ----------------------------------------------------------------------------------------------------------- |
| feat     | Features                 | A new feature                                                                                               |
| fix      | Bug Fixes                | A bug fix                                                                                                   |
| docs     | Documentation            | Documentation only changes                                                                                  |
| style    | Styles                   | Changes that do not affect the meaning of the code (white-space, formatting, missing semi-colons, etc.)      |
| refactor | Code Refactoring         | A code change that neither fixes a bug nor adds a feature                                                   |
| perf     | Performance Improvements | A code change that improves performance                                                                     |
| test     | Tests                    | Adding missing tests or correcting existing tests                                                           |
| build    | Builds                   | Changes that affect the build system or external dependencies (example scopes: gulp, broccoli, npm)         |
| ci       | Continuous Integrations  | Changes to our CI configuration files and scripts (example scopes: Travis, Circle, BrowserStack, SauceLabs) |
| chore    | Chores                   | Other changes that don't modify, backend or test files                                                    |
| revert   | Reverts                  | Reverts a previous commit                                                                                   |

> _Sample Commit Messages_

- `chore: Updated README file`: `chore` is used because the commit didn't make any changes to the frontend or test folders in any way.
- `feat: Added xyz feature to the courses' module endpoint`: `feat` is used here because the feature was non-existent before the commit.
