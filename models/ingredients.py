# coding: utf8
import re
from datetime import datetime

db.define_table('user',
    Field('userid', db.auth_user, default=auth.user_id, writable=False),
    Field('posting_date', 'datetime', default=datetime.utcnow(), writable=False, readable=False),
    Field('fname', 'string', length=32), 
    Field('lname', 'string', length=32), 
    Field('email', 'string', length=64), 
    )

db.define_table('ingredients',
    Field('name', 'string', length=64, unique='True'),
    Field('type', 'string', length=32), 
    )    

db.define_table('combinations',
    Field('name', 'string', length=64), 
    Field('posting_date', 'datetime', default=datetime.utcnow(), writable=False, readable=False),
    ) 
    
db.define_table('ingredients_in_combination',
    Field('ingredientId',  'reference ingredients', readable=False), 
    Field('combinationId', 'reference combinations', readable=False), 
    )    
 
 
#db.define_table('cooking_method',
#    Field('method', 'string', length=64), 
#    Field('combinationId', 'references combination'), 
#    )   

db.define_table('ingredients_weighted_value',
    Field('ingredientId1',  'reference ingredients'), 
    Field('ingredientId2',  'reference ingredients'),
    Field('value', 'double'),
    )
              
#db.define_table('ratings_ingredients',
#    Field('userId', 'references user'), 
#    Field('ingredientId',  'references ingredient'), 
#    Field('rating', 'integer'), 
#    Field('posting_date', 'datetime', default=datetime.utcnow(), writable=False, readable=False),
#    )     
        
#db.define_table('ratings_combination',
#    Field('userId',  'references user'), 
#    Field('combinationId', 'references combination'), 
#    Field('rating', 'integer'), 
#    Field('posting_date', 'datetime', default=datetime.utcnow(), writable=False, readable=False),
#    )    
    
#db.define_table('ratings_cooking_method',
#    Field('userId',  'references user'), 
#    Field('cookingId', 'references cooking_method'), 
#    Field('rating', 'integer'), 
#    Field('posting_date', 'datetime', default=datetime.utcnow(), writable=False, readable=False),
#    )
