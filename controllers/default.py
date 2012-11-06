# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

#########################################################################
## This is a samples controller
## - index is the default action of any application
## - user is required for authentication and authorization
## - download is for downloading files uploaded in the db (does streaming)
## - call exposes all registered services (none by default)
#########################################################################

from gluon.tools import Crud
import time

def index():
	# User goes to main page
	# User starts adding ingredients ->
	#	This grabs the said ingredient ids from the db and stores them in a list
	# User presses 'recommend' ->
	#	This creates a combination, and creates an ingredient_in_combination for each ingredient
			
	# Form used to ask for a recommendation
	# Preconditions: All the ingredients in ingredientList are actual ingredients
	submitForm=FORM(INPUT(_type='submit',_value='Recommend'))		
	if submitForm.accepts(request,session):	
		combinationid = db.combinations.insert(name="temp")
		for ingredient in session.ingredientList:
			db.ingredients_in_combination.insert(combinationId=combinationid,ingredientId=ingredient.id)
		
	return dict(submitForm=submitForm)


def findIngredientName():
	name = request.vars.values()[0]
	#result = db(db.ingredients.name == ).select().first()	
	return name + "oholhlohlholhol"
	
def ajaxlivesearch():
    partialstr = request.vars.values()[0]
    query = db.ingredients.name.like('%'+partialstr+'%')
    ingredients = db(query).select(db.ingredients.name)
    items = []
    for (i,ingredient) in enumerate(ingredients):
        items.append(DIV(A(ingredient.name, _id="res%s"%i, _href="#", _onclick="copyToBox($('#res%s').html())"%i), _id="resultLiveSearch"))

    return TAG[''](*items)
  
def ingredients():
    ingredients = db(db.ingredients).select()
    return dict(ingredients=ingredients, user_id = auth.user_id)

@auth.requires_signature()
def combinations():
    combinations = db(db.combinations).select()
    return dict(combinations=combinations, user_id = auth.user_id)
            
def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    """
    return dict(form=auth())


def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request,db)


def call():
    """
    exposes services. for example:
    http://..../[app]/default/call/jsonrpc
    decorate with @services.jsonrpc the functions to expose
    supports xml, json, xmlrpc, jsonrpc, amfrpc, rss, csv
    """
    return service()


@auth.requires_signature()
def data():
    """
    http://..../[app]/default/data/tables
    http://..../[app]/default/data/create/[table]
    http://..../[app]/default/data/read/[table]/[id]
    http://..../[app]/default/data/update/[table]/[id]
    http://..../[app]/default/data/delete/[table]/[id]
    http://..../[app]/default/data/select/[table]
    http://..../[app]/default/data/search/[table]
    but URLs must be signed, i.e. linked with
      A('table',_href=URL('data/tables',user_signature=True))
    or with the signed load operator
      LOAD('default','data.load',args='tables',ajax=True,user_signature=True)
    """
    return dict(form=crud())
