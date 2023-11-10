from flask import Flask, request, jsonify
from flask_cors import CORS
from gui import classify
from Main import main
app = Flask(__name__)

cors = CORS(app)
@app.route('/getdata',methods=["POST","GET"])
def getMe():
    if(request.method == 'POST'): 
        data=request.get_json()
        item=data.get('name')
        item='C:/number-plate-recognition-code/carDB/'+item
        result=classify(item)
        print(result)
        return result
    if(request.method=='GET'):
        result=main()
        print(result)
        return result
    
if __name__ == "__main__":
     app.run(debug=True)