# coding: utf8
import re
from datetime import datetime

db.define_table('user',
    Field('userid', db.auth_user, default=auth.user_id, writable=False),
    Field('posting_date', 'datetime', default=datetime.utcnow(), writable=False),
    Field('fname', 'string', length=32), 
    Field('lname', 'string', length=32), 
    Field('email', 'string', length=64), 
    )

db.define_table('ingredient',
    Field('name', 'string', length=64), 
    Field('type', 'string', length=32), 
    )    

db.define_table('combination',
    Field('name', 'string', length=64), 
    ) 
    
db.define_table('ingredients_in_combination',
    Field('ingredientId',  'references ingredient'), 
    Field('combinationId', 'references combination'), 
    )    
  
db.define_table('cooking_method',
    Field('method', 'string', length=64), 
    Field('combinationId', 'references combination'), 
    )   
  
db.define_table('ratings_ingredients',
    Field('userId', 'references user'), 
    Field('ingredientId',  'references ingredient'), 
    Field('rating', integer), 
    )     
        
db.define_table('ratings_combination',
    Field('userId',  'references user'), 
    Field('combinationId', 'references combination'), 
    Field('rating', integer), 
    )    
    
db.define_table('ratings_cooking_method',
    Field('userId',  'references user'), 
    Field('cookingId', 'references cooking_method'), 
    Field('rating', integer), 
    )
