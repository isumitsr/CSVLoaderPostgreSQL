#!/usr/bin/env python3

import tkinter as tk
from tkinter import messagebox
import csv
import psycopg2

def run_script():
    csv_file_path = csv_path_entry.get()
    table_name = table_name_entry.get()
    
    if not csv_file_path or not table_name:
        messagebox.showwarning("Input Error", "Please provide both CSV file path and table name.")
        return
    
    try:
        # Database connection parameters
        conn = psycopg2.connect(
            dbname="projectBloom",
            user="postgres",
            password="523041",
            host="localhost",
            port="5432"
        )
        cursor = conn.cursor()

        # Reading CSV headers
        with open(csv_file_path, 'r') as f:
            reader = csv.reader(f)
            headers = next(reader)

        # Check if the table exists
        cursor.execute(f"""
            SELECT EXISTS (
                SELECT 1 
                FROM information_schema.tables 
                WHERE table_name = '{table_name}'
            );
        """)
        table_exists = cursor.fetchone()[0]

        if not table_exists:
            # Create table if it doesn't exist
            columns = ", ".join([f"{header} TEXT" for header in headers])
            create_table_query = f"""
                CREATE TABLE {table_name} (
                    {columns}
                );
            """
            cursor.execute(create_table_query)
        else:
            # Truncate table if it exists
            truncate_table_query = f"TRUNCATE TABLE {table_name};"
            cursor.execute(truncate_table_query)
        
        conn.commit()

        # Loading data into the table
        copy_sql = f"COPY {table_name} FROM STDIN WITH CSV HEADER DELIMITER AS ','"
        with open(csv_file_path, 'r') as f:
            cursor.copy_expert(sql=copy_sql, file=f)
        conn.commit()

        cursor.close()
        conn.close()

        # Display success message
        messagebox.showinfo("Success", "Data loaded successfully into PostgreSQL. Check projectBloom DB")

    except Exception as e:
        # Display error message
        messagebox.showerror("Error", f"An error occurred: {e}")

# Create the main window
app = tk.Tk()
app.title("Data Loader")

# Instructions label
tk.Label(app, text="Enter CSV file path and table name, then click the button below to load data.").pack(pady=10)

# CSV file path entry
tk.Label(app, text="CSV File Path:").pack(pady=5)
csv_path_entry = tk.Entry(app, width=50)
csv_path_entry.pack(pady=5)

# Table name entry
tk.Label(app, text="Table Name:").pack(pady=5)
table_name_entry = tk.Entry(app, width=50)
table_name_entry.pack(pady=5)

# Run button
run_button = tk.Button(app, text="Run", command=run_script)
run_button.pack(pady=10)

# Start the GUI event loop
app.mainloop()
