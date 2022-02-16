from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
app = Flask(__name__)

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

engine = create_engine('sqlite:///restaurantmenu.db?check_same_thread=False')
Base.metadata.bind = engine
DBSession = sessionmaker(bind = engine)
session = DBSession()

@app.route('/')
@app.route('/restaurants/<int:restaurant_id>/')
def restaurantMenu(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
    items = session.query(MenuItem).filter_by(restaurant_id = restaurant.id).all()
    return render_template("menu.html", restaurant=restaurant, items=items)

@app.route('/restaurant/<int:restaurant_id>/new/', methods=["GET", "POST"])
def newMenuItem(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one().name
    
    if request.method=="POST":
        newItem = MenuItem(name = request.form['name'],description=request.form['description'], price=request.form['price'], restaurant_id=restaurant_id)
        session.add(newItem)
        session.commit()
        flash("new menu item created")
        return redirect(url_for('restaurantMenu',restaurant_id=restaurant_id))
    else:
        return render_template("new_menu_item.html", restaurant=restaurant, restaurant_id=restaurant_id)
    

@app.route('/restaurant/<int:restaurant_id>/<int:menu_id>/edit/', methods=["GET", "POST"])
def editMenuItem(restaurant_id, menu_id):
    editedItem = session.query(MenuItem).filter_by(id=menu_id).one()
    if request.method == "POST":
        editedItem.name = request.form['name']
        editedItem.description = request.form['description'] if request.form['description'] != None else editedItem.description
        editedItem.price = request.form['price'] if request.form['price'] != None else editedItem.price
        flash("menu item updated")
        return redirect(url_for('restaurantMenu',restaurant_id=restaurant_id))
    else:
        return render_template("edit_menu_item.html", restaurant_id=restaurant_id, menu_id=menu_id, item = editedItem)    


@app.route('/restaurant/<int:restaurant_id>/<int:menu_id>/delete', methods=["GET", "POST"])
def deleteMenuItem(restaurant_id, menu_id):
    deleteItem = session.query(MenuItem).filter_by(id=menu_id).one()
    if request.method == "POST":
        session.delete(deleteItem)
        session.commit()
        flash("menu item deleted")
        return redirect(url_for('restaurantMenu',restaurant_id=restaurant_id))
    else:
        return render_template("delete_menu_item.html",item=deleteItem)    

### API GET configuration
@app.route('/restaurants/<int:restaurant_id>/menu/JSON')
def restaurantMenuJSON(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
    items = session.query(MenuItem).filter_by(restaurant_id = restaurant.id).all()
    return jsonify(MenuItems=[i.serialize for i in items])

@app.route('/restaurants/<int:restaurant_id>/menu/<int:menu_id>/JSON')
def menuItemJSON(restaurant_id, menu_id):
    #restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
    item = session.query(MenuItem).filter_by(id = menu_id).one()
    return jsonify(MenuItem=[item.serialize])    

if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)