import sequelize from './database';
import { DataTypes, Model, Optional } from 'sequelize';

export type TUser = {
    id: number,
    first_name: string,
    last_name: string,
    age: number,
};

type UserCreationAttributes = Optional<TUser, 'id'>;

export interface UserModel extends Model<TUser, UserCreationAttributes>, TUser { }

export const User = sequelize.define<UserModel>("user", {
    id: {
        primaryKey: true,
        type: DataTypes.INTEGER,
        autoIncrement: true,
    },
    first_name: DataTypes.TEXT,
    last_name: DataTypes.TEXT,
    age: DataTypes.INTEGER,
});

(
    async () => {
        await sequelize.sync();
    }
)();
