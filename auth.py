import hashlib
import streamlit as st
from database import get_database


def hash_password(password):
    """Hash password using SHA-256"""
    return hashlib.sha256(password.encode()).hexdigest()


def signup_user(fname, lname, email, password, phoneno=None):
    """Register a new user"""
    db = get_database()
    
    # Check if email already exists
    check_query = "SELECT * FROM USER_EMAIL WHERE Email = %s"
    existing_user = db.execute_query(check_query, (email,), fetch=True)
    
    if existing_user:
        return False, "Email already registered"
    
    # Insert user
    hashed_pwd = hash_password(password)
    user_query = """
        INSERT INTO USER (Fname, Lname, Password, Phoneno) 
        VALUES (%s, %s, %s, %s)
    """
    user_id = db.execute_query(user_query, (fname, lname, hashed_pwd, phoneno))
    
    if user_id:
        # Insert email
        email_query = "INSERT INTO USER_EMAIL (UID, Email) VALUES (%s, %s)"
        db.execute_query(email_query, (user_id, email))
        return True, "User registered successfully"
    
    return False, "Registration failed"


def login_user(email, password):
    """Authenticate user"""
    db = get_database()
    
    hashed_pwd = hash_password(password)
    query = """
        SELECT u.* FROM USER u
        INNER JOIN USER_EMAIL ue ON u.UID = ue.UID
        WHERE ue.Email = %s AND u.Password = %s
    """
    result = db.execute_query(query, (email, hashed_pwd), fetch=True)
    
    if result:
        return True, result[0]
    return False, None


def get_user_by_id(user_id):
    """Get user details by ID"""
    db = get_database()
    query = "SELECT * FROM USER WHERE UID = %s"
    result = db.execute_query(query, (user_id,), fetch=True)
    return result[0] if result else None


def get_user_email(user_id):
    """Get user's primary email"""
    db = get_database()
    query = "SELECT Email FROM USER_EMAIL WHERE UID = %s LIMIT 1"
    result = db.execute_query(query, (user_id,), fetch=True)
    return result[0]['Email'] if result else None
