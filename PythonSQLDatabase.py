import tkinter as tk
from tkinter import messagebox
import mysql.connector
from tkinter import *
from tkinter import ttk
from datetime import datetime, date

# End Imports .
db = mysql.connector.connect(
    host="localhost",
   # user="root",
    #password="123456"
    user="sqluser",
    password="password"
)
if (db):
    print("coneccted")
else:
    print("not connect")

# Create the main window ( root ) .
root = tk.Tk()
root.title("Phase1")
root.configure(bg="black")

# Set the window size and position it at the center of the screen .
window_width = 500
window_height = 500
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x = (screen_width // 2) - (window_width // 2)
y = (screen_height // 2) - (window_height // 2)

root.geometry(f"{window_width}x{window_height}+{x}+{y}")


def initialize():
    # create the user database and select it
    cursor = db.cursor()
    cursor.execute("SHOW DATABASES")

    if "user" not in cursor:
        cursor.execute("CREATE DATABASE IF NOT EXISTS user")
        cursor.execute("USE user")

        # create the user table
        cursor.execute("CREATE TABLE IF NOT EXISTS user ("
                       "username VARCHAR(255) PRIMARY KEY,"
                       "password VARCHAR(255),"
                       "firstName VARCHAR(255),"
                       "lastName VARCHAR(255),"
                       "email VARCHAR(255) UNIQUE)")
        db.commit()

        # create the "items" table
        cursor.execute("CREATE TABLE IF NOT EXISTS items ("
                       "id INT AUTO_INCREMENT PRIMARY KEY,"
                       "user_id VARCHAR(255),"
                       "title VARCHAR(255),"
                       "description TEXT,"
                       "category VARCHAR(255),"
                       "price DECIMAL(10, 2),"
                       "created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)")
        db.commit()
        cursor.execute("CREATE TABLE IF NOT EXISTS rateitems ("
                       "id INT,"
                       "user_id VARCHAR(255),"
                       "title VARCHAR(255),"
                       "description TEXT,"
                       "category VARCHAR(255),"
                       "price DECIMAL(10, 2),"
                       "created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,"
                       "rate_description TEXT,"
                       "counter INT,"
                       "rating VARCHAR(255))")
        db.commit()
    else:
        invalidlabel = tk.Label(root, bg="pink", text="DB already initialized")
        invalidlabel.pack()


post_count = 0
# rate_count =0
usernames = []


# user_id = []
# Define a function to create a new window for the register page .
def homepage():
    def post_item():
        global post_count
        first = title_entry.get()
        last = description_entry.get()
        user = category_entry.get()
        passw = price_entry.get()
        
        if (first == "" or last == "" or user == "" or passw == ""):
            popup = tk.Toplevel()
            label = tk.Label(popup, text='Fields cannot be empty')
            label.pack(side="top", fill="x", pady=10)
            B1 = tk.Button(popup, text="OK", command=popup.destroy)
            B1.pack()
        else:
            result = create1(first, last, user, passw)
            if result == "success":
                success_popup = tk.Toplevel()
                success_label = tk.Label(success_popup, text='Item inserted successfully.')
                post_count += 1
                success_label.pack(side="top", fill="x", pady=10)
                success_B1 = tk.Button(success_popup, text="OK", command=success_popup.destroy)
                # clear the entry fields
                title_entry.delete(0, tk.END)
                description_entry.delete(0, tk.END)
                category_entry.delete(0, tk.END)
                price_entry.delete(0, tk.END)

                success_B1.pack()
            else:
                error_popup = tk.Toplevel()
                error_label = tk.Label(error_popup, text='Error: You can only post 3 items a day.')
                error_label.pack(side="top", fill="x", pady=10)
                error_B1 = tk.Button(error_popup, text="OK", command=error_popup.destroy)
                error_B1.pack()

    def create1(first, last, username, password):
        # create the user database and select it
        cursor = db.cursor()

        cursor.execute("SELECT username FROM user WHERE username = %s", (username,))
        result = cursor.fetchone()
        user_id = None  # set a default value for user_id

        if result is not None:
            user_id = result[0]

        # handle the case where the query returned no results
        if user_id is None:
            if post_count >= 10:
                cursor.close()
                return "error"

        # Insert the item into the database with the user_id
        cursor.execute("INSERT INTO rateitems (title, description, category, price, user_id) VALUES (%s, %s, %s, %s, %s)",
                        (title_entry.get(), description_entry.get(), category_entry.get(), price_entry.get(), user_id))
        db.commit()
        cursor.close()
        return "success"


    # create a new Toplevel window
    home_window = tk.Toplevel(root)
    home_window.title("Home Page")
    home_window.configure(bg="pink")
    home_window.geometry(f"{window_width}x{window_height}+{x}+{y}")

    # Create a title label ( Register ) .
    home_label = tk.Label(home_window, bg="pink", text="Welcome!", font=50)
    home_label.pack()

    # Create a form to insert an item
    item_frame = tk.Frame(home_window, bg="pink")
    item_frame.pack(pady=10)

    title_label = tk.Label(item_frame, text="Title:", font=20, bg="pink")
    title_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")
    title_entry = tk.Entry(item_frame, font=20)
    title_entry.grid(row=0, column=1, padx=5, pady=5)

    description_label = tk.Label(item_frame, text="Description:", font=20, bg="pink")
    description_label.grid(row=1, column=0, padx=5, pady=5, sticky="w")
    description_entry = tk.Entry(item_frame, font=20)
    description_entry.grid(row=1, column=1, padx=5, pady=5)

    category_label = tk.Label(item_frame, text="Category:", font=20, bg="pink")
    category_label.grid(row=2, column=0, padx=5, pady=5, sticky="w")
    category_entry = tk.Entry(item_frame, font=20)
    category_entry.grid(row=2, column=1, padx=5, pady=5)

    price_label = tk.Label(item_frame, text="Price:", font=20, bg="pink")
    price_label.grid(row=3, column=0, padx=5, pady=5, sticky="w")
    price_entry = tk.Entry(item_frame, font=20)
    price_entry.grid(row=3, column=1, padx=5, pady=5)

    insert_button = tk.Button(item_frame, text="Insert", font=20, command=post_item)
    insert_button.grid(row=4, column=1, padx=5, pady=5)

    # Create the Search button for the homepage window .
    search_button = tk.Button(home_window, bg="black", fg="pink", activebackground="pink", activeforeground="pink",
                              text="S e a r c h   ( c a t e g o r i e s )", width=30, height=3, command=search)
    search_button.pack(pady=25)

    # Create a new button for the homepage window ( for tasks 1 , 6 , and 7 ) .
    list_and_display_button = tk.Button(home_window, bg="black", fg="pink", activebackground="pink",
                                        activeforeground="pink",
                                        text="P a r t s   1   ,   6   ,   7", width=30, height=3,
                                        command=list_and_display)
    list_and_display_button.pack(pady=0)

      # Create a new button for the homepage window ( for tasks 2 , 3 , 4 ) .
    category_display_button = tk.Button(home_window, bg="blue", fg="pink", activebackground="pink",
                                        activeforeground="pink",
                                        text="P a r t s:   2   ,   3   ,   4", width=30, height=3,
                                        command=category_display)
    category_display_button.pack(pady=0)

def register():
    def create():
        first = first_name_entry.get()
        last = last_name_entry.get()
        user = username_entry.get()
        passw = password_entry.get()
        confirmpass = confirm_password_entry.get()
        email = email_entry.get()
        if (first == "" or last == "" or user == "" or passw == "" or confirmpass == "" or email == ""):
            popup = tk.Tk()
            label = tk.Label(popup, text='Fields cannot be empty')
            label.pack(side="top", fill="x", pady=10)
            B1 = tk.Button(popup, text="OK", command=popup.destroy)
            B1.pack()
            # popup.mainloop()

        else:
            create1(first, last, user, passw, confirmpass, email)

    def create1(first, last, username, password, confirm, email):

        # create the user database and select it
        cursor = db.cursor()

        # cursor.execute("SHOW DATABASES")

        cursor.execute("USE user")
        cursor.execute("SELECT * FROM user WHERE username = %s OR email = %s",
                       (username, email))
        user = cursor.fetchone()

        if user:

            print("User name or email already exists")
            invalidlabel = tk.Label(register_window, bg="pink", text="Username or email already exists")
            invalidlabel.pack()
        else:
            if (password == confirm):

                cursor.execute("INSERT INTO user (username, password, firstName, lastName, email) "
                               "VALUES (%s, %s, %s, %s, %s)",
                               (username, password, first, last, email))
                db.commit()
                popup = tk.Tk()
                label = tk.Label(popup, text='Account Registered!')
                label.pack(side="top", fill="x", pady=10)
                B1 = tk.Button(popup, text="OK", command=popup.destroy)
                B1.pack()
            else:
                print("Passwords not match")
                invalidlabel = tk.Label(register_window, bg="pink", text="Passwords not match")
                invalidlabel.pack()

    register_window = tk.Toplevel(root)
    register_window.title("Register")
    register_window.configure(bg="pink")
    register_window.geometry(f"{window_width}x{window_height}+{x}+{y}")

    # Create a title label ( Register ) .
    register_label = tk.Label(register_window, bg="pink", text="R e g i s t e r", font=50)
    register_label.pack(pady=40)

    # Create 6 labels and entry boxes ( for first name , last name , username , email , password , and confirm password ) .
    # ( 1 ) .
    first_name_label = tk.Label(register_window, bg="pink", text="First Name :")
    first_name_label.pack()
    first_name_entry = tk.Entry(register_window, bg="black", fg="pink", width=50)
    first_name_entry.pack()
    # ( 2 ) .
    last_name_label = tk.Label(register_window, bg="pink", text="Last Name :")
    last_name_label.pack()
    last_name_entry = tk.Entry(register_window, bg="black", fg="pink", width=50)
    last_name_entry.pack()
    # ( 3 ) .
    username_label = tk.Label(register_window, bg="pink", text="Username :")
    username_label.pack()
    username_entry = tk.Entry(register_window, bg="black", fg="pink", width=50)
    username_entry.pack()
    # ( 4 ) .
    email_label = tk.Label(register_window, bg="pink", text="Email :")
    email_label.pack()
    email_entry = tk.Entry(register_window, bg="black", fg="pink", width=50)
    email_entry.pack()
    # ( 5 ) .
    password_label = tk.Label(register_window, bg="pink", text="Password :")
    password_label.pack()
    password_entry = tk.Entry(register_window, bg="black", fg="pink", width=50, show="•")
    password_entry.pack()
    # ( 6 ) .
    confirm_password_label = tk.Label(register_window, bg="pink", text="Confirm Password :")
    confirm_password_label.pack()
    confirm_password_entry = tk.Entry(register_window, bg="black", fg="pink", width=50, show="•")
    confirm_password_entry.pack()

    # Create a register button .
    register_window_button = tk.Button(register_window, command=create, bg="black", fg="pink", activebackground="pink",
                                       activeforeground="pink", text="R e g i s t e r", width=30, height=3)
    register_window_button.pack(pady=40)

# Define a function to create a new window for the login page .
def login():
    def submit():
        username = username_entry_login.get()
        password = password_entry_login.get()
        if (username == "" or password == ""):
            invalidlabel = tk.Label(login_window, bg="pink", text="Fields are empty")
            invalidlabel.pack()
        else:
            submit1(username, password)

    def submit1(username, password):

        # create the user database and select it
        cursor = db.cursor()
        cursor.execute("USE user")

        # Select the user from the user table
        cursor.execute("SELECT * FROM user WHERE username = %s AND password = %s", (username, password))
        user = cursor.fetchone()

        if user:
            # Save the username to the rateitems table
            cursor.execute("INSERT INTO rateitems (user_id) VALUES (%s)", (username,))
            db.commit()

            homepage()
            global usernames
            usernames = username
                
        else:
            print("invalid")
            invalidlabel = tk.Label(login_window, bg="pink", text="Wrong username or password")
            invalidlabel.pack()


    # Create a new window .
    login_window = tk.Toplevel(root)
    login_window.title("Login")
    login_window.configure(bg="pink")
    login_window.geometry(f"{window_width}x{window_height}+{x}+{y}")

    # Create a title label ( Login ) .
    login_label = tk.Label(login_window, bg="pink", text="L o g i n", font=50)
    login_label.pack(pady=40)

    # Create 2 labels and entry boxes ( for username and password ) .
    # ( 1 ) .
    username_label_login = tk.Label(login_window, bg="pink", text="Username :")
    username_label_login.pack()
    username_entry_login = tk.Entry(login_window, bg="black", fg="pink", width=50)
    username_entry_login.pack()
    # ( 2 ) .
    password_label_login = tk.Label(login_window, bg="pink", text="Password :")
    password_label_login.pack()
    password_entry_login = tk.Entry(login_window, bg="black", fg="pink", width=50, show="•")
    password_entry_login.pack()

    # Create a login button .
    login_window_button = tk.Button(login_window, command=submit, bg="black", fg="pink", activebackground="pink",
                                    activeforeground="pink", text="L o g i n", width=30, height=3)
    login_window_button.pack(pady=40)

# Define a function to create a new window for the search interface .
def search():
    # Create a new window .
    search_window = tk.Toplevel(root)
    search_window.title("Search")
    search_window.configure(bg="pink")
    search_window.geometry(f"{window_width}x{window_height}+{x}+{y}")

    # Create a title label ( Search ) .
    search_label = tk.Label(search_window, bg="pink", text="S e a r c h", font=50)
    search_label.pack(pady=40)

    # Create one label and entry box ( for search ) .
    search_label_search = tk.Label(search_window, bg="pink", text="Search ( categories ) :")
    search_label_search.pack()
    search_entry_search = tk.Entry(search_window, bg="black", fg="pink", width=50)
    search_entry_search.pack()

    # Create a search button .
    search_window_button = tk.Button(search_window, bg="black", fg="pink", activebackground="pink",
                                     activeforeground="pink", text="S e a r c h", width=30, height=3,
                                     command=lambda: search_categories(search_window, search_entry_search))
    search_window_button.pack(pady=40)

rate_count = 0

# Define a function to retrieve data based on user input and display it in a table / list .
def search_categories(search_window, search_entry_search):
    def rating(evt):

        def postrate():
            global rate_count
            # global rate_count

            des = description_entry.get()
            rate = chooserate.get()
            l = list(value)
            # for name in l:

            # cursor = db.cursor()
            # cursor.execute("SELECT * FROM user.items WHERE user_id = %s",(name,))
            # item=cursor.fetchone()
            if usernames in l:
                print("username found")
                invalid = tk.Label(rate_window, bg="pink", text="cannot rate your items")
                invalid.grid(row=7, column=1, )




            else:
                if (rate_count < 3):

                    for i in value:
                        cursor = db.cursor()
                        query = "SELECT * FROM items WHERE id = %s"
                        cursor.execute(query, (i,))
                        row = cursor.fetchall()
                        for rowc in row:
                            print(rowc, des, rate)
                            rowc = rowc + (des, rate)
                            print(rowc)
                            cursor.execute(
                                "INSERT INTO user.rateitems (id,user_id,title,description,category,price,created_at,rate_description,rating) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                                rowc)
                            db.commit()
                    rate_count += 1
                else:

                    error_popup = tk.Toplevel()
                    error_label = tk.Label(error_popup, text='Error: You can only rate 3 items a day.')
                    error_label.pack(side="top", fill="x", pady=10)
                    error_B1 = tk.Button(error_popup, text="OK", command=error_popup.destroy)
                    error_B1.pack()
                # cursor = db.cursor()
                #

        value = result_listbox.get(ANCHOR)
        rate_window = tk.Toplevel(root)
        rate_window.title("Review Page")
        rate_window.configure(bg="pink")
        rate_window.geometry(f"{window_width}x{window_height}+{x}+{y}")

        items = []
        rating = ['excellent', 'good', 'fair', 'poor']
        rate_label = tk.Label(rate_window, bg="pink", text=value, font=50)
        rate_label.grid(row=1, column=1)
        rate_label = tk.Label(rate_window, bg="pink", text="Rating", font=50)
        rate_label.grid(row=2, column=1)

        chooserate = ttk.Combobox(rate_window, width=27, values=rating)
        chooserate.grid(column=1, row=3)
        description_label = tk.Label(rate_window, text="Description:", font=20, bg="pink")
        description_label.grid(row=4, column=1, padx=5, pady=5, sticky="w")
        description_entry = tk.Entry(rate_window, font=20)
        description_entry.grid(row=5, column=1, padx=5, pady=5)

        ratesubmit = tk.Button(rate_window, text="Rate", font=20, command=postrate)
        ratesubmit.grid(row=6, column=1, padx=5, pady=5)

    # Retrieve the category name entered by the user .
    category_name = search_entry_search.get()

    # Execute a SELECT query to retrieve the necessary data .
    cursor = db.cursor()
    query = "SELECT * FROM items WHERE category = %s"
    cursor.execute(query, (category_name,))
    rows = cursor.fetchall()

    # Display the necessary data in a table / list on the search page .
    result_label = tk.Label(search_window, bg="pink", text="⚫ ⚫ ⚫")
    result_label.pack()

    result_listbox = tk.Listbox(search_window, bg="black", fg="pink", width=80)
    for row in rows:
        result_listbox.insert(tk.END, row)

    result_listbox.bind("<Double-Button-1>", rating)
    result_listbox.pack()

    # Close .
    cursor.close()

# function for phase 3 part 2,3,4.
def category_display():
    # Create a new window.
    category_display_window = tk.Toplevel(root)
    category_display_window.title("P a r t s   2   ,   3   ,   4")
    category_display_window.configure(bg="pink")
    category_display_window.geometry(f"{window_width}x{window_height}+{x}+{y}")

    # Create a title label.
    category_display_label = tk.Label(category_display_window, bg="pink", text="P a r t s   2   ,   3   ,   4", font=50)
    category_display_label.pack(pady=40)

    # Create a frame to hold the buttons.
    button_frame = tk.Frame(category_display_window, bg="pink")
    button_frame.pack(pady=25)



    # Create a button for task 2.
    category_display_button_2 = tk.Button(button_frame, bg="black", fg="pink", activebackground="pink",
                                        activeforeground="pink", text="2", width=10, height=3,
                                        command=lambda: category_user_posted(category_display_window, results_display_window))
    category_display_button_2.pack(side=tk.LEFT, padx=10, fill=tk.X)

    # Create the results display window.
    results_display_window = tk.Toplevel(category_display_window)
    # Create a button for task 3.
    category_display_button_6 = tk.Button(button_frame, bg="black", fg="pink", activebackground="pink",
                                          activeforeground="pink", text="3", width=10, height=3,
                                          command=lambda: category_user_comment2(category_display_window))
    category_display_button_6.pack(side=tk.LEFT, padx=10, fill=tk.X)

    # Create a button for task 4.
    category_display_button_7 = tk.Button(button_frame, bg="black", fg="pink", activebackground="pink",
                                          activeforeground="pink", text="4", width=10, height=3, 
                                          command=lambda: list_top_posters(category_display_window))
    category_display_button_7.pack(side=tk.LEFT, padx=10, fill=tk.X)

#phase 3 part 2
def category_user_posted(category_display_window, results_display_window):
    cursor = db.cursor()

    # Create two Entry widgets for the category inputs.
    category1_label = tk.Label(category_display_window, text="Category 1:", font=("Arial", 12))
    category1_label.pack()
    category1_field = tk.Entry(category_display_window, font=("Arial", 12))
    category1_field.pack()

    category2_label = tk.Label(category_display_window, text="Category 2:", font=("Arial", 12))
    category2_label.pack()
    category2_field = tk.Entry(category_display_window, font=("Arial", 12))
    category2_field.pack()

    # Add a button to trigger the search.
    search_button = tk.Button(category_display_window, text="Search", font=("Arial", 12), command=lambda: search(category1_field, category2_field, results_display_window))
    search_button.pack()

    # Define the search function.
    def search(category1_field, category2_field, results_display_window):
        # Retrieve the category search terms from the category1_field and category2_field.
        category1 = category1_field.get()
        category2 = category2_field.get()

        # Check if categories are the same.
        if category1 == category2:
            title_label = tk.Label(results_display_window, text=f"The two categories must be different.", font=("Arial", 13, "underline"), bg="pink")
            title_label.pack()
        else:
            cursor = db.cursor()
            query = "SELECT DISTINCT user_id FROM rateitems WHERE category = %s OR category = %s"
            cursor.execute(query, (category1, category2,))
            rows = cursor.fetchall()

            # Create two lists to hold the users who posted items in each category.
            users_in_category1 = []
            users_in_category2 = []

            # Loop through the results and add the user IDs to the appropriate list.
            for row in rows:
                user_id = row[0]
                query = "SELECT category FROM rateitems WHERE user_id = %s AND (category = %s OR category = %s) GROUP BY category HAVING COUNT(DISTINCT created_at) > 1"
                cursor.execute(query, (user_id, category1, category2,))
                categories = [r["category"] for r in cursor.fetchall()]
                if len(categories) == 2:
                    if categories[0] == category1:
                        users_in_category1.append(user_id)
                        users_in_category2.append(user_id)
                    else:
                        users_in_category1.append(user_id)
                        users_in_category2.append(user_id)

            # Add a label widget above the displayed data.
            title_label = tk.Label(results_display_window, text=f"Users who posted items in both the {category1} and {category2} categories on the same day", font=("Arial", 13, "underline"), bg="pink")
            title_label.pack()

            # Display the results on the results_display_window.
            if users_in_category1 and users_in_category2:
                for user_id in set(users_in_category1).intersection(users_in_category2):
                    label_text = f"{user_id}"
                    label = tk.Label(results_display_window, bg="pink", font=("Arial", 10), text=label_text)
                    label.pack()
            else:
                label = tk.Label(results_display_window, bg="pink", font=("Arial", 10), text=f"No users found who posted items in both the {category1} and {category2} categories on the same day")
                label.pack()

        # Close the cursor.
        cursor.close()



    #phase 3 part 3

def category_user_comment(category_display_window):
    cursor = db.cursor()

    cursor.execute("""
        SELECT DISTINCT user.username AS username, 
        good_items.num_good_items AS num_good_items, 
        excellent_items.num_excellent_items AS num_excellent_items 
        FROM user 
        LEFT JOIN items ON user.username = items.user_id 
        LEFT JOIN (
            SELECT rateitems.user_id, COUNT(*) AS num_good_items  
            FROM rateitems 
            WHERE rateitems.rating = 'good'                      
            GROUP BY rateitems.user_id 
        ) AS good_items ON user.username = good_items.user_id     
        LEFT JOIN (
            SELECT rateitems.user_id, COUNT(*) AS num_excellent_items  
            FROM rateitems 
            WHERE rateitems.rating = 'excellent'                      
            GROUP BY rateitems.user_id 
        ) AS excellent_items ON user.username = excellent_items.user_id 
        WHERE good_items.num_good_items IS NOT NULL OR excellent_items.num_excellent_items IS NOT NULL 
    """)

    # Fetch all the results.
    results = cursor.fetchall()

    # Add a label widget above the displayed data.
    title_label = tk.Label(category_display_window, text="Items with Excellent or Good Comments from User", font=("Arial", 13, "underline"), bg="pink")
    title_label.pack()

    # Display the dropdown menu for users.
    user_label = tk.Label(category_display_window, text="Select a user:", font=("Arial", 10), bg="pink")
    user_label.pack()
    user_var = tk.StringVar()
    user_dropdown = tk.OptionMenu(category_display_window, user_var, *[""] + [result["username"] for result in results])
    user_dropdown.pack()

    def check_comment():
        user = user_var.get()
        if user:
            result = next((r for r in results if r["username"] == user), None)
            if result:
                label_text = "Excellent" if result["num_excellent_items"] else "Good"
                label = tk.Label(category_display_window, bg="pink", font=("Arial", 10), text=label_text)
                label.pack()
            else:
                label = tk.Label(category_display_window, bg="pink", font=("Arial", 10), text="User has no comments.")  
                label.pack()
        else:
            label = tk.Label(category_display_window, bg="pink", font=("Arial", 10), text="Please select a user.")  
            label.pack()

    # Display the button to check comments.
    check_button = tk.Button(category_display_window, text="Check", command=check_comment)
    check_button.pack()

    # Close the cursor.
    cursor.close()


def category_user_comment2(category_display_window):
    cursor = db.cursor()

    cursor.execute("""
        SELECT user.username AS username, 
        good_items.num_good_items AS num_good_items, 
        excellent_items.num_excellent_items AS num_excellent_items 
        FROM user 
        LEFT JOIN rateitems ON user.id = rateitems.user_id 
        LEFT JOIN (
            SELECT rateitems.user_id, COUNT(*) AS num_good_items  
            FROM rateitems 
            WHERE rateitems.rating = 'good'                      
            GROUP BY rateitems.user_id 
        ) AS good_items ON user.id = good_items.user_id     
        LEFT JOIN (
            SELECT rateitems.user_id, COUNT(*) AS num_excellent_items  
            FROM rateitems 
            WHERE rateitems.rating = 'excellent'                      
            GROUP BY rateitems.user_id 
        ) AS excellent_items ON user.id = excellent_items.user_id 
        WHERE good_items.num_good_items IS NOT NULL OR excellent_items.num_excellent_items IS NOT NULL 
    """)

    # Fetch all the results.
    results = cursor.fetchall()

    # Filter the results to only include users with comments.
    results = [result for result in results if result["num_good_items"] or result["num_excellent_items"]]

    # Add a label widget above the displayed data.
    title_label = tk.Label(category_display_window, text="Items with Excellent or Good Comments from User", font=("Arial", 13, "underline"), bg="pink")
    title_label.pack()

    # Display the dropdown menu for users.
    user_label = tk.Label(category_display_window, text="Select a user:", font=("Arial", 10), bg="pink")
    user_label.pack()
    user_var = tk.StringVar()
    user_dropdown = tk.OptionMenu(category_display_window, user_var, *[""] + [result["username"] for result in results])
    user_dropdown.pack()

    def check_comment():
        user = user_var.get()
        if user:
            result = next((r for r in results if r["username"] == user), None)
            if result:
                label_text = "Excellent" if result["num_excellent_items"] else "Good"
                label = tk.Label(category_display_window, bg="pink", font=("Arial", 10), text=label_text)
                label.pack()
            else:
                label = tk.Label(category_display_window, bg="pink", font=("Arial", 10), text="User has no comments.")  
                label.pack()
        else:
            label = tk.Label(category_display_window, bg="pink", font=("Arial", 10), text="Please select a user.")  
            label.pack()

    # Display the button to check comments.
    check_button = tk.Button(category_display_window, text="Check", command=check_comment)
    check_button.pack()

    # Close the cursor.
    cursor.close()


#function phase 3 part 4
def list_top_posters(category_display_window):
    # Create a cursor object.
    cursor = db.cursor()

    # Execute a query to find the users who posted the most items since 5/1/2020 (inclusive).
    cursor.execute("SELECT user_id, COUNT(*) as count FROM rateitems WHERE created_at >= '2020-05-01' GROUP BY user_id ORDER BY count DESC")

    # Fetch all the results.
    results = cursor.fetchall()

    # Create a list to store the user_id(s) with the highest count.
    top_posters = []

    # Store the user_id(s) with the highest count in the list.
    for user_id, count in results:
        if not top_posters:
            top_posters.append(user_id)
            highest_count = count
        elif count == highest_count:
            top_posters.append(user_id)
        else:
            break

    # Add a label widget above the displayed data.
    title_label = tk.Label(category_display_window, text="Users who posted the most items since 5/1/2020 (inclusive)",
                           font=("Arial", 13, "underline"), bg="pink")
    title_label.pack()

    # Display the results on the category_display_window.
    if not top_posters:
        # If no results are found, display a message.
        no_results_label = tk.Label(category_display_window, bg="pink", font=("Arial", 10),
                                    text=f"No users found who posted any items since 5/1/2020.")
        no_results_label.pack()
    else:
        # Create a label with the user_id(s) who posted the most items since 5/1/2020 (inclusive).
        label_text = f"User ID(s): {', '.join(str(user_id) for user_id in top_posters)}\nNumber of items posted: {highest_count}"
        label = tk.Label(category_display_window, bg="pink", font=("Arial", 10), text=label_text)
        label.pack()

    # Close the cursor.
    cursor.close()


# Define a function to create a new window for tasks 1, 6, and 7 of Phase Three.
def list_and_display():
    # Create a new window.
    list_and_display_window = tk.Toplevel(root)
    list_and_display_window.title("P a r t s   1   ,   6   ,   7")
    list_and_display_window.configure(bg="pink")
    list_and_display_window.geometry(f"{window_width}x{window_height}+{x}+{y}")

    # Create a title label.
    list_and_display_label = tk.Label(list_and_display_window, bg="pink", text="P a r t s   1   ,   6   ,   7", font=50)
    list_and_display_label.pack(pady=40)

    # Create a frame to hold the buttons.
    button_frame = tk.Frame(list_and_display_window, bg="pink")
    button_frame.pack(pady=25)

    # Create a button for task 1.
    list_and_display_button_1 = tk.Button(button_frame, bg="black", fg="pink", activebackground="pink",
                                          activeforeground="pink", text="1", width=10, height=3,
                                          command=lambda: list_most_expensive_items(list_and_display_window))
    list_and_display_button_1.pack(side=tk.LEFT, padx=10, fill=tk.X)

    # Create a button for task 6.
    list_and_display_button_6 = tk.Button(button_frame, bg="black", fg="pink", activebackground="pink",
                                          activeforeground="pink", text="6", width=10, height=3,
                                          command=lambda: display_users_with_no_excellent_items(list_and_display_window))
    list_and_display_button_6.pack(side=tk.LEFT, padx=10, fill=tk.X)

    # Create a button for task 7.
    list_and_display_button_7 = tk.Button(button_frame, bg="black", fg="pink", activebackground="pink",
                                          activeforeground="pink", text="7", width=10, height=3, 
                                          command=lambda: display_users_who_never_posted_poor_review(list_and_display_window))
    list_and_display_button_7.pack(side=tk.LEFT, padx=10, fill=tk.X)

# Define a function to list the most expensive items in each category.
def list_most_expensive_items(list_and_display_window):
    # Create a cursor object.
    cursor = db.cursor()

    # For each category, the following query will return...
    # the category name, the highest price for that category, and the title of the item with the highest price in that category.
    cursor.execute("SELECT category, MAX(price), MAX(title) FROM items GROUP BY category;")

    # Fetch all the results.
    results = cursor.fetchall()

    # Add a label widget above the displayed data.
    title_label = tk.Label(list_and_display_window, text="Most Expensive Items", font=("Arial", 13, "underline"),
                           bg="pink")
    title_label.pack()

    # Display the results on the list_and_display_window.
    for category, max_price, title in results:
        # Create a label with the category, the maximum price, and the maximum title of items for each category.
        label = tk.Label(list_and_display_window, bg="pink", font=("Arial", 10),
                         text=f"Category: {category}   ,   Title: {title}   ,   Price: {max_price}")
        label.pack()

    # Close the cursor.
    cursor.close()
    
# Define a function to display users who have never posted any "excellent" items.
def display_users_with_no_excellent_items(list_and_display_window):
    # Create a cursor object.
    cursor = db.cursor()

    # Execute a query to get all users who have never posted any "excellent" items.
    cursor.execute("""
        SELECT DISTINCT user.username 
        FROM user 
        LEFT JOIN items ON user.username = items.user_id 
        LEFT JOIN (
            SELECT rateitems.user_id, COUNT(*) AS num_excellent_items
            FROM rateitems 
            WHERE rateitems.rating = 'excellent' 
            GROUP BY rateitems.user_id 
            HAVING num_excellent_items >= 3
        ) AS excellent_items ON user.username = excellent_items.user_id 
        WHERE excellent_items.num_excellent_items IS NULL
    """)

    # Fetch all the results.
    results = cursor.fetchall()

    # Add a label widget above the displayed data.
    title_label = tk.Label(list_and_display_window, text="Users With No Excellent Items", font=("Arial", 13, "underline"), bg="pink")
    title_label.pack()

    # Display the results on the list_and_display_window.
    if results:
        for result in results:
            label = tk.Label(list_and_display_window, bg="pink", font=("Arial", 10), text=result[0])
            label.pack()
    else:
        label = tk.Label(list_and_display_window, bg="pink", font=("Arial", 10), text="No Users Found !")
        label.pack()

    # Close the cursor.
    cursor.close()

def display_users_who_never_posted_poor_review(list_and_display_window):
    # Create a cursor object.
    cursor = db.cursor()

    # Execute a query to get all users who have never posted a "poor" review.
    cursor.execute("""
        SELECT DISTINCT user.username 
        FROM user 
        LEFT JOIN rateitems ON user.username = rateitems.user_id AND rateitems.rating = 'poor'
        WHERE rateitems.rating IS NULL
    """)

    # Fetch all the results.
    results = cursor.fetchall()

    # Add a label widget above the displayed data.
    title_label = tk.Label(list_and_display_window, text='''Users Who've Never Posted A "Poor" Review''', font=("Arial", 13, "underline"), bg="pink")
    title_label.pack()

    # Display the results on the list_and_display_window.
    if results:
        for result in results:
            label = tk.Label(list_and_display_window, bg="pink", font=("Arial", 10), text=result[0])
            label.pack()
    else:
        label = tk.Label(list_and_display_window, bg="pink", font=("Arial", 10), text="No Users Found !")
        label.pack()

    # Close the cursor.
    cursor.close()

# Create the Register , Login , and Initialize Database buttons for the main window .
register_button = tk.Button(root, bg="pink", fg="black", activebackground="black", activeforeground="black",
                            text="Register", width=25, height=5, command=register)
register_button.place(relx=0.5, rely=0.25, anchor=tk.CENTER)

login_button = tk.Button(root, bg="pink", fg="black", activebackground="black", activeforeground="black", text="Login",
                         width=25, height=5, command=login)
login_button.place(relx=0.5, rely=0.50, anchor=tk.CENTER)

initialize_database_button = tk.Button(root, bg="pink", fg="black", activebackground="black", activeforeground="black",
                                       text="Initialize Database", width=25,
                                       height=5, command=initialize)  # add command=initialize_database
initialize_database_button.place(relx=0.5, rely=0.75, anchor=tk.CENTER)

# Start the GUI .
root.mainloop()