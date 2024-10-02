#!/usr/bin/env python3

import tkinter as tk
from tkinter import simpledialog, messagebox, filedialog
import csv
import psycopg2
import logging
import os

# Configure logging
logging.basicConfig(filename='data_loader.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Function to check the database connection
def check_db_connection(dbname, user, password, host, port):
    try:
        conn = psycopg2.connect(
            dbname=dbname,
            user=user,
            password=password,
            host=host,
            port=port
        )
        conn.close()
        return True
    except psycopg2.OperationalError as e:
        logging.error(f"Database connection failed: {e}")
        return False

# Function to get new database connection details from the user input
def get_db_details():
    dbname = simpledialog.askstring("Database Info", "Enter database name:", initialvalue="projectBloom")
    user = simpledialog.askstring("Database Info", "Enter user:", initialvalue="postgres")
    password = simpledialog.askstring("Database Info", "Enter password:", show='*')
    host = simpledialog.askstring("Database Info", "Enter host:", initialvalue="localhost")
    port = simpledialog.askstring("Database Info", "Enter port:", initialvalue="5432")
    return dbname, user, password, host, port

# Function to select the CSV file
def select_csv_file():
    file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
    if file_path:
        csv_path_entry.delete(0, tk.END)
        csv_path_entry.insert(0, file_path)

# Function to run the script
def run_script():
    csv_file_path = csv_path_entry.get()
    table_name = table_name_entry.get()
    schema_name = schema_name_entry.get() or "public"
    delimiter = delimiter_var.get()

    if not csv_file_path or not table_name:
        messagebox.showwarning("Input Error", "Please provide both CSV file path and table name.")
        return

    if not os.path.isfile(csv_file_path):
        messagebox.showwarning("File Error", "The CSV file does not exist or is not accessible.")
        return

    try:
        # Database connection
        conn = psycopg2.connect(
            dbname=dbname,
            user=user,
            password=password,
            host=host,
            port=port
        )
        cursor = conn.cursor()
        logging.info("Database connection established.")

        # Reading CSV headers
        with open(csv_file_path, 'r') as f:
            reader = csv.reader(f, delimiter=delimiter)
            headers = next(reader)

        # Check if the table exists
        cursor.execute(f"""
            SELECT EXISTS (
                SELECT 1 
                FROM information_schema.tables 
                WHERE table_schema = %s AND table_name = %s
            );
        """, (schema_name, table_name))
        table_exists = cursor.fetchone()[0]

        if not table_exists:
            # Create table if it doesn't exist
            columns = ", ".join([f"{header} TEXT" for header in headers])
            create_table_query = f"CREATE TABLE {schema_name}.{table_name} ({columns});"
            cursor.execute(create_table_query)
            logging.info(f"Table {schema_name}.{table_name} created.")
        else:
            # Truncate table if it exists
            truncate_table_query = f"TRUNCATE TABLE {schema_name}.{table_name};"
            cursor.execute(truncate_table_query)
            logging.info(f"Table {schema_name}.{table_name} truncated.")

        conn.commit()

        # Loading data into the table
        copy_sql = f"COPY {schema_name}.{table_name} FROM STDIN WITH CSV HEADER DELIMITER AS '{delimiter}'"
        with open(csv_file_path, 'r') as f:
            cursor.copy_expert(sql=copy_sql, file=f)
        conn.commit()
        logging.info(f"Data loaded successfully into {schema_name}.{table_name}.")

        cursor.close()
        conn.close()

        messagebox.showinfo("Success", f"Data loaded successfully into PostgreSQL. Check {dbname}.{schema_name} schema")
        app.quit()

    except (Exception, psycopg2.DatabaseError) as e:
        logging.error(f"An error occurred: {e}")
        messagebox.showerror("Error", f"An error occurred: {e}")

# Create the main window
app = tk.Tk()
app.title("CSV Data Loader")

# Default database connection details
dbname = "projectBloom"
user = "postgres"
password = "523041"
host = "localhost"
port = "5432"

# Check the default database connection
if check_db_connection(dbname, user, password, host, port):
    use_default = messagebox.askyesno("Database Connection", f"Connection to DB {dbname}, username {user} successful. Do you want to use these credentials?")
    if not use_default:
        dbname, user, password, host, port = get_db_details()
else:
    messagebox.showwarning("Database Connection", "Could not connect with the default settings. Please provide new connection details.")
    dbname, user, password, host, port = get_db_details()

# Instructions label
tk.Label(app, text="Enter CSV file path, table name, and schema (optional), then click the Run button to load data.").pack(pady=10)

# CSV file path entry
tk.Label(app, text="CSV File Path:").pack(pady=5)
csv_frame = tk.Frame(app)
csv_frame.pack(pady=5)

csv_path_entry = tk.Entry(csv_frame, width=50)
csv_path_entry.pack(side=tk.LEFT, padx=5)

csv_browse_button = tk.Button(csv_frame, text="Browse", command=select_csv_file)
csv_browse_button.pack(side=tk.RIGHT, padx=5)

# Table name entry
tk.Label(app, text="Table Name:").pack(pady=5)
table_name_entry = tk.Entry(app, width=50)
table_name_entry.pack(pady=5)

# Schema name entry (optional)
tk.Label(app, text="Schema Name (Optional, default is 'public'):").pack(pady=5)
schema_name_entry = tk.Entry(app, width=50)
schema_name_entry.pack(pady=5)

# Delimiter selection
tk.Label(app, text="Select Delimiter:").pack(pady=5)
delimiter_var = tk.StringVar(value=',')  # Default to comma
delimiter_frame = tk.Frame(app)
delimiter_frame.pack(pady=5)

tk.Radiobutton(delimiter_frame, text="Comma (,)", variable=delimiter_var, value=',').pack(side=tk.LEFT)
tk.Radiobutton(delimiter_frame, text="Pipe (|)", variable=delimiter_var, value='|').pack(side=tk.LEFT)
tk.Radiobutton(delimiter_frame, text="Tilde (~)", variable=delimiter_var, value='~').pack(side=tk.LEFT)

# Run button
run_button = tk.Button(app, text="Run", command=run_script)
run_button.pack(pady=10)

tk.Label(app, text="CSV to PostgreSQL Data Loader \nCreated by Sumit").pack(pady=5)

# Start the GUI event loop
app.mainloop()
