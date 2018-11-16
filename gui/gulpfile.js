let gulp = require('gulp');
let jsdoc = require('gulp-jsdoc3');
 
gulp.task('doc', function (cb) {
    var config = require('./docs/jsdoc_config.json');
    gulp.src(['README.md', './src/**/*.js', 'main.js'], {read: false})
        .pipe(jsdoc(config, cb));
});

gulp.task('watch-docs', function() {
  gulp.watch('./main.js', ['doc']);
  gulp.watch('./src/**/*.js', ['doc']);
  gulp.watch('./README.md', ['doc']);
  gulp.watch('./docs/jsdoc_config.json', ['doc']);
});

