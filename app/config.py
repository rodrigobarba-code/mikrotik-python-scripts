import os  # Importing OS module to generate a random secret key

# Config class to store all the configurations of the application
class AppConfig:
    PORT = 5000  # Port number for the app
    DEBUG = True  # Debug mode for the app
    SECRET_KEY = os.urandom(24)  # Secret key for the app
    METADATA = {  # Metadata for the app
        'title': 'Seven Suite',  # Title of the app
        'description': 'Seven Suite is a network management tool',  # Description of the app
        'author': 'Seven Suite Team',  # Author of the app
        'keywords': 'network, management, tool',  # Keywords for the app
        'progress_scan': 0  # Progress of the router_scan
    }


# Config class to store all the configurations of the application

# Class for sidebar definition
class Sidebar:
    # Sidebar menu items
    menu_items = [
        {
            'name': 'Dashboard',  # Name of the menu item
            'icon': 'fa-solid fa-gauge',  # Icon of the menu item
            'endpoint': 'dashboard.dashboard',  # Endpoint of the menu item
            'submenu': None  # Submenu of the menu item
        },
        {
            'name': 'Databases',  # Name of the menu item
            'icon': 'fa-solid fa-database',  # Icon of the menu item
            'endpoint': '#',  # Endpoint of the menu item, if endpoint is # then it is a dropdown menu
            'submenu': [  # Submenu of the menu item
                {'name': 'Regions', 'endpoint': 'regions.regions'},  # Name and endpoint of the submenu item
                {'name': 'Sites', 'endpoint': 'sites.sites'},  # Name and endpoint of the submenu item
                'separator',  # Separator for the submenu
                {'name': 'Routers', 'endpoint': 'routers.routers'}  # Name and endpoint of the submenu item
            ]
        },
        {
            'name': 'Users',  # Name of the menu item
            'icon': 'fa-solid fa-users',  # Icon of the menu item
            'endpoint': '#',  # Endpoint of the menu item, if endpoint is # then it is a dropdown menu
            'submenu': [  # Submenu of the menu item
                {'name': 'Users', 'endpoint': 'users.users'},  # Name and endpoint of the submenu item
                {'name': 'Log', 'endpoint': 'users.log'}  # Name and endpoint of the submenu item
            ]
        },
        {
            'name': 'Router Scan',  # Name of the menu item
            'icon': 'fa-solid fa-satellite-dish',  # Icon of the menu item
            'endpoint': 'router_scan.scan',  # Endpoint of the menu item
            'submenu': None  # Submenu of the menu item
        },
        {
            'name': 'IP Management',  # Name of the menu item
            'icon': 'fa-solid fa-ethernet',  # Icon of the menu item
            'marquee': False,  # Marquee menu item
            'endpoint': 'ip_management.ip_management',  # Endpoint of the menu item, if endpoint is # then it is a dropdown menu
            'submenu': None  # Submenu of the menu item
        }
    ]
    # Sidebar menu items

    # Sidebar profile menu items
    profile_menu_items = [
        {
            'name': 'Profile',  # Name of the menu item
            'icon': 'fa-solid fa-address-card',  # Icon of the menu item
            'endpoint': 'profile.profile',  # Endpoint of the menu item blank if endpoint is #
            'profile': True  # Profile menu item
        },
        'separator',  # Separator for the profile menu items
        {
            'name': 'Settings',  # Name of the menu item
            'icon': 'fa-solid fa-cog',  # Icon of the menu item
            'endpoint': 'settings.settings',  # Endpoint of the menu item
            'profile': True  # Profile menu item
        },
        'separator',  # Separator for the profile menu items
        {
            'name': 'Log Out',  # Name of the menu item
            'icon': 'fa-solid fa-right-from-bracket',  # Icon of the menu item
            'endpoint': 'auth.logout',  # Endpoint of the menu item
            'profile': True  # Profile menu item
        }
    ]
    # Sidebar profile menu items


# Class for sidebar definition

# Class for user jobs
class UserJobs:
    # User jobs
    job_display = {'admin': 'Admin', 'employee': 'Employee', 'guest': 'Guest', 'superadmin': 'Super Admin'}
    # User jobs
# Class for user jobs
