# Hotel Jayaria Management System

## Overview

The **Hotel Jayaria Management System** is a Python-based application designed for managing hotel operations. It supports user management, booking management, and room information functionalities. The system utilizes a MySQL database for data storage and retrieval.

## File Extensions

- **Text File**: 
  - `About.txt`: Contains information about the hotel. This is a plain text file created and used within the program.

- **Python Script**: 
  - `main.py`: The main Python script for running the application.

## Key Functionalities

### User Management

- **Sign Up**: Create a new account with a unique Guest ID, name, Aadhaar number, address, and phone number.
- **Log In**: Access your account using your Guest ID and phone number.

### Guest Details Management

- **View/Modify Details**: Guests can view or update their personal details including name, Aadhaar number, address, and phone number.

### Booking Management

- **Book a Room**: Select dates and room types to book a room. The system checks room availability for the selected dates.
- **View/Cancel Bookings**: Guests can view their existing bookings and cancel them if needed.

### Room Information

- **Room Details**: Display detailed information about available rooms, including pricing and features.

### Database Interaction

- **Database**: Interacts with a MySQL database to manage guest and booking information.
- **Tables**:
  - **guests**: Stores guest details (GID, Gname, Aadhaar number, address, phone number).
  - **rooms**: Stores room information (Room ID, type, cost per day, availability).
  - **bookings**: Stores booking information (Booking ID, Guest ID, Room ID, check-in, check-out dates).

## Modules Used

- **datetime**: For handling date inputs for bookings.
- **tabulate**: To display data in a tabular format.
- **art & pyfiglet**: For creating and displaying ASCII art for the hotel name.
- **colorama & termcolor**: For colored text output in the terminal.
- **mysql.connector**: For connecting and interacting with the MySQL database.

