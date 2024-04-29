import mysql.connector
from flask import Flask, request

app = Flask(__name__)

db = mysql.connector.connect(
    host='localhost', user='root', password='12345', database='sri', auth_plugin='mysql_native_password')
cursor = db.cursor()


@app.route('/users', methods=['GET'])
def users():
    cursor.execute("SELECT * FROM table1")
    users = cursor.fetchall()
    user_list = [{'sno': user[0], 'name': user[1], 'city': user[2]} for user in users]
    return {'users': user_list}


@app.route('/create_users', methods=['POST'])
def create_user():
    new_user = request.json
    cursor.execute("INSERT INTO table1 (sno, name, city) VALUES (%s, %s, %s)",
                   (new_user['sno'], new_user['name'], new_user['city']))
    db.commit()
    new_user_sno = cursor.lastrowid  # Corrected attribute name
    return {'message': 'User successfully created', 'user_sno': new_user_sno}


# @app.route('/update_users/<int:user_sno>', methods=['PUT'])
# def update_users(user_sno):
#     updated_user_data = request.json
#     cursor.execute(" update table1 sno=%s, name =%s ,city =%s",
#                    (updated_user_data['sno'], updated_user_data['name'], updated_user_data['city']))
#     db.commit()
#     if cursor.rowcount > 0:
#         return {'message': f'user with sno {user_sno}  updated successfully'}
#     else:
#         return {'error': 'user not found'}, 404


@app.route('/update_users/<int:user_sno>', methods=['PUT'])
def update_users(user_sno):
    updated_user_data = request.json
    sno = updated_user_data.get('sno', None)
    name = updated_user_data.get('name', None)
    city = updated_user_data.get('city', None)

    if sno is not None and name is not None and city is not None:
        cursor.execute("UPDATE table1 SET sno=%s, name=%s, city=%s WHERE sno=%s",
                       (sno, name, city, user_sno))
        db.commit()
        if cursor.rowcount > 0:
            return {'message': f'user with sno {user_sno} updated successfully'}
        else:
            return {'error': 'user not found'}, 404
    else:
        return {'error': 'invalid data provided'}, 400




@app.route('/delete_users/<int:user_sno>', methods=['DELETE'])
def delete_users(user_sno):
    # No need to check if the request is JSON, as data is in the URL
    cursor.execute("DELETE FROM table1 WHERE sno=%s", (user_sno,))
    db.commit()
    if cursor.rowcount > 0:
        return {'message': f'User with Sno {user_sno} deleted successfully'}
    else:
        return {'error': 'User not found'}, 404



if __name__ == "__main__":
  app.run(debug=True)
