from flask_app.config.mysqlconnection import connectToMySQL   # need a connection from mysqlconnection -->
from flask_app import DATABASE
from flask_app.models import user_model 
import re
from flask import flash
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 
ALPHA = re.compile(r"^[a-zA-Z]+$")


class Recipe:                        
    def __init__(self, data) -> None:  #takes in data dictionary "__Init__"
        self.id = data['id']
        self.name = data['name']
        self.date_made = data['date_made']
        self.under_30min = data['under_30min']
        self.description= data['description']
        self.instructions= data['instructions']
        self.user_id= data['user_id']
        self.created_at =data['created_at']
        self.updated_at = data['updated_at']





# Create Method------------------------------------------------------------------

    @classmethod
    def create(cls, data):  
        query = """
            INSERT INTO recipes (name, date_made, under_30min, description, instructions, user_id)
            VALUES (%(name)s, %(date_made)s, %(under_30min)s, %(description)s, %(instructions)s, %(user_id)s);
        """
        return connectToMySQL(DATABASE).query_db(query,data)


# Delete Method-------------------------------------------------------------------

    @classmethod
    def delete(cls,data):
        query = """
        DELETE FROM recipes WHERE  = %(id)s;
    """
        return  connectToMySQL(DATABASE).query_db(query, data)




# Get all with-------- Join Method-------------------------------------------------
    @classmethod
    def get_all(cls):
        query = """
            SELECT * FROM recipes JOIN users ON users.id = user_id;
    """
        results = connectToMySQL(DATABASE).query_db(query)  # list of all the dictionary keys
        all_recipes = []      #This is the recipe object !IMPORTANT FOR TEST
        if results:
            for row_from_db in results:
                recipe_instance = cls(row_from_db)
                user_data = { 
                    
                    **row_from_db, #copied the whole row
                    "id": row_from_db['users.id'],   #asking for the user id not recipe_id
                    "created_at": row_from_db['users.created_at'],
                    "updated_at": row_from_db['users.updated_at']
                    }
                user_instance = user_model.User(user_data)
                recipe_instance.chef = user_instance   #made up teh chef name
                all_recipes.append(recipe_instance)    
        return all_recipes    #THIS IS RETURNING THE recipes OBJECT



# Get one----------- Join Method----------------------------------------------------
    @classmethod
    def get_one(cls, data):
        query= """
        SELECT * FROM recipes JOIN users On recipes.user_id = user_id
        WHERE recipes.id=%(id)s;
        """
        results = connectToMySQL(DATABASE).query_db(query, data)
        if results:
            row = results[0]
            recipe_instance = cls(row)
            user_data = {                     
                    **row, #copied the whole row
                    "id": row['users.id'],   #asking for the user id not recipe_id
                    "created_at": row['users.created_at'],
                    "updated_at": row['users.updated_at']
                    }
            user_instance = user_model.User(user_data)
            recipe_instance.chef = user_instance   #made up teh chef name
            return recipe_instance       #THIS IS RETURNING THE recipes OBJEC
        return False    



# Get by ID Method--------------------------------------------------------------
    @classmethod
    def get_by_id(cls,data):  #getting by_id
        query = """
            SELECT * FROM recipes WHERE id = %(id)s;
        """
        results = connectToMySQL(DATABASE).query_db(query, data)
        if results:    #if statement asking if i find the id return the results in the first index as a object
            return cls(results[0])
        return False   #otherwise return false.... THis is like a boolean check




# update method--------------------------------------------------------------------

    @classmethod
    def update(cls, data):
        query = "UPDATE recipes SET name = %(name)s, description = %(description)s, instructions = %(instructions)s, date_made = %(date_made)s, under_30min = %(under_30min)s WHERE id = %(id)s;"
        results = connectToMySQL(DATABASE).query_db(query, data) 
        return results



# Static Method---------------------------------------------------------------------
    @staticmethod
    def is_valid(data):
        is_valid = True

    #name validation
        if len(data['name']) < 1: 
            flash('Bro.. Name is required ')
            is_valid = False
        elif len(data['name']) < 2:
            flash('Bro.. Name must be 2 characters at least' )
            is_valid = False
        elif not ALPHA.match(data['name']): 
            flash('Seriously.. Name can only contain letters' )
            is_valid = False

    #description validation
        if len(data['description']) < 1:
            flash('Fool... Description required' )
            is_valid = False
        elif len(data['description']) < 2:
            flash(' Bro.. Description must be 2 characters at least' )
            is_valid = False
        # elif not ALPHA.match(data['description']): 
        #     flash('Seriously.. Description can only contain letters' )
        #     is_valid = False

    #instruction validation
        if len(data['instructions']) < 1:
            flash('Fool... Instructions name required' )
            is_valid = False
        elif len(data['instructions']) < 2:
            flash(' Bro.. Instructions name must be 2 characters at least' )
            is_valid = False
        # elif not ALPHA.match(data['instructions']): 
        #     flash('Seriously.. Instructions name can only contain letters' )
            # is_valid = False  

    #Under_30 min validation
        if "under_30min" not in data:
            flash('Fool... Must select a checkbox required' )
            is_valid = False
        # elif data['under_30min'] != '0':
        #     flash('Fool... Must select a checkbox required' )
        #     is_valid = False
        # elif data['under_30min'] != '1':
        #     flash(' Bro.. Must seclect a checkbox ' )
        #     is_valid = False

    #date_made
        if len(data['date_made']) < 1:
            flash('Fool... Date required' )
            is_valid = False
        return is_valid 










   






