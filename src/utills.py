import socket
 

# the root my project
root_path="/home/admin/Documents/ayyash/"

def is_connected(host="8.8.8.8", port=53, timeout=3):
    """
    Host: 8.8.8.8 (google-public-dns-a.google.com)
    OpenPort: 53/tcp
    Service: domain (DNS/TCP)
    """
    try:
        socket.setdefaulttimeout(timeout)
        socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((host, port))

        return True
    except socket.error as ex:
        print(ex)
        return False

def map_range(value, from_min, from_max, to_min, to_max):
    # Check for invalid input range
    if from_max <= from_min:
        raise ValueError("Invalid input range: from_max must be greater than from_min")
    
    # Calculate the ratio of the input value relative to the input range
    ratio = (value - from_min) / (from_max - from_min)
    
    # Map the ratio to the output range
    mapped_value = to_min + ratio * (to_max - to_min)
    
    # Clip the mapped value to ensure it stays within the output range
    # mapped_value = max(min(mapped_value, to_max), to_min)
    
    # Clip the mapped value to ensure it stays within the range of -1.0 to 1.0
    # mapped_value = max(min(mapped_value, 1.0), -1.0)
    
    return mapped_value

def is_close(value, target, tolerance):
    """
    Check if the given value is within the specified tolerance of the target value.
    """
    return abs(value - target) <= tolerance
 