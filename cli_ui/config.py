from __future__ import print_function, division

import curses, traceback
from tabulate import tabulate

from sqlalchemy import create_engine
engine = create_engine('sqlite:///alchemy.db', echo=False)    # echo=True to show SQL statements

from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()

from sqlalchemy.orm import sessionmaker
Session = sessionmaker(bind=engine)
session = Session()

