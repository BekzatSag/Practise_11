import psycopg2
def setup_conn():
    dbname = "postgres" #input("Please enter the name of dbname: ") 
    user = "postgres"#input("Please enter the name of user: ") #
    password = "wwweeemmm"#input("Please enter the password: ") #www......
    host = "localhost" #input("Please enter the name of host: ") #localhost
    port = "5432" #input("Please enter the port: ") #5432
    return psycopg2.connect(
        dbname = dbname,
        user = user,
        password = password,
        host = host,
        port = port
    )
while True:
    try: 
        conn = setup_conn()
        break
    except Exception: 
        print("There are some mistakes in your data. Please check it and try again")
cur = conn.cursor()

cur.execute("""
CREATE OR REPLACE FUNCTION filter_by_pattern(pattern TEXT)
RETURNS SETOF phonebook AS $$
BEGIN
RETURN QUERY
    SELECT *
    FROM phonebook
    WHERE name ILIKE pattern
        OR phone ILIKE pattern;
END;
$$ LANGUAGE plpgsql;""")

cur.execute("""
CREATE OR REPLACE PROCEDURE inserting (name_user TEXT, phone_num VARCHAR(11))
LANGUAGE plpgsql
AS $$
BEGIN
    IF EXISTS(select * FROM phonebook WHERE name = name_user) THEN 
            UPDATE phonebook 
            SET phone = phone_num 
            WHERE name = name_user;
    ELSE INSERT INTO phonebook (name, phone) VALUES (name_user, phone_num);
END IF;
END;
$$;""")


"""
I want to put this part in my code insted of part of above. Because it is logically convenient.

ELSIF EXISTS(select * FROM phonebook WHERE phone = phone_num) THEN 
    UPDATE phonebook 
    SET name = name_user
    WHERE phone = phone_num;
"""

cur.execute("""
CREATE OR REPLACE PROCEDURE inserting_by_list (name_user TEXT[], phone_num TEXT[])
LANGUAGE plpgsql
AS $$
DECLARE wrong_data TEXT[] := '{}'; name_u TEXT; num TEXT; i INT;
BEGIN
    FOR i IN 1..array_length(name_user, 1) LOOP
        name_u := name_user[i];
        num := phone_num[i];
        IF num ~ '^\\d{11}$' AND name_u ~ '^[A-Za-z]+$' 
        THEN CALL inserting(name_u, num);
        ELSE 
            IF num !~ '^\\d{11}$' THEN wrong_data := array_append(wrong_data, name_u);
            END IF;
            IF name_u !~'^[A-Za-z]+$' THEN wrong_data := array_append(wrong_data, num);
            END IF;
END IF;
END LOOP;
RAISE NOTICE 'Wrong data: %', wrong_data;
END;
$$;""")

cur.execute("""
CREATE OR REPLACE FUNCTION querying_data (limit_p INTEGER, offset_p INTEGER)
RETURNS SETOF phonebook AS $$
BEGIN
    RETURN QUERY
    SELECT *
    FROM phonebook
    LIMIT limit_p
    OFFSET offset_p;
END;
$$ LANGUAGE plpgsql;""")

cur.execute("""
CREATE OR REPLACE PROCEDURE deleting (data TEXT)
LANGUAGE plpgsql
AS $$
BEGIN
    DELETE FROM phonebook 
    WHERE name = data
    OR phone = data;
END;
$$;""")

conn.commit()


