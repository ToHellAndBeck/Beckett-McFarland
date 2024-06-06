def create_fedex_tracking_urls_from_file(file_path, chunk_size=29):
    # Base FedEx tracking URL
    base_url = "https://www.fedex.com/fedextrack/summary?trknbr="
    
    # Initialize an empty list to hold the URLs
    urls = []
    
    # Initialize an empty list to hold the tracking numbers from the file
    tracking_numbers = []
    
    # Read tracking numbers from file
    with open(file_path, 'r') as file:
        for line in file:
            # Strip newline and whitespace and add to the list if not empty
            tracking_number = line.strip()
            if tracking_number:
                tracking_numbers.append(tracking_number)
    
    # Process the tracking numbers in chunks of 'chunk_size'
    for i in range(0, len(tracking_numbers), chunk_size):
        # Extract the current chunk of tracking numbers
        chunk = tracking_numbers[i:i+chunk_size]
        
        # Create the tracking URL for the current chunk and append it to the list of URLs
        urls.append(base_url + ",".join(chunk))
    
    return urls

# Example usage
if __name__ == "__main__":
    file_path = r"C:\Users\beckett.mcfarland\Desktop\Beckett-McFarland\Work Scripts\tracking_scripts\FEDEX_SHIPPING_INFO_GRABBER\tracking_numbers.txt"
    
    # Generate the FedEx tracking URLs from file
    fedex_urls = create_fedex_tracking_urls_from_file(file_path)
    
    # Print each URL
    for url in fedex_urls:
        print(url)
        print("")
