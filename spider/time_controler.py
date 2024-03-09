import datetime
import os
import spider_configs as sconfig

CONTROL_FILEPATH = sconfig.DATA_PATH + sconfig.DATETIME_EXEC_PATH

def have_it_ran():
    """Checks if the script has been called in the past 6 hours.

    Returns:
    True if the script has been called in the past 6 hours, False otherwise.
    """

    # Get the current date and time.
    now = datetime.datetime.now()

  
    # Read the data control file.
    try:
        with open(CONTROL_FILEPATH, "r") as f:
            last_called = datetime.datetime.strptime(f.read(), "%Y-%m-%d %H:%M:%S")
    except FileNotFoundError:
    # The data control file does not exist, so the script has not been called before.
        return False

    # Check if the script has been called in the past 6 hours.
    if now - last_called < datetime.timedelta(hours=6):
        return True
    else:
        return False


def main():
    """Writes the current date and time to the data control file."""

    # Get the current date and time.
    now = datetime.datetime.now()

    # Write the current date and time to the data control file.
    with open(CONTROL_FILEPATH, "w") as f:
        f.write(now.strftime("%Y-%m-%d %H:%M:%S"))


    if __name__ == "__main__":
        main()