from faker import Faker
from datetime import date, timedelta
import random

fake = Faker()

print(type(fake.date_between_dates(date_start=date(2023,1,1), date_end=date(2024,1,1))))
print(type(fake.date_between_dates(date_start=date(2023,1,1), date_end=date(2024,1,1))+timedelta(days=10)))
