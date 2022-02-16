from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
app = Flask(__name__)

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

engine = create_engine('sqlite:///restaurantmenu.db?check_same_thread=False')
Base.metadata.bind = engine
DBSession = sessionmaker(bind = engine)
session = DBSession()

#Fake Restaurants
restaurant = {'name': 'The CRUDdy Crab', 'id': '1'}

restaurants = [{'name': 'The CRUDdy Crab', 'id': '1'}, {'name':'Blue Burgers', 'id':'2'},{'name':'Taco Hut', 'id':'3'}]


#Fake Menu Items
items = [ {'name':'Cheese Pizza', 'description':'made with fresh cheese', 'price':'$5.99','course' :'Entree', 'id':'1'}, {'name':'Chocolate Cake','description':'made with Dutch Chocolate', 'price':'$3.99', 'course':'Dessert','id':'2'},{'name':'Caesar Salad', 'description':'with fresh organic vegetables','price':'$5.99', 'course':'Entree','id':'3'},{'name':'Iced Tea', 'description':'with lemon','price':'$.99', 'course':'Beverage','id':'4'},{'name':'Spinach Dip', 'description':'creamy dip with fresh spinach','price':'$1.99', 'course':'Appetizer','id':'5'} ]
item =  {'name':'Cheese Pizza','description':'made with fresh cheese','price':'$5.99','course' :'Entree'}


@app.route('/')
@app.route('/restaurants')
def showRestaurants():
    return render_template('restaurants.html', restaurants=restaurants)


@app.route('/restaurant/new')
def newRestaurant():
    return render_template('new_restaurant.html')

@app.route('/restaurant/<int:restaurant_id>/edit', methods=["GET", "POST"])
def editRestaurant(restaurant_id):
    
    return render_template('edit_restaurant.html', restaurant_id=restaurant_id)

@app.route('/restaurant/<int:restaurant_id>/delete', methods=["GET", "POST"])
def deleteRestaurant(restaurant_id):
    return render_template('delete_restaurant.html', restaurant_id=restaurant_id)

@app.route('/restaurant/<int:restaurant_id>', methods=["GET"])
@app.route('/restaurant/<int:restaurant_id>/menu', methods=["GET", "POST"])
def showRestaurantMenu(restaurant_id):
    return render_template("menu.html", restaurant=restaurant, items=items)

@app.route('/restaurant/<int:restaurant_id>/menu/new', methods=["GET", "POST"])
def newMenuItem(restaurant_id):
    if request.method=="POST":
        newItem = MenuItem(name = request.form['name'],description=request.form['description'], price=request.form['price'], restaurant_id=restaurant_id)
        session.add(newItem)
        session.commit()
        flash("new menu item created")
        return redirect(url_for('restaurantMenu',restaurant_id=restaurant_id))
    else:
        return render_template("new_menu_item.html", restaurant=restaurant, restaurant_id=restaurant_id)

@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/edit', methods=["GET", "POST"])
def editMenuItem(restaurant_id,menu_id):
    if request.method == "POST":
        editedItem.name = request.form['name']
        editedItem.description = request.form['description'] if request.form['description'] != None else editedItem.description
        editedItem.price = request.form['price'] if request.form['price'] != None else editedItem.price
        flash("menu item updated")
        return redirect(url_for('restaurantMenu',restaurant_id=restaurant_id))
    else:
        return render_template("edit_menu_item.html", restaurant_id=restaurant_id, menu_id=menu_id, item = editedItem)

@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/delete', methods=["GET", "POST"])
def deleteMenuItem(restaurant_id,menu_id):
    if request.method == "POST":
        session.delete(deleteItem)
        session.commit()
        flash("menu item deleted")
        return redirect(url_for('restaurantMenu',restaurant_id=restaurant_id))
    else:
        return render_template("delete_menu_item.html",item=deleteItem)


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)