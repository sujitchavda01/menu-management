from flask import Flask, render_template, request, jsonify
from flask_mysqldb import MySQL

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'menu_management'

mysql = MySQL(app)

def fetch_menu():
    try:
        cur = mysql.connection.cursor()
        cur.execute("SELECT id, name, parent_id FROM menus")
        menus = cur.fetchall()
        cur.close()
    except Exception as e:
        print("Database Error:", e)
        return []

    def build_tree(menu_list, parent_id=None):
        tree = []
        for menu in menu_list:
            if menu[2] == parent_id:
                tree.append({
                    'id': menu[0],
                    'name': menu[1],
                    'children': build_tree(menu_list, menu[0])
                })
        return tree

    return build_tree(menus)

def render_menu(menus):
    html = '<ul>'
    for menu in menus:
        html += f'<li>'
        html += f'<span class="tree-item">{menu["name"]} '
        html += f'<i class="fa fa-edit edit-btn" onclick="editMenu({menu["id"]}, \'{menu["name"]}\')"></i>'
        html += f'<i class="fa fa-trash delete-btn" onclick="deleteMenu({menu["id"]})"></i></span>'
        if "children" in menu and menu["children"]:
            html += '<div class="arrow-down">↓</div>'
            html += render_menu(menu["children"])
        html += '</li>'
    html += '</ul>'
    return html

app.jinja_env.filters['render_menu'] = render_menu

@app.route('/')
def index():
    menus = fetch_menu()
    return render_template('index.html', menus=menus)

@app.route('/get_menus', methods=['GET'])
def get_menus():
    menus = fetch_menu()
    return jsonify(menus)

@app.route('/add_menu', methods=['POST'])
def add_menu():
    data = request.json
    menu_name = data.get('name')
    parent_id = data.get('parent_id')

    if not menu_name:
        return jsonify({'error': 'Menu name is required'}), 400

    parent_id = int(parent_id) if parent_id else None

    try:
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO menus (name, parent_id) VALUES (%s, %s)", (menu_name, parent_id))
        mysql.connection.commit()
        cur.close()
        return jsonify({'success': 'Menu added successfully'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/edit_menu', methods=['POST'])
def edit_menu():
    data = request.json
    menu_id = data.get('id')
    new_name = data.get('name')

    if not menu_id or not new_name:
        return jsonify({'error': 'Menu ID and new name are required'}), 400

    try:
        cur = mysql.connection.cursor()
        cur.execute("UPDATE menus SET name = %s WHERE id = %s", (new_name, menu_id))
        mysql.connection.commit()
        cur.close()
        return jsonify({'success': 'Menu updated successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/delete_menu', methods=['POST'])
def delete_menu():
    data = request.json
    menu_id = data.get('id')

    if not menu_id:
        return jsonify({'error': 'Menu ID is required'}), 400

    try:
        cur = mysql.connection.cursor()
        cur.execute("DELETE FROM menus WHERE id = %s", (menu_id,))
        mysql.connection.commit()
        cur.close()
        return jsonify({'success': 'Menu deleted successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)