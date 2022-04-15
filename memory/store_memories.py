import sqlite3
import os


# Retrieve sqlite file.
__location__ = os.path.realpath(
  os.path.join(os.getcwd(), os.path.dirname(__file__)))
sqlite_file = os.path.join(__location__, 'memories.sqlite')


text_type="TEXT"
table_name = "MEMORY"

#Connect to DB
conn = sqlite3.connect(sqlite_file)
c = conn.cursor()

def database_exists():
  # Returns true if db is found
  return os.stat(sqlite_file).st_size > 0


def store_task(key, raw_memory, coded_memory):
  """
    Function to store a task into memory.
    Tasks are learned procedures from the learning module.
  """
  query = "INSERT INTO {} (NAME,RAW,CODE) \
        VALUES ('{}', '{}', '{}')".format(table_name, key.lower(), raw_memory, coded_memory)
  try:
    c.execute(query)
    conn.commit()
  except Exception as e: print (e)


def recall_all():
  """
    Function to simply print the whole MEMORY table.
  """
  c.execute("SELECT * FROM {}".format(table_name))
  print (c.fetchall())


def recall_memory(memory_name):
  """
    Function to recall a certain memory by NAME column in the MEMORY table.
  """
  c.execute("SELECT * FROM {} WHERE NAME = '{}'".format(table_name, memory_name))
  return c.fetchall()


def init_db():
  """
    The main function creates the table if it run.
    TODO this should be moved to another function.
  """
  # Create SQLite table
  try:
    c.execute("CREATE TABLE {tn} ({t1} UNIQUE, {t2}, {t3});"\
      .format(tn=table_name, t1="NAME", t2="RAW", t3="CODE"))
  except Exception as e: print (e)
  
  #Save
  conn.commit()
  
def close_db():
  conn.close()


"""
Vocabulary/ Tasks:
  Name, Raw, Code 

Personal Pronouns
  Pronoun, Replacement

"""