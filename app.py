import pickle
import numpy as np
from flask import Flask,escape,request, render_template
from sklearn.preprocessing import StandardScaler
scaler = StandardScaler()


app = Flask(__name__)
model = pickle.load(open('dt_model10.pkl', 'rb'))


@app.route('/')
def home():
    return render_template("prediction-1.html", **locals())


@app.route('/predict', methods=['POST', 'GET'])
def predict():
    result=''
    if request.method == 'POST':
        Gender = request.form['Gender']
        loan_type = request.form['loan_type']
        credit_type = request.form['credit_type']
        income = float(request.form['income'])
        rate_of_interest = float(request.form['rate_of_interest'])
        loan_amount = float(request.form['loan_amount'])
        LTV = float(request.form['LTV'])
        dtir1 = float(request.form['dtir1'])
        age=float(request.form['age'])

        Credit_Score=int(request.form['Credit_Score'])
        term=float(request.form['term'])
        if (Gender == "Male"):
            Male = 1
            Female = 0
            Joint = 0
            Sexnotavailable = 0
        elif (Gender == "Female"):
            Male = 0
            Female = 1
            Joint = 0
            Sexnotavailable = 0
        elif (Gender == 'Joint'):
            Male = 0
            Female = 0
            Joint = 1
            Sexnotavailable = 0
        elif (Gender == 'Sexnotavailable'):
            Male = 0
            Female = 0
            Joint = 0
            Sexnotavailable = 1
        else:
            Male = 0
            Female = 0
            Joint = 0
            Sexnotavailable = 0

        if (loan_type == "loan_type_type1"):
            loan_type_type1 = 1
            loan_type_type2 = 0
            loan_type_type3 = 0
        elif (loan_type == "loan_type_type2"):
            loan_type_type1 = 0
            loan_type_type2 = 1
            loan_type_type3 = 0
        elif (loan_type == "loan_type_type3"):
            loan_type_type1 = 0
            loan_type_type2 = 0
            loan_type_type3 = 1
        else:
            loan_type_type1 = 0
            loan_type_type2 = 0
            loan_type_type3 = 0

        if (credit_type == "credit_type_CIB"):
            credit_type_CIB = 1
            credit_type_CRIF = 0
            credit_type_EQUI = 0
            credit_type_EXP = 0
        elif (credit_type == "credit_type_CRIF"):
            credit_type_CIB = 0
            credit_type_CRIF = 1
            credit_type_EQUI = 0
            credit_type_EXP = 0
        elif (credit_type == "credit_type_EQUI"):
            credit_type_CIB = 0
            credit_type_CRIF = 0
            credit_type_EQUI = 1
            credit_type_EXP = 0
        elif (credit_type == "credit_type_EXP"):
            credit_type_CIB = 0
            credit_type_CRIF = 0
            credit_type_EQUI = 0
            credit_type_EXP = 1
        else:
            credit_type_CIB = 0
            credit_type_CRIF = 0
            credit_type_EQUI = 0
            credit_type_EXP = 0




        rate_of_interest_log = np.log(rate_of_interest)
        income_log = np.log(income)
        term_log=np.log(term)
        loan_amount_log = np.log(loan_amount)
        LTV_log = np.log(LTV)
        dtir1 = np.log(dtir1)

        feature = scaler.fit_transform([[ loan_amount_log, LTV_log, dtir1, Male, Female, Joint, Sexnotavailable,age,
                                     loan_type_type1, loan_type_type2, loan_type_type3, credit_type_CIB,
                                     credit_type_CRIF, credit_type_EQUI, credit_type_EXP,income_log,rate_of_interest,term_log]])

        prediction = model.predict(feature)[0]
        if (prediction== 0):
           prediction = "not defaulted"
        elif (prediction== 1):
            prediction = "defaulted"

        else:
            prediction="Nil"
        return render_template("prediction-1.html", prediction_text="loan status is {}".format(prediction), **locals())
    else:
        return render_template("prediction-1.html", **locals())


if __name__ == "__main__":
    app.run(debug=True)

