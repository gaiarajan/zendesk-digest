import json
import requests
import datetime
import time

from requests.auth import HTTPBasicAuth
from markdown_pdf import MarkdownPdf, Section

zendesk_url = "https://YOUR-URL.zendesk.com" 
email_address = 'YOUR-EMAIL@gmail.com'
api_token = 'YOUR-API=TOKEN'

query = "/api/v2/search.json?query=type:ticket status:open"
url = zendesk_url + query
headers = {
    "Content-Type": "application/json",
}
auth = HTTPBasicAuth(f'{email_address}/token', api_token)

# Fetching tickets from Zendesk API
response = requests.request(
    "GET",
    url,
    auth=auth,
    headers=headers
)

# Parsing the response
data = json.loads(response.text)
# Start building the content for the PDF
content = """
<style>
    body {
        font-family: Arial, sans-serif;
        color: #333;
        line-height: 1.6;
    }
    h1 {
        color: #2c3e50;
        border-bottom: 2px solid #2c3e50;
        padding-bottom: 10px;
        margin-bottom: 20px;
    }
    h4 {
        color: #34495e;
        margin-top: 20px;
        margin-bottom: 5px;
    }

    .date {
        font-size:10px;
        color: #7f8c8d;
    }

    .ticket {
        margin-bottom: 30px;
    }
    .tags {
        margin-top: 10px;
        color: #2980b9;
    }
    hr {
        border: 0;
        border-top: 1px solid #ecf0f1;
        margin: 40px 0;
    }
</style>
"""
content += "<h1>Ticket Digest: " + datetime.datetime.now().strftime("%x") + "</h1>"

# Initialize PDF creation
pdf = MarkdownPdf()
pdf.meta["title"] = 'Digest'

tickets = []

# Process each ticket
for ticket in data["results"]:
    # Extracting and formatting the ticket information
    subject = f"<h4>SUBJECT:</h4> {ticket['subject']}"
    description = f"<h4>DESCRIPTION:</h4> {ticket['description']}"

    # Format tags with custom styling
    tags = ticket.get("tags", [])
    formatted_tags = f"<div class='tags'><strong>Tags:</strong> " + ", ".join(f"<span>{tag}</span>" for tag in tags) + "</div>"
    
    # Format creation date
    created_at = datetime.datetime.strptime(ticket['created_at'], "%Y-%m-%dT%H:%M:%SZ").strftime("%B %d, %Y at %H:%M")
    formatted_date = f"<div class='date'>{created_at}</div>"

    # Combine the ticket details
    ticket_content = f"<div class='ticket'>{subject}{description}{formatted_tags}{formatted_date}</div><hr>"
    tickets.append(ticket_content)

# Combine all tickets into the final content
for ticket in tickets:
    content += ticket

# Add content to the PDF
pdf.add_section(Section(content, toc=False))
# Save the PDF
pdf.save('digest.pdf')
