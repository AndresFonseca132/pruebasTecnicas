from .entities.User import User
from werkzeug.security import generate_password_hash

class ModelUser():

    @classmethod
    def login(self, db, user):
        try:
            cursor=db.connection.cursor()
            sql="""SELECT ID, name, last_name, email,  password, document, super_user FROM user 
                    WHERE email = '{}'""".format(user.email)
            cursor.execute(sql)
            row = cursor.fetchone()
            if row != None:
                user = User(row[0], row[1], row[2], row[3], User.check_password(row[4], user.password), row[5],  row[6])
                return user
            else:
                return None
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def get_by_ID(self, db, ID):
        try:
            cursor = db.connection.cursor()
            sql = "SELECT ID, name, last_name, email, document, super_user FROM user WHERE ID = {}".format(ID)
            cursor.execute(sql)
            row = cursor.fetchone()
            if row != None:
                return User(row[0], row[1], row[2], row[3], None, row[4], row[5])
            else:
                return None
        except Exception as ex:
            raise Exception(ex)
        
    
    
    @classmethod
    def create(cls, db, user):
        try:
            cursor = db.connection.cursor()
            hashed_password = generate_password_hash(user.password)
            sql = "INSERT INTO user (name, last_name, email, password, document, super_user) VALUES ('{}', '{}', '{}', '{}', '{}', '{}')".format(user.name, user.last_name, user.email, hashed_password, user.document, user.super_user)
            cursor.execute(sql)
            db.connection.commit()
            return True
        except Exception as ex:
            raise Exception(ex)