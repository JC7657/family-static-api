from flask_sqlalchemy import SQLAlchemy
import random

db = SQLAlchemy()

class Family:
    
    def __init__(self, last_name):
        self.last_name = last_name
        # example list of members
        self._members = [{
            "id": 27381008,
            "first_name": "John",
            "age": 33,
            "lucky_numbers": [7, 13, 22]
        },
        {
            "id": 27367877,
            "first_name": "Jane",
            "age": 35,
            "lucky_numbers": [10, 14, 3]    
        },
        {
            "id": 75904477,
            "first_name": "Jimmy",
            "age": 5,
            "lucky_numbers": [1]    
        }]

        # read-only: Use this method to generate random members ID's when adding members into the list
    def _generateId(self):
        return random.randint(0, 99999999)

    def add_member(self, member):
        ## you have to implement this method
        ## append the member to the list of _members
        self._members.append(member)
        return self._members
        

    def delete_member(self, id):
        ## you have to implement this method
        ## loop the list and delete the member with the given id
        newList = []
        for member in self._members:
            if member['id'] != id:
                newList.append(member)
        self._members = newList
        return({"msg": "ok"})
        

    def update_member(self, id, member):
        ## you have to implement this method
        ## loop the list and replace the memeber with the given id
        newList = []
        for member in self._members:
            if member['id'] != id:
                newList.append.member
            
        self._members = newList
        member['id']: id
        self._members.append(member)
        return self._members

    def get_member(self, id):
        ## you have to implement this method
        ## loop all the members and return the one with the given id
        for member in self._members:
            if member['id'] == id:
                print("match")
                return member
            else:
                print("not match")
            

    def get_all_members(self):
        return self._members