from flask_app import app       #import app from my _init__
from flask import render_template, redirect, request, flash, session  
from flask_app import DATABASE #imported from my server.py
from flask_app.models.recipe_model import Recipe   #import recipe_model
from flask_app.models.user_model import User



# All routes below ↓↓↓↓↓↓↓


#This is the home route for my page stacked with dashboard and recipes
@app.route('/')  
@app.route('/dashboard') 

# Create-recipe route-----------------------------------------------------------
@app.route('/recipes')  
def all_recipes():
    if 'user_id' not in session:
        return redirect('/')  #if not in session will redirect to home ('/')
    data = {
        'id': session['user_id']  #calling the user to the database
    }
    logged_user = User.get_by_id(data)
    all_recipes = Recipe.get_all()
    return render_template("dashboard.html", all_recipes=all_recipes, logged_user =logged_user)



# Create Route----With Validation-------------------------------------------------
@app.route('/recipes/create', methods=['POST'])  #create a new recipe when they login
def create_recipe():
    if not Recipe.is_valid(request.form):  # message will show up in staticmethod
        return redirect("/recipes/new")
    print("Request form", request.form)
    Recipe.create(request.form)
    return redirect('/dashboard')  #needs to redirect to dojos



# New_recipe Route--------------------------------------------------------------------
@app.route('/recipes/new')
def new_recipe():
    if 'user_id' not in session:
        return redirect("/")
    return render_template("new_recipe2.html")



# View one recipe by id-------------------------------------------------------------
@app.route('/recipes/<int:id>/view') #only asking to get one recipe view link
def view_one_recipe(id):
    if 'user_id' not in session:
        return redirect('/')
    user_data = {
        'id': session['user_id']  #calling the user to the database
    }
    logged_user = User.get_by_id(user_data)
    data = {
        'id': id
    }
    get_one = Recipe.get_one(data)
    return render_template('view_recipe.html', recipe= get_one, user=logged_user)



# Edit Recipe-------------------------------------------------------------------------
@app.route("/recipes/<int:id>/edit")
def edit_recipe(id):
    data = {
        "id": id
    }
    return render_template("edit_recipe.html", recipe = Recipe.get_one(data))



# Delete Route-----------------------------------------------------------------------
@app.route('/recipes/<int:id>/delete')  # Update is a action route so we will be returning a redirect back to that action route just deleting the recipe
def delete_recipe(id):
    data = {
        'id': id
    }
    Recipe.delete(data)   #Linking to delete @classmethod
    return redirect('/')



# Update Route----------------------------------------------------------------------------
@app.route('/recipes/<int:id>/update', methods=['POST'])  # Update is a action route so we will be returning a redirect back to that action route
def update_recipe(id):
    print(request.form)
    data = {
    'id':id,
    'name':request.form['name'],
    'description':request.form['description'],
    'under_30min':request.form['under_30min'],
    'instructions':request.form['instructions'],
    'date_made':request.form['date_made']
    }
    if not Recipe.is_valid(data):  # message will show up in staticmethod
        return redirect(f"/recipes/{id}/edit")
    Recipe.update(data)         #Linking to update @classmethod
    return redirect('/dashboard')








