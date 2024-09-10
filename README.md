# CSVLoaderPostgreSQL
This application (exe) can take csv file path and table_name as an input from user and then load the csv file directly to postgreSQL database called - projectBloom. Modify the "conn" dict in the py code by adding your postgreSQL connection info and then run the command to create exe using pyinstaller pkg, and just RUN exe. See the magic!

### Once App is opened, confirm whether to use default DB or give custom DB as an input
<img width="416" alt="Screenshot 2024-09-05 at 2 03 20 AM" src="https://github.com/user-attachments/assets/ddd4b1f3-5b71-48b7-abc9-cef3ac71a55b">

### Give inputs
<img width="416" alt="Screenshot 2024-09-05 at 2 03 52 AM" src="https://github.com/user-attachments/assets/cf3f904e-005a-44a2-b11e-4f0e01c8eeaa">

### Provide csv file path (you can browse and let the app choose it now), table name and schema (optional, default is public) that should be created automatically in PostGreSQL through csv file. And data to be loaded in that table.
<img width="678" alt="Screenshot 2024-09-11 at 12 06 45 AM" src="https://github.com/user-attachments/assets/7ea49380-39d1-48fd-8195-fec3d4ad3861">

### Successful Message!!!
<img width="606" alt="Screenshot 2024-09-05 at 2 05 23 AM" src="https://github.com/user-attachments/assets/6c5ed231-ab94-42ed-9104-493148cf025e">

### DATA LOADED SUCCESFULLY, Can check the DB now!!!