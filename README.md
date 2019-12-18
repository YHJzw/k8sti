# k8sti

## Database
Uses SQLAlchemy

User
* id: Primary Key Auto Increment
* uname: user id for login
* pw: password for user

Project
* pid: Primary Key Auto Increment
* title: Title of the project
* URL: Github repository URL of project
* Branch: Branch name
* Token: Github repository token
* k8s_url: Project Container URL
* uid: Foreign Key of User(id)
* status: Current project build status (not saved in DB)

## Web
| URI | METHOD | Description |
| --- | ------ | ----------- |
| / | POST | Send project information to Build Service |
| /join | POST | Create account to use the web |
| /login | POST | Login to use the web |
| /logout | GET | Logout user |
| /projects | POST | Send deletion request to Kubernetes |

## html
| FILE | Description |
| ---- | ----------- |
| base.html | Base page of the website |
| join.html | Page for creating account |
| login.html | Page for login |
| home.html | Page for adding projects |
| plist.html | Page for managing(deleting) projects |
