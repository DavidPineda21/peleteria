from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.models import User,Group
from django.db import connections
from django.contrib.auth.hashers import check_password
from django.contrib import messages

class CustomAuthBackend(BaseBackend):
    def authenticate(self, request, idusuario=None, contrasena=None, **kwargs):
        try:
            #print(f"Authenticating user: {idusuario}")

            # Using the default database
            with connections['default'].cursor() as cursor:
                # Ensure correct table and column names
                query = """
                    SELECT 
    u.idusuario, 
    u.contrasena, 
    u.activo, 
    u.nombre AS nombre,  -- Concatenate and uppercase the user's name
    u.cambiocontrasena
FROM 
    tblusuarios u
WHERE 
    u.idusuario = %s
                """
                cursor.execute(query, [idusuario])
                result = cursor.fetchone()
                #print(f"Database result: {result}")

                if result:
                    db_idusuario, db_contrasena,db_activo, db_nombre, db_cambiocontrasena = result
                    # print(f"User found in DB: {db_idusuario} {db_contrasena} {contrasena}, now checking password...")

                    # Verify the password
                    if self.check_password(contrasena, db_contrasena):
                        if db_activo == 'ACTIVO':
                            # print(f"Password matched for user: {db_idusuario}")
                            request.session['usuario']=db_idusuario
                            request.session['nombre']=db_nombre
                            request.session['cambiocontrasena']=db_cambiocontrasena

                            nombre = request.session.get('nombre', '')
                            partes = nombre.split()

                            iniciales = ''
                            if len(partes) >= 2:
                                iniciales = partes[0][0] + partes[1][0]
                            elif len(partes) == 1:
                                iniciales = partes[0][0]

                            request.session['iniciales'] = iniciales.upper()

                            # Return a dummy user if the user is not in Django's User model
                            try:
                                user = User.objects.get(username=idusuario)
                            except User.DoesNotExist:
                                # Create a new Django User if needed or handle as appropriate
                                user = User(username=idusuario)
                                user.save()
                                #print(f"Created new Django User: {idusuario}")
                            return user
                        else:
                            messages.error(request, 'La cuenta se encuentra inactiva')
                    else:
                        messages.error(request, 'Usuario o contraseña ingresada incorrecta')
                else:
                    messages.error(request, 'Usuario o contraseña ingresada incorrecta')
        except Exception as e:
            messages.error(request, f"Error durante autenticacion. Por favor, intente nuevamente.")  # Add an error message
        return None


    def check_password(self, password, hashed_password):
        """
        Check if the provided password matches the hashed password.
        """
        # Use PostgreSQL's crypt function to hash the provided password and compare
        with connections['default'].cursor() as cursor:
            query = """
                SELECT crypt(%s, %s) = %s
            """
            cursor.execute(query, [password, hashed_password, hashed_password])
            return cursor.fetchone()[0]


    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
