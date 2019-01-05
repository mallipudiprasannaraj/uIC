from flask import Flask, render_template
from flask import request, redirect, jsonify, url_for, flash
from sqlalchemy import create_engine, asc
from sqlalchemy.orm import sessionmaker
from camdatabase import Base,UserData, Brand, ModelName
from flask import session as login_session
import random
import string

from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
from flask import make_response
import requests

app = Flask(__name__)

CLIENT_ID = json.loads(
    open('client_secret.json', 'r').read())['web']['client_id']
APPLICATION_NAME = "Digital Camera world Application"


''' Connect to Database and create database session'''
engine = create_engine('sqlite:///camcatalog.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()
''' Create anti-forgery state token'''


@app.route('/login')
def showLogin():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in xrange(32))
    login_session['state'] = state
    ''' return "The current session state is %s" % login_session['state']'''
    return render_template('login.html', STATE=state)

'''
gconnect check client access token with project json file,
and validate user Login
'''
@app.route('/gconnect', methods=['POST'])
def gconnect():
    ''' Validate state token'''
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    ''' Obtain authorization code'''
    code = request.data

    try:
        ''' Upgrade the authorization code into a credentials object'''
        oauth_flow = flow_from_clientsecrets('client_secret.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    ''' Check that the access token is valid.'''
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
    ''' If there was an error in the access token info, abort.'''
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    ''' Verify that the access token is valid for this app.'''
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        print "Token's client ID does not match app's."
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps(
            'Current user is already connected.'
            ), 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    ''' Store the access token in the session for later use.'''
    login_session['access_token'] = credentials.access_token
    login_session['gplus_id'] = gplus_id
    ''' Get user info'''
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    #data = answer.json()
    data=json.loads(answer.txt)

    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    #login_session['email'] = data['email']

    #login_session['provider'] = 'google'

    ''' See if a user exists, if it doesn't make a new one '''
    user_id = getUserID(login_session['username'])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id
    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    flash("you are now logged in as %s" % login_session['username'])
    print "done!"
    return output
'''def createUser(login_session):
    session = DBSession()
    newUser = user(username=login_session['name'], email=login_session[
                   'email'], picture=login_session['picture'])
    session.add(newUser)
    session.commit()
    user = session.query(User).filter_by(email=login_session['email']).one()
    session.close()
    return user.id


def getUserInfo(user_id):

    session = DBSession()
    user = session.query(User).filter_by(id=user_id).one()
    session.close()
    return user


def getUserID(email):
    try:
        session = DBSession()
        user = session.query(User).filter_by(email=name).one()
        session.close()
        return user.id
    except:
        return None'''


''' DISCONNECT - Revoke a current user's token and reset their login_session'''

'''
@app.route('/logout')
def gdisconnect():
     Only disconnect a connected user.'''
    '''access_token = login_session.get('access_token')
    print(access_token)
    if access_token is None:
        response = make_response(
            json.dumps('Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % access_token
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    if result['status'] == '200':
         Reset the user's sesson. '''
        '''del login_session['access_token']
        del login_session['gplus_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']
        del login_session['user_id']'''

        '''response = make_response(json.dumps('Successfully disconnected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        flash('Successfully Logged Out')
        return redirect('/')
    else:'''
        ''' For whatever reason, the given token was invalid. '''
    '''    response = make_response(
            json.dumps('Failed to revoke token for given user.', 400))
        response.headers['Content-Type'] = 'application/json'
        return response'''
''' To See All Brands '''
''' localhost:5000/ '''
''' localhost:5000/brand '''
@app.route('/')
@app.route('/brand')
def showBrands():
    try:
        session = DBSession()
        brands = session.query(Brand).order_by(asc(Brand.name)).all()
        if not brands:
            '''flash message'''
            flash("No Brands to show.")
        session.close()
        return render_template(
            'show_Brand.html',
            brands=brands,
            cur_user=login_session)
    except Exception as E:
        print(E)


''' To Add New Brand '''
''' localhost:5000/brand/new '''


@app.route('/brand/new', methods=['GET', 'POST'])
def newBrand():
    if 'username' in login_session:
        if request.method == 'POST':
            newBrd = Brand(
                name=request.form['name'],
                user_id=login_session['user_id'])
            session = DBSession()
            session.add(newBrd)
            session.commit()
            '''flash message'''
            flash(newBrd.name + "Brand successfully added.")
            session.close()
            return redirect('/')
        else:
            return render_template('newBrand.html', cur_user=login_session)
    else:
        '''flash message'''
        flash("Login to Proceed !")
        return redirect('/login')


''' To Edit Particular Brand '''
''' localhost:5000/brand/brand_id/edit '''


@app.route('/brand/<int:brand_id>/edit', methods=['GET', 'POST'])
def editBrand(brand_id):
    session = DBSession()
    editBrd = session.query(Brand).filter_by(id=brand_id).one()
    if 'username' in login_session:
        if login_session['user_id'] == editBrd.user_id:
            before = editBrd.name
            if request.method == 'POST':
                editBrd.name = request.form['name']
                session.add(editBrd)
                session.commit()
                '''flash message'''
                flash(
                    before + " Brand successfully changed as " + editBrd.name)
                session.close()
                return redirect('/')
            else:
                return render_template(
                    'editBrand.html',
                    br=editBrd,
                    cur_user=login_session)
        else:
            '''flash message'''
            flash("Permissions deniend !")
            return redirect('/')
    else:
        '''flash message'''
        flash("Login to Proceed !")
        return redirect('/login')


''' To Delete Particular Brand '''
''' localhost:5000/brand/brand_id/delete '''


@app.route('/brand/<int:brand_id>/delete', methods=['GET', 'POST'])
def deleteBrand(brand_id):
    session = DBSession()
    deleteBr = session.query(Brand).filter_by(id=brand_id).one()
    if 'username' in login_session:
        if login_session['user_id'] == deleteBrd.user_id:
            deleteMoDU = session.query(model).filter_by(brand_id=brand_id).all()
            if request.method == 'POST':
                for i in deleteMoDU:
                    print("deleting ", i.id)
                    session.delete(i)
                    session.commit()
                session.delete(deleteBrd)
                session.commit()
                '''flash message'''
                flash(deleteBrd.name + " Brand, successfully deleted.")
                session.close()
                return redirect('/')
            else:
                return render_template(
                    'deleteBrand.html',
                    br=deleteBrd,
                    cur_user=login_session)
        else:
            '''flash message'''
            flash("Permissions deniend !")
            return redirect('/')
    else:
        '''flash message'''
        flash("Login to Proceed !")
        return redirect('/login')


''' To See All Models '''
''' localhost:5000/brand/brand_id/model/ '''
''' localhost:5000/brand/brand_id/ '''


@app.route('/brand/<int:brand_id>/model')
@app.route('/brand/<int:brand_id>/')
def showModels(brand_id):
    try:
        session = DBSession()
        brand = session.query(Brand).filter_by(id=brand_id).one()
        model = session.query(ModelName).filter_by(
            brand_id=brand.id).order_by(
                ModelName.name).all()
        if not model:
            '''flash message'''
            flash("No Models to show.")
        session.close()
        return render_template(
            'showModels4User.html',
            brand=brand,
            model=model,
            cur_user=login_session)
    except Exception as E:
        print(E)


''' To Add New Model '''
''' localhost:5000/brand/brand_id/model/model_id/new '''


@app.route('/brand/<int:brand_id>/model/new', methods=['GET', 'POST'])
def newModel(brand_id):
    if 'username' in login_session:
        session = DBSession()
        brand = session.query(Brand).filter_by(id=brand_id).one()
        if login_session['user_id'] == brand.user_id:
            if request.method == 'POST':
                brand = session.query(Brand).filter_by(id=brand_id).one()
                newMo = ModelName(
                    modelname=request.form['modelname'],
                    brands=request.form['brands'],
                    modelnumber=request.form['modelnumber'],
                    ctype=request.form['ctype'],
                    user_id=login_session['user_id'],
                    brand_id=brand_id,
                    colors=request.form['colors'],
                    wifi=request.form['wifi'],
                    facedetection=request.form['facedetection'],
                    pixels=request.form['pixels'],
                    builtinflash=request.form['builtinflash'],
                    videoformat=request.form['videoformat'],
                    price=request.form['price'],

                    description=request.form['des'])
                session.add(newMo)
                session.commit()
                '''flash message'''
                flash(
                    newMo.name + " Model, successfully added to " +
                    brand.name)
                session.close()
                return redirect(url_for('showModels', brand_id=brand_id))
            else:
                return render_template(
                    'newModel.html',
                    brand=brand,
                    cur_user=login_session)
        else:
            '''flash message'''
            flash("Permissions deniend !")
            return redirect('/')
    else:
        '''flash message'''
        flash("Login to Proceed !")
        return redirect('/login')


''' To Edit Particular Model '''
''' localhost:5000/brand/brand_id/model/model_id/edit '''


@app.route(
    '/brand/<int:brand_id>/model/<int:model_id>/edit',
    methods=['GET', 'POST'])
def editModel(brand_id, model_id):
    if 'username' in login_session:
        session = DBSession()
        brand = session.query(Brand).filter_by(id=brand_id).one()
        editMod = session.query(ModelName).filter_by(id=model_id).one()
        if login_session['user_id'] == brand.user_id:
            if request.method == 'POST':
                editMod.modelname = request.form['modelname']
                editMod.brands = request.form['brands']
                editMod.modelnumber = request.form['modelnumber']
                editMod.ctype = request.form['ctype']
                editMod.colors = login_session['colors']
                editMod.brand_id = brand_id
                editMod.wifi = request.form['wifi']
                editMod.facedetection = request.form['facedetection']
                editMod.pixels = request.form['pixels']
                editMod.builtinflash = request.form['builtinflash']
                editMod.videoformat = request.form['videoformat']

                editMod.price = request.form['price']
                editMod.description = request.form['des']
                session.add(editMod)
                session.commit()
                '''flash message'''
                flash("Successfully Changes made for " + editMod.name+" Model")
                session.close()
                return redirect(url_for('showModels', brand_id=brand_id))
            else:
                return render_template(
                    'editModel.html', brand=brand,
                    model=editMod, cur_user=login_session)
        else:
            '''flash message'''
            flash("Permissions deniend !")
            return redirect('/')
    else:
        '''flash message'''
        flash("Login to Proceed !")
        return redirect('/login')


''' To Delete Particular Model '''
''' localhost:5000/brand/brand_id/model/model_id/delete '''


@app.route(
    '/brand/<int:brand_id>/model/<int:model_id>/delete',
    methods=['POST', 'GET'])
def deleteModel(brand_id, model_id):
    if 'username' in login_session:
        session = DBSession()
        brand = session.query(Brand).filter_by(id=brand_id).one()
        if login_session['user_id'] == brand.user_id:
            deleteMod = session.query(ModelName).filter_by(
                id=model_id).filter_by(brand_id=brand_id).one()
            if request.method == 'POST':
                session.delete(deleteMo)
                session.commit()
                '''flash message'''
                flash(deleteMod.name + " Model, Successfully deleted.")
                session.close()
                return redirect(url_for(
                    'showModels', brand_id=brand_id))
            else:
                return render_template(
                    'deleteModel.html', brand=brand,
                    model=deleteMod, cur_user=login_session)
        else:
            '''flash message'''
            flash("Permissions deniend !")
            return redirect('/')
    else:
        '''flash message'''
        flash("Login to Proceed !")
        return redirect('/login')


''' To See Particular Model Specifications '''
''' localhost:5000/brand/brand_id/model/model_id/specifications '''


@app.route(
    '/brand/<int:brand_id>/model/<int:model_id>/specifications',
    methods=['POST', 'GET'])
def showSpecificationsOfModel(brand_id, model_id):
    session = DBSession()
    brand = session.query(Brand).filter_by(id=brand_id).one()
    details = session.query(ModelName).filter_by(
        id=model_id).filter_by(brand_id=brand.id).one()
    session.close()
    return render_template(
            'SpecificationsOfModel.html',
            brand=brand, model=details,
            cur_user=login_session)


''' JSON END API's'''
''' returns all models of particular brand as JSON object '''


@app.route('/brand/<int:brand_id>/JSON')
def BrandModelsJSON(brand_id):
    session = DBSession()
    models = session.query(ModelName).filter_by(brand_id=brand_id).all()
    session.close()
    return jsonify(brand=[i.serialize for i in models])


''' returns particular Model as JSON object '''


@app.route('/brand/<int:brand_id>/model/<int:model_id>/JSON')
def ModelsJSON(brand_id, model_id):
    session = DBSession()
    brand = session.query(Brand).filter_by(id=brand_id).one()
    model = session.query(ModelName).filter_by(id=model_id).one()
    session.close()
    return jsonify(model=model.serialize)


''' default constructor '''
if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
