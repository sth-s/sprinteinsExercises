import { Sequelize } from 'sequelize';

const PG_HOST = 'localhost';
const PG_PORT = 5432;
const PG_USERNAME = 'admin';
const PG_PASSWORD = 'password';
const PG_DATABASE = 'user';

const sequelize = new Sequelize(`postgres://${PG_USERNAME}:${PG_PASSWORD}@${PG_HOST}:${PG_PORT}/${PG_DATABASE}`);

export default sequelize;
