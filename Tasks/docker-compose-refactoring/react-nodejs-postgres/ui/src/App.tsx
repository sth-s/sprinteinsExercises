import { useEffect, useState } from 'react'
import './App.css'
import { User, fetch_users, put_user, } from './api'
import { DataGrid, GridColDef, GridValueGetterParams } from '@mui/x-data-grid';


function App() {
  const [users, setUsers] = useState<User[]>([])

  async function fetch_users_and_set() {
    try {
      setUsers(await fetch_users())
    } catch (error) {
      alert(`Server error has occurred: ${error}`)
    }
  }

  useEffect(
    () => {
      fetch_users_and_set()
    }, []
  )

  const [newUser, setNewUser] = useState<User>({ first_name: "", last_name: "", age: 0 });

  const handleChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = event.target;
    setNewUser((prevData) => ({ ...prevData, [name]: value }))
  };

  const handleSubmit = async (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault()
    try {
      await put_user(newUser)
      await fetch_users_and_set()
    } catch (error) {
      console.error(error)
      alert(`User could not be created: ${error}`)
    }
  }

  const columns: GridColDef[] = [
    { field: 'id', headerName: 'ID', width: 70 },
    { field: 'first_name', headerName: 'First name', width: 130 },
    { field: 'last_name', headerName: 'Last name', width: 130 },
    {
      field: 'age',
      headerName: 'Age',
      type: 'number',
      width: 70,
    },
    {
      field: 'full_name',
      headerName: 'Full name',
      description: 'This column is not sortable.',
      sortable: false,
      width: 200,
      valueGetter: (params: GridValueGetterParams) =>
        `${params.row.first_name || ''} ${params.row.last_name || ''}`,
    },
    {
      field: 'createdAt',
      headerName: 'Added at',
      type: 'string',
      width: 250,
      valueFormatter(params) {
        return new Date(params.value as string).toUTCString();
      },
    }
  ];

  return (
      <>
        <form id="add-user-form" onSubmit={handleSubmit}>
          <label className="label" htmlFor="first_name">First Name: </label>
          <input type='text' id="first_name" name="first_name" placeholder="Ela" value={newUser.first_name} onChange={handleChange} />

          <label className="label" htmlFor="last_name">Last Name: </label>
          <input type='text' id="last_name" name="last_name" placeholder="Brown" value={newUser.last_name} onChange={handleChange} />

          <label className="label" htmlFor="age">Age: </label>
          <input type='number' min="0" id="age" name="age" placeholder="38" value={newUser.age} onChange={handleChange} />

          <button className="button" type="submit">Add User</button>
        </form>


        <div style={{ height: 400, width: '100%' }}>
          <DataGrid
              rows={users}
              columns={columns}
              initialState={{
                pagination: {
                  paginationModel: { page: 0, pageSize: 5 },
                },
              }}
              pageSizeOptions={[5, 10]}
              sx={{
                marginTop: 2,
                boxShadow: 2,
                border: 2,
              }}
          />
        </div>

      </>
  )
}

export default App
