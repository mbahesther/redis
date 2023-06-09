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
    r.set('test', 'testing')
    return jsonify(msg="hello")


@app.route('/rediss', methods=['GET', 'POST'])
def rediss():
    user = 'esther'
    response = {
        'name':'esther',
        'age':'16',
        'designation':'software engineer',
        'hobbies':'sleeping'
    }
    r.setex(f"BV{user}", timedelta(minutes=4), value=json.dumps(response))
    return jsonify(msg= 'Redis is saved')


@app.route('/retrieve', methods=['GET', 'POST'])
def retrieve():
        user = 'esther'
        doja_cache = r.get(f"BV{user}")
        if doja_cache is None:
             return jsonify(msg = "cached expired or not cached")
        
        response = json.loads(doja_cache)

        return jsonify(msg=response)

# mydb = mysql.connector.connect(**config)
# mydb.close()
                
      
#             mydb.close()    
#             # print(type(category))
#             ca = json.dumps(category)
#             r.set("cat", ca)
#             pr= r.get("cat")
#             print(pr)
#             return jsonify(categories=pr),200      
    

if __name__ == '__main__':
     app.run(host='0.0.0.0', port=4000)
