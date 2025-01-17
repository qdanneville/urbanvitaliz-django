const { resolve } = require('path');

module.exports = {
    plugins: [],
    root: resolve('./src'),
    base: '/static/',
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
                home: resolve('./src/js/apps/home.js'),
                crm: resolve('./src/js/apps/crm.js'),
                project: resolve('./src/js/apps/project.js'),
                auth: resolve('./src/js/apps/auth.js'),
                projectDetails : resolve('./src/js/apps/projectDetails.js'),
                projectShare : resolve('./src/js/apps/projectShare.js'),
                map: resolve('./src/js/apps/map.js'),
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
