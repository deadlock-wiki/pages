# Pages
Manages the wiki's public pages using previously uploaded data pages and blueprints

## Installing dependencies
1. Run `pip install -r requirements.txt` - also try pip3

## Configure environment variables
1. Create `./.env` file
2. Copy content from `./.env.example` and paste into `./.env`
3. Change variables as needed, follow comments for guidelines
    1. Note: This currently requires access to the DeadBot wiki account with moderator permissions

## Program walkthrough
Within `./src/core/`:
1. `read-current.py` - data pages, blueprints, and resource pages are read from the wiki then stored to `./data`
2. `write-new.py` - new resource pages are then written
3. `validate.py` - current and new resource pages are compared, all warnings written
4. `upload-new.py` - commit new resource pages by uploading them to the wiki

## Standards
1. Use 4 spaces for indentation
    Visual Studio Code: Settings -> Editor Tab Size -> 4
2. Use pull requests 