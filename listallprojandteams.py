import os
import csv
from dotenv import load_dotenv
from azure.devops.connection import Connection
from msrest.authentication import BasicAuthentication

# Load .env if present
load_dotenv()

print("Current working directory:", os.getcwd())

organization_url = os.getenv("AZURE_DEVOPS_ORGANIZATION_URL")
personal_access_token = os.getenv("AZURE_DEVOPS_PAT")

if not organization_url or not personal_access_token:
    print("Missing AZURE_DEVOPS_ORGANIZATION_URL or AZURE_DEVOPS_PAT in environment.")
    exit(1)

credentials = BasicAuthentication('', personal_access_token)
connection = Connection(base_url=organization_url, creds=credentials)
core_client = connection.clients.get_core_client()

projects = core_client.get_projects()
print(f"Found {len(projects)} projects.")

if not projects:
    print("No projects found. Exiting.")
    exit(1)

with open("project_team_ids.csv", "w", newline="") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Project Name", "Project ID", "Team Name", "Team ID"])
    for project in projects:
        teams = core_client.get_teams(project.id)
        for team in teams:
            writer.writerow([project.name, project.id, team.name, team.id])

print("Saved to project_team_ids.csv")