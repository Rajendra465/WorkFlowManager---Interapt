import pandas as pd
import datetime

# Need 1 intermediate 1 junior, 2 senior resource available for new products
# starting on May 15 2021 for build location in IL?
# (Hint: Resources have to be found based on product end-date closest to May 15
# 2021, their level and their location)
def find_team(dt, intermediate, junior, senior, start_date, location):
    dt = dt.loc[(dt['Location'] == location )| (dt['Available for Other areas'] == 'Y')]
    dt['Prod End Date'] = pd.to_datetime(dt['Prod End Date'])
    date = pd.to_datetime(start_date)
    #dt.sort_values(by=(abs([['Prod End Date' ]- date])))
    #print(dt)


def find_resources_by_column(dt, column, value):
    return dt.loc[dt[column] == value]

# Alert on product missing end date despite it is going on for one month?
def missing_end_date(dt):
    x = float("nan")
    bool_series = pd.isnull(dt['Prod End Date'])
    dt = dt[bool_series]
    bool_series = pd.notnull(dt['Prod Start Date'])
    dt = dt[bool_series]

    dt['Prod Start Date'] = pd.to_datetime(dt['Prod Start Date'])
    today = pd.to_datetime('today')
    # print(dt.loc[dt['Prod Start Date'] < today])
    #return dt.loc[(dt['Prod End Date'] == '') & (dt['Prod Start Date'] )]

# Resource ready for next rotation? (Hint: Identify folks working longest on
# product based on their resource product start date compared to current date?)
# currently returns a list of rersources sorted by start date, ascending
def resources_ready_for_rotation(dt):
    dt['resource product start date'] = pd.to_datetime(dt['resource product start date'])
    return dt.sort_values(by=['resource product start date'], ascending=True)

# Location-wise resources – PMs, UXs, Engrs?
def location_ratio_for_project(dt, location):
    return ratio(dt.loc[(dt['Location'] == location)])

# What is the PM to UX to Engr ratio?
def ratio(dt, path):
    return dt.groupby(['Role']).size().reset_index(name='Number of Resources')

def ratio_for_project(dt, project):
    return ratio(dt.loc[(dt['Product'] == project)])

# How many contractor resources? Vendor-wise, Location-wise
def find_num_resources_by_column(dt, column):
    return dt.groupby([column]).size().reset_index(name='Number of Resources')

# Who is the PM, UX or Engr on a product?
def find_person_by_product_and_role(dt, project, role):
    return dt.loc[(dt['Product'] == project) & (d['Role'] == role)]

# Who is the Security Maven on a product?
# Area refers to: Anchor, Work Intake Scoping, Interviewer, Security Maven, Accessibility, DevSecOps, Education Tracks
def find_person_by_project_and_area(dt, project, area):
    return dt.loc[(dt['Product'] == project) & (d[area] == 'Y')]

# Skill set of a resource?
def skill_set_by_resource(dt, name):
    return dt.loc[dt['Name'] == 'name', ['Skill 1', 'Skill 2', 'Skill 3', 'Skill 4', 'Skill 5']]

# What is our diversity/Gender mix?
def diversity(dt):
    return dt.groupby(['Gender', 'Color (Y/N)']).size().reset_index(name='Number of Resources')

def diversity_for_project(dt, project):
    return diveristy(dt.loc[(dt['Product'] == project)])

def main():
    dt = pd.read_csv("../data.csv")
    # find_team(dt, 1, 2, 3, "05/12/21", "IL")
    missing_end_date(dt)


if __name__ == "__main__":
    main()
