from flask import Flask, render_template, request,redirect,url_for,flash,jsonify
app = Flask(__name__)

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import and_, or_
from database_setup import Restaurant, Base, MenuItem
 
engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

# API endpoints
@app.route('/restaurants/JSON')
def restaurantsListJSON():
	restaurants = session.query(Restaurant).all()
	return jsonify(Restaurants = [i.serialize for i in restaurants])

@app.route('/restaurants/<int:restaurant_id>/menu/JSON')
def restaurantMenuJSON(restaurant_id):
	restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
	menuitems = session.query(MenuItem).filter_by(restaurant_id = restaurant.id).all()
	return jsonify(MenuItems = [i.serialize for i in menuitems])

@app.route('/restaurants/<int:restaurant_id>/menu/<int:menu_id>/JSON')
def menuItemJSON(restaurant_id,menu_id):
	restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
	menuitem = session.query(MenuItem).filter_by(id = menu_id).one()
	return jsonify(mi = [menuitem.serialize])

#Restaurant Methods
@app.route('/')
@app.route('/restaurants/')
def restaurantsList():
	restaurants = session.query(Restaurant).all()
	return render_template('restaurantlist.html',restaurants = restaurants)

@app.route('/restaurants/new' ,methods = ['GET','POST'])
def newRestaurant():
	if request.method == 'POST':
		newRest = Restaurant(name = request.form['name'])
		session.add(newRest)
		session.commit()
		flash("new restaurant created")
		return redirect(url_for('restaurantsList'))
	else:
		return render_template('newrestaurant.html')

@app.route('/restaurants/<int:restaurant_id>/edit',methods = ['GET','POST'])
def editRestaurant(restaurant_id):
	restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
	if request.method == 'POST':
		restaurant.name = request.form['name']
		session.add(restaurant)
		session.commit()
		flash("restaurant edited")
		return redirect(url_for('restaurantsList'))
	else:
		return render_template('editrestaurant.html',restaurant = restaurant)

@app.route('/restaurants/<int:restaurant_id>/delete',methods = ['GET','POST'])
def deleteRestaurant(restaurant_id):
	restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
	menuitems = session.query(MenuItem).filter_by(restaurant_id = restaurant.id).all()
	count = len(menuitems)
	if request.method == 'POST':
		for i in menuitems:
			session.delete(i)
			session.commit()
		session.delete(restaurant)
		session.commit()
		flash("restaurant deleted")
		return redirect(url_for('restaurantsList'))
	else:
		return render_template('deleterestaurant.html',restaurant = restaurant,menuitems = menuitems, count = count)


#Menu Item Methos

@app.route('/restaurants/<int:restaurant_id>/')
def restaurantMenu(restaurant_id):
	restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
	items = session.query(MenuItem).filter_by(restaurant_id = restaurant.id)
	return render_template('menu.html',restaurant = restaurant,items = items)

# Task 1: Create route for newMenuItem function here

@app.route('/restaurants/<int:restaurant_id>/new/',methods = ['GET','POST'])
def newMenuItem(restaurant_id):
	if request.method == 'POST':
		newItem = MenuItem(name = request.form['name'],restaurant_id = restaurant_id)
		session.add(newItem)
		session.commit()
		flash("new menu item created!")
		return redirect(url_for('restaurantMenu',restaurant_id = restaurant_id))		
	else:
		return render_template('newmenuitem.html',restaurant_id = restaurant_id)


	

# Task 2: Create route for editMenuItem function here

@app.route('/restaurants/<int:restaurant_id>/<int:menu_id>/edit/', methods = ['GET','POST'])
def editMenuItem(restaurant_id, menu_id):
	menuitem = session.query(MenuItem).filter_by(id= menu_id).one()
	if request.method == 'POST':
		if request.form['name']:
			menuitem.name = request.form['name']
		if request.form['course']:
			menuitem.course = request.form['course']
		if request.form['description']:
			menuitem.description = request.form['description']
		if request.form['price']:
			menuitem.price = request.form['price']
		session.add(menuitem)
		session.commit()
		flash("menu item edited",'edititem')
		return redirect(url_for('restaurantMenu',restaurant_id = restaurant_id))
	else:
		return render_template('editmenuitem.html',item = menuitem)

# Task 3: Create a route for deleteMenuItem function here

@app.route('/restaurants/<int:restaurant_id>/<int:menu_id>/delete/', methods = ['GET','POST'])
def deleteMenuItem(restaurant_id, menu_id):
	menuitem = session.query(MenuItem).filter_by(id = menu_id).one()
	if request.method == 'POST':
		session.delete(menuitem)
		session.commit()
		flash("menu item deleted",'deleteitem')
		return redirect(url_for('restaurantMenu',restaurant_id = restaurant_id))
	else:
		return render_template('deletemenuitem.html',item = menuitem)

#Main Method
if __name__ == '__main__':
	app.secret_key = 'super_secret_key'
	app.debug = True
	app.run(host = '0.0.0.0',port = 5000)