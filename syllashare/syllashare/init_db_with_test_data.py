from user_data.models import School, Department, Term, EventType, Teacher, Class, Group, User, SyllabusEvent
from django.utils import timezone
import datetime

class init_db_with_test_data():

    def main(self):
        #school model
        poly = School(name='Cal Poly Pomona', city='Pomona', state='California', pic_key='logo1')
        poly.save()
        diego = School(name='UCSD', city='SanDiego', state='California', pic_key='logo2')
        diego.save()
        berkeley = School(name='UC Berkeley', city='Berkeley', state='California', pic_key='logo3')
        berkeley.save()
        fullerton = School(name='Cal State Fullerton', city='Fullerton', state='California', pic_key='logo4')
        fullerton.save()

        #department model
        cs = Department(department_name='Computer Science')
        cs.save()
        lit = Department(department_name='Literature')
        lit.save()
        bio = Department(department_name='Biology')
        bio.save()
        business = Department(department_name='Business')
        business.save()
        math = Department(department_name='Math')
        math.save()

        #term model
        fall = Term(term='FALL')
        fall.save()
        winter = Term(term='WINTER')
        winter.save()
        spring = Term(term='SPRING')
        spring.save()
        summer = Term(term='SUMMER')
        summer.save()

        #eventtype model
        hw = EventType(event_type='homework')
        hw.save()
        midterm = EventType(event_type='midterm')
        midterm.save()
        final = EventType(event_type='final')
        final.save()
        event = EventType(event_type='event')
        event.save()

        #teacher model
        teacher1 = Teacher(first_name='Sam', last_name='Baker', department=cs, school=poly,
                           rating=70.5, website='website.com')
        teacher1.save()
        teacher2 = Teacher(first_name='Rushi', last_name='Kri', department=math, school=poly,
                           rating=None, website='website2.com')
        teacher2.save()
        teacher3 = Teacher(first_name='Barbra', last_name='Ledger', department=bio, school=diego,
                           rating=99.2, website=None)
        teacher3.save()
        teacher4 = Teacher(first_name='Damian', last_name='Wayne', department=lit, school=diego,
                           rating=52, website='website3.com')
        teacher4.save()
        teacher5 = Teacher(first_name='Kelly', last_name='Mo', department=cs, school=berkeley,
                           rating=29.9, website='website4.com')
        teacher5.save()
        teacher6 = Teacher(first_name='Deb', last_name='Rider', department=business, school=berkeley,
                           rating=92.5, website=None)
        teacher6.save()
        teacher7 = Teacher(first_name='Ken', last_name='Sa', department=cs, school=fullerton,
                           rating=42.4, website='website5.com')
        teacher7.save()
        teacher8 = Teacher(first_name='Tet', last_name='Ser', department=lit, school=fullerton,
                           rating=None, website=None)
        teacher8.save()

        #class model
        algorithm = Class(department=cs, class_description='Algorithms', class_number='CS450', school=poly,
                          teacher=teacher1, term=winter, year=2018)
        algorithm.save()
        data = Class(department=cs, class_description='Data Structures', class_number='CS240', school=berkeley,
                          teacher=teacher5, term=None, year=2018)
        data.save()
        software = Class(department=cs, class_description='Software Development', class_number='CS480', school=fullerton,
                          teacher=teacher7, term=fall, year=None)
        software.save()
        calc = Class(department=math, class_description='Calculus', class_number='MAT230', school=poly,
                          teacher=teacher2, term=spring, year=2017)
        calc.save()
        animal = Class(department=bio, class_description='Animal Health', class_number='Bio320', school=diego,
                          teacher=teacher3, term=None, year=2017)
        animal.save()
        poem = Class(department=lit, class_description='Great Poets', class_number='LIT110', school=diego,
                          teacher=teacher4, term=winter, year=2017)
        poem.save()
        market = Class(department=business, class_description='Intro to Marketing', class_number='=CBE101', school=berkeley,
                          teacher=teacher6, term=summer, year=2016)
        market.save()
        haiku = Class(department=lit, class_description='Haiku Analysis', class_number='LIT100', school=fullerton,
                          teacher=teacher8, term=None, year=None)
        haiku.save()

        #group model
        css = Group(group_name='Computer Science Society')
        css.save()
        dps = Group(group_name='Dead Poet Society')
        dps.save()
        bff = Group(group_name='Biology Friends Forever')
        bff.save()

        #user model
        user1 = User(id='234d3', first_name='Justin', last_name='Corcuera', username='yaboi', email=None, pic_key=None,
                     school=poly)
        user1.save()
        user1.classes.add(algorithm)
        user1.classes.add(calc)
        user1.groups.add(css)
        user2 = User(id='438d2', first_name='Guy', last_name='Fieri', username='flame', email='cooking@flavortown.com',
                     pic_key='png1', school=poly)
        user2.save()
        user2.groups.add(css)
        user3 = User(id='19fg3', first_name='Mo', last_name='Smalls', username='idot', email='j@uc.edu', pic_key=None,
                     school=diego)
        user3.save()
        user3.classes.add(animal)
        user3.groups.add(bff)
        user4 = User(id='8yf74', first_name='Kal', last_name='Ces', username='ieatpants', email=None, pic_key='png2',
                     school=diego)
        user4.save()
        user4.classes.add(poem)
        user4.groups.add(dps)
        user5 = User(id='ef584', first_name='Jiren', last_name='Palin', username='amenee', email='d@uc.edu', pic_key='png3',
                     school=berkeley)
        user5.save()
        user5.classes.add(market)
        user6 = User(id='f7873', first_name='Los', last_name='Marcy', username='amen', email='Kaleid@calstate.edu',
                     pic_key='png4',school=fullerton)
        user6.save()
        user7 = User(id='fgm0s', first_name='Zed', last_name='Darcy', username='denk', email='Kkeekd@calstate.edu',
                     pic_key='png4', school=fullerton)
        user7.save()
        user7.classes.add(haiku)
        user7.groups.add(dps)

        #timezone setting
        now = datetime.datetime.now()
        due_date = timezone.make_aware(now)
        due_date1 = due_date + datetime.timedelta(days=7)
        due_date2 = due_date + datetime.timedelta(days=13)
        due_date3 = due_date + datetime.timedelta(days=29)


        # syllabusevent model
        event1 = SyllabusEvent(event_name='Algorithms Final', date=due_date1)
        event1.save()
        event1.from_class.add(algorithm)
        event1.event_type.add(final)
        event2 = SyllabusEvent(event_name='CSS Meeting', date=due_date2)
        event2.save()
        event2.from_group.add(css)
        event2.event_type.add(event)
        event3 = SyllabusEvent(event_name='Study Session with friend', date=due_date3)
        event3.save()
        event3.from_user.add(user2)
        event3.event_type.add(event)
