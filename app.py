from run import *

@app.route('/index', methods=['GET', 'POST'])
def chat():
    r.set("msg", "hello word")
    msgg = r.get("msg")
    print(msgg)
    r.set("mofe", b'{"boy":"girl", "boy":"girl"}',30)
    # print("testing")
    m = r.get("mofe")
    print(m)
    return jsonify(msg="hello")


mydb = mysql.connector.connect(**config)
mydb.close()

# specific resturant to get all their category
@app.route('/api/merchant/category', methods=['GET'])
@jwt_required()
def food_category():
    try:
        current_restaurant = get_jwt_identity()
        restaurant_id = current_restaurant[0]
        mydb = mysql.connector.connect(**config)
        my_cursor = mydb.cursor(buffered=True)
        my_cursor.execute('SELECT cat_id, LOWER(category) FROM food_category WHERE restaurant_id =%s', [restaurant_id])
        query = my_cursor.fetchall()      
        if query:
            category = []
            for result in query:         
                category.append({
                    'id':result[0],
                    'category_name'  :result[1]                
                } )
            my_cursor.close()
            mydb.close()    
            # print(type(category))
            ca = json.dumps(category)
            r.set("cat", ca)
            pr= r.get("cat")
            print(pr)
            return jsonify(categories=pr),200      
        else:
            my_cursor.close()
            mydb.close()
            return jsonify({'categories':query}),200  
    except Exception as e:
        my_cursor.close()
        mydb.close()
        return jsonify(msg=e),403 
    

if __name__ == '__main__':
     app.run(host='0.0.0.0', port=5000)
