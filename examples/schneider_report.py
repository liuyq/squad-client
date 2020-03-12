#!/usr/bin/env python3
import os
import jinja2
import sys


sys.path.append('..')


from squad_client.core.api import SquadApi
from squad_client.core.models import Squad


SquadApi.configure(url='https://qa-reports.linaro.org/', token=os.getenv('QA_REPORTS_TOKEN'))
group = Squad().group('schneider')
project = group.project('warrior-4.9')
build = project.build('50')
testruns = build.testruns(bucket_suites=True, completed=True).values()

templateLoader = jinja2.FileSystemLoader(searchpath="./")
templateEnv = jinja2.Environment(loader=templateLoader)
TEMPLATE_FILE = "schneider_template.html"
template = templateEnv.get_template(TEMPLATE_FILE)
outputText = template.render(group=group, project=project, build=build, testruns=testruns)
with open('schneider_generated_report.html', 'w') as reportFile:
    reportFile.write(outputText)
if os.getenv('TO_PDF'):
    bash_cmd = "wkhtmltopdf schneider_generated_report.html schneider_generated_report.pdf"
    import subprocess
    process = subprocess.Popen(bash_cmd.split(), stdout=subprocess.PIPE)
    output, error = process.communicate()
