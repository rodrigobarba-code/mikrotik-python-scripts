import os
from . import home_bp
from flask import render_template
from app.decorators import RequirementsDecorators as restriction

def download_nextcloud_images() -> None:
    """
    This function downloads all the images from the news directory in the Next Cloud server
    :return: None, it doesn't return anything
    """

    # Import the owncloud module
    import dotenv
    import owncloud

    # Load the environment variables
    dotenv.load_dotenv()

    nextcloud_username = os.getenv('NEXTCLOUD_USERNAME' or 'default')
    nextcloud_password = os.getenv('NEXTCLOUD_PASSWORD' or 'default')

    # Create a new ownCloud client
    oc = owncloud.Client('http://localhost:8082/')

    # Log into the ownCloud server
    oc.login(nextcloud_username, nextcloud_password)

    # Get all the files and folders from the news directory
    files = oc.list('news')

    # Download all the files from the news directory
    print('Downloading files from the news directory...')
    for file in files:
        oc.get_file('news/' + file.get_name(), f'./app/static/img/nextcloud/news/{file.get_name()}')
        print(f'{file.get_name()} downloaded successfully from the news directory')

    # Log out from the ownCloud server
    oc.logout()

def get_nexcloud_local_images() -> list:
    """
    This function gets all the images from the local news directory
    :return: A list with the images from the local news directory
    """

    # Import the os module
    import os

    # Get the current directory
    current_dir = os.path.dirname(os.path.realpath(__file__))

    # Get the news directory
    news_dir = os.path.join('./app/static/img/nextcloud/news/')

    # Get all the files from the news directory
    files = os.listdir(news_dir)

    # Return the files from the news directory
    return files

def get_time_status() -> str:
    try:
        # Import the time module
        import time

        # Get the current time
        actual = time.localtime()

        # Print the current time
        print(f"Hora actual: {actual.tm_hour}:{actual.tm_min}")

        # Check if the current time is less than 12 PM
        if actual.tm_hour < 12:
            return 'Good Morning'
        elif actual.tm_hour < 18:
            return 'Good Afternoon'
        else:
            return 'Good Evening'
    except Exception as e:
        print(f"Error: {str(e)}")
        return 'Good Day'


def get_current_changelog() -> dict:
    try:
        # Import the os module
        import os

        # Get the current directory
        current_dir = os.path.dirname(os.path.realpath(__file__))

        # Get the changelog file
        changelog_file = os.path.join(current_dir, './changelog.json')

        # Check if the changelog file exists
        if os.path.exists(changelog_file):
            # Import the json module
            import json

            # Open the changelog file
            with open(changelog_file, 'r') as file:
                # Load the changelog file
                changelog = json.load(file)

                # Sort the changes by date
                changelog.sort(key=lambda x: x['date'], reverse=True)

                # Return the changelog
                return changelog
        else:
            return {
                'version': '1.0.0',
                'date': '2021-09-01',
                'changes': [
                    'Initial release'
                ]
            }
    except Exception as e:
        print(f"Error: {str(e)}")
        return {
            'version': '1.0.0',
            'date': '2021-09-01',
            'changes': [
                'Initial release'
            ]
        }


@home_bp.route('/', methods=['GET'])
@restriction.login_required
@restriction.check_scan_status
def home():
    try:
        download_nextcloud_images()
    except Exception as e:
        print(f"Error while downloading images: {str(e)}")
        pass
    return render_template(
        'home/home.html',
        nextcloud=get_nexcloud_local_images(),
        changelog=get_current_changelog(),
        time=get_time_status(),
    )
