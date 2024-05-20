import psycopg2
from psycopg2.extensions import connection

# In case you wanted to directly use the functions from the file .

# conn = psycopg2.connect(
#     dbname=DB_INFO['name'],
#     user=DB_INFO['usr'],
#     password=DB_INFO['passwd'],
#     host=DB_INFO['host'],
#     port=DB_INFO['port']
# )


def db_create_post(conn: connection, title: str, article: str) -> bool:
	try:
		with conn.cursor() as cursor:
			cursor.execute(
				f"INSERT INTO posts (title, article) VALUES (%s, %s);",
				(title, article)
			)
			conn.commit()

		print("Post created successfully!")
		return True

	except (Exception, psycopg2.DatabaseError) as error:
		print("Error creating post:", error)
		conn.rollback()
		return False

def db_fetch_post(conn: connection, post_id: int) -> tuple | None:
	try:
		with conn.cursor() as cursor:
			cursor.execute(
				f"SELECT post_id, title, article, creation_date FROM posts WHERE post_id = %s;",
				(post_id,)
			)
			post = cursor.fetchone()
		return post
	except (Exception, psycopg2.DatabaseError) as error:
		print("Error fetching post by ID:", error)
		return None

def db_update_post(conn: connection, post_id: int, title: str, article: str) -> bool:
	try:
		with conn.cursor() as cursor:
			cursor.execute(
				f"UPDATE posts SET title = %s, article = %s WHERE post_id = %s;",
				(title, article, post_id)
			)
			conn.commit()

		print("Post updated successfully!")
		return True

	except (Exception, psycopg2.DatabaseError) as error:
		print("Error updating post:", error)
		conn.rollback()
		return False

def db_delete_post(conn: connection, post_id: int) -> bool:
	try:
		with conn.cursor() as cursor:
			cursor.execute(
				f"DELETE FROM POSTS WHERE post_id = %s;",
				(post_id,)
			)
			conn.commit()

		print("Post deleted successfully!")
		return True

	except (Exception, psycopg2.DatabaseError) as error:
		print("Error updating post:", error)
		conn.rollback()
		return False
	
def db_fetch_posts(conn: connection) -> list[tuple] | None:
	try:
		with conn.cursor() as cursor:
			cursor.execute("SELECT post_id, title, SUBSTRING(article, 1, 250) AS article_snippet, creation_date "
					"FROM posts ORDER BY creation_date DESC LIMIT 5;")

			rows = cursor.fetchall()
			cursor.close()
			return rows

	except (Exception, psycopg2.DatabaseError) as error:
		print("Error fetching last 5 posts:", error)
		return None