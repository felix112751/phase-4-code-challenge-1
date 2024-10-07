from faker import Faker
from app import app
from models import db, Hero, Power, HeroPower

class TestApp:
    '''Flask application in app.py'''

    def test_gets_heroes(self):
        '''Retrieves heroes with GET requests to /heroes.'''
        with app.app_context():
            fake = Faker()
            hero1 = Hero(name=fake.name(), super_name=fake.name())
            hero2 = Hero(name=fake.name(), super_name=fake.name())
            db.session.add_all([hero1, hero2])
            db.session.commit()

            response = app.test_client().get('/heroes')
            heroes = Hero.query.all()

            assert response.status_code == 200
            assert response.content_type == 'application/json'
            response_json = response.get_json()

            assert [hero['id'] for hero in response_json] == [hero.id for hero in heroes]
            assert [hero['name'] for hero in response_json] == [hero.name for hero in heroes]
            assert [hero['super_name'] for hero in response_json] == [hero.super_name for hero in heroes]
            
            # Update this assertion to check for 'hero_powers' in each hero
            for hero in response_json:
                assert 'hero_powers' in hero  # Adjust based on your API design

    def test_gets_hero_by_id(self):
        '''Retrieves one hero using its ID with GET request to /heroes/<int:id>.'''
        with app.app_context():
            fake = Faker()
            hero = Hero(name=fake.name(), super_name=fake.name())
            db.session.add(hero)
            db.session.commit()

            response = app.test_client().get(f'/heroes/{hero.id}')

            assert response.status_code == 200
            assert response.content_type == 'application/json'
            response_json = response.get_json()

            assert response_json['id'] == hero.id
            assert response_json['name'] == hero.name
            assert response_json['super_name'] == hero.super_name
            assert 'hero_powers' in response_json  # Adjust based on your API design

    def test_returns_404_if_no_hero_to_get(self):
        '''Returns an error message and 404 status code with GET request to /heroes/<int:id> by a non-existent ID.'''
        with app.app_context():
            response = app.test_client().get('/heroes/0')
            assert response.status_code == 404
            assert response.content_type == 'application/json'
            assert 'error' in response.get_json()

    def test_gets_powers(self):
        '''Retrieves powers with GET requests to /powers.'''
        with app.app_context():
            fake = Faker()
            power1 = Power(name=fake.name(), description=fake.sentence(nb_words=10))
            power2 = Power(name=fake.name(), description=fake.sentence(nb_words=10))
            db.session.add_all([power1, power2])
            db.session.commit()

            response = app.test_client().get('/powers')
            powers = Power.query.all()

            assert response.status_code == 200
            assert response.content_type == 'application/json'
            response_json = response.get_json()

            assert [power['id'] for power in response_json] == [power.id for power in powers]
            assert [power['name'] for power in response_json] == [power.name for power in powers]
            assert [power['description'] for power in response_json] == [power.description for power in powers]
            for power in response_json:
                assert 'hero_powers' not in power  # Adjust based on your API design

    def test_gets_power_by_id(self):
        '''Retrieves one power using its ID with GET request to /powers/<int:id>.'''
        with app.app_context():
            fake = Faker()
            power = Power(name=fake.name(), description=fake.sentence(nb_words=10))
            db.session.add(power)
            db.session.commit()

            response = app.test_client().get(f'/powers/{power.id}')

            assert response.status_code == 200
            assert response.content_type == 'application/json'
            response_json = response.get_json()

            assert response_json['id'] == power.id
            assert response_json['name'] == power.name
            assert response_json['description'] == power.description
            assert 'hero_powers' not in response_json  # Adjust based on your API design

    def test_returns_404_if_no_power_to_get(self):
        '''Returns an error message and 404 status code with GET request to /powers/<int:id> by a non-existent ID.'''
        with app.app_context():
            response = app.test_client().get('/powers/0')
            assert response.status_code == 404
            assert response.content_type == 'application/json'
            assert 'error' in response.get_json()

    def test_patches_power_by_id(self):
        '''Updates one power using its ID and JSON input for its fields with a PATCH request to /powers/<int:id>.'''
        with app.app_context():
            fake = Faker()
            power = Power(name=fake.name(), description=fake.sentence(nb_words=10))
            db.session.add(power)
            db.session.commit()

            response = app.test_client().patch(
                f'/powers/{power.id}',
                json={'description': power.description + ' (updated)'}
            )

            assert response.status_code == 200
            assert response.content_type == 'application/json'
            response_json = response.get_json()

            power_updated = Power.query.get(power.id)

            assert response_json['name'] == power.name
            assert response_json['description'] == power_updated.description
            assert '(updated)' in power_updated.description

    def test_validates_power_description(self):
        '''Returns an error message if a PATCH request to /powers/<int:id> contains a "description" value that is not a string of 20 or more characters.'''
        with app.app_context():
            fake = Faker()
            power = Power(name=fake.name(), description=fake.sentence(nb_words=10))
            db.session.add(power)
            db.session.commit()

            response = app.test_client().patch(
                f'/powers/{power.id}',
                json={'description': ''}
            )

            assert response.status_code == 400
            assert response.content_type == 'application/json'
            assert response.get_json()['errors'] == ["Description must be at least 20 characters long."]

    def test_404_no_power_to_patch(self):
        '''Returns an error message if a PATCH request to /powers/<int:id> references a non-existent power.'''
        with app.app_context():
            response = app.test_client().patch(
                '/powers/0',
                json={'description': ''}
            )
            assert response.status_code == 404
            assert response.content_type == 'application/json'
            assert 'error' in response.get_json()

    def test_creates_hero_power(self):
        '''Creates one hero_power using a strength, a hero_id, and a power_id with a POST request to /hero_powers.'''
        with app.app_context():
            fake = Faker()
            hero = Hero(name=fake.name(), super_name=fake.name())
            power = Power(name=fake.name(), description=fake.sentence(nb_words=10))
            db.session.add_all([hero, power])
            db.session.commit()

            response = app.test_client().post(
                '/hero_powers',
                json={
                    'strength': 'Weak',
                    'hero_id': hero.id,
                    'power_id': power.id,
                }
            )

            assert response.status_code == 201  # Correct status for creation
            assert response.content_type == 'application/json'
            response_json = response.get_json()

            assert response_json['hero_id'] == hero.id
            assert response_json['power_id'] == power.id
            assert response_json['strength'] == 'Weak'
            assert 'id' in response_json  # Check for the generated ID

            query_result = HeroPower.query.filter(
                HeroPower.hero_id == hero.id, HeroPower.power_id == power.id).first()
            assert query_result.strength == 'Weak'

    def test_validates_hero_power_strength(self):
        '''Returns an error message if a POST request to /hero_powers contains a "strength" value other than "Strong", "Weak", or "Average".'''
        with app.app_context():
            fake = Faker()
            hero = Hero(name=fake.name(), super_name=fake.name())
            power = Power(name=fake.name(), description=fake.sentence(nb_words=10))
            db.session.add_all([hero, power])
            db.session.commit()

            response = app.test_client().post(
                '/hero_powers',
                json={
                    'strength': 'Cheese',
                    'hero_id': hero.id,
                    'power_id': power.id,
                }
            )

            assert response.status_code == 400
            assert response.content_type == 'application/json'
            assert response.get_json()['errors'] == ["Strength must be one of 'Strong', 'Weak', or 'Average'."]
