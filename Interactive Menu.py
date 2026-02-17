import os 
import time
import bcrypt
import json

HomeDir = os.path.dirname(os.path.abspath(__file__))
choice = None
special_chars = "!@#$%^&*()-_=+[]{}|;:'\",.<>?/`~"

def options():
    return input("\nMercy) Please enter one of the following options: ")

def database_path():
    name = input("Mercy) Please enter the name of the database: ")
    name == name.strip().lower()

    name = os.path.basename(name)
    if not name.endswith(".json"):
        name += ".json"

    return os.path.join(HomeDir, name)

def initialize_db(database):
    if os.path.exists(database):
        print("Mercy) Database already exists.")
        return
    
    with open(database, "w") as w:
        json.dump([], w, indent=8)

    print("Mercy) Database has been intialized.")


def DB(database, username, password, hashed_password, work_factor):
    if os.path.exists(database):
        with open(database, "r") as r:
                data = json.load(r)

    data.append({
        "Username": username,
        "Password": password,
        "Hashed Password": hashed_password,
        "Work_factor": work_factor
    })

    with open(database, "w") as w:
        json.dump(data, w, indent=8)

def load_database(database):
    if not os.path.exists(database):
        print("Mercy) No Database found")
        return
    
    with open(database, "r") as r:
        data = json.load(r)

    print("\nMercy) Welcome to the Mercy username & password verification services menu")

    while True:
        print("\nMercy) Please select one of the following options.")
        print("1)Search for an existing username")
        print("2)Search for existing password hash")
        print("3)Return to main menu")

        choice = options()

        if choice == "1":
            max_attempts = 3
            attempts = 0 
            while attempts < max_attempts:
                get_user = input("Mercy) Please enter the username to search for: ").strip().lower()

                for entry in data:
                    if entry.get("Username") == get_user:
                        print(f"Mercy)'{entry['Username']}' exists in this database")
                        return
                    
                attempts += 1 
                remaining = max_attempts - attempts

                if remaining > 0:
                    print("Mercy) Invalid username. Please try again.")
                    continue
                else:
                    print("Mercy) You have run out of attempts. Account is locked.")
                    return
            
        elif choice == "2":
            max_attempts = 3
            attempts = 0
            get_user = input("Mercy) Please enter the username to search for: ").strip().lower()
            stored_hashed = None

            for entry in data:
                if entry.get("Username") == get_user:
                    stored_hashed = entry["Hashed Password"].encode()
                    break
                    
            if stored_hashed is None:
                print("Mercy) Invalid Credentials")
                return 
            
            while attempts < max_attempts:
                get_pass = input("Mercy) Please enter your password to verify your account: ")

                if bcrypt.checkpw(get_pass.encode(), stored_hashed):
                    print("Mercy) Password is valid.")
                    return
                
                attempts += 1
                remaining = max_attempts - attempts
                if remaining > 0:
                    print("Mercy) Invalid Password. Please try again.")
                else:
                    print("Mercy) Account has been locked. Have a good day")
                    return
            
        elif choice == "3":
            return
        
        else:
            print("Mercy) Please select a valid option (1/2/3).")

def main():
    database = database_path()
    initialize_db(database)
    
    print("Welcome to Mercy Account System Manager")
    

    while True: 
        print("\nMercy) Please select from one of the following options")
        print("1) Create a new username.")
        print("2) Create a new password that will be hashed")
        print("3) Account Services Menu")
        print("4) Exit program")

        choice = options()

        if choice == "1":
            username = input("Mercy) Please enter your desired username: ").strip().lower()
            new_user = username
            continue

        elif choice == "2":
            while True:
                password = input("Mercy) Please enter the desired password you wish to be hashed: ")
           
                if len(password) <= 8: 
                    print("Mercy) Password length must be greater than 8 characters")
                    print("Mercy) Please try again")
                    continue

                if not any(char.isdigit() for char in password):
                    print("Mercy) Password must include atleast 1 number.")
                    print("Mercy) Please try again")
                    continue

                if not any(char in special_chars for char in password):
                    print("Mercy) Password must contain 1 special character")
                    print("Mercy) Please try again")
                    continue

                if not any(char.isupper() for char in password):
                    print("Mercy) Password must contain atleast 1 uppercase letter.")
                    print("Mercy) Please try again")
                    continue

                print(f'\nMercy) {new_user} has selected {password} to be hashed')
                break
        elif choice == "3":
            load_database(database)
            continue
        elif choice == "4":
            print("\nMercy) Thank you for running Mercy Account System Manager")
            print("Mercy) Program is now closing\n")
            break
        else:
            print("\nMercy) Please select from one one of the following options.")

        password_bytes = password.encode()
        work_factor = 13 
        hash_start = time.perf_counter()
        hashed_password = bcrypt.hashpw(password_bytes, bcrypt.gensalt(rounds=work_factor))
        hash_end = time.perf_counter()

        runtime = hash_end - hash_start
        print(f"Mercy) This hash took {runtime:.4f} seconds")
        print(f'Mercy) Password has successfully been hashed: {hashed_password.decode()}')

        DB(database, new_user, password, hashed_password.decode(), work_factor)

if __name__ == "__main__":
    main()


        

