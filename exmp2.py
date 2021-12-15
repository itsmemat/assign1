


def menu():
    print("welcome to the system...")
    print("=====================")
    print("1. Add a new student")
    print("2. Add a new course")
    print("3. Add grade ")
    print("4. Save and exit")
    print("5. for viewing all students")    
    print("6. View all staff and edit")
   
    choice = int(input())
   
    if choice == 1:
        addNewStudent()
    elif choice ==2:
        addCourse() 
    elif choice ==3:
        addGrade() 
    elif choice ==5:
        viewAll()
    elif choice == 7:
        exit()
    elif choice == 4:
        saveAndExit() 
    elif choice == 6:
        staff()    
    else:
        menu()
        
menu()