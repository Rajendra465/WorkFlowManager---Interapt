# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/core/actions/#custom-actions/


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker   
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet
from rasa_sdk.forms import FormAction


import pandas as pd 
import numpy as np 
import datetime as dt 

df = pd.read_csv('Team Info - Hackathon.csv')
df['Prod Start Date']= pd.to_datetime(df['Prod Start Date'])
df['Prod End Date']= pd.to_datetime(df['Prod End Date'])
df['resource product start date']= pd.to_datetime(df['resource product start date'])
df['resource product end date']= pd.to_datetime(df['resource product end date'])
df.columns =[column.replace(" ", "_") for column in df.columns]


def q1(df,im,jr,sr,date,location):
    data = df.query('Prod_Build_Location == "{loc}" and resource_product_end_date < "{date}"'.format(loc=location, date = date))
    data1 = data.query('Role_Level == "Senior"').sort_values('Burnout_rate')['Name'].to_list()
    data2 = data.query('Role_Level == "Junior"').sort_values('Burnout_rate')['Name'].to_list()
    data3 = data.query('Role_Level == "Mid"').sort_values('Burnout_rate')['Name'].to_list()

    return data3[0:im], data2[0:jr], data1[0:sr]


def q9(df, resource):
    tt = list(df.loc[df['Name'] == resource, ['Skill_1', 'Skill_2', 'Skill_3', 'Skill_4', 'Skill_5']].iloc[0])
    ll = [x for x in tt if x != 'nan']
    return tt

def q10(df):
    div = df['Gender'].value_counts()
    div_l = div.values
    return div_l

def q8(df, product):
    tt = list(df.loc[(df['Product'] == product) & (df['Security_Maven'] == 'Y')].iloc[0])
    return tt[0]

def q7(df, product):
    fl = []
    try:
        tt1 = list(df.loc[(df['Product'] == product) & (df['Role'] == 'PM')].iloc[0])
        fl.append(tt1[0])
    except:
        fl.append('None')
    try:
        tt2 = list(df.loc[(df['Product'] == product) & (df['Role'] == 'UX')].iloc[0])
        fl.append(tt2[0])
    except:
        fl.append('None')
    try:
        tt3 = list(df.loc[(df['Product'] == product) & (df['Role'] == 'Engr')].iloc[0])
        fl.append(tt3[0])
    except:
        fl.append('None')

    return fl

def q4(df):
    location = 'IL'
    data = df.query('Prod_Build_Location == "{loc}"'.format(loc = location))
    loc_1 = data['Name'].to_list()
    location = 'AX'
    data = df.query('Prod_Build_Location == "{loc}"'.format(loc = location))
    loc_2 = data['Name'].to_list()
    location = 'TX'
    data = df.query('Prod_Build_Location == "{loc}"'.format(loc = location))
    loc_3 = data['Name'].to_list()

    return loc_1, loc_2, loc_3

def q6(df, column):
    return df.groupby([column]).size().reset_index(name='Number of Resources')
#
#
# class ActionHelloWorld(Action):
#
#     def name(self) -> Text:
#         return "action_hello_world"
#
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#
#         dispatcher.utter_message(text="Hello World!")
#
#         return []



class Query1(Action):

     def name(self) -> Text:
         return "query_1"

     def run(self, dispatcher: CollectingDispatcher,
             tracker: Tracker,
             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

         im = 1
         jr = 1
         sr = 2
         date = '12/04/2021'
         location = 'IL'
         
         i,j,s = q1(df,im,jr,sr,date,location)

         dispatcher.utter_message(response = "utter_query1",im = i,jr=j,sr=s)

         #return [SlotSet("name", name)]
         return []

class Query4(Action):

     def name(self) -> Text:
         return "query_4"

     def run(self, dispatcher: CollectingDispatcher,
             tracker: Tracker,
             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

         loc1, loc2, loc3 = q4(df)   
         dispatcher.utter_message(response = "utter_query4",loc1 = loc1, loc2 = loc2, loc3 = loc3)

         #return [SlotSet("name", name)]
         return []

class Query6(Action):

     def name(self) -> Text:
         return "query_6"

     def run(self, dispatcher: CollectingDispatcher,
             tracker: Tracker,
             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

         c_lw = q6(df,'Location')   
         dispatcher.utter_message(response = "utter_query6",c_lw = c_lw)
         #return [SlotSet("name", name)]
         return []

class Query10(Action):

     def name(self) -> Text:
         return "query_10"

     def run(self, dispatcher: CollectingDispatcher,
             tracker: Tracker,
             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

         ratio_li = q10(df)   
         dispatcher.utter_message(response = "utter_query10",male_per = np.round((ratio_li[0]/sum(ratio_li))*100), female_per = np.round((ratio_li[1]/sum(ratio_li))*100))

         #return [SlotSet("name", name)]
         return []

class Query9(FormAction):

     def name(self) -> Text:
         return "query_9"
     

     @staticmethod
     def required_slots(tracker: Tracker) -> List[Text]:
        """A list of required slots that the form has to fill"""
        
        return ["resource"]

    

     def submit(self, dispatcher: CollectingDispatcher,
             tracker: Tracker,
             domain: Dict[Text, Any],
     ) -> List[Dict]:
         resource = tracker.get_slot('resource')
         resource = 'Resource ' + str(resource)
         skills = q9(df,resource)
         print(skills)
         l = len(skills)
         pp =''
         t = 0
         while t<l:
             pp =  pp + str(skills[t]) + ' '
             t += 1
         print(pp)
         dispatcher.utter_message(response = "utter_query9",resource = resource, skills=pp)

         return []

class Query7(FormAction):

     def name(self) -> Text:
         return "query_7"
     

     @staticmethod
     def required_slots(tracker: Tracker) -> List[Text]:
        """A list of required slots that the form has to fill"""
        
        return ["product"]

     def submit(self, dispatcher: CollectingDispatcher,
             tracker: Tracker,
             domain: Dict[Text, Any],
     ) -> List[Dict]:
         product = tracker.get_slot('product')
         product = 'Product ' + str(product)
         res = q7(df,product)
         dispatcher.utter_message(response = "utter_query7",product= product, pm = res[0], ux = res[1], er = res[2])

         return []

class Query8(FormAction):

     def name(self) -> Text:
         return "query_8"
     

     @staticmethod
     def required_slots(tracker: Tracker) -> List[Text]:
        """A list of required slots that the form has to fill"""
        
        print("required_slots(tracker: Tracker)")
        return ["product"]

     def submit(self, dispatcher: CollectingDispatcher,
             tracker: Tracker,
             domain: Dict[Text, Any],
     ) -> List[Dict]:
         product = tracker.get_slot('product')
         product = 'Product ' + str(product)
         res = q8(df,product)
         dispatcher.utter_message(response = "utter_query8",product = product,res = res)

         return []