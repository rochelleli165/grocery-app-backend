import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

# Fetch the service account key JSON file contents
cred = credentials.Certificate('/Users/rochelleli/Code/coupon test/firebasics-ca388-firebase-adminsdk-wypkc-fcc49e378d.json')

# Initialize the app with a service account, granting admin privileges
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://firebasics-ca388-default-rtdb.firebaseio.com'
})

def getTranslation(ingredient):
    ref = db.reference(f'translations/{ingredient}')
    t = ref.get()
    if t:
        return t
    return

def setRecipe(recipeTitle, recipeLink, ingredients):
    # As an admin, the app has access to read and write all data, regradless of Security Rules
    ref = db.reference('recipes')

    new_ref = ref.push()

    new_ref.update({
        'recipe-title': recipeTitle,
        'recipe-link': recipeLink,
        'ingredients': ingredients
    })
    
def getAllRecipes():
    ref = db.reference('recipes')
    return ref.get()

def updateTranslations(req):
    ref = db.reference('translations')
    ref.update(req)

def addStore(req):
    ref = db.reference('stores')
    new_ref = ref.push()
    new_ref.set({
        'name': req['name'],
        'address': req['address'],
        'recent-ad': "",
    })
    return new_ref

def postAd(req):
    ref = db.reference(f'ads/{req['id']}')   
    new_ref = ref.push()
    new_ref.set({
        'date': req['date'],
        'items': req['items']
    })

    store_ref = db.reference(f'stores/{req['id']}')
    store_ref.update({
        'recent-ad': new_ref
    })

def subscribeStore(req):
    ref = db.reference(f'users/{req['id']}/subscriptions')
    ref.update({
       req['store']: True
    })


def getAd(req):
    store_ref = db.reference(f'stores/{req['id']}')
    store = store_ref.get()
    
    ad_ref = db.reference(f'ads/{req['id']}/{store['recent-ad']}') 
    return  {
        'store-name': store['name'],
        'store-address': store['address'],
        'items': ad_ref.get()
    }

def getSubscriptions(req):
    ref = db.reference(f'users/{req['id']}/subscriptions')
    s = ref.get()
    return s

def getPantryItems(req):
    ref = db.reference(f'users/{req['id']}/pantry')
    p = ref.get()
    return p

def addToPantry(req):
    ref = db.reference(f'users/{req['id']}/pantry')
    ref.update(
        req['pantry']
    )