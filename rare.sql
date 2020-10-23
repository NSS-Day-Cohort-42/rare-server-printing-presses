CREATE TABLE `users` (
	`id`	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
	`email`	TEXT NOT NULL,
	`name`	TEXT NOT NULL,
	`password`	TEXT NOT NULL
);

CREATE TABLE `categories` (
    `id`    INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    `label`    TEXT NOT NULL
);

CREATE TABLE `tags` (
	`id`  INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
	`label`  TEXT NOT NULL
);


CREATE TABLE `posts` (
	`id`	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
	`user_id`	INTEGER NOT NULL,
	`title`	TEXT NOT NULL,
	`content` INTEGER NOT NULL,
	`category_id` INTEGER NOT NULL,
	FOREIGN KEY(`user_id`) REFERENCES `users`(`id`),
	FOREIGN KEY(`category_id`) REFERENCES `categories`(`id`)
);

CREATE TABLE `post_tags` (
	`id`	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
	`tag_id`	INTEGER NOT NULL,
	`post_id`	INTEGER NOT NULL,
	FOREIGN KEY(`tag_id`) REFERENCES `tags`(`id`),
	FOREIGN KEY(`post_id`) REFERENCES `posts`(`id`)
);

CREATE TABLE `comments` (
	`id`	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
	`user_id`	INTEGER NOT NULL,
	`post_id`	INTEGER NOT NULL,
	`subject`	TEXT NOT NULL,
	`content`	TEXT NOT NULL,
	FOREIGN KEY(`user_id`) REFERENCES `users`(`id`),
	FOREIGN KEY(`post_id`) REFERENCES `posts`(`id`)
);


INSERT INTO `users` VALUES (null, 'mo@mo.com', "Mo", "password");
INSERT INTO `users` VALUES (null, 'bob@bob.com', "Bob", "password");


INSERT INTO `categories` VALUES (null, "Animal");
INSERT INTO `categories` VALUES (null, "Magazine");
INSERT INTO `categories` VALUES (null, "Music");
INSERT INTO `categories` VALUES (null, "Travel");


INSERT INTO `tags` VALUES (null, "dog");
INSERT INTO `tags` VALUES (null, "Vogue");
INSERT INTO `tags` VALUES (null, "Beatles");
INSERT INTO `tags` VALUES (null, "Fiji");



INSERT INTO `posts` VALUES (null, 1, "I Love Dogs", "Dogs are the best.", 1);
INSERT INTO `posts` VALUES (null, 2, "Fashion", "This years style is the best.", 2);

SELECT * FROM users