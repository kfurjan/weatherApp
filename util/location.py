import ipinfo


def get_location(access_token):
    """
    Function for getting current location
    :return: Current location based on IP address
    """
    handler = ipinfo.getHandler(access_token=access_token)
    details = handler.getDetails()

    return details.city
