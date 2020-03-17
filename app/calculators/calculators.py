from flask import Blueprint, render_template, request, redirect
from app.models.models import Recipe

calculators_bp = Blueprint('calculators_bp', __name__,
                             template_folder='templates',
                             static_folder='static', static_url_path='assets')


@calculators_bp.route('/', methods=['GET'])
def calculators_root():
  return redirect('/calculators/bmi')

@calculators_bp.route('/bmi', methods=['GET','POST'])
def calculate_bmi():
  bmi = None

  if request.method == 'POST':
    bmi = None
    height = float(request.form.get("height"))/100
    weight = float(request.form.get("weight"))
    bmi = weight / pow(height, 2)
    bmi = round(bmi, 2)

  return render_template('calculators/bmi.html', bmi=bmi)


@calculators_bp.route('/bmr', methods=['GET', 'POST'])
def calculate_bmr():
  bmr = 0.0
  activity = 1

  if request.method == 'POST':
    height = float(request.form.get('height'))
    weight = float(request.form.get('weight'))
    age = float(request.form.get('age'))
    sex = float(request.form.get('sex'))
    activity = float(request.form.get('activity'))

  #women
    if sex == 1:
      bmr = 655 + (9.563 * weight) + (1.85 * height) - (4.676 * age)
      bmr = bmr * activity
  #men
    else:
      bmr = 66.74 + (13.75 * weight) + (5.003 * height) - (6.755 * age) + 5
      bmr = bmr * activity

  bmr = round(bmr, 2)

  return render_template('calculators/bmr.html', bmr=bmr, activity=activity)

@calculators_bp.route('/bf', methods=['GET', 'POST'])
def calculate_bf():
  bf = 0.0
  d = 0.0

  if request.method == 'POST':
    sex = float(request.form.get('sex'))
    weight = float(request.form.get('weight'))
    waist = float(request.form.get('waist'))

    if sex == 1:
      d = (((4.15 * waist) / 2.54) - (0.082 * weight * 2.2)) - 76.76

    else:
      d = (((4.15 * waist) / 2.54) - (0.082 * weight * 2.2)) - 98.42

    bf = round(d / (weight*2.2) * 100, 2)

  return render_template('calculators/bf.html', bf=bf)
