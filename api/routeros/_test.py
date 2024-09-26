import ros_api

c = ros_api.Api('', '', '', port=7372, use_ssl=True)

def _run(api: ros_api.Api, command: str):
    try:
        for item in api.talk([command]):
            print(item)
    except Exception as e:
        print(f"Error running {command}: {e}")
    finally:
        api.close()

_run(c, 'your_command_here')
