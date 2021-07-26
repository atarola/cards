const path = require('path');

module.exports = {
    mode: 'development',
    devtool: false,
    entry: path.resolve(__dirname, 'cards', 'index.js'),
    output: {
        path: path.resolve(__dirname, 'bin'),
        filename: 'bundle.js'
    },
    resolve: {
        extensions: ['.js']
    },
    module: {
        rules: [{
             test: /\.js/,
             use: {
                loader: 'babel-loader',
                options: {
                    presets: ['@babel/preset-react', '@babel/preset-env']
                }
             }
         }]
   }
};
