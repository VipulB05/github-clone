import mysql.connector
from mysql.connector import Error
import streamlit as st
from config import DB_CONFIG


class Database:
    """Database connection and query management class"""
    
    def __init__(self):
        self.connection = None
    
    def connect(self):
        """Establish database connection"""
        try:
            self.connection = mysql.connector.connect(**DB_CONFIG)
            if self.connection.is_connected():
                return True
        except Error as e:
            st.error(f"Database connection error: {e}")
            return False
    
    def disconnect(self):
        """Close database connection"""
        if self.connection and self.connection.is_connected():
            self.connection.close()
    
    def execute_query(self, query, params=None, fetch=False):
        """Execute a query and return results if needed"""
        try:
            if not self.connection or not self.connection.is_connected():
                self.connect()
            
            cursor = self.connection.cursor(dictionary=True)
            cursor.execute(query, params or ())
            
            if fetch:
                result = cursor.fetchall()
                cursor.close()
                return result
            else:
                self.connection.commit()
                last_id = cursor.lastrowid
                cursor.close()
                return last_id
        except Error as e:
            st.error(f"Query execution error: {e}")
            return None if fetch else False
    
    def execute_many(self, query, params_list):
        """Execute multiple queries with different parameters"""
        try:
            if not self.connection or not self.connection.is_connected():
                self.connect()
            
            cursor = self.connection.cursor()
            cursor.executemany(query, params_list)
            self.connection.commit()
            cursor.close()
            return True
        except Error as e:
            st.error(f"Batch query execution error: {e}")
            return False


# Singleton instance
@st.cache_resource
def get_database():
    """Get or create database instance"""
    db = Database()
    db.connect()
    return db
