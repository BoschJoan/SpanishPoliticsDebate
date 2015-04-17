# -*- coding: utf-8 -*-
"""
Created on Thu Apr 16 10:23:26 2015

@author: boschj
"""

#%%

import pymongo

try:
    connection=pymongo.MongoClient()
    print "Connection to Mongo Daemon successful!!!"
except pymongo.errors.ConnectionFailure, e:
    print "Could not connect to MongoDB: %s" % e
    
#%%

db = connection['congres'] 

print "Collections : ", db.collection_names()

#%%

for col in db.collection_names():
    print col + ': ' + str(db[col].count()) + ' elements'
    
docs = db.document

#%%

import datetime
dates = []

for doc in docs.find():
    dates.append(doc['date'])
    
dates.sort()

#%%

print ('Tenim ' + str(len(dates)) + ' sessions de control entre el ' + 
            dates[0].strftime("%d/%m/%Y") + ' i el ' + 
            dates[-1].strftime("%d/%m/%Y"))

#%%

start_date = "08/02/2012"
start_date = datetime.datetime.strptime(start_date, "%d/%m/%Y")

last_dates = []

for doc in docs.find({'date':{'$gte': start_date}}):
    last_dates.append(doc['date'])
    
last_dates.sort()

#%%
print ('Ara tenim ' + str(len(last_dates)) + ' sessions de control entre el ' + 
            last_dates[0].strftime("%d/%m/%Y") + ' i el ' + 
            last_dates[-1].strftime("%d/%m/%Y"))
            
#%%

start_date = "01/01/2015"
start_date = datetime.datetime.strptime(start_date, "%d/%m/%Y")

end_date = "31/01/2015"
end_date = datetime.datetime.strptime(end_date, "%d/%m/%Y")

docs_gen_2015 = []

for doc in docs.find({'date':{'$gte': start_date, '$lte': end_date}}):
    docs_gen_2015.append(doc)

#%%

d = docs_gen_2015[0]

ds = d['session_dictionary']

ds[0]
       
#%% Revisar data inicial
        
import collections

kw = collections.Counter()

start_date = "01/11/2011"
start_date = datetime.datetime.strptime(start_date, "%d/%m/%Y")

for doc in docs.find({'date':{'$gte': start_date}}):
    for pregunta in doc['session_dictionary']:
        ks = []
        for k in pregunta['keywords']:
            ks.append(k[0])
        kw.update(ks)
        for interv in pregunta['intervention_dictionary']:
            ks = []
            for k in interv['keywords']:
                ks.append(k[0])
            kw.update(ks)
    print doc['date'].strftime("%d/%m/%Y")

#%% Repassar valor
to_filter = []
for k in kw:
    if kw[k] < 4:
        to_filter.append(k)

#%%

for k in to_filter:
    del kw[k]
    
#%%

to_filter = []
for k in kw.keys():
    if k[0] in ['-',',','.']:
        to_filter.append(k)

#%%  

for k in to_filter:
    del kw[k]
    
#%% Canviar a sparse Matrix??
    
import numpy as np

keywords = kw.keys()

mat = np.zeros((len(keywords), len(keywords)), dtype = float)

#%% Revisar data d'inici ??

start_date = "01/01/2011"
start_date = datetime.datetime.strptime(start_date, "%d/%m/%Y")
    
for doc in docs.find({'date':{'$gte': start_date}}):
    for pregunta in doc['session_dictionary']:
        ks = []
        for k in pregunta['keywords']:
            ks.append(k[0])
        for interv in pregunta['intervention_dictionary']:
            for k in interv['keywords']:
                ks.append(k[0])
        
        for k1 in ks:
            if k1 in keywords:
                for k2 in ks:
                    if k2 in keywords:
                        mat[keywords.index(k1), keywords.index(k2)] += 1
        
    print doc['date'].strftime("%d/%m/%Y")

#%%

import cPickle as cp

with open('matrix.pickle', 'wb') as handle:
    cp.dump(mat, handle)
    
#%% Prova de càrrega

with open('matrix.pickle', 'rb') as handle:
    mat2 = cp.load(handle)

#%%

