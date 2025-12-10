import phonenumbers as ph
from phonenumbers import carrier
from phonenumbers import geocoder
from phonenumbers import timezone
number = input("please insert your phonenumber :")
number =ph.parse(number)
print(f'Timezone is : {timezone.time_zones_for_number(number)}')
print(f'Carrier Name is : {carrier.name_for_number(number,'en')}')
print(f'country is : {geocoder.description_for_number(number,'en')}')