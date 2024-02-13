from faker import Faker
from datetime import date

fake = Faker()

print(fake.date_between_dates(date_start=date(2015,1,1), date_end=date(2019,12,13)))