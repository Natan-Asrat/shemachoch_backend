from rest_framework.authentication import BaseAuthentication
from . import exceptions
from django.contrib.auth import get_user_model
import firebase_admin
from firebase_admin import credentials, auth
from django.conf import settings

cred = credentials.Certificate({
        "type" : settings.FIREBASE_ACCOUNT_TYPE,
        "project_id" : settings.FIREBASE_PROJECT_ID,
        "private_key_id" : settings.FIREBASE_PRIVATE_KEY_ID,
        "private_key" : settings.FIREBASE_PRIVATE_KEY.replace('\\n', '\n'),
        "client_email" : settings.FIREBASE_CLIENT_EMAIL,
        "client_id" : settings.FIREBASE_CLIENT_ID,
        "auth_uri" : settings.FIREBASE_AUTH_URI,
        "token_uri" : settings.FIREBASE_TOKEN_URI,
        "auth_provider_x509_cert_url" : settings.FIREBASE_AUTH_PROVIDER_X509_CERT_URL,
        "client_x509_cert_url" : settings.FIREBASE_CLIENT_X509_CERT_URL
})
default_app = firebase_admin.initialize_app(cred)
class FirebaseAuthentication(BaseAuthentication):
    def authenticate(self, request):
        token = request.headers.get('Authorization')
        if not token:
            return None
        
        try:
            decoded_token = auth.verify_id_token(token)
            print(decoded_token)

            phone = decoded_token["phone_number"]
        except Exception as e:
            print(e)
            return None
        User = get_user_model()
        print(phone)
        user = User.objects.get(phoneNumber=phone)
        print(user.first_name)
        return user, None
