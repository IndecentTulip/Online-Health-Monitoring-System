-- Insert sample users without specifying IDs
INSERT INTO users (username, email, password) VALUES
('alice', 'alice@example.com', 'hashed_password1'),
('bob', 'bob@example.com', 'hashed_password2');

-- Insert sample posts without specifying IDs
INSERT INTO posts (user_id, title, content) VALUES
(1, 'First Post by Alice', 'This is the content of Alice first post.'),
(1, 'Second Post by Alice', 'This is the content of Alice second post.'),
(2, 'First Post by Bob', 'This is the content of Bob first post.');

