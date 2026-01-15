import express from 'express';
import { get_users, put_user } from './http';

const PORT = 5000;

const app = express();

app.use(express.json());

app.use(function (req, res, next) {
    res.setHeader('Access-Control-Allow-Origin', '*');
    res.setHeader('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE');
    res.setHeader('Access-Control-Allow-Headers', 'Content-Type');
    res.setHeader('Access-Control-Allow-Credentials', 'true');
    next();
});

app.get('/', async (req, res) => {
    res.send('API is Running!');
});

const BASE_USERS_API = '/api/user';

app.get(`${BASE_USERS_API}/all`, get_users);
app.put(BASE_USERS_API, put_user);

app.listen(PORT, () => {
    console.log(`Users app listening at http://localhost:${PORT}`)
})
