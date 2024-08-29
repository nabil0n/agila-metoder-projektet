import pandas as pd
import psycopg2

from newsfeed.datatypes import BlogInfo

TABLE_NAME = "iths.articles"


def create_connection() -> tuple[psycopg2.extensions.connection, psycopg2.extensions.cursor]:
    # Establish a connection to the PostgreSQL database
    connection = psycopg2.connect(
        host="localhost",
        port=5432,
        database="airflow",
        user="airflow",
        password="airflow",
    )

    # Create a cursor object to execute SQL queries
    cursor = connection.cursor()
    return connection, cursor


def create_articles_table() -> None:
    connection, cursor = create_connection()

    # Execute SQL queries to create a table
    create_table_query = f"""
        CREATE TABLE IF NOT EXISTS "{TABLE_NAME}" (
            id SERIAL PRIMARY KEY,
            unique_id TEXT,
            title TEXT,
            description TEXT,
            link TEXT,
            blog_text TEXT,
            published DATE,
            timestamp TIMESTAMP
        )
    """
    cursor.execute(create_table_query)
    connection.commit()

    # Close the cursor and connection
    cursor.close()
    connection.close()


def delete_articles_table() -> None:
    connection, cursor = create_connection()

    # Execute SQL query to drop the table
    drop_table_query = f'DROP TABLE IF EXISTS "{TABLE_NAME}"'
    cursor.execute(drop_table_query)
    connection.commit()

    # Close the cursor and connection
    cursor.close()
    connection.close()


def add_articles(articles: list[BlogInfo]) -> None:
    connection, cursor = create_connection()

    # Execute SQL query to insert the article into the table
    insert_query = f"""
        INSERT INTO  "{TABLE_NAME}" (unique_id, title, description, link, blog_text, published, timestamp)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """
    for article in articles:
        cursor.execute(
            insert_query,
            (
                article.unique_id,
                article.title,
                article.description,
                article.link,
                article.blog_text,
                article.published,
                article.timestamp,
            ),
        )
        connection.commit()

    # Close the cursor and connection
    cursor.close()
    connection.close()


def load_articles() -> list[BlogInfo]:
    connection, cursor = create_connection()

    # Execute SQL query to fetch articles from the table
    select_query = f'SELECT * FROM "{TABLE_NAME}"'
    cursor.execute(select_query)
    rows = cursor.fetchall()

    # Create a list of BlogInfo instances from the fetched rows
    articles = []
    for row in rows:
        article = BlogInfo(
            unique_id=row[1],
            title=row[2],
            description=row[3],
            link=row[4],
            blog_text=row[5],
            published=pd.to_datetime(row[6]).date(),
            timestamp=pd.to_datetime(row[7]),
        )
        articles.append(article)

    # Close the cursor and connection
    cursor.close()
    connection.close()

    return articles


def debug_database() -> None:
    connection, cursor = create_connection()

    # Check tables
    cursor.execute(
        "SELECT table_name FROM information_schema.tables WHERE table_name LIKE 'iths.%'"
    )
    tables = cursor.fetchall()
    print("Tables:")
    for table in tables:
        print(table[0])
    print("")

    # Print column information
    cursor.execute(
        f"SELECT column_name, data_type FROM information_schema.columns WHERE table_name = '{TABLE_NAME}'"
    )
    column_info = cursor.fetchall()
    print("Column Information:")
    for column in column_info:
        print("Column Name:", column[0])
        print("Data Type:", column[1])
        print("")

    # Print first rows
    cursor.execute(f'SELECT * FROM "{TABLE_NAME}" LIMIT 3')
    rows = cursor.fetchall()
    print("First Rows:")
    for row in rows:
        print(row)
    print("")

    # Close the cursor and connection
    cursor.close()
    connection.close()


if __name__ == "__main__":
    # delete_articles_table()
    debug_database()
