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
	ingredient_input = request.vars.values()[0]
	ingredient_output = ''
	
	ingredient_list = ingredient_input.split(',')
	combinationid = db.combinations.insert(name="temp")
	session.comboId = combinationid
	for each_ingredient in ingredient_list:
		full_ingredient = db(db.ingredients.name == str(each_ingredient)).select().first()
		if full_ingredient != None:
			ingredient_output += str(full_ingredient.name) + ','
			db.ingredients_in_combination.insert(ingredientId=full_ingredient.id,combinationId=combinationid)
		else:
			ingredient_output += 'fail,'

	#redirect(URL('combinations'),type='auto')	
	
	return 'combinations'

def ajaxlivesearch():
    partialstr = request.vars.values()[0]
    query = db.ingredients.name.like('%'+partialstr+'%')
    ingredients = db(query).select(db.ingredients.name)
    items = []
    for (i,ingredient) in enumerate(ingredients):
        items.append(DIV(A(ingredient.name, _id="res%s"%i, _href="#", _onclick="copyToBox($('#res%s').html())"%i), _id="resultLiveSearch"))

    return TAG[''](*items)
  
def addingredient():
	add_ingredient_form = SQLFORM(db.ingredients)
	if add_ingredient_form.process().accepted:
		# add a new ingredient to the db
		new_ingredient_id = db.ingredients.insert(name=add_ingredient_form.vars.name, type=add_ingredient_form.vars.type)

		# grab all ingredients that are not the newly inserted
		other_ingredients = db(db.ingredients.id!=new_ingredient_id).select()
		# add a relation to each other ingredients
		for each_ingredient in other_ingredients:
			db.ingredients_weighted_value.insert(ingredientId1=new_ingredient_id,ingredientId2=each_ingredient.id, value=0.5)
			
	return dict(add_ingredient_form=add_ingredient_form)
 
def recommend():
	total_group_of_edges = []
	ingredients_in_combo = db(db.ingredients_in_combination.combinationId==session.comboId).select()
	for each_ingredient in ingredients_in_combo:
		total_group_of_edges |= db(db.ingredients_weighted_value.ingredientId1==each_ingredient.ingredientId |
								   db.ingredients_weighted_value.ingredientId2==each_ingredient.ingredientId).select()
		
 
def ingredients():
	ingredients = db(db.ingredients).select()
	ingredient_pairs = db(db.ingredients_weighted_value).select()
	return dict(ingredients=ingredients, ingredient_pairs=ingredient_pairs)

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
