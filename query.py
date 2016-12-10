from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import and_, or_
 
from database_setup import Restaurant, Base, MenuItem
 
engine = create_engine('sqlite:///restaurantmenu.db')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine
 
DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()

# aunty = session.query(Restaurant).filter(Restaurant.name.like('%Ann%')).one()
# print aunty.name
# delicacy = session.query(MenuItem).filter(and_(MenuItem.name.like('%Spinach%'), MenuItem.restaurant_id == aunty.id)).one()
# session.delete(delicacy)
# session.commit()
r = session.query(Restaurant).filter_by(id = 2).one()
print r.name
