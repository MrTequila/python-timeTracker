import os
import sys
from sqlalchemy import Column, Interval, String, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from datetime import timedelta
Base = declarative_base()


class Program(Base):
    __tablename__ = 'Program'
    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String(250),nullable=False)
    duration = Column(Integer, nullable=False)

# Create engine that stores data in local directory
engine = create_engine('sqlite:///focustracker.db')

# Create all tables in the engine. This is equivalent to "Create Table" in SQL
Base.metadata.create_all(engine)

Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

# Insert a Program in the Program Table
#new_program = Program(name='Opera12', duration=timedelta(hours=2, minutes=30))
#session.add(new_program)
#session.commit()

#for prog in session.query(Program):
#    print(prog.name, prog.duration)