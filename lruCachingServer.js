const http = require('http');
const axios = require('axios');
const minimist = require('minimist');

// Parse command line arguments
const args = minimist(process.argv.slice(2));
const port = args.port || 3000;
const origin = args.origin;
const clearCache = args['clear-cache'];

// In-memory cache
const cache = new Map();    // A map maintains the order entries
const CACHE_LIMIT = 3;

if (clearCache) {
    console.log('Clearing cache...');
    cache.clear;    // Cleared the map
    console.log('Cache cleared!');
    process.exit(0);
}

if (!origin) {
    console.error('Error: Origin URL is required.');
    console.error('Usage: caching-proxy --port <number> --origin <url>');
    process.exit(1);
}

// Create the server. callback func executes whenever server gets http request
const server = http.createServer(async (req, res) => {
    const requestUrl = `${origin}${req.url}`;
    console.log(`\nRequest received: ${requestUrl}`);

    // Check if the response is already cached
    if (cache.has(requestUrl)) {
        console.log('Cache HIT');

        const cachedResponse = cache.get(requestUrl);
        cache.delete(requestUrl);
        cache.set(requestUrl, cachedResponse);

        res.writeHead(200, {
            ...cachedResponse.headers,
            'X-Cache': 'HIT',
        });
        res.end(cachedResponse.data);    // Send res to client
        return;
    }

    try {
        // Fetch the response from origin server
        console.log('Cache MISS');
        const response = await axios.get(requestUrl);   // Forward request to origin
        
        cachedData = {
            data: JSON.stringify(response.data),    // Convert the data to a string
            headers: response.headers,
        };

        cache.set(requestUrl, cachedData);

        if (cache.size > CACHE_LIMIT) {
            const oldestKey = cache.keys().next().value;
            cache.delete(oldestKey);
            console.log(`Cache limit exceeded. Removed oldest entry: ${oldestKey}\n`);
        }

        // Send the response to the client
        res.writeHead(200, {
            ...response.headers,
            'X-Cache': 'MISS',
        });
        res.end(JSON.stringify(response.data));

    } catch (error) {
        console.error('Error fetching from origin:', error.message);
        res.writeHead(500, { 'Content-Type': 'text/plain' });
        res.end('Error fetching from origin server');
    }

});



server.listen(port, () => {
    console.log(`Caching proxy server is running on port ${port}`)
    console.log(`Forwarding requests to ${origin}\n`)
});
