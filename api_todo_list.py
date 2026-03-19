import requests
from tabulate import tabulate

BASE_URL = "https://jsonplaceholder.typicode.com"

def get_all_todos(user_id=1):
    """Get all todos for a user"""
    url = f"{BASE_URL}/users/{user_id}/todos"
    response = requests.get(url)

    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error fetching todos: {response.status_code}")
        return []

def create_todo(title, priority, user_id=1):
    """Create a new todo"""
    url = f"{BASE_URL}/todos"
    data = {
        "userId": user_id,
        "title": title,
        "completed": False,
        "priority": priority
    }

    response = requests.post(url, json=data)

    if response.status_code == 201:
        print(f"Created todo: {title}")
        return response.json()
    else:
        print(f"Failed to create todo: {response.status_code}")
        return None

def mark_complete(todo_id):
    """Mark a todo as complete"""
    url = f"{BASE_URL}/todos/{todo_id}"
    data = {
        "completed": True
    }

    response = requests.patch(url, json=data)

    if response.status_code == 200:
        print(f"Marked todo {todo_id} as complete")
        return response.json()
    else:
        print(f"Failed to update: {response.status_code}")
        return None

def delete_todo(todo_id):
    """Delete a todo"""
    url = f"{BASE_URL}/todos/{todo_id}"

    response = requests.delete(url)

    if response.status_code == 200:
        print(f"Deleted todo {todo_id}")
        return True
    else:
        print(f"Failed to delete: {response.status_code}")
        return False

def display_todos(todos):
    """Display todos in a table"""
    if not todos:
        print("No todos found!")
        return

    # Prepare data for table
    table_data = []
    for todo in todos:
        status = "Done" if todo['completed'] else "   " 
        priority = todo.get('priority', "N/A") 
        # not all todo will have priority. safely get value or fill in if blank.      
        table_data.append([
            todo['id'],
            status,
            priority,
            todo['title']
        ])

    headers = ["ID", "Done", "Priority", "Task"]
    print("\n" + tabulate(table_data, headers=headers, tablefmt="grid"))

def filter_todo(filter_choice, user_id):
    """Display complete/incomplete todos in a table"""
    # [1] complet or [2] incomplete filter

    todos = get_all_todos(user_id)

    if not todos:
        print("No todos found!")
        return
    
    # Prepare data for table
    table_data = []
    if filter_choice == "1":
        for todo in todos:
            if todo['completed']:        
                status = "Done"
                table_data.append([
                    todo['id'],
                    status,
                    todo['title']
                ])

    if filter_choice == "2":
        for todo in todos:
            if not todo['completed']:        
                status = "Not Done"
                table_data.append([
                    todo['id'],
                    status,
                    todo['title']
                ])
    if not table_data:
        print("No matching todos found.")         

    headers = ["ID", "Done", "Task"]
    print("\n" + tabulate(table_data, headers=headers, tablefmt="grid"))

def edit_todo(todo_id):
    """Edit todo title"""

    new_title = input(f'Enter new title for todo ID #{todo_id}: ')

    url = f"{BASE_URL}/todos/{todo_id}"
    data = {
        "title": new_title
    }

    response = requests.patch(url, json=data)

    if response.status_code == 200:
        print(f"Updated todo {todo_id} title.")
        return response.json()
    else:
        print(f"Failed to update: {response.status_code}")
        return None


def search_todos(search_term, user_id):
    """Search by keyword"""

    todos = get_all_todos(user_id)

    if not todos:
        print("No todos found!")
        return
    
    # make search term lower case
    lowercase_search_term = search_term.lower()

    table_data =[]
    for todo in todos:
        # make searchable fields lowercase
        lowercase_title = todo['title'].lower()
        status = todo.get('status', "N/A")
        lowercase_status = status.lower()

        if lowercase_search_term in lowercase_title or lowercase_search_term in lowercase_status:
            # find matching todo and fill in blanks to avoid error
            status = "Done" if todo['completed'] else " "
            priority = todo.get('priority', "N/A")
            table_data.append([
            todo['id'],
            status,
            priority,
            todo['title']
        ])

    if not table_data:
        print(f'No todos found with "{search_term}" keyword.')

    headers = ["ID", "Done", "Priority", "Task"]
    print("\n" + tabulate(table_data, headers=headers, tablefmt="grid"))


def main():
    """Main program loop"""
    user_id = 1

    print("API-Based Todo List\n")

    while True:
        print("\nOptions:")
        print("1. View all todos")
        print("2. Add todo")
        print("3. Mark todo complete")
        print("4. Delete todo")
        print("5. Filter by complet/incomplete")
        print("6. Edit todo title")
        print("7. Search todo")
        print("8. Quit")

        choice = input("\nChoose an option: ")

        if choice == "1":
            todos = get_all_todos(user_id)
            display_todos(todos)

        elif choice == "2":
            title = input("Enter todo title: ")
            while True:
                priority = input(f'Enter priority (low / medium/ high): ')
                if priority.lower() in ["low", "medium", "high"]:
                    break
                else:
                    print("Please enter low, medium, or high")
            create_todo(title, user_id)

        elif choice == "3":
            todo_id = input("Enter todo ID to complete: ")
            mark_complete(int(todo_id))

        elif choice == "4":
            todo_id = input("Enter todo ID to delete: ")
            delete_todo(int(todo_id))

        elif choice == "5":            
            filter_choice = input("Enter [1] complet or [2] incomplete filter: ")
            if filter_choice == "1" or filter_choice == "2":            
                filter_todo(filter_choice, user_id)                
            else:
                print("Enter option 1 or 2")
                continue

        elif choice == "6":
            todo_id = input("Enter todo ID to edit: ")
            edit_todo(int(todo_id))

        elif choice == "7":            
            search_term = input("Enter keyword to search by: ")                       
            search_todos(search_term, user_id)             
            
        elif choice == "8":
            print("Goodbye!")
            break

        else:
            print("Invalid choice!")

if __name__ == "__main__":
    main()
