import random
used_library_numbers = set()
def generate_library_number():
    while True:
        num = random.randint(10000, 99999)  # 5-digit number
        if num not in used_library_numbers:
            used_library_numbers.add(num)
            return num
librarians=[]
assistants=[]
students=[]
faculties=[]
communities=[]
child=[]
class Person:#DONE
    def __init__(self, name, age):
        self.name = name
        self.age = age

class Staff(Person):
    def __init__(self, name, age, username, password):
        super().__init__(name, age)
        self.username=username
        self.password=password
        #ADD ATTRIBUTES AND METHODS COMMON IN ASSISTANT AND LIBRARY
        #COMMON METHODS
    def delete_own_account(self):
        pass
    def add_fines(self,patron):
        pass
    def calculate_fines(self,patron):
        pass
    def lend_book(self):
        pass
    def receive_book(self,patron):
        pass
    def report(self):
        pass


class Librarian(Staff):
    def add_assistant(self, name, age, username, password): 
        if username in [a.username for a in assistants]:
          print(f'Assistant with username {username} already exists.')
          return
         
        else:
                new_assistant = Assistant(name, age, username, password)
                assistants.append(new_assistant)
                print(f'Assistant with username {username} added successfully.')

    def remove_assistant(self, username):
        for assistant in assistants:
            if assistant.username == username:
                assistants.remove(assistant)
                print(f'Assistant {username} removed successfully.')
                return
        print(f'Assistant with username {username} not found.')
    
    def show_assistants_info(self):
        if not assistants:
            print('No assistants available.')
            return
        for assistant in assistants:
            print(f'Name: {assistant.name}, Age: {assistant.age}, Username: {assistant.username}')
#ADD_PATRON HAS BEEN CHECKED THOROUGHLY BUT PUT VALIDATION ON OUTER CODE LIKE AGE ETC
    def add_patron(self,name,age,fines,borrowed_books,days_overdue,max_books_allowed,max_days_allowed, five_point_one):#YUNG MENU 5.1, number 1 yung student, 2 faculty,3 community,4 child
        library_number = generate_library_number()
        if five_point_one==1:
            new_patron=Student(name,age,library_number,fines,borrowed_books,days_overdue,max_books_allowed,max_days_allowed)
            students.append(new_patron)
            print(f'Student added succesfully with library number {library_number}.')
        elif five_point_one ==2:
            new_patron=Faculty(name,age,library_number,fines,borrowed_books,days_overdue,max_books_allowed,max_days_allowed)
            faculties.append(new_patron)
            print(f'Faculty added successfully with library number {library_number}.')
        elif five_point_one ==3:
            new_patron=Community(name,age,library_number,fines,borrowed_books,days_overdue,max_books_allowed,max_days_allowed)
            communities.append(new_patron)
            print(f'Community added successfully with library number {library_number}.')
        elif five_point_one ==4:
            new_patron=Child(name,age,library_number,fines,borrowed_books,days_overdue,max_books_allowed,max_days_allowed)
            child.append(new_patron)
            print(f'Child added successfully with library number {library_number}.')
#REMOVE_PATRON HAS BEEN CHECKED THOROUGHLY 
    def remove_patron(self,six_point_one, library_number): # MENU 6.1
        if library_number not in used_library_numbers:
            print('Library number does not exist.')
            return
        elif six_point_one==1:
            for patron in students:
                if patron.library_number==library_number:
                    students.remove(patron)
                    print('Student removed successfully.')
                    return
            print('Student not found.')
        elif six_point_one==2:
            for patron in faculties:
                if patron.library_number==library_number:
                    faculties.remove(patron)
                    print('Faculty removed successfully.')
                    return
            print('Faculty not found.')
        elif six_point_one==3:
            for patron in communities:
                if patron.library_number==library_number:
                    communities.remove(patron)
                    print('Community removed successfully.')
                    return
            print('Community not found.')
        elif six_point_one==4:
            for patron in child:
                if patron.library_number==library_number:
                    child.remove(patron)
                    print('Child removed successfully.')
                    return
            print('Child not found.')
#EDIT_PATRON_INFO HAS BEEN CHECKED THOROUGHLY, BUT STILL LACKS VALIDATION LIKE AGE ETC
    def edit_patron_info(self, seven_point_one, seven_point_2, library_number, new_value): #7.1 and 7.2 Info
        if library_number not in used_library_numbers:
            print('Library number does not exist.')
            return
        list1= [students, faculties, communities, child]
        for patron in list1[seven_point_one - 1]:
         if patron.library_number == library_number:
            if seven_point_2 == 1:
                patron.name = new_value
            elif seven_point_2 == 2:
                patron.age = new_value
            elif seven_point_2 == 3:
                patron.fines = new_value
            elif seven_point_2 == 4:
                patron.borrowed_books = new_value
            elif seven_point_2 == 5:
                patron.days_overdue = new_value
            elif seven_point_2 == 6:
                patron.max_books_allowed = new_value
            elif seven_point_2 == 7:
                patron.max_days_allowed = new_value

            print("Patron information updated successfully.")
            return
    


    
        pass
    def add_book(self):
        pass
    def remove_book(self):
        pass
    



class Assistant(Staff):
    pass

class Patron(Person):
    def __init__(self, name, age,library_number, fines ,borrowed_books,days_overdue, max_books_allowed, max_days_allowed):
        super().__init__(name, age)
        self.fines=fines
        self.borrowed_books=borrowed_books
        self.days_overdue=days_overdue
        self.max_books_allowed=max_books_allowed
        self.max_days_allowed=max_days_allowed
        self.library_number=library_number

        #ADD ATTRIBUTES AND METHODS COMMON IN PATRON TYPES
    
class Student(Patron):
    pass

class Faculty(Patron):
    pass

class Community(Patron):
    pass    

class Child(Patron):
    pass

