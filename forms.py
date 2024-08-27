# This is the form for the DNS Tool app.
class DomainForm(forms.Form):
    # Define a form field for the domain input
    domain = forms.CharField(
        # Label that will be displayed with the input field
        label="Domain Name:",
        # Maximum length of the input string
        max_length=253,
        # help_text="Enter a valid domain name (e.g., example.com).",
    )
