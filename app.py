'''
===================================================================================================================================

MODELING PERFORMANCE AND EMISSION CHARACTERISTICS OF \
BIODIESEL FUELED ENGINE FOR OPTIMAL OPERATION WITH PYTHON

VITALIS KIBIWOT NGELECHEI

===================================================================================================================================
'''
# Libraries and modulles
from flask import Flask
from flask import render_template, request
import scipy.optimize as optimize
from os import system
import numpy as np
import sympy as sy
import datetime
import time
app = Flask(__name__)


# globals and constants
html_output = {}
form_fields = {}
errors = {}
random_id = {}
raw_output = []


@app.route('/', methods=['GET', 'POST'])
def main():

    # try:
    errors.clear()
    if request.method == 'GET':
        html_output.clear()
        # form_fields.clear()
        # print(time.mktime(datetime.datetime.now().timetuple()) * 1000)
    elif request.method == 'POST':
        raw_output.clear()
        #  input variables
        n = float(request.form['n'])  # speed (r.p.m.)
        w = float(request.form['w'])  # mass /load Kg
        cv = float(request.form['cv'])  # calorific value
        m = float(request.form['m'])  # mass of fuel consumed
        v = float(request.form['v'])  # fuel viscosity
        b = float(request.form['b'])  # blend Ratio (%)

        # constants a1,b1,c1 .... an,bn,cn

        # BPE
        a1 = float(request.form['a1'])
        b1 = float(request.form['b1'])
        c1 = float(request.form['c1'])

        # BP
        a2 = float(request.form['a2'])
        b2 = float(request.form['b2'])
        c2 = float(request.form['c2'])

        # CO EMISSION
        a3 = float(request.form['a3'])
        b3 = float(request.form['b3'])
        c3 = float(request.form['c3'])

        # NO EMISSION
        a4 = float(request.form['a4'])
        b4 = float(request.form['b4'])
        c4 = float(request.form['c4'])

        # update random id
        random_id.update(
            {"current": time.mktime(datetime.datetime.now().timetuple()) * 1000})

        # update form fields
        form_fields.update(
            {"n": n, "w": w, "cv": cv, "m": m, "v": v, "b": b, "a1": a1, "a2": a2, "a3": a3, "a4": a4, "b1": b1, "b2": b2, "b3": b3, "b4": b4, "c1": c1, "c2": c2, "c3": c3, "c4": c4})

        # computations
        x1 = b/100
        x2 = cv/(v*n)
        x3 = m/(w*n)
        initial_val = [x1, x2, x3]

        # Break thermal Efficiency
        def bte(params):
            # print(params)
            x1, x2, x3 = params
            return (0.9508*pow(x1, a1)*pow(x2, b1)*pow(x3, c1))
            # return (0.9508*pow(x1, -0.0020)*pow(x2, -0.0070)*pow(x3, -0.9970))

        bte_result = optimize.minimize(bte, initial_val)

        if bte_result.success:
            fitted_params = bte_result.x
            opt1 = fitted_params[0]
            raw_output.append(opt1)
            html_output.update(
                {"bte": str(round(fitted_params[0], 5)) + str(' % \n')})

        # Bp
        def bp(params):
            # print(params)
            x1, x2, x3 = params
            return 100.7861*pow(x1, a2)*pow(x2, b2)*pow(x3, c2)
            # return 100.7861*pow(x1, -0.6711)*pow(x2, -0.1098)*pow(x3, -0.0458)
        bp_result = optimize.minimize(bp, initial_val)
        print(bp_result)
        if bp_result.success:
            fitted_params = bp_result.x
            opt2 = fitted_params[0]
            raw_output.append(opt2)
            html_output.update(
                {"bp": str(round(fitted_params[0], 4)) + str(' % \n')})

        # No emission
        def NO(params):
            # print(params)
            x1, x2, x3 = params
            return 1.453*pow(x1, a3)*pow(x2, b3)*pow(x3, c3)
            # return 1.453*pow(x1, -2.34)*pow(x2, -0.6305)*pow(x3, -0.739)

        no_result = optimize.minimize(NO, initial_val)
        if no_result.success:
            fitted_params = no_result.x
            opt3 = fitted_params[0]
            raw_output.append(opt3)
            html_output.update(
                {"no": str(fitted_params[0]) + str(' % \n')})

        # CO Emissions
        def CO(params):
            # print(params)
            x1, x2, x3 = params
            return 7.937*pow(x1, a4)*pow(x2, b4)*pow(x3, c4)
            # return 7.937*pow(x1, -1.08)*pow(x2, -1.635)*pow(x3, -0.142)
        co_result = optimize.minimize(CO, initial_val)
        if co_result.success:
            fitted_params = co_result.x
            opt4 = fitted_params[0]
            raw_output.append(opt4)
            html_output.update(
                {"co": str(round(fitted_params[0], 4)) + str(' % \n')})

        # optimized blend ratio

        if html_output:
            html_output.update(
                {"obr": str(np.mean(raw_output)) + str(' % \n')})
        # except:
        #     print('errors')
        #     errors.update(
        #         {"message": "please fill all fields correctly and try again"})

    return render_template('index.html', random_id=random_id, title='calculate', errors=errors, heading="Optimization model Model", result=html_output, form_fields=form_fields)
    main()
