# Cameroon IT Job Market Insight/DashBoard 
- This is a python tool (web crawler) that scrap IT job from cameroonian job posting sites.
## Tool description
- The crawler scrap job posting using python module SCRAPY.
- The data is collected into data form  with property such as: Date (job posting date), Job Tiltle, Link ( to view the job), Company, Location (which region is the job posting from), Job Type (full-time, internship or Part-time), and Job category (Dev, Network, IT manager)
- The data collected is save as a .csv (comma separated values) file.
- Pandas is use to view the date in Dataframes so that python module Streamlit can easily be to visualize the data.
## Installation 
\`\`\ bash 
git clone https://github.com/yourname/Cameroon-IT-Job-Market_Insight.git
cd Web Crawler 
pip install -r requirement.txt 
\`\`\

## Usage 
\`\`\ bash
streamlit run job_app1.py
\`\`\

## License
NexoraSolutions
