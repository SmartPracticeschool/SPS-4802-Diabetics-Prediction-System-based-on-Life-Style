from flask import Flask,render_template,request,url_for
import requests
import urllib3, json
app=Flask(__name__)
@app.route('/',methods=['POST','GET'])
def hello():
    if request.method=='POST':
        preg=request.form['a']
        glc=request.form['b']
        bp=request.form['c']
        skt=request.form['d']
        ins=request.form['e']
        bmi=request.form['f']
        dpf=request.form['g']
        age=request.form['h']
        print(age,glc,bp,skt,ins,bmi,dpf,age)
        try:
            preg=int(preg)
            glc=int(glc)
            bp=int(bp)
            skt=int(skt)
            ins=int(ins)
            bmi=float(bmi)
            dpf=float(dpf)
            age=float(age)
        except:
            return render_template('data.html',err_msg='Enter Valid Data')
        url = "https://iam.cloud.ibm.com/identity/token"
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        data = "apikey=" + 'QvJzvnM7aA6NO735Xmoy7XwhOaFV2ipS2s_T8leapztL' + "&grant_type=urn:ibm:params:oauth:grant-type:apikey"
        IBM_cloud_IAM_uid = "bx"
        IBM_cloud_IAM_pwd = "bx"
        response = requests.post(url, headers=headers, data=data, auth=(IBM_cloud_IAM_uid, IBM_cloud_IAM_pwd))
        print(response)
        iam_token = response.json()["access_token"]
        header = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + iam_token}
        payload_scoring = {"input_data": [
            {"fields": ["Pregnancies","Glucose","BloodPressure","SkinThickness","Insulin","BMI","DiabetesPedigreeFunction","Age"],
             "values": [[preg,glc,bp,skt,ins,bmi,dpf,age]]}]}
        response_scoring = requests.post(
            'https://us-south.ml.cloud.ibm.com/ml/v4/deployments/51302426-6bb3-4183-8d39-8b495cb7f036/predictions?version=2020-10-20',
            json=payload_scoring, headers=header)
        print(response_scoring)
        a = json.loads(response_scoring.text)
        print(a)
        pred = a['predictions'][0]['values'][0][0]
        return render_template('index.html', result=pred)
    else:
        return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)