from flask import Flask, render_template, url_for, request
import sqlite3
import json
import os

connection = sqlite3.connect('Database.db')
cursor = connection.cursor()

command = """CREATE TABLE IF NOT EXISTS admin(name TEXT, password TEXT)"""
cursor.execute(command)

name='ganesh'
password='ganesh@222'
cursor.execute("INSERT INTO admin VALUES ('"+name+"', '"+password+"')")
connection.commit()

cursor.execute("drop table intracity_book")