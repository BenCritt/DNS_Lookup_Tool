# This is the code for the DNS Lookup Tool app.
# Decorator to set cache control headers to prevent caching of the page
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def dns_tool(request):
    # Initialize an empty dictionary to store DNS results
    results = {}
    # Initialize error message as None
    error_message = None
    # Create an instance of the DomainForm
    form = DomainForm()

    # Check if the request method is POST
    if request.method == "POST":
        # Populate form with POST data
        form = DomainForm(request.POST)
        # Validate the form input
        if form.is_valid():
            # Retrieve the cleaned domain name
            domain = form.cleaned_data["domain"]
            # List of DNS record types to query
            record_types = [
                "A",
                "AAAA",
                "MX",
                "NS",
                "CNAME",
                "TXT",
                "SOA",
                "SRV",
                "CAA",
            ]

            # Loop through each record type to perform DNS queries
            for record_type in record_types:
                try:
                    # Resolve the DNS records for the given domain and record type
                    answers = dns.resolver.resolve(domain, record_type)
                    # Store the results in the dictionary with the record type as key
                    results[record_type] = [r.to_text() for r in answers]
                except dns.resolver.NoAnswer:
                    # Handle cases where no records are found for the given type
                    results[record_type] = ["No records found"]
                except dns.resolver.NXDOMAIN:
                    # Handle cases where the domain does not exist
                    results[record_type] = ["Domain does not exist"]
                except dns.resolver.Timeout:
                    # Handle cases where the DNS query times out
                    results[record_type] = ["DNS query timed out"]
                except Exception as e:
                    # Handle any other exceptions that may occur
                    results[record_type] = [
                        f"Error retrieving {record_type} records: {str(e)}"
                    ]
                    # Set a general error message for unexpected errors
                    error_message = (
                        "An unexpected error occurred while retrieving DNS records."
                    )

    # Render the template with form, results, and error message
    response = render(
        request,
        "projects/dns_tool.html",
        {"form": form, "results": results, "error_message": error_message},
    )

    # Sets additional anti-caching headers directly on the response object
    response["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response["Pragma"] = "no-cache"
    response["Expires"] = "0"

    # Return the HTTP response
    return response
