import os.path
import sys
import random
import string

sys.path.append(os.path.join(os.path.dirname(__file__), '.'))

def create_password():
    return 'goiaba10'


def create_super_user(username, email):

    password = create_password()
    try:
        u = User.objects.create_superuser(username,
                                          email,
                                          password,
                                          is_active=True)
        EmailAddress.objects.create(
            user=u, email=email,
            primary=True, verified=True)
        u.set_password(password)
        u.save()
        print ('\nSuperUser:', User.objects.get(is_superuser=True).username)
        print('username: {0} -- password: {1} \n'.format(username, password))

        return u

    except IntegrityError:
        raise ValidationError("An error occurred. Stopping the script")


def create_user(full_name, telegram, username, email, cpf, is_responsible, is_active):

    password = create_password()

    try:
        u = User.objects.create_user(
            full_name=full_name,
            telegram=telegram,
            cpf=cpf,
            is_responsible=is_responsible,
            username=username,
            email=email,
            password=password,
            is_active=is_active,
        )

        print('User: - {0} {1}'.
              format(str(u.first_name), str(u.last_name)))
        print('username: {0}  -- password: {1} \n'.format(username, password))

        return u

    except IntegrityError:
        raise ValidationError("An error occurred. Stopping the script")


def create_plantation(farm, name, responsible, employees):
    try:
        plantation = Plantation.objects.create(
            farm=farm,
            name=name,
            responsible=responsible,
        )
        for e in employees:
            plantation.employees.add(e)
        plantation.save()
        print('Creating plantation of ' + name + ' for farm ' + farm)
        return plantation
    except IntegrityError:
        raise ValidationError("An error occurred. Stopping the script")

def create_reading(parameter):
    for i in range(50):
        Reading.objects.create(
            parameter=parameter, 
            value=randint(2, 40)
        )


def populate():
    print ('\n----------------------')
    print ('Populating Database...')
    print ('----------------------\n')

    create_super_user('admin', 'admin@admin.com')
    
    user_1 = create_user(
        full_name='Geovana Ramos Sousa Silva', 
        telegram='Geovana_RMS', 
        username='geovana',
        email='geovana@email.com',
        cpf='111111111111',
        is_responsible=True,
        is_active=True
    )

    user_2 = create_user(
        full_name='Gabriela Medeiros da Silva', 
        telegram='g_msilva', 
        username='gabriela',
        email='gabriela@email.com',
        cpf='222222222222',
        is_responsible=False,
        is_active=True
    )

    user_3 = create_user(
        full_name='Vinícius Rodrigues Oliveira', 
        telegram='vinicinoliveira', 
        username='vinicius',
        email='vinicius@email.com',
        cpf='33333333333',
        is_responsible=False,
        is_active=False
    )

    user_4 = create_user(
        full_name='Cauê Mateus Oliveira', 
        telegram='oliveiracaue', 
        username='caue',
        email='caue@email.com',
        cpf='44444444444',
        is_responsible=False,
        is_active=False
    )

    user_5 = create_user(
        full_name='Thiago Ribeiro Pereira', 
        telegram='thiagorpereira7', 
        username='thiago',
        email='thiago@email.com',
        cpf='5555555555',
        is_responsible=False,
        is_active=True
    )
    
    plantation_1 = create_plantation('Rancho Bom', 'Milho', user_1, [user_2, user_3, user_4, user_5])
    
    print ('Creating parameters\n')
    par_1 = Parameter.objects.create(
        parameter_type=Parameter.WIND, 
        min_value=10, max_value=12, 
        plantation=plantation_1
    )
    par_2 = Parameter.objects.create(
        parameter_type=Parameter.SOIL_TEMPERATURE, 
        min_value=20, max_value=25, 
        plantation=plantation_1
    )
    par_3 = Parameter.objects.create(
        parameter_type=Parameter.AIR_TEMPERATURE, 
        min_value=25, max_value=30, 
        plantation=plantation_1
    )
    par_4 = Parameter.objects.create(
        parameter_type=Parameter.PH, 
        min_value=5, max_value=8, 
        plantation=plantation_1
    )
    par_5 = Parameter.objects.create(
        parameter_type=Parameter.SOIL_UMIDITY, 
        min_value=5, max_value=10, 
        plantation=plantation_1
    )
    par_6 = Parameter.objects.create(
        parameter_type=Parameter.AIR_UMIDITY, 
        min_value=10, max_value=12, 
        plantation=plantation_1
    )
    par_7 = Parameter.objects.create(
        parameter_type=Parameter.RAIN, 
        min_value=5, max_value=12, 
        plantation=plantation_1
    )

    print ('Creating readings\n')
    create_reading(par_1)
    create_reading(par_2)
    create_reading(par_3)
    create_reading(par_4)
    create_reading(par_5)
    create_reading(par_6)
    create_reading(par_7)
    


    print ('\n------------------------------\n')
    print ('Database populated with sucess')
    print ('------------------------------\n')


import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sics.settings')
django.setup()
from django.utils import timezone
from sics.api.models import User, Plantation, Parameter, Reading
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from allauth.account.models import EmailAddress
from random import seed
from random import randint
seed(1)
populate()