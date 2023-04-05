
CREATE TABLE IF NOT EXISTS user (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	login TEXT(80) UNIQUE  NOT NULL,	
	nick TEXT(20) UNIQUE NOT NULL,
	sex INTEGER NOT NULL,
	is_blocked INTEGER DEFAULT 0,
	avatar TEXT(80),
	password TEXT(100) NOT NULL,
	date_of_reg DATETIME DEFAULT CURRENT_DATETIME,	
	time_of_change_info INTEGER NOT NULL,
	time_of_last_action INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS wall_message (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	senderId INTEGER NOT NULL,
	receiverId INTEGER NOT NULL,
	message TEXT(1000) NOT NULL,
	date DATETIME DEFAULT CURRENT_TIMESTAMP,	
	timestamp INTEGER NOT NULL,
	FOREIGN KEY (senderId) REFERENCES user(id),
	FOREIGN KEY (receiverId) REFERENCES user(id)
);

CREATE TABLE IF NOT EXISTS friend_request (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	friend1 INTEGER NOT NULL,
	friend2 INTEGER NOT NULL,
	date DATETIME DEFAULT CURRENT_TIMESTAMP,	
	timestamp INTEGER NOT NULL,
	FOREIGN KEY (friend1) REFERENCES user(id),
	FOREIGN KEY (friend2) REFERENCES user(id)
);


CREATE TABLE IF NOT EXISTS friend (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	friend1 INTEGER NOT NULL,
	friend2 INTEGER NOT NULL,
	date DATETIME DEFAULT CURRENT_TIMESTAMP,	
	timestamp INTEGER NOT NULL,
	FOREIGN KEY (friend1) REFERENCES user(id),
	FOREIGN KEY (friend2) REFERENCES user(id)
);

CREATE TABLE IF NOT EXISTS forum (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	creatorId INTEGER NOT NULL,
	name TEXT(256) UNIQUE NOT NULL,
	name_lower TEXT(256) UNIQUE NOT NULL,
	message TEXT(1000) NOT NULL,
	date DATETIME DEFAULT CURRENT_TIMESTAMP,	
	timestamp INTEGER NOT NULL,
	FOREIGN KEY (creatorId) REFERENCES user(id)
);

CREATE TABLE IF NOT EXISTS forum_message (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	senderId INTEGER NOT NULL,
	forumId INTEGER NOT NULL,
	message TEXT(1000) NOT NULL,
	date DATETIME DEFAULT CURRENT_TIMESTAMP,	
	timestamp INTEGER NOT NULL,
	FOREIGN KEY (senderId) REFERENCES user(id),
	FOREIGN KEY (forumId) REFERENCES forum(id)  ON DELETE CASCADE
);

 CREATE TABLE IF NOT EXISTS dialog (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	senderId INTEGER NOT NULL,
	receiverId INTEGER NOT NULL,
	date DATETIME DEFAULT CURRENT_TIMESTAMP,
	last_message TEXT(1000) NOT NULL,	
	timestamp INTEGER NOT NULL,
	is_readen INTEGER DEFAULT 0,
	FOREIGN KEY (senderId) REFERENCES users(id),
	FOREIGN KEY (receiverId) REFERENCES users(id)
);

CREATE TABLE IF NOT EXISTS dialog_message (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	userId INTEGER NOT NULL,
	dialogId INTEGER NOT NULL,
	message TEXT(1000) NOT NULL,
	date DATETIME DEFAULT CURRENT_TIMESTAMP,	
	timestamp INTEGER NOT NULL,
	FOREIGN KEY (userId) REFERENCES user(id),
	FOREIGN KEY (dialogId) REFERENCES dialog(id)
);

CREATE TABLE IF NOT EXISTS user_page_like (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	userId INTEGER NOT NULL,
	likerId INTEGER NOT NULL,
	date DATETIME DEFAULT CURRENT_TIMESTAMP,	
	timestamp INTEGER NOT NULL,
	FOREIGN KEY (userId) REFERENCES user(id),
	FOREIGN KEY (likerId) REFERENCES user(id)
);

CREATE TABLE IF NOT EXISTS black_list (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	user1 INTEGER NOT NULL,
	user2 INTEGER NOT NULL,
	date DATETIME DEFAULT CURRENT_TIMESTAMP,	
	timestamp INTEGER NOT NULL,
	FOREIGN KEY (user1) REFERENCES user(id),
	FOREIGN KEY (user2) REFERENCES user(id)
);

CREATE TRIGGER IF NOT EXISTS [UpdateLastTime]
AFTER
UPDATE
ON dialog
FOR EACH ROW
WHEN NEW.date <= OLD.date
BEGIN
update dialog set date=CURRENT_TIMESTAMP where id=OLD.id;
END
 

