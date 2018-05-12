from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models import *

engine = create_engine('sqlite:///problems.db')

Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)

session = DBSession()

category1 = Categories(name="Mess Facilities Feedback", image="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQyBtvgVNT4gvtUKam8a8VlhJgBbHcwYMP7vz3dhok9k51E0i-JRQ", description="Give your views regarding the Mess Facilities!", user_id=1)
session.add(category1)
session.commit()

feedback1 = Feedback(name="Mess", rating1=0, rating2=0, rating3=0, rating4=0, rating5=0, totalrating=0, avgratings=0,categories_id=1)
session.add(feedback1)
session.commit()

category2 = Categories(name="Hostel Facilities Feedback", image="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQfXajlsvoOQ7ml55B78fMF5H4EGLWQ_AMRRynUsL4jPDBOvtAh", description="Give your views about the Hostel Facilities!", user_id=1)
session.add(category2)
session.commit()

feedback2 = Feedback(name="Hostel", rating1=0, rating2=0, rating3=0, rating4=0, rating5=0, totalrating=0, avgratings=0,categories_id=2)
session.add(feedback2)
session.commit()

category3 = Categories(name="Warden and Other Staff Members Feedback", image="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQfXajlsvoOQ7ml55B78fMF5H4EGLWQ_AMRRynUsL4jPDBOvtAh", description="Give your views about the Warden and other Staff Members of the Hostel!", user_id=1)
session.add(category3)
session.commit()

feedback3 = Feedback(name="Warden", rating1=0, rating2=0, rating3=0, rating4=0, rating5=0, totalrating=0, avgratings=0,categories_id=3)
session.add(feedback3)
session.commit()

category4  = Categories(name="Food and Water", image="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRfToJCmzMnwzt1n5LBlfb_CEgpazIVSUfuaZqbXSrn-FPZs0fQ", description="Give your views about the Food and Water Facilities in the Hostel!", user_id=1)
session.add(category4)
session.commit()

feedback4 = Feedback(name="Food", rating1=0, rating2=0, rating3=0, rating4=0, rating5=0, totalrating=0, avgratings=0,categories_id=4)
session.add(feedback4)
session.commit()

category5 = Categories(name="Medical Facilities Feedback", image="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQu9L7JDLXB3AyLOV0sKOk6ZnsHi3eA60jkZOySFpcsza5o3CxwYQ", description="Give your views about the Medical Facilities in the' Hostel!", user_id=1)
session.add(category5)
session.commit()

feedback5 = Feedback(name="Medical", rating1=0, rating2=0, rating3=0, rating4=0, rating5=0, totalrating=0, avgratings=0,categories_id=5)
session.add(feedback5)
session.commit()

print "added categories"