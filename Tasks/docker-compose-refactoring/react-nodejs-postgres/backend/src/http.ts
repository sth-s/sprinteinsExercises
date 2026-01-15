import { Request, Response } from 'express';
import { TUser, User } from "./model";

export const get_users = async (_: Request, res: Response) => {
    const users = await User.findAll();
    res.json(users);
}

export const put_user = async (req: Request, res: Response) => {
    const { first_name, last_name, age } = req.body as TUser;

    if (!first_name || !last_name || !age) {
        res.status(400).json({ error: 'Missing one or more of the parameters: first_name, last_name, age.' });
        return;
    }

    const { id } = await User.create({ first_name, last_name, age });

    const user = await User.findOne({
        where: { id }
    });

    if (!user) {
        res.status(500).json({ error: 'Failed to create user.' });
        return;
    }

    res.json(user);
}

