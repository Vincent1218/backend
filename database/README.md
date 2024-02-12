# To start the services
brew services start mongodb-community@6.0

# To stop the services
brew services stop mongodb-community@6.0

# To open mongodb shell
mongosh

# Exit mongodb shell
exit

# To show databases
show dbs

# To use a database
use '..database name..'

# Create new database
use '..database name..'

# View collections in database
show collections

# Delete entire database
db.dropDatabase()

# To access current database
db

# To insert one into single collection (user is collection)
db.users.insertOne({ name: "John})

# To retrieve all from collection
db.users.find()