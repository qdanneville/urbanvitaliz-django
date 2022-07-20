const { resolve } = require('path');

module.exports = {
    plugins: [],
    root: resolve('./src'),
    base: '/static/dist/',
    server: {
        host: 'localhost',
        port: 3000,
        open: false,
        watch: {
            usePolling: true,
            disableGlobbing: false,
        },
    },
    resolve: {
        extensions: ['.js', '.json'],
    },
    build: {
        outDir: resolve('./dist'),
        assetsDir: '',
        manifest: true,
        emptyOutDir: true,
        target: 'es2017',
        rollupOptions: {
            input: {
                main: resolve('./src/js/main.js'),
            },
            output: {
                chunkFileNames: undefined,
            },
        },
    },
    test: {
        globals: true,
    },
};