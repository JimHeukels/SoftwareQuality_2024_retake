# Class Member with FirstName, Lastname, Age, Gender, Weight, Address, Phone Number, Email, and Member ID
# Methods: __init__, __str__, __repr__, __eq__, __lt__, __le__, __gt__, __ge__, __hash__
class Member:
    def __init__(self, first_name, last_name, age, gender, weight, street, housenumber, zipcode, city, phone_number, email, id):
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.age = age
        self.gender = gender
        self.weight = weight
        self.address = street + ' ' + housenumber + ' ' + zipcode + ' ' + city
        self.phone_number = phone_number
        self.email = email
        

    
    def __str__(self):
        return f'{self.first_name} {self.last_name}'
