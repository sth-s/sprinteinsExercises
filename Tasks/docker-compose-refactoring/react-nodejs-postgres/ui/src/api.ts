const BASE_USER_API = 'http://localhost:5000/api/user';

export const fetch_users = async (): Promise<User[]> => {
    try {
        const response = await fetch(`${BASE_USER_API}/all`);

        if (!response.ok) {
            throw new Error(`Failed to fetch users: Status ${response.status}`);
        }

        const data: User[] = await response.json();
        return data;
    } catch (error) {
        throw new Error(`${(error as Error).message}`);
    }
}

// write an api function to put a user to the backend
export const put_user = async (user: User): Promise<User> => {
    try {
        const response = await fetch(BASE_USER_API, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(user)
        });

        if (!response.ok) {
            throw new Error(`Failed to put user: Status ${response.status}`);
        }

        const data = await response.json() as User;
        return data;
    } catch (error) {
        throw new Error(`Failed to put user: ${(error as Error).message}`);
    }
}

export interface User {
    first_name: string
    last_name: string
    age: number
}
