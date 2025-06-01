## Lab 1: Build a Redis-like TCP Server in Python

### What is TCP?

**TCP (Transmission Control Protocol)** is a **reliable, connection-oriented** protocol that allows servers to communicate with multiple clients safely.

**Key Features:**

* Reliable (no data loss)
* Ordered data transfer
* Full-duplex communication
* Used by Redis, HTTP, FTP, etc.

---

### Why Does Redis Use TCP?

Redis uses TCP because:

* It ensures **reliable and ordered** delivery of commands and responses.
* Multiple clients can **safely connect and interact** with the Redis server.
* Unlike UDP, TCP guarantees **data integrity and delivery**.

---

### Objectives

Lab 1 focuses on building the foundational components of a Redis-like server. The three main tasks include:

1. **Creating a TCP server using Python's `socket` module**
2. **Handling multiple client connections (multi-client support)**
3. **Implementing a basic REPL loop for processing commands like `SET` and `GET`**

---

### What Was Done:

#### 1. **TCP Server using `socket` Module**

* A server was implemented using Python's built-in `socket` module.
* Listens on port `6379` (like Redis).
* Accepts connections and reads commands from clients.

#### 2. **Multi-Client Handling**

* The server can handle multiple clients concurrently using a `selectors` loop.
* Each client has its own connection but shares a common in-memory key-value store.

#### 3. **REPL (Read–Eval–Print Loop) Command Processing**

* Supports Redis-like command structure:

  * `PING`
  * `SET key value`
  * `GET key`
* Responses follow Redis RESP format.

---

### Commands and Outputs

#### Command: `PING`

* **Client Input:**

  ```
  PING
  ```
* **Server Output:**

  ```
  +PONG
  ```
A simple test to check if the server is responsive. `+PONG` is a standard Redis response.

---

#### Command: `SET key1 hello`

* **Client Input:**

  ```
  SET key1 hello
  ```
* **Server Output:**

  ```
  +OK
  ```
Successfully stores the key `key1` with value `hello`.

---

#### Command: `GET key1`

* **Client Input:**

  ```
  GET key1
  ```
* **Server Output:**

  ```
  $5
  hello
  ```
Returns the value of key `key1`. `$5` indicates the length of the string `hello`.

---

#### Command: `GET unknown`

* **Client Input:**

  ```
  GET unknown
  ```
* **Server Output:**

  ```
  $-1
  ```
Key doesn't exist. `$-1` is a Redis-style nil response.

---

#### Command: `HELLO`

* **Client Input:**

  ```
  HELLO
  ```
* **Server Output:**

  ```
  -ERR unknown command 'HELLO'
  ```
The command is not supported, so an error is returned.

---

#### Command: `SET onlykey`

* **Client Input:**

  ```
  SET onlykey
  ```
* **Server Output:**

  ```
  -ERR wrong number of arguments for 'SET'
  ```
SET requires both key and value. Missing value triggers argument error.

---

### Multiple Client Testing (Telnet)

#### Terminal 1:

```bash
$ telnet localhost 6379
SET user1 Alice
+OK
GET user1
$5
Alice
```

#### Terminal 2:

```bash
$ telnet localhost 6379
SET user2 Bob
+OK
GET user2
$3
Bob
GET user1
$5
Alice
```

Multiple clients can work in parallel and access the shared in-memory data.

---

