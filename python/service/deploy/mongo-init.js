db = db.getSiblingDB('service');

db.createUser({
    user: "admin",
    pwd: "admin",
    roles: [{
        role: "readWrite",
        db: "service"
    }]
});

db.user.createIndex( { "email": 1 }, { unique: true } )

db.user.insertMany([
    { email: "festrela@email.com", password: '123456' }
]);