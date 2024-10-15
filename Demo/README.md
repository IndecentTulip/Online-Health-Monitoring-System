# Simplified overview

front end:

1. idex.js 
  render reactDOM
  include <App> html element

2. App.js
  include other related html element that where defined with React(login,Dashboard)
  define App func
    set variables
    return html 
      include appropriate logic with <Login> and <Dashboard> element
      pass variables into <login> and <Dashboard>
  export App

3. Login.js
  define Login
    set variables
    set func
      use axios to create a POST request to the server and spesify path
      use variable passed by APP
    return html
      include layout and logic where needed
  export Login

3. Dashboard.js 
  define Dashboard
    return html
      include layout and use variable passed by APP
  export Dashboard


back end:

connect to db as "conn"

at route /login POST
  get data from the POST
  SELECT from db
  put result into "user"
  close db connect and cursor

  if user exist in db 
    return json with it's name
  else 
    return json with error

db:

tables are created
pupulated
and it's now on and is listening

