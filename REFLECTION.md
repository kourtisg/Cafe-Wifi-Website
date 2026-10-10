# Reflection – Day 88: Cafe & Wifi Website

## How did I approach the project?
I started by opening `cafes.db` to see the table and its columns, then planned the pages before writing code:
a home page with the cafe list, an add page, and POST routes for updating the price and deleting.
I built it in small steps: database model first, then the list, the filter, the form, and finally the styling.

## What was hard?
Making the SQLAlchemy model match an existing table exactly, and a bug where the app opened an empty database
when I ran it from a different folder. Flask was creating the `instance` folder relative to the current
working directory, so I had to set `instance_path` explicitly. Handling broken image links from the data was also new.

## What was easy?
Reusing what I learnt in the previous days: Jinja template inheritance, Bootstrap cards and WTForms validation.

## How might I improve for the next project?
Check the data first and test the app from more than one place (folder, terminal, VS Code) early on.
I would also like to add an edit page for all fields and search by name.

## What was my biggest learning?
Actions that change data (delete, update) should use POST with a CSRF token, not plain GET links.
I also learnt how Flask decides where the `instance` folder lives.

## What would I do differently?
I would split the routes into a REST API and a front end that calls it, like the Day 66 project, so the same
data could also serve a mobile app.
