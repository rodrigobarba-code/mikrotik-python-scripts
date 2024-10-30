from . import home_bp
from flask import render_template
from app.decorators import RequirementsDecorators as restriction

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
        changelog_file = os.path.join(current_dir, 'changelog.json')

        # Check if the changelog file exists
        if os.path.exists(changelog_file):
            # Import the json module
            import json

            # Open the changelog file
            with open(changelog_file, 'r') as file:
                # Load the changelog file
                changelog = json.load(file)

                # Sort by date
                changelog['date'].sort()

                # Return the changelog
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
def home():
    print(get_current_changelog())
    return render_template(
        'home/home.html',
        changelog=get_current_changelog(),
        time=get_time_status(),
    )

