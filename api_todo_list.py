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

def create_todo(title, user_id=1):
    """Create a new todo"""
    url = f"{BASE_URL}/todos"
    data = {
        "userId": user_id,
        "title": title,
        "completed": False
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
        table_data.append([
            todo['id'],
            status,
            todo['title']
        ])

    headers = ["ID", "Done", "Task"]
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
        print("5. Quit")

        choice = input("\nChoose an option: ")

        if choice == "1":
            todos = get_all_todos(user_id)
            display_todos(todos)

        elif choice == "2":
            title = input("Enter todo title: ")
            create_todo(title, user_id)

        elif choice == "3":
            todo_id = input("Enter todo ID to complete: ")
            mark_complete(int(todo_id))

        elif choice == "4":
            todo_id = input("Enter todo ID to delete: ")
            delete_todo(int(todo_id))

        elif choice == "5":
            print("Goodbye!")
            break

        else:
            print("Invalid choice!")

if __name__ == "__main__":
    main()
