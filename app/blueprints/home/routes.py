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

@home_bp.route('/', methods=['GET'])
@restriction.login_required
def home():
    return render_template(
        'home/home.html',
        time=get_time_status()
    )

