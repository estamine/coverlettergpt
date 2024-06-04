from openai import OpenAI
import urllib.request
import sys
from datetime import date
from bs4 import BeautifulSoup

# you have to add your OpenAI API Key to your development system to use the OpenAI Library, for example: export OPENAI_API_KEY=[OpenAI_API_Key here]

# initiate OpenAI Client
client = OpenAI()

# Get today's date to write unique
today = date.today()

# get job description url from the command line
url = sys.argv[1]

# get the notes to improve your prompt from the command line. the text should be inside ""
notes = sys.argv[2]

# open the cv.txt file with the text of your CV - I just copied the PDF text into a text file. depending on how your formatted it, that should be enough
f = open("cv.txt","r")
cv = f.read()
f.close()

# use Beautiful Soup to extract only the text from the page, removing all HTML tags and other items we don't need. Some text will be kept that has nothing to do with the job description, but it doesn't influence GPT's performance significantly
html = urllib.request.urlopen(url)
soup = BeautifulSoup(html, features="html.parser")
jobdescription = soup.get_text()

# concatenate the prompt using the information retrieved
prompt = "Job Description: '" + jobdescription + "'\n\nCV: '" + cv + "\n\nNotes: '" + notes + "'"

# call OpenAI API with the role Description for the system, in this case a Professional Cover Letter writer. Does that even exist? :D - I haven't been able to land a job with this script. Just so you knooowwww.
completion = client.chat.completions.create(
  model="gpt-4-turbo",
  messages=[
    {"role": "system", "content": "You are a professional writer of cover letters in [CHOOSE LANGUAGE]. You are given a Job Description a CV and Notes. You create the best one page cover letter possible combining the Job Description with the CV and taking into consideration the Notes given."},
    {"role": "user", "content": prompt}
  ]
)

# format the generated cover letter text to make the newlines \n actual newlines
coverlettertext = completion.choices[0].message.content
coverlettertext = coverlettertext.replace('\\n', '\n').replace('\\t', '\t')

# printout the cover letter text for control
print(coverlettertext)

# create a unique filename for each generation
outputfilename = today.strftime("%m%d%y%H%M%S_") + "coverlettertext.txt"

# write the generated cover letter text into a text file with the unique filename
f = open(outputfilename, "w")
f.write(coverlettertext)
f.close()
