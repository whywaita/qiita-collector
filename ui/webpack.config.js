module.exports = {
  entry: {
    javascript: "./src/app.js",
  },
  output: {
    path: __dirname + "/build",
    filename: 'bundle.js',
  },
  module: {
    loaders: [
      {
        test: /\.js$/,
        loader: 'babel-loader',
        exclude: /node_modules/,
      },
    ],
  },
}
