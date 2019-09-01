import ipinfo


def get_location():
    """
    Function for getting current location
    :return: Current location based on IP address
    """
    handler = ipinfo.getHandler(access_token='8a826a8c8acb10')
    details = handler.getDetails()

    return details.city
