## Documentation

#### To use the API:

    Set up packages: Run <npm install> to install all the packages.

    Set up db-migrate: Run <npm i -g db-migrate> to have access to db-migrate commands.

    Set up database: Connect to postgres <psql -U postgres>.
        - Then, create two databases: one for development and one for testing e.g. <CREATE DATABASE db_name;>.
        - Then, create a user for the database e.g. <CREATE USER user_name WITH PASSWORD 'password';>.
        - Then, grant the user to both databases e.g. <GRANT ALL PRIVILEGES ON DATABASE db_name TO user_name;>.

    Set up env: See the dotenv variables in the next section.

    Launch database: Run `db-migrate up` to create the tables.

### Dotenv Variables:

This is the list for all the variables used in this project. You can copy them in a dotenv file with your own values for use:

> - ENV
>     > `test` - For testing.
>     > `dev` - For development.
> - POSTGRES_HOST
> - POSTGRES_PORT
>     > `5432` - By default.
> - POSTGRES_DB
> - POSTGRES_DB_TEST
> - POSTGRES_USER
> - POSTGRES_PASSWORD

<h3 align="center">
  Thank you!
</h3>

---
