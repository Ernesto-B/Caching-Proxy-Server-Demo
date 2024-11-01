# Caching-Proxy-Server-Demo

The purpose of this project is to show how a simple cache is made and works (barring TTL), and how it can be modified to acomodate different caching replacement policies. This project was also aimed at getting experience working with the axios and http libraries.

This project implements a simple caching proxy server in Node.js that forwards requests to an origin server and caches the responses. It has two versions: 
1. A basic caching server (`cachingServer.js`).
2. An LRU (Least Recently Used) caching server (`lruCachingServer.js`) that limits the cache size and uses an LRU policy to manage cache entries.

## Prerequisites

- Node.js (v12 or higher)
- npm (comes with Node.js)

## Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/Ernesto-B/Caching-Proxy-Server-Demo.git
   cd Caching-Proxy-Server-Demo
   ```
2. **Install dependencies**:
   ```bash
   npm install
   ```
## Usage
1. **Start the caching server**:
- The recommended originURL is `https://dummyjson.com`.
   ```bash
   node cachingServer.js --port <port> --origin <originURL>
   ```
   or
   ```bash
   node lruCachingServer.js --port <port> --origin <originURL>
   ```
2. **Send requests to the caching server**:
    - You can send requests to the caching server using `curl`, `postman` a web browser, or using `Thunder Client`. If using Thunder Client, open `request.REST` file and click on the `Send Request` button.
3. **View the cached responses**:
   - The LRU caching server limits the cache size to 3 entries by default. You can change this by modifying the `MAX_CACHE_SIZE` constant in `lruCachingServer.js`.
