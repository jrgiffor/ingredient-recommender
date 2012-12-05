# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

#########################################################################
## This is a samples controller
## - index is the default action of any application
## - user is required for authentication and authorization
## - download is for downloading files uploaded in the db (does streaming)
## - call exposes all registered services (none by default)
#########################################################################

from gluon.sql import Rows
from gluon.tools import Crud
from math import sqrt
import time
import operator

def index():

	return dict()


# make everything lower case
def createcombination():
	ingredient_input = request.vars.values()[0]
	ingredient_output = ''
	
	ingredient_list = ingredient_input.split(',')
	combinationid = db.combinations.insert(name="temp")
	session.comboId = combinationid
	for each_ingredient in ingredient_list:
		full_ingredient = db(db.ingredients.name.lower() == str(each_ingredient).lower()).select().first()
		if full_ingredient != None:
			ingredient_output += str(full_ingredient.name) + ','
			db.ingredients_in_combination.insert(ingredientId=full_ingredient.id,combinationId=combinationid)
		else:
			ingredient_output += 'fail,'

	# redirect(URL('recommend'),type='auto')	
	
	return ingredient_output

def ajaxlivesearch():
    partialstr = request.vars.values()[0]
    query = db.ingredients.name.like('%'+partialstr+'%')
    ingredients = db(query).select(db.ingredients.name)
    items = []
    for (i,ingredient) in enumerate(ingredients):
        items.append(DIV(A(ingredient.name, _id="res%s"%i, _href="#", _onclick="copyToBox($('#res%s').html())"%i), _id="resultLiveSearch"))

    return TAG[''](*items)
  
# for some reason, adds a copy of each ingredient as well
def addingredient():
	add_ingredient_form = SQLFORM(db.ingredients)
	if add_ingredient_form.process().accepted:
		# add a new ingredient to the db
		new_ingredient_id = db.ingredients.insert(name=add_ingredient_form.vars.name, type=add_ingredient_form.vars.type)

		# grab all ingredients that are not the newly inserted
		other_ingredients = db(db.ingredients.id!=new_ingredient_id).select()
		# add a relation to each other ingredients
		for each_ingredient in other_ingredients:
			db.ingredients_weighted_value.insert(ingredientId1=new_ingredient_id,ingredientId2=each_ingredient.id)
			
	return dict(add_ingredient_form=add_ingredient_form)
 
def recommend():
	total_group_of_edges = None
	# grab all the ingredients in the combo
	find_ingredients_query = db.ingredients_in_combination.combinationId == session.comboId
	find_ingredients_query &= db.ingredients_in_combination.ingredientId == db.ingredients.id
	ingredients_in_combo = db(find_ingredients_query).select(db.ingredients.id)
	ingredient_names_in_combo = db(find_ingredients_query).select(db.ingredients.name, db.ingredients.type)
	# select all ingredient relations that have only one ingredient in the combo
	#lhs_ingredients = db(db.ingredients_weighted_value.ingredientId1==each_ingredient.id).select()
	chosen_ingredient = db.ingredients.with_alias('chosen_ingredient')
	other_ingredient  = db.ingredients.with_alias('other_ingredient')
	
	#ingredient_name_query =  (chosen_ingredient.id == db.ingredients_weighted_value.ingredientId1) & (other_ingredient.id == db.ingredients_weighted_value.ingredientId2)
	#ingredient_name_query |= (chosen_ingredient.id == db.ingredients_weighted_value.ingredientId2) & (other_ingredient.id == db.ingredients_weighted_value.ingredientId1)
	
	# grab all ingredients related to the one chosen
	ingredient_name_query =  chosen_ingredient.id.belongs(ingredients_in_combo)
	ingredient_name_query &= ~other_ingredient.id.belongs(ingredients_in_combo)
	
	# let this save the value of the computed "closest distance"
	compute_value = {}
	# things to do to improve complex_rec_ingredients:
	# take the "closest distance" for all the ingredients. 
	# let val(ingredient1, ingredient2) stand for the AVG value of all ingredient1-ingredient2, value pairings
	# and "closest distance" would be sqrt(val(ingredient1,ingredientK)^2 + val(ingredient2,ingredientK)^2 + ... + val(ingredientN,ingredientK)^2)
	# for example for the ingredient pairings: beef-bell pepper and beef-onion, 
	#	"closest distance" ranking for beef would be sqrt(val(beef, bell pepper)^2 + val(beef, onion)^2)
	#complex_rec_ingredients = db(ingredient_name_query).select(chosen_ingredient.name, other_ingredient.name, db.ingredients_weighted_value.value.avg(), groupby=chosen_ingredient.name|other_ingredient.name)
	#for each_ingredient in complex_rec_ingredients:
	#	if each_ingredient.other_ingredient.name in compute_value:
	#		ongoing_value = float(compute_value[each_ingredient.other_ingredient.name])
	#		compute_value[each_ingredient.other_ingredient.name] = sqrt(pow(ongoing_value, 2) + pow(float(db.ingredients_weighted_value.value.avg)(), 2))
	#	else:
	#		compute_value[each_ingredient.other_ingredient.name] = db.ingredients_weighted_value.value.avg()
	
	#sorted_recommendations = sorted(compute_value.iteritems(), key=operator.itemgetter(1))
	#top_ingredients = []
	# this will grab the top three ingredients
	#for index in range(3):
	#	top_ingredients.append(sorted_recommendations[index][0])
		
	simple_rec_ingredients = db(ingredient_name_query).select(other_ingredient.name, db.ingredients_weighted_value.value.avg(), groupby=other_ingredient.name, orderby=db.ingredients_weighted_value.value.avg(), limitby=(0, 3))
	# , complex_rec_ingredients=top_ingredients
	return dict(ingredient_names_in_combo=ingredient_names_in_combo,simple_rec_ingredients=simple_rec_ingredients)
	
# create a function to accept input from the recommendations page. This will be ajax and should return true 
def recieve_rating():
	# this function will set ingredient_weighted_value.value for each ingredient in the combo and the ingredient "chosen" (clicked on)
	# partialstr = request.vars.values()[0]
	# with this wwe can find the combo and all the ingredients in the combo
	# then we will rate each ingrdient
	# it will return true to let the recommendation page change the view
	return True
	
 
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
