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

	return dict()


def createcombination():
	# User goes to main page
	# User starts adding ingredients ->
	#	This grabs the said ingredient ids from the db and stores them in a list
	# User presses 'recommend' ->
	#	This creates a combination, and creates an ingredient_in_combination for each ingredient
	ingredientList = request.vars.values()[0]
#	full_ingredient = db(db.ingredients.name == name).select().first()
#	if result != None:
	# session.ingredientList.append(name)
	#combinationid = db.combinations.insert(name="temp")
	#session.comboId = combinationid
	# do some validaiton on the returned string
	redirect(URL('combinations'))	
	
	return ingredientList
	
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

def combinations():
	user_comboid = session.comboId
	if user_comboid == None:
		return dict(user_comboid='None')
	else:
		combination = db.combinations[user_comboid]
		ingredients = db(db.ingredients_in_combination.combinationId == user_comboid).select()
		return dict(user_comboid=user_comboid,combination=combination,ingredients=ingredients)
	
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
